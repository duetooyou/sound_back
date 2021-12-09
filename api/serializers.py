from rest_framework import serializers
from .models import Company, Studio, Record
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password', 'password_confirmation')
        }
        data['password'] = validated_data['password']
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'password1', 'password2',
            'first_name', 'last_name',
        )
        read_only_fields = ('id',)


class CompanySerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:
        model = Company
        fields = ('id', 'name', 'owner', 'company_logo',)
        read_only_fields = ('id', 'owner',)


class CompanyNonValidateSerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        extra_kwargs = {'name': {
            'validators': [],
            }
        }
        read_only_fields = ('company_logo',)


class StudioSerializer(serializers.ModelSerializer):

    company = CompanyNonValidateSerializer()

    class Meta:
        model = Studio
        fields = '__all__'


class StudioSerializerForRecord(StudioSerializer):

    company = serializers.StringRelatedField()

    class Meta(StudioSerializer.Meta):
        model = Studio
        fields = ('id', 'name', 'company')
        extra_kwargs = {'name': {
            'validators': [],
            }
        }


class RecordSerializer(serializers.ModelSerializer):

    studio = StudioSerializerForRecord()

    class Meta:
        model = Record
        fields = '__all__'
