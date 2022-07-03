from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .change_detection import Change
import os
from .models import AlborzUrban, AlborzBare, AlborzRoad, AlborzGrass, AlborzTree, Alborz, AlborzWater , AlborzCropLand
from django.core import serializers
import json
import shapely.wkt
import geojson
from download_images.manual_run import sentinel_download


model_index = {
    'tree': AlborzTree,
    'urban': AlborzUrban,
    'grass': AlborzGrass,
    'water': AlborzWater,
    'crop': AlborzCropLand,
    'road': AlborzRoad,
    'bare': AlborzBare
}


class ChangeDetectionStatics(APIView):
    def post(self, request):
        geom_id = request.data["geom_id"]
        before_name = request.data["before_name"]
        after_name = request.data["after_name"]
        path = os.getcwd()

        p1 = Change(geom_id, before_name, after_name, path)
        p1.get_datasets()
        result, _ = p1.change_analysis()
        return Response(data=result, status=status.HTTP_200_OK)


class ChangeDetectionPolygon(APIView):
    def post(self, request):
        class_change = request.data['class_change']
        geom_id = request.data['geom_id']
        before_name = request.data['before_name']
        after_name = request.data['after_name']
        path = os.getcwd()

        p1 = Change(geom_id, before_name, after_name, path)
        p1.get_datasets()
        geom = p1.get_polygons(class_change)
        return Response(data=geom, status=status.HTTP_200_OK)


class ClassStaticsGeom(APIView):
    def post(self, request):
        data = []

        geom_id = request.data.get('geom_id')
        geom_model = Alborz.objects.get(id= geom_id)

        date = request.data.get('date')
        date_year , date_month = date[:4], date[4:]

        tree_model = serializers.serialize('json', AlborzTree.objects.filter(region = geom_model , date__year = date_year , date__month = date_month))
        data.append({"tree" : json.loads(tree_model)})

        urban_model = serializers.serialize('json', AlborzUrban.objects.filter(region = geom_model , date__year = date_year , date__month = date_month))
        data.append({"urban": json.loads(urban_model)})

        bare_model = serializers.serialize('json', AlborzBare.objects.filter(region = geom_model , date__year = date_year , date__month = date_month))
        data.append({"bare": json.loads(bare_model)})

        road_model = serializers.serialize('json', AlborzRoad.objects.filter(region = geom_model , date__year = date_year , date__month = date_month))
        data.append({"road": json.loads(road_model)})

        grass_model = serializers.serialize('json', AlborzGrass.objects.filter(region = geom_model , date__year = date_year , date__month = date_month))
        data.append({"grass": json.loads(grass_model)})

        water_model = serializers.serialize('json', AlborzWater.objects.filter(region = geom_model , date__year = date_year , date__month = date_month))
        data.append({"water": json.loads(water_model)})

        crop_model = serializers.serialize('json', AlborzCropLand.objects.filter(region = geom_model , date__year = date_year , date__month = date_month))
        data.append({"crop": json.loads(crop_model)})

        return Response(status=status.HTTP_200_OK, data=data)


# (region_id , date , class): (area , plygon)


class ClassStatics(APIView):
    def post(self , request):
        data = []

        geom_id = request.data.get('geom_id')
        geom_model = Alborz.objects.get(id = geom_id)

        date = request.data.get('date')
        date_year , date_month = date[:4] , date[4:]

        tree_model = serializers.serialize('json', AlborzTree.objects.filter(region = geom_model , date__year = date_year , date__month = date_month) , fields = ('date' , 'area' , 'region'))
        data.append({"tree" : json.loads(tree_model)})

        urban_model = serializers.serialize('json', AlborzUrban.objects.filter(region = geom_model , date__year = date_year , date__month = date_month) , fields = ('date' , 'area' , 'region'))
        data.append({"urban": json.loads(urban_model)})

        bare_model = serializers.serialize('json', AlborzBare.objects.filter(region = geom_model , date__year = date_year , date__month = date_month) , fields = ('date' , 'area' , 'region'))
        data.append({"bare": json.loads(bare_model)})

        road_model = serializers.serialize('json', AlborzRoad.objects.filter(region = geom_model , date__year = date_year , date__month = date_month) , fields = ('date' , 'area' , 'region'))
        data.append({"road": json.loads(road_model)})

        grass_model = serializers.serialize('json', AlborzGrass.objects.filter(region = geom_model , date__year = date_year , date__month = date_month) , fields = ('date' , 'area' , 'region'))
        data.append({"grass": json.loads(grass_model)})

        water_model = serializers.serialize('json', AlborzWater.objects.filter(region = geom_model , date__year = date_year , date__month = date_month) , fields = ('date' , 'area' , 'region'))
        data.append({"water": json.loads(water_model)})

        crop_model = serializers.serialize('json', AlborzCropLand.objects.filter(region = geom_model , date__year = date_year , date__month = date_month) , fields = ('date' , 'area' , 'region'))
        data.append({"crop": json.loads(crop_model)})

        return Response(status=status.HTTP_200_OK , data=data)


class ClassIndiv(APIView):
    def post(self, request):

        geom_id = request.data.get('geom_id')
        geom_model = Alborz.objects.get(id=geom_id)

        date = request.data.get('date')
        date_year, date_month = date[:4], date[4:]

        classify = request.data.get('classify')

        model = serializers.serialize('json', model_index[str(classify)].objects.filter(region=geom_model, date__year=date_year, date__month=date_month))
        wkt_data = json.loads(model)[0]["fields"]["geom"]
        wkt_data = wkt_data.split(";")[1]
        g1 = shapely.wkt.loads(wkt_data)
        g2 = geojson.Feature(geometry=g1, properties={})
        list_data = g2.geometry["coordinates"]
        data = []
        for index in list_data:
            data.append(index[0])

        return Response(status=status.HTTP_200_OK, data=data)


class ManualRun(APIView):
    def post(self, request):
        start_date_string = request.data.get('start_date_string')
        end_date_string = request.data.get('end_date_string')

        sentinel_download(start_date_string, end_date_string)
