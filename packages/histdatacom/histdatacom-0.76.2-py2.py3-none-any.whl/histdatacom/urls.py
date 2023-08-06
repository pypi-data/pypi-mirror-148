import os
import sys
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import multiprocessing
from urllib.parse import urlparse
import requests
from rich import print
from rich.progress import Progress
from rich.progress import TextColumn
from rich.progress import BarColumn
from rich.progress import TimeElapsedColumn
import bs4
from bs4 import BeautifulSoup
from histdatacom.utils import get_year_from_datemonth
from histdatacom.utils import get_month_from_datemonth
from histdatacom.utils import get_current_datemonth_gmt_plus5
from histdatacom.utils import get_pool_cpu_count
from histdatacom.fx_enums import Timeframe, get_valid_format_timeframes
from histdatacom.records import Record


class _URLs:
    def __init__(self, args, records_current_, records_next_):
        # setting relationship to global outer parent
        self.args = args

        global records_current
        records_current = records_current_

        global records_next
        records_next = records_next_

        self.args["base_url"] = 'http://www.histdata.com/download-free-forex-data/'
        self.args["post_headers"] = {
            "Host": "www.histdata.com",
            "Connection": "keep-alive",
            "Content-Length": "101",
            "Cache-Control": "max-age=0",
            "Origin": "http://www.histdata.com",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9"}

    def init_counters(self, records_current_, records_next_, args_):
        global records_current
        records_current = records_current_
        global records_next
        records_next = records_next_
        global args
        args = args_

    def populate_initial_queue(self, records_current, records_next):
        for url in self.generate_form_urls(self.args["start_yearmonth"],
                                           self.args["end_yearmonth"],
                                           self.args['formats'],
                                           self.args["pairs"],
                                           self.args['timeframes'],
                                           self.args["base_url"]):
            record = Record()
            record(url=url, status="URL_NEW")
            record.restore_momento(base_dir=self.args['default_download_dir'])

            if record.status != "URL_NO_REPO_DATA":
                record.write_info_file(base_dir=self.args['default_download_dir'])
                records_next.put(record)

        records_next.dump_to_queue(records_current)

    def validate_url(self, record):
        try:
            if record.status == "URL_NEW":
                page_data = self.get_page_data(record.url)
                self.fetch_form_values(page_data, record)

                if record.data_tk == "":
                    raise ValueError

                record.status = "URL_VALID"
                record.write_info_file(base_dir=args['default_download_dir'])

            records_next.put(record)
        except ValueError:
            print(f"Info: Histdata.com does not have: {record.url}")
            record.status = "URL_NO_REPO_DATA"
            record.write_info_file(base_dir=args['default_download_dir'])
        except Exception:
            print(f"Unknown Error for URL: {record.url}", sys.exc_info())
            record.delete_info_file()
            raise
        finally:
            records_current.task_done()

    def validate_urls(self, records_current, records_next):

        records_count = records_current.qsize()
        with Progress(TextColumn(text_format=f"[cyan]Validating {records_count} URLs..."),
                      BarColumn(),
                      "[progress.percentage]{task.percentage:>3.0f}%",
                      TimeElapsedColumn()) as progress:
            task_id = progress.add_task("Validating URLs", total=records_count)

            with ThreadPoolExecutor(max_workers=(get_pool_cpu_count(self.args['cpu_utilization']) * 3),
                                    initializer=self.init_counters,
                                    initargs=(records_current,
                                              records_next,
                                              self.args.copy())) as executor:
                futures = []

                while not records_current.empty():
                    record = records_current.get()

                    if record is None:
                        return

                    future = executor.submit(self.validate_url, record)
                    progress.advance(task_id, 0.25)
                    futures.append(future)

                for future in as_completed(futures):
                    self.complete_future(progress, task_id, futures, future)

        records_current.join()
        records_next.dump_to_queue(records_current)

    def download_zip(self, record):
        try:
            if "URL_VALID" in record.status \
            or (self.args['from_api']
                and not (os.path.exists(record.data_dir + record.zip_filename)
                         or os.path.exists(record.data_dir + record.csv_filename)
                         or os.path.exists(record.data_dir + record.jay_filename))
                ):
                res = self.request_file(record)
                record.zip_filename = res.headers["Content-Disposition"].split(";")[1].split("=")[1]
                self.write_file(record, res.content)

                record.status = "CSV_ZIP" if record.status == "URL_VALID" else record.status
                record.write_info_file(base_dir=args['default_download_dir'])

            records_next.put(record)
        except KeyError:
            print(f"Invalid Zip on histdata.com: {record.url}", sys.exc_info())
            record.delete_info_file()
        except Exception:
            print("Unexpected error:", sys.exc_info())
            record.delete_info_file()
            raise
        finally:
            records_current.task_done()

    def request_file(self, record):
        post_headers = args['post_headers'].copy()
        post_headers["Referer"] = record.url
        return requests.post("http://www.histdata.com/get.php",
                             data={"tk": record.data_tk,
                                   "date": record.data_date,
                                   "datemonth": record.data_datemonth,
                                   "platform": record.data_format,
                                   "timeframe": record.data_timeframe,
                                   "fxpair": record.data_fxpair},
                             headers=post_headers)

    def write_file(self, record, content):
        zip_path = record.data_dir + record.zip_filename
        with open(zip_path, "wb") as zip_file:
            zip_file.write(content)

    def download_zips(self, records_current, records_next):

        records_count = records_current.qsize()
        with Progress(TextColumn(text_format=f"[cyan]Downloading {records_count} ZIPs..."),
                      BarColumn(),
                      "[progress.percentage]{task.percentage:>3.0f}%",
                      TimeElapsedColumn()) as progress:
            task_id = progress.add_task("[cyan]Downloading ZIPs", total=records_count)

            with ThreadPoolExecutor(max_workers=(get_pool_cpu_count(self.args['cpu_utilization']) * 3),
                                    initializer=self.init_counters,
                                    initargs=(records_current,
                                              records_next,
                                              self.args.copy())) as executor:
                futures = []

                while not records_current.empty():
                    record = records_current.get()

                    if record is None:
                        return

                    future = executor.submit(self.download_zip, record)
                    progress.advance(task_id, 0.25)
                    futures.append(future)

                for future in as_completed(futures):
                    self.complete_future(progress, task_id, futures, future)
        records_current.join()

        records_next.dump_to_queue(records_current)

    def complete_future(self, progress, task_id, futures, future):
        progress.advance(task_id, 0.75)
        futures.remove(future)
        del future

    @classmethod
    def get_page_data(cls, url):
        request = requests.get(url)

        page_content = BeautifulSoup(request.content, "html.parser")
        encoding = dict(request.headers)['Content-Encoding']
        bytes_length = dict(request.headers)['Content-Length']

        return {"page_content": page_content, "encoding": encoding, "bytes_length": bytes_length}

    @classmethod
    def get_base_url(cls, url):
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    @classmethod
    def fetch_form_values(cls, page_data, record):
        form_page_content = page_data['page_content']
        form = form_page_content.find_all('form', id='file_down')

        for element in form:
            for value in element:
                if type(value) is bs4.element.Tag:
                    match value.get("id"):
                        case "tk":
                            record.data_tk = value.get("value")
                        case "date":
                            record.data_date = value.get("value")
                        case "datemonth":
                            record.data_datemonth = value.get("value")
                        case "platform":
                            record.data_format = value.get("value")
                        case "timeframe":
                            record.data_timeframe = value.get("value")
                        case "fxpair":
                            record.data_fxpair = value.get("value")
        return record

    @classmethod
    def valid_format_timeframe_pair_urls(cls, formats, timeframes, pairs):
        for csv_format in formats:
            for timeframe in timeframes:
                if timeframe in get_valid_format_timeframes(csv_format):
                    for pair in pairs:
                        yield f"{csv_format}/{Timeframe[timeframe].value}/{pair}/", timeframe

    @classmethod
    def correct_for_zero_month(cls, month):
        if month == 0:
            month = 1
        return month

    @classmethod
    def generate_form_urls(cls,
                           start_yearmonth,
                           end_yearmonth,
                           formats,
                           pairs,
                           timeframes,
                           base_url):
        current_yearmonth = get_current_datemonth_gmt_plus5()
        current_year = int(get_year_from_datemonth(current_yearmonth))

        if start_yearmonth is None and end_yearmonth is None:
            start_yearmonth, end_yearmonth = "200001", current_yearmonth

        for sub_url, timeframe in cls.valid_format_timeframe_pair_urls(formats, timeframes, pairs):
            form_url = f"{base_url}?/{sub_url}"

            if end_yearmonth is None:
                for date_url in cls.yield_single_year_or_month(timeframe, start_yearmonth):
                    yield f"{form_url}{date_url}"
            else:
                start_year = int(get_year_from_datemonth(start_yearmonth))
                start_month = int(get_month_from_datemonth(start_yearmonth))
                end_year = int(get_year_from_datemonth(end_yearmonth))
                end_month = int(get_month_from_datemonth(end_yearmonth))

                for year in range(start_year, end_year + 1):
                    yield from cls.yield_range_of_yearmonths(year, timeframe, form_url,
                                                             start_year, start_month,
                                                             end_year, end_month,
                                                             current_year)

    @classmethod
    def yield_range_of_yearmonths(cls, year, timeframe, form_url,
                                  start_year, start_month,
                                  end_year, end_month,
                                  current_year):

        match year:
            case _ if year == current_year:
                for date_url in cls.yield_current_year(year,
                                                       start_year,
                                                       start_month,
                                                       end_year,
                                                       end_month):
                    yield f"{form_url}{date_url}"

            case _ if start_year == year == end_year:
                for date_url in cls.yield_same_year(timeframe, year, start_month, end_month):
                    yield f"{form_url}{date_url}"

            case _ if year == start_year != end_year:
                for date_url in cls.yield_start_year(timeframe, year, start_month):
                    yield f"{form_url}{date_url}"

            case _ if year == end_year != start_year:
                for date_url in cls.yield_end_year(timeframe, year, end_month):
                    yield f"{form_url}{date_url}"
            case _:
                for date_url in cls.yield_year(timeframe, year):
                    yield f"{form_url}{date_url}"

    @classmethod
    def yield_current_year(cls, year, start_year, start_month, end_year, end_month):
        if start_year == end_year:
            for month in range(start_month, end_month + 1):
                yield f"{year}/{month}"
        else:
            for month in range(1, end_month + 1):
                yield f"{year}/{month}"

    @classmethod
    def yield_same_year(cls, timeframe, year, start_month, end_month):
        match timeframe:
            case "M1":
                yield f"{year}"
            case _:
                for month in range(start_month, end_month + 1):
                    yield f"{year}/{month}"

    @classmethod
    def yield_start_year(cls, timeframe, year, start_month):
        match timeframe:
            case "M1":
                yield f"{year}"
            case _:
                for month in range(start_month, 12 + 1):
                    yield f"{year}/{month}"

    @classmethod
    def yield_end_year(cls, timeframe, year, end_month):
        match timeframe:
            case "M1":
                yield f"{year}"
            case _:
                for month in range(1, end_month + 1):
                    yield f"{year}/{month}"

    @classmethod
    def yield_year(cls, timeframe, year):
        match timeframe:
            case "M1":
                yield f"{year}"
            case _:
                for month in range(1, 12 + 1):
                    yield f"{year}/{month}"

    @classmethod
    def yield_single_year_or_month(cls, timeframe, start_yearmonth):

        current_yearmonth = get_current_datemonth_gmt_plus5()
        current_year = int(get_year_from_datemonth(current_yearmonth))
        current_month = int(get_month_from_datemonth(current_yearmonth))

        start_year = int(get_year_from_datemonth(start_yearmonth))
        start_month = int(get_month_from_datemonth(start_yearmonth))

        if start_month == 0:  # return the year's data
            if start_year == current_year:
                for month in range(1, current_month + 1):
                    yield f"{start_year}/{month}"
            else:
                for date_url in cls.yield_year(timeframe, start_year):
                    yield date_url
        else:
            if start_year == current_year:
                yield f"{start_year}/{start_month}"
            else:
                match timeframe:
                    case "M1":
                        yield f"{start_year}"
                    case _:
                        yield f"{start_year}/{start_month}"
