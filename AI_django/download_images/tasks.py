from celery import shared_task
from download_images.get_images import get_images, unzip_images, select_background
from download_images.cloud_mask import cloud_mask
from download_images.apply_model import median_images, AI_image_preparation, run_model
from download_images.mosaic_images import mosaic_labels, stack_tci_files, mosaic_alborz_tiles, crop_images
from datetime import datetime
from dateutil.relativedelta import relativedelta
from download_images.DateTime import date_time
from image_analysis.label_analysis import update_database
import os


@shared_task(autoretry_for=(Exception,), retry_kwargs={'b': 7, 'countdown': 5})
def download_base_images():
    path = os.getcwd()
    end_time = datetime.today().strftime('%Y%m%d')
    start_time = (datetime.today() - relativedelta(months=1)).strftime('%Y%m%d')

    date, _ = date_time()

    print('path : ', path)
    get_images(start_time=start_time, end_time=end_time, path=path)
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
