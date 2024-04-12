import datetime
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# videostreamingapp/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Video
from .serializers import VideoSerializer
from rest_framework.authtoken.models import Token 
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from datetime import datetime, timedelta
import jwt

@csrf_exempt
@api_view(["POST"])
def signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    data = json.loads(request.body.decode("utf-8"))
    username = data.get("username", "")
    password = data.get("password", "")


    if not (username and password):
        return JsonResponse({"error": "Username and password are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    try:
        user = User.objects.create_user(username=username, password=password)
   
        
        return JsonResponse({"message": "User created successfully"})
    except Exception as e:
        print("An error occurred:", e)
        return JsonResponse({"error": "Failed to create user"}, status=500)

@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Calculate expiration time
        expiration_time = datetime.utcnow() + timedelta(days=1)
        
        # Convert expiration_time to string
        expiration_time_str = expiration_time.strftime('%Y-%m-%dT%H:%M:%S')

        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'expiration_time': expiration_time_str  # Serialized expiration time
        }, 'your_secret_key', algorithm='HS256')

        return Response({'token': token})
    else:
        return Response({'error': 'Invalid username or password.'}, status=400)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_video(request):
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def video_detail(request, pk):
    try:
        video = Video.objects.get(pk=pk, )
    except Video.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = VideoSerializer(video)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        video.delete()
        return Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_videos(request):
    query = request.query_params.get('query', '')
    videos = Video.objects.filter(name__icontains=query, owner=request.user)
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_videos(request):
    videos = Video.objects.filter(owner=request.user)
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)
