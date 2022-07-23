from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils import return_all
from rest_framework import status
from authe.models import Alborz, User
from rest_framework.permissions import AllowAny , IsAuthenticated
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
import os


headers = {'Content-Type': 'application/json',
         'Access-Control-Allow-Origin': os.environ.get('ALLOW_ORIGIN'),
         'Access-Control-Allow-Credentials': True,
         'Access-Control-Allow-Methods': 'OPTIONS',
         'Access-Control-Allow-Headers': ['Origin', 'Content-Type', 'Accept']}


class Index(APIView):
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

        geom_name = request.data.get('geom')
        user_geometry = Alborz.objects.filter(user=user)
        if user_geometry.filter(id=geom_name).exists():
            # get before and after from request
            before = request.data.get('before')  # that must be like 140101
            after = request.data.get('after')  # that must be like 140102

            # get before and after URL from utils
            beforeURL, afterURL = return_all(geom_name, before, after)

            data = {
                "before": beforeURL,
                "after": afterURL
            }
            return Response(data=data, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, headers=headers)



