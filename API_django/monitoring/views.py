from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from datetime import datetime, timedelta
import jdatetime
from utils import return_before
from rest_framework.permissions import AllowAny, IsAuthenticated
from authe.models import Alborz, User
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
import os


headers = {'Content-Type': 'application/json',
         'Access-Control-Allow-Origin': os.environ.get('ALLOW_ORIGIN'),
         'Access-Control-Allow-Credentials': True,
         'Access-Control-Allow-Methods': 'OPTIONS',
         'Access-Control-Allow-Headers': ['Origin', 'Content-Type', 'Accept']}


def SendToAuth(token):
    respond = requests.post(url='http://127.0.0.1:8001/auth/', json={"token": token})
    return respond


class Monitor(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # take jwt token from request
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # take user from jwt token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED, headers=headers)

        geom_name = request.data.get('geom')
        user_geometry = Alborz.objects.filter(user=user)
        if not user_geometry.filter(id=geom_name).exists():
            Response(status=status.HTTP_403_FORBIDDEN)

        # get after time and URL
        after = datetime.now()
        after_jalali = jdatetime.date.fromgregorian(date=after)
        after_URL = f'zamin2:{geom_name}_{ after_jalali.strftime("%Y%m")}'

        # get before month time and URL
        before_month_URL = return_before(geom_name, after, 1)

        # get before season time and URL
        before_season_URL = return_before(geom_name, after, 3)

        # get before year time and URL
        before_year_URL = return_before(geom_name, after, 12)

        data = {
            "after": after_URL,
            "before_month": before_month_URL,
            "before_season": before_season_URL,
            "before_year": before_year_URL
        }
        return Response(status=status.HTTP_200_OK, data=data, headers=headers)

    def get(self, request):
        return Response(status=status.HTTP_200_OK, headers=headers)
