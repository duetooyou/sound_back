from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import (viewsets,
                            generics,
                            permissions,
                            status,
                            response,
                            decorators, )
from ..serializers import (CompanySerializer,
                           StudioSerializer,
                           RecordSerializer,
                           UserSerializer, )
from ..models import Company, Studio, Record


class UserSignUPView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_view_name(self):
        return f"Список пользователей"


class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.active.all()

    def create(self, request, *args, **kwargs):
        try:
            return super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)
        except IntegrityError:
            content = {'Внимание': 'Для одного аккаунта вы можете'
                                   'зарегистрировать только одну компанию.'
                                   'Спасибо за понимание'}
            return response.Response(content, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_view_name(self):
        return f"Ваша компания"


class StudioView(viewsets.ModelViewSet):
    serializer_class = StudioSerializer

    def get_queryset(self):
        return Studio.objects.filter(company__owner=self.request.user)

    def perform_create(self, serializer):
        if Company.active.filter(owner=self.request.user).exists():
            company_object = Company.active.get(owner=self.request.user)
            serializer.save(company=company_object)
        else:
            serializer.save()

    def get_view_name(self):
        return f"Список ваших студий"


class RecordStudioView(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()

    @decorators.action(detail=True, url_path='single-studio')
    def get_studio_records(self, request, pk):
        single_studio_records = Record.objects.filter(studio_id=pk)
        serializer = RecordSerializer(single_studio_records, many=True)
        return response.Response(serializer.data)

    @decorators.action(detail=False, url_path='single-company')
    def get_company_records(self, request):
        print(self.get_queryset())
        single_company_records = Record.objects.filter(studio__company__owner=self.request.user)
        serializer = RecordSerializer(single_company_records, many=True)
        return response.Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(studio=Studio.objects.get(name=self.request.data['studio.name']))

    def get_view_name(self):
        return f"Сеансы студий и компаний"
