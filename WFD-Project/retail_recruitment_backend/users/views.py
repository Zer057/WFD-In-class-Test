from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, CandidateProfile, RecruiterProfile, ManagerProfile
from .serializers import (
    UserSerializer,
    CandidateProfileSerializer,
    RecruiterProfileSerializer,
    ManagerProfileSerializer,
)

class RegisterView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            role = user.role

            # Create associated profile based on role
            if role == 'candidate':
                CandidateProfile.objects.create(user=user)
            elif role == 'recruiter':
                RecruiterProfile.objects.create(user=user)
            elif role == 'manager':
                ManagerProfile.objects.create(user=user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

