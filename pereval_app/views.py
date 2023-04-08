from django.db.utils import OperationalError
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *


class PerevalViewSet(viewsets.ModelViewSet):
    serializer_class = PerevalSerializer
    parser_classes = (MultiPartParser, FormParser)

    # получаем список перевалов по мэйлу пользователя:
    def get_queryset(self):
        user_email = self.request.query_params.get('user_email')
        if user_email:
            queryset = Pereval.objects.filter(user__email=user_email)
        else:
            path = self.request.get_full_path()
            if path == '/submitData/':
                queryset = Pereval.objects.none()
            else:
                queryset = Pereval.objects.all()
        return queryset


    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response({'post':'создан новый объект', 'id': f'{serializer.instance.id}', 'status':'200'})

    def retrieve(self, request, *args, **kwargs):
        try:
            if not Pereval.objects.filter(id=kwargs['pk']).exists():
                return Response({"error": "Такого объекта не существует"}, status=400)
            return super().retrieve(request, *args, **kwargs)
        except OperationalError:
            raise DBConnectException()
    def partial_update(self, request, *args, **kwargs):
        try:
            queryset = Pereval.objects.filter(id=kwargs['pk'])
            if not queryset.exists():
                return Response({"error": "Такого объекта не существует"}, status=400)
            query_object = queryset.first()
            if not query_object.status == 'new':
                return Response({"message": "Перевал на модерации, вы не можете его изменить",
                                 "state": 0}, status=400)
            response = super().partial_update(request, *args, **kwargs)
            response.data = {
                'status': "200",
                'message': 'Запись обновлена',
                'state': 1,
            }
            return response
        except OperationalError:
            raise DBConnectException()