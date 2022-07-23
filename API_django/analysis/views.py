import jdatetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .change_detection import Change
import os
from .models import AlborzUrban, AlborzBare, AlborzRoad, AlborzGrass, AlborzTree, AlborzWater , AlborzCropLand
from authe.models import Alborz , User
from django.core import serializers
import json
import shapely.wkt
import geojson
from rest_framework.permissions import IsAuthenticated , AllowAny
from datetime import datetime , timedelta
from dateutil.relativedelta import *
from django.contrib.auth import get_user_model


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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)

        geom_id = request.data["geom_id"]
        user_geometry = Alborz.objects.filter(user=user)
        if not user_geometry.filter(id=geom_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN, headers=headers)
        before_name = request.data["before_name"]
        after_name = request.data["after_name"]
        path = os.getcwd()

        p1 = Change(geom_id, before_name, after_name, path)
        p1.get_datasets()
        result, _ = p1.change_analysis()
        return Response(data=result, status=status.HTTP_200_OK)


class ChangeDetectionPolygon(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)

        class_change = request.data['class_change']
        geom_id = request.data['geom_id']
        user_geometry = Alborz.objects.filter(user=user)
        if not user_geometry.filter(id=geom_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN, headers=headers)
        before_name = request.data['before_name']
        after_name = request.data['after_name']
        path = os.getcwd()

        p1 = Change(geom_id, before_name, after_name, path)
        p1.get_datasets()
        geom = p1.get_polygons(class_change)
        return Response(data=geom, status=status.HTTP_200_OK)


class ClassStaticsGeom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)

        data = []

        geom_id = request.data.get('geom_id')
        geom_model = Alborz.objects.get(id= geom_id)
        user_geometry = Alborz.objects.filter(user=user)
        if not user_geometry.filter(id=geom_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN, headers=headers)

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


class ClassStatics(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)


        geom_id = request.data.get('geom_id')
        geom_model = Alborz.objects.get(id = geom_id)
        user_geometry = Alborz.objects.filter(user=user)
        if not user_geometry.filter(id=geom_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN, headers=headers)
        date = request.data.get('date')
        date_year , date_month = date[:4] , date[4:]

        data = []
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)

        geom_id = request.data.get('geom_id')
        geom_model = Alborz.objects.get(id=geom_id)
        user_geometry = Alborz.objects.filter(user=user)
        if not user_geometry.filter(id=geom_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN, headers=headers)

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
            sub_data = []
            for sub in index[0]:
                sub_data.append([sub[1], sub[0]])
            data.append(sub_data)

        # for index in list_data:
        #     data.append(index[0])

        return Response(status=status.HTTP_200_OK, data=data)


class ManualRun(APIView):
    def post(self, request):
        start_date_string = request.data.get('start_date_string')
        end_date_string = request.data.get('end_date_string')

        sentinel_download(start_date_string, end_date_string)


def month_first(month):
    # 1401-07-07
    # 1401-07-01
    day = month.split('-')
    return f'{day[0]}-{day[1]}-01'


class ClassLastAreaChanges(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):

        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)

        # take geom model
        geom_id = request.data.get('geom')
        geom_model = Alborz.objects.get(id = geom_id)
        user_geometry = Alborz.objects.filter(user = user)
        if not user_geometry.filter(id = geom_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN, headers=headers)

        # take now time by str
        now_time = datetime.now()
        now_time_str = datetime.now().strftime("%Y-%m-%d")

        # take past times by str
        month_before = now_time + relativedelta(months=-1)
        month_before_str_jalali = month_first(jdatetime.date.fromgregorian(date=month_before).strftime("%Y-%m-%d"))

        three_months_before = now_time + relativedelta(months=-3)
        three_months_before_str_jalali =  month_first(jdatetime.date.fromgregorian(date=three_months_before).strftime("%Y-%m-%d"))

        year_before = now_time + relativedelta(years=-1)
        year_before_str_jalali =  month_first(jdatetime.date.fromgregorian(date=year_before).strftime("%Y-%m-%d"))

        data = []
        for key , value in model_index.items():
            # get model for each class
            item_model = value.objects.filter(region=geom_model)

            # take area from model for now time
            now_model = item_model.last()
            now_model_area  = now_model.area

            # take area from model for before times
            month_before_model_area = item_model.get(date = month_before_str_jalali).area
            three_months_before_model_area = item_model.get(date = three_months_before_str_jalali).area
            year_before_model_area = item_model.get(date = year_before_str_jalali).area

            # differ area
            month_before_differ = now_model_area - month_before_model_area
            three_months_before_differ = now_model_area - three_months_before_model_area
            year_before_differ = now_model_area - year_before_model_area

            data.append({
                key : {
                "month_before" : month_before_differ,
                "three_months_before" : three_months_before_differ,
                "year_before" : year_before_differ
                }
            })


        return Response(data=data , status=status.HTTP_200_OK)


class ClassYearAreaChanges(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):

        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)

        # take
        # year = jdatetime.date.fromgregorian(date=datetime.now()).strftime("%Y")

        # take geom model
        geom_id = request.data.get('geom')
        geom_model = Alborz.objects.get(id=geom_id)
        user_geometry = Alborz.objects.filter(user = user)
        if not user_geometry.filter(id = geom_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN, headers=headers)

        # take classify model for region needed
        classify = request.data.get('classify')
        class_model = model_index[classify].objects.filter(region=geom_model).order_by('-date')[:12]
        data = json.loads(serializers.serialize('json' , class_model , fields=('date','area')))

        return Response(data=data , status=status.HTTP_200_OK)

# TODO : it is just for test.
class Some(APIView):
    permission_classes =  [AllowAny]
    def get(self , request):

        data = get_user_model().objects.all()
        data = json.loads(serializers.serialize('json' , data))
        return  Response(data=data)
