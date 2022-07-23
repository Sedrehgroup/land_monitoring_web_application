from utils import LayerAdd
import os


for root , dirs , files in os.walk('/ai_django/images/alborz'):
    if len(files) == 0 :
        pass
    else:
        directory = root.split('/')
        region_id = [directory[-1]]
        province = directory[-2]
        for item in files:
            if item.startswith('TCI'):
                filename = item
                print(province , region_id , filename)
                LayerAdd(filename=filename , region_id=region_id , province=province).tif_add()
