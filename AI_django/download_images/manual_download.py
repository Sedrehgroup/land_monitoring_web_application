from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import jdatetime
from download_images.get_data import get_images, unzip_images, select_background, cloud_mask, mosaic_images, median_images, crop_images, delete_images


def jalali_to_gregorian(date):
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    date_gregorian = jdatetime.date(year=year, month=month, day=day).togregorian()
    return date_gregorian.strftime("%Y%m%d")


def sentinel_downoad(start_date_string, end_date_string):
    path = os.getcwd()

    start_date = datetime.strptime(start_date_string, '%Y%m%d')
    end_date = datetime.strptime(end_date_string, '%Y%m%d')

    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    for month in range(num_months):
        start = (start_date + relativedelta(months=month)).strftime("%Y-%m-%d")
        date = (start_date + relativedelta(months=month)).strftime("%Y%m")
        start = jalali_to_gregorian(start)
        end = (start_date + relativedelta(months=month + 1)).strftime("%Y-%m-%d")
        end = jalali_to_gregorian(end)

        print('path : ', path)
        get_images(start_time=start, end_time=end, path=path)
        unzip_images(path=path)
        select_background(path=path)
        cloud_mask(path=path)
        median_images(path=path)
        mosaic_images(path=path)
        crop_images(path=path, time=date)
        delete_images(path=path)


# start_date_string = '14000101'
# end_date_string = '14000201'





