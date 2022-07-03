import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .models import Alborz, User
from django.core import serializers


class UserGeometry(APIView):
    """return geometries of each user"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return  Response(status= status.HTTP_401_UNAUTHORIZED)

        data = []
        # user = User.objects.get(username='alid1')
        geometry = Alborz.objects.filter(user=user)
        print(geometry)
        for item in geometry:
            geom = {"id": item.id, "name": item.per_nam, "geometry": json.loads(item.geom.geojson)}
            data.append(geom)

        return Response(data=data)


class SetGeometry(APIView):
    """set geometry for each user by admin"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        geom_id = request.data.get('geom')

        try:
            user = User.objects.get(username=username)
            geom = Alborz.objects.get(id=geom_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.geom.add(geom)
        user.save()

        return Response(status=status.HTTP_200_OK)


class SetActive(APIView):
    """activate users by admin"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        user.is_verified = True
        user.save()

        return Response({"message": "done"})


class Geometry(APIView):
    """return all geometries by admin"""
    permission_classes = [AllowAny]

    def get(self, request):
        data = []
        geometry = Alborz.objects.all()
        for item in geometry:
            geom = {"id": item.id, "name": item.per_nam, "geometry": json.loads(item.geom.geojson)}
            data.append(geom)
        # data = serializers.serialize('json' , geom , fields = ('per_nam'))
        return Response(data=data, status=status.HTTP_200_OK)


class Users(APIView):
    """return all users by admin"""
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        data = serializers.serialize('json', users)
        return Response(data=data)
