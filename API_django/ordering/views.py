import json

from django.shortcuts import render
from .models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from  rest_framework import status
from authe.models import Alborz
import datetime
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.contrib.auth import get_user_model
from django.core import serializers
from django.contrib.gis.geos import MultiPolygon , MultiPoint , Polygon
from analysis import change_detection
from .change_detection import Change
import os
from django.contrib.gis.geos import GEOSGeometry , MultiPoint , Point

# Create your views here.
# TODO : 'path' parameter should be specified
class  OrderStatistics(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self , request):

        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)


        # get geom_id & check if it is in user geometries or not
        geom_id = request.data.get('geom_id')
        user_geometry = Alborz.objects.filter(user=user)
        if not user_geometry.filter(id=geom_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)



        # get before & after time
        before_time = request.data.get('before')
        # before_time = '1401-01-01'
        after_time = request.data.get('after')
        # after_time = '1401-03-01'
        try:
             datetime.datetime.strptime(before_time, '%Y-%m-%d')
             datetime.datetime.strptime(after_time, '%Y-%m-%d')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST , data={"fail" : "Incorrect date format! must be YYYY-mm-dd"})

        # get title
        title = request.data.get('title')
        if title is None:
            user_id = user.id
            title = f'{user_id}_{geom_id}_{before_time}_{after_time}'
        elif len(title) > 200:
            return Response(status=status.HTTP_400_BAD_REQUEST , data={"fail" : "title parameter is longer than 200 characters"})

        # get description
        description = request.data.get('description')

        # save order in DB
        try:
            order = Order()
            order.user = user
            order.geom_id = geom_id
            order.order_title = title
            order.order_description = description
            order.before_time = before_time
            order.after_time = after_time
            order.save()
        except:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE , data={"fail" : "order could not be registered. try again now or later!"})


        before_time_split = before_time.split("-")
        before_time_split_concat = f'{before_time_split[0]}{int(before_time_split[1])}'
        before_name = f'label_{before_time_split_concat}.tiff'

        after_time_split = after_time.split("-")
        after_time_split_concat = f'{after_time_split[0]}{int(after_time_split[1])}'
        after_name = f'label_{after_time_split_concat}.tiff'

        path = '/api_django'


        # get polygon & check if it is in geom or not
        polygon = request.data.get('polygon')
        try:
            polygon_type = GEOSGeometry(str(polygon['features'][0]['geometry']))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST , data={"fail" : "Incorrect polygon format!"})
        if not user_geometry.objects.filter(id=geom_id,geom__contains=polygon_type).exists():
            return Response(status=status.HTTP_403_FORBIDDEN , data={"fail" : "geom id does not contain polygon!"})


        change = Change(polygon = polygon , geom_id=geom_id , before_name=before_name , after_name=after_name , path=path)
        change.get_datasets()
        data , some = change.change_analysis()
        return Response(data=data , status=status.HTTP_200_OK)


class OrderObserv(APIView):
    def post(self , request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)

        try:
            # get multipoints & check correct format
            wrong_points = request.data.get('wrong')
            wrong_points_list = []
            for feature in wrong_points['features']:
                point = Point(feature['geometry']['coordinates'])
                wrong_points_list.append(point)
            wrong_points_multipoint = MultiPoint(*wrong_points_list)

            invest_need_points = request.data.get('investigated')
            invest_need_points_list = []
            for feature in invest_need_points['features']:
                point = Point(feature['geometry']['coordinates'])
                invest_need_points_list.append(point)
            invest_need_points_multipoint = MultiPoint(*invest_need_points_list)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST , data={"fail" : "Incorrect multipoint format"})


        # get order id and check order is for user or not
        order_id = request.data.get('order_id')
        order = Order.objects.filter(user = user , id=order_id)
        if not order.exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        # # assign points to order
        try:
            order.wrong_predicted = wrong_points_multipoint
            order.invest_needed = invest_need_points_multipoint
            order.save()
        except:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE , data={"fail" : "points could not be registered. try again now or later!"})

        return  Response(status=status.HTTP_200_OK)




class ShowOrder(APIView):
    permission_classes = [AllowAny]
    def get(self , request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        orders = Order.objects.filter(user = user)
        data = serializers.serialize('json' , orders)


        return  Response(status=status.HTTP_200_OK , data=data)



class Index(APIView):
    def get(self  , request):
        data = Alborz.objects.get(id = 1)
        data = serializers.serialize('json' , data , fields = ('geom'))
        return Response(data=data , status=status.HTTP_200_OK)
