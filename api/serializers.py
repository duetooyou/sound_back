from rest_framework import serializers
from .models import Company, Studio, Record
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
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
