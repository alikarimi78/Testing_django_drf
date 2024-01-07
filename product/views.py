from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializer import ProductSerializer
from .models import Product
from rest_framework import status
from config.exeption import PriceNotFound, CantUpdate, CantDelete


# Create your views here.

class AllTest(APIView):
    def get_queryset(self):
        return Product.objects.all()

    def post(self, request: Request, *args, **kwargs):
        data = ProductSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_201_CREATED)
        raise PriceNotFound()

        # param1 = request.query_params.get("param1")
        # param2 = request.query_params.get("param2")
        instance = self.get_queryset()
        data = ProductSerializer(instance=instance, many=True)
        return Response(data.data, status.HTTP_200_OK)

    def get(self, request: Request, *args, **kwargs):
        instance = self.get_queryset()
        data = ProductSerializer(instance, many=True)
        return Response(data.data)


class GetTest(APIView):

    def get_object(self, pk):
        instance = Product.objects.get(pk=pk)
        return instance

    def get(self, request: Request, *args, **kwargs):
        get_param = kwargs.get("pk")
        instance = self.get_object(get_param)
        data = ProductSerializer(instance=instance)
        return Response(data.data, status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        get_param = kwargs.get("pk")
        instance = self.get_object(get_param)
        data = request.data
        data = ProductSerializer(data=data, instance=instance, partial=True, context={"user": request.user})
        if data.is_valid():
            data.save()
            return Response(data.data, status.HTTP_202_ACCEPTED)
        raise CantUpdate()

    def delete(self, request: Request, *args, **kwargs):
        get_param = kwargs.get("pk")
        try:
            instance = self.get_object(get_param)
            instance.delete()
            return Response(data="the object was deleted", status=status.HTTP_204_NO_CONTENT)
        except:
            raise CantDelete()
