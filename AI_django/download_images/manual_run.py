from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import jdatetime
from download_images.get_images import get_images, unzip_images, select_background
from download_images.cloud_mask import cloud_mask
from download_images.apply_model import median_images, AI_image_preparation, run_model
from download_images.mosaic_images import mosaic_labels, stack_tci_files, mosaic_alborz_tiles, crop_images
from image_analysis.label_analysis import update_database


def jalali_to_gregorian(date):
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    date_gregorian = jdatetime.date(year=year, month=month, day=day).togregorian()
    return date_gregorian.strftime("%Y%m%d")


def sentinel_download(start_date_string, end_date_string):
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
        AI_image_preparation(path=path)
        run_model(path=path)
        mosaic_labels(path=path)
        stack_tci_files(path=path)
        mosaic_alborz_tiles(path=path)
        crop_images(path=path, time=date)
        update_database(path=path, date=date)


# start_date_string = '14000101'
# end_date_string = '14000201'





