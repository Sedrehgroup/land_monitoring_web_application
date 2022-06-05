from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, make_path_filter
import os
from glob import glob
import zipfile
import rasterio
import cv2
import numpy as np
from rasterio.merge import merge
from rasterio.mask import mask
import fiona
from rasterio.warp import calculate_default_transform, reproject
import shutil
from utils import LayerAdd

# username : sedreh1998
# password : 123456789

# username : mantis98
# password : 0123456789

# username : biomed.norouzi
# password : Alireza12851376


def get_images(start_time, end_time, path, cloud_percentage=50):
    geojson_path = os.path.join(path, 'alborz_province.geojson')

    api = SentinelAPI('mantis98', '0123456789')
    footprint = geojson_to_wkt(read_geojson(geojson_path))

    products = api.query(footprint,
                          date=(start_time, end_time),
                          producttype='S2MSI2A',
                          orbitdirection='DESCENDING',
                          platformname='Sentinel-2',
                          cloudcoverpercentage=(0, cloud_percentage),
                          )

    products_df = api.to_dataframe(products)
    products_df_sorted = products_df[products_df['title'].str.contains('R006_T39SVV') | products_df['title'].str.contains('R006_T39SVA') |products_df['title'].str.contains('R006_T39SWV') |products_df['title'].str.contains('R006_T39SWA')]
    print(products_df_sorted)
    api.download_all(products_df_sorted.index)


def unzip_images(path):
    print(os.getcwd())
    images_path = os.path.join(path, 'images')
    if not os.path.isdir(images_path):
        os.mkdir(images_path)
    print(images_path)

    unzip_path = os.path.join(images_path, 'unzip_files')
    if not os.path.isdir(unzip_path):
        os.mkdir(unzip_path)
    print(unzip_path)

    t39svv_path = glob(path+"/*R006_T39SVV*")
    t39sva_path = glob(path+"/*R006_T39SVA*")
    t39swv_path = glob(path+"/*R006_T39SWV*")
    t39swa_path = glob(path+"/*R006_T39SWA*")

    tiles = [t39svv_path, t39sva_path, t39swv_path, t39swa_path]

    for tile in tiles:
        for path_to_zip_file in tile:
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
                print('unzipped files!')

    print('unzip done!')


def select_background(path):
    unzip_path = os.path.join(path, 'images/unzip_files')
    background_path = os.path.join(path, 'images/background_images')

    if not os.path.isdir(background_path):
        os.mkdir(background_path)

    for root, dirs, files in os.walk(unzip_path):
        tci_files = [x for x in files if '_TCI_10m' in x]
        cloud_files = [y for y in files if 'MSK_CLDPRB_20m' in y]

        if len(tci_files) != 0:
            original = os.path.join(root, tci_files[0])
            target = os.path.join(background_path, tci_files[0])
            shutil.copy(original, target)
        if len(cloud_files) != 0:
            original = os.path.join(root, cloud_files[0])
            target = os.path.join(background_path, root.split("/")[-2]+cloud_files[0])
            shutil.copy(original, target)


def apply_mask(tci_image, cloud_image, cloud_masked_path, background_path):

    cloud_masked_sentinel = []

    sentinel_image = rasterio.open(tci_image)
    cloud_image = rasterio.open(cloud_image)

    metadata = sentinel_image.meta.copy()
    # make cloud mask
    mask = cloud_image.read()[0]
    sentinel = sentinel_image.read()
    mask = cv2.resize(mask, sentinel[1].shape, interpolation=cv2.INTER_AREA)
    mask = mask < 50

    # turn zero values to nan values
    out = mask.astype(sentinel.dtype)

    # apply mask on sentinel bands
    for i in range(len(sentinel)):
        cloud_masked_sentinel.append(out * sentinel[i])

    os.chdir(cloud_masked_path)

    image_name = tci_image.split('.')[0]
    with rasterio.open(image_name + '_cloud_masked.jp2', 'w', **metadata) as reprojected:
        reprojected.write(np.array(cloud_masked_sentinel))

    os.chdir(background_path)


def cloud_mask(path):
    cloud_masked_path = os.path.join(path, 'images/cloud_masked_images')
    background_path = os.path.join(path, 'images/background_images')

    if not os.path.isdir(cloud_masked_path):
        os.mkdir(cloud_masked_path)

    os.chdir(background_path)

    tiles = ['T39SVV', 'T39SVA', 'T39SWV', 'T39SWA']
    for tile in tiles:
        tile_tci_images = sorted(glob(f'{tile}*'))
        print(tile_tci_images)
        tile_cloud_images = sorted(glob(f'*_{tile}*'))
        print(tile_cloud_images)
        for i in range(len(tile_tci_images)):
            apply_mask(tci_image=tile_tci_images[i], cloud_image=tile_cloud_images[i], cloud_masked_path=cloud_masked_path, background_path=background_path)
            print('mask applied')


def median_images(path):
    cloud_masked_path = os.path.join(path, 'images/cloud_masked_images')
    os.chdir(cloud_masked_path)
    tiles = ['T39SVV', 'T39SVA', 'T39SWV', 'T39SWA']
    print(os.getcwd())

    print('starting combine images')
    for tile in tiles:
        tile_images = glob(tile+'*')
        print(tile_images)
        raster = []
        for image in tile_images:
            dataset = rasterio.open(image)
            metadata = dataset.meta.copy()
            raster.append(dataset.read())
        median_raster = np.median(raster, axis=0).astype('uint8')
        with rasterio.open(f'{tile}_median.jp2', 'w', **metadata) as tile_dataset:
            tile_dataset.write(np.array(median_raster))
    print('median_images')


def mosaic_images(path):
    cloud_masked_path = os.path.join(path, 'images/cloud_masked_images')
    os.chdir(cloud_masked_path)

    print('glob median images')
    median_src = glob('*median*')
    src_files_to_mosaic = []
    for fp in median_src:
        src = rasterio.open(fp)
        metadata = src.meta.copy()
        src_files_to_mosaic.append(src)

    mosaic, out_trans = merge(src_files_to_mosaic)
    metadata.update({'transform': out_trans, 'width': mosaic.shape[2], 'height': mosaic.shape[1]})

    alborz_path = os.path.join(path, 'images/alborz')
    if not os.path.isdir(alborz_path):
        os.mkdir(alborz_path)
    os.chdir(alborz_path)

    print('create alborz images')
    with rasterio.open(alborz_path+'/alborz_median.jp2', 'w', **metadata) as tile_dataset:
        tile_dataset.write(np.array(mosaic))
    print('alborz image created')


def turn_jp2_tiff(jp2_dataset, path):
    target_crs = 'EPSG:4326'
    transform, width, height = calculate_default_transform(jp2_dataset.crs, target_crs, jp2_dataset.width,
                                                           jp2_dataset.height,
                                                           *jp2_dataset.bounds)
    metadata = jp2_dataset.meta.copy()
    metadata.update({'driver': 'GTiff', 'crs': target_crs, 'transform': transform, 'width': width, 'height': height})

    with rasterio.open(path, 'w', **metadata) as reprojected:
      for band in range(1, jp2_dataset.count + 1):
          reproject(
              source=rasterio.band(jp2_dataset, band),
              destination=rasterio.band(reprojected, band),
              src_transform=jp2_dataset.transform,
              src_crs=jp2_dataset.crs,
              dst_transform=transform,
              dst_crs=target_crs
          )


def crop_images(path, time=14012):
    print('starting')
    alborz_path = os.path.join(path, 'images/alborz')
    aoi_file = fiona.open(os.path.join(path, 'shape_files/alborz.shp'))
    aoi_file_province = fiona.open(os.path.join(path, 'shape_files/Palborz.shp'))

    dataset = rasterio.open(os.path.join(alborz_path, 'alborz_median.jp2'))

    for i in range(len(aoi_file)):
        geometry = [aoi_file[i]['geometry']]
        per_name = [aoi_file[i]['properties']['PER_NAM']]
        print(per_name, ':', i)

        out_meta = dataset.meta.copy()
        out_image, out_transform = mask(dataset, geometry, crop=True)
        out_meta.update({"height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform})

        directory_path = os.path.join(alborz_path, str(i+1))
        if not os.path.isdir(directory_path):
            os.mkdir(directory_path)

        out_raster = rasterio.open(os.path.join(directory_path, f'{time}.jp2'), 'w', **out_meta)
        out_raster.write(out_image)

        # turn jp2 to tiff file
        tiff_path = os.path.join(directory_path, f'{time}.tiff')
        turn_jp2_tiff(jp2_dataset=out_raster, path=tiff_path)
        print(i)

    dataset = rasterio.open(os.path.join(alborz_path, 'alborz_median.jp2'))
    out_meta = dataset.meta.copy()
    geometry = [aoi_file_province[0]['geometry']]

    out_image, out_transform = mask(dataset, geometry, crop=True)
    out_meta.update({"height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    province_path = os.path.join(alborz_path, 'province')
    if not os.path.isdir(province_path):
        os.mkdir(province_path)

    out_raster = rasterio.open(os.path.join(province_path, f'{time}.jp2'), 'w', **out_meta)
    out_raster.write(out_image)

    tiff_path = os.path.join(province_path, f'{time}.tiff')
    turn_jp2_tiff(jp2_dataset=out_raster, path=tiff_path)

    list_images = [str(item + 1) for item in range(30)]
    list_images.append("province")
    LayerAdd(filename=f'{time}.tiff', region_id=list_images, province='alborz').tif_add()


def delete_images(path):
    os.chdir(path)

    zip_files = glob(path+'/*.zip')
    for file in zip_files:
        os.remove(file)

    os.remove(path+'/images/alborz/alborz_median.jp2')

    shutil.rmtree(path+'/images/background_images')
    shutil.rmtree(path+'/images/unzip_files')
    shutil.rmtree(path+'/images/cloud_masked_images')


