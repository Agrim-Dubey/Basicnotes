from rest_framework import serializers
from notes.models import Note
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^[A-Za-z0-9\s]{5,20}$',
             message="Username must be 5–20 characters and can include letters, numbers, and spaces"
        )],
        trim_whitespace=True
    )
    password = serializers.CharField(
        write_only=True,
        validators=[RegexValidator(
            regex=r'^[A-Za-z0-9@#$^&+=]{5,20}$',
            message="Password must be 5–20 characters and can include letters, numbers, and @#$^&+="
        )]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'image', 'create_date']

