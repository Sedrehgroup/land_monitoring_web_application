from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, make_path_filter
import os
from glob import glob
import zipfile
import shutil

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
    images_path = os.path.join(path, 'images')
    if not os.path.isdir(images_path):
        os.mkdir(images_path)

    unzip_path = os.path.join(images_path, 'unzip_files')
    if not os.path.isdir(unzip_path):
        os.mkdir(unzip_path)

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

    os.chdir(path)
    zip_files = glob(path+'/*.zip')
    for file in zip_files:
        os.remove(file)

    print('zip files removed')


def select_background(path):
    unzip_path = os.path.join(path, 'images/unzip_files')
    background_path = os.path.join(path, 'images/background_images')

    if not os.path.isdir(background_path):
        os.mkdir(background_path)

    for root, dirs, files in os.walk(unzip_path):
        tci_files = [x for x in files if '_TCI_10m' in x]
        b02_files = [x for x in files if '_B02_10m' in x]
        b03_files = [x for x in files if '_B03_10m' in x]
        b04_files = [x for x in files if '_B04_10m' in x]
        b05_files = [x for x in files if '_B05_20m' in x]
        b06_files = [x for x in files if '_B06_20m' in x]
        b07_files = [x for x in files if '_B07_20m' in x]
        b08_files = [x for x in files if '_B08_10m' in x]
        b08a_files = [x for x in files if '_B8A_20m' in x]
        b11_files = [x for x in files if '_B11_20m' in x]
        b12_files = [x for x in files if '_B12_20m' in x]
        cloud_files = [y for y in files if 'MSK_CLDPRB_20m' in y]

        if len(tci_files) != 0:
            original = os.path.join(root, tci_files[0])
            target = os.path.join(background_path, tci_files[0])
            shutil.copy(original, target)

        if len(b02_files) != 0:
            original = os.path.join(root, b02_files[0])
            target = os.path.join(background_path, b02_files[0])
            shutil.copy(original, target)

        if len(b03_files) != 0:
            original = os.path.join(root, b03_files[0])
            target = os.path.join(background_path, b03_files[0])
            shutil.copy(original, target)

        if len(b04_files) != 0:
            original = os.path.join(root, b04_files[0])
            target = os.path.join(background_path, b04_files[0])
            shutil.copy(original, target)

        if len(b05_files) != 0:
            original = os.path.join(root, b05_files[0])
            target = os.path.join(background_path, b05_files[0])
            shutil.copy(original, target)

        if len(b06_files) != 0:
            original = os.path.join(root, b06_files[0])
            target = os.path.join(background_path, b06_files[0])
            shutil.copy(original, target)

        if len(b07_files) != 0:
            original = os.path.join(root, b07_files[0])
            target = os.path.join(background_path, b07_files[0])
            shutil.copy(original, target)

        if len(b08_files) != 0:
            original = os.path.join(root, b08_files[0])
            target = os.path.join(background_path, b08_files[0])
            shutil.copy(original, target)

        if len(b08a_files) != 0:
            original = os.path.join(root, b08a_files[0])
            target = os.path.join(background_path, b08a_files[0])
            shutil.copy(original, target)

        if len(b11_files) != 0:
            original = os.path.join(root, b11_files[0])
            target = os.path.join(background_path, b11_files[0])
            shutil.copy(original, target)

        if len(b12_files) != 0:
            original = os.path.join(root, b12_files[0])
            target = os.path.join(background_path, b12_files[0])
            shutil.copy(original, target)

        if len(cloud_files) != 0:
            original = os.path.join(root, cloud_files[0])
            target = os.path.join(background_path, root.split("/")[-2]+cloud_files[0])
            shutil.copy(original, target)

    shutil.rmtree(unzip_path)
