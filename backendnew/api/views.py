from django.shortcuts import render
from rest_framework import viewsets, status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import sailors,sailor_users
from django.http import JsonResponse
from .serializers import SailorSerializer,sailoruseserializer
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_verification_email(user, email):
    # Generate UID + token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    verification_link = f"http://127.0.0.1:8000/verify/{uid}/{token}/"

    subject = "Verify your email"
    from_email = "yourgmail@gmail.com"
    to = [email]

    # Plain text version (fallback)
    text_content = f"Please click the link to verify your email: {verification_link}"

    # HTML version (with button)
    html_content = f"""
    <html>
      <body>
        <p>Welcome! Please verify your email by clicking the button below:</p>
        <a href="{verification_link}" 
           style="background-color:#4CAF50;
                  color:white;
                  padding:10px 20px;
                  text-decoration:none;
                  border-radius:5px;">
           Verify Email
        </a>
        <p>If the button doesn't work, copy and paste this link into your browser:</p>
        <p>{verification_link}</p>
      </body>
    </html>
    """

    # Create email
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = sailor_users.objects.create(email=email, password=password)
    
    # send verification email
    send_verification_email(user, email)

    return JsonResponse({"message": "Verification email sent. Please check your inbox."})

class sailorlist(generics.ListAPIView):
    queryset = sailor_users.objects.all()
    serializer_class = sailoruseserializer
    

# Create your views here.
##########   Sailor Details   API ####################
class sailorusersdetails(generics.ListCreateAPIView):
    queryset = sailors.objects.all()
    serializer_class = SailorSerializer


@api_view(['POST'])
def create_sailor(request):
    name = request.data.get('name')
    email = request.data.get('email')
    age = request.data.get('age')
    rank = request.data.get('rank')
    experience_years = request.data.get('experience_years')
    spouse_name = request.data.get('spouse_name', None)
    childern_names = request.data.get('childern_names', None)
    home_location = request.data.get('home_location', None)
    hobbies = request.data.get('hobbies', None)
    company_name = request.data.get('company_name', None)
    try:
        sailor_user = sailor_users.objects.get(email=email)
    except sailor_users.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, 
                        status=status.HTTP_404_NOT_FOUND)
    if not name or not age or not rank or not experience_years:
        return Response({"error": "Missing required fields"}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    sailor = sailors.objects.create(
        name=name,
        age=age,
        rank=rank,
        experience_years=experience_years,
        spouse_name=spouse_name,
        childern_names=childern_names,
        home_location=home_location,
        hobbies=hobbies,
        company_name=company_name
    )
    return Response({'msg':"created successfully"}, status=status.HTTP_201_CREATED)


    
    



