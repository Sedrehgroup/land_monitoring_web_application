from celery import shared_task
from download_images.get_data import get_images, unzip_images, select_background, cloud_mask, mosaic_images, crop_images, delete_images
from datetime import datetime
from dateutil.relativedelta import relativedelta
from download_images.DateTime import date_time
import os


@shared_task(autoretry_for=(Exception,), retry_kwargs={'b': 7, 'countdown': 5})
def download_base_images():
    path = os.getcwd()
    end_time = datetime.today().strftime('%Y%m%d')
    start_time = (datetime.today() - relativedelta(months=1)).strftime('%Y%m%d')

    date, _ = date_time()

    get_images(start_time=start_time, end_time=end_time, path=path)
    unzip_images(path=path)
    select_background(path=path)
    cloud_mask(path=path)
    max_images(path=path)
    mosaic_images(path=path)
    crop_images(path=path, time=date)
    delete_images(path=path)
