from geoserver.geoserver import create_layer_with_store , get_or_create_workspace , exist_layer
from django.conf import settings
import os
import requests


class LayerAdd():
    def __init__(self, filename, region_id, province):
        # self.workspace = get_or_create_workspace()
        self.layer_name = filename.split('.')[0]
        self.filename = filename
        self.store_name = self.layer_name
        self.path = settings.GEOSERVER.get('RASTER_URL')
        self.region_id = region_id
        self.province = province
        self.url = None
        self.layer = None

    def tif_add(self):
        for item in self.region_id:
            self.url = os.path.join(self.path, self.province, item, self.filename)
            self.layer = item+'_'+self.layer_name
            if exist_layer(self.layer):
                print('layer exists! ignoring.. ')
                break
            create_layer_with_store(data_type='tiff', url=self.url, layer_name=self.layer, store_name=self.layer )
            self.input_transparent()
        return self.layer

    def input_transparent(self):
        user = settings.GEOSERVER.get('USERNAME')
        password = settings.GEOSERVER.get('PASSWORD')
        workspace = settings.GEOSERVER.get('WORKSPACE')
        host = settings.GEOSERVER.get('HOST')
        port = settings.GEOSERVER.get('PORT')
        headers = {
            'Content-Type': 'text/xml',
        }
        data = '<coverage><parameters><entry><string>InputTransparentColor</string><string>#000000</string></entry></parameters></coverage>'
        response = requests.put(f'http://{host}:{port}/geoserver/rest/workspaces/{workspace}/coveragestores/{self.layer}/coverages/{self.layer}.xml',
                                headers=headers, data=data, auth=(user, password))
