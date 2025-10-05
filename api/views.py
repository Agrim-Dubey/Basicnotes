from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from .serializers import UserSerializer, NoteSerializer
from notes.models import Note
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=UserSerializer,
        responses={
            201: openapi.Response('Created - User successfully registered', UserSerializer),
            400: 'Bad Request - Invalid input data',
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Note.objects.none()
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Retrieve all notes for the authenticated user",
        responses={
            200: openapi.Response('OK - Notes retrieved successfully', NoteSerializer(many=True)),
            401: 'Unauthorized - Invalid or missing token',
            403: 'Forbidden - Permission denied',
            500: 'Internal Server Error - Unexpected issue',
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Create a new note for the authenticated user",
        request_body=NoteSerializer,
        responses={
            201: openapi.Response('Created - Note successfully created', NoteSerializer),
            400: 'Bad Request - Invalid input data',
            401: 'Unauthorized - Invalid or missing token',
            500: 'Internal Server Error - Unexpected issue',
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Note.objects.none()
        return Note.objects.filter(user=self.request.user)
