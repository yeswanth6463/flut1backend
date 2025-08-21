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
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from .models import sailor_users   # make sure this is your User mode
import secrets
from django.core.cache import cache
from django.utils import timezone
from .utils import generate_token, verify_token 


from django.conf import settings

def send_verification_email(user, email=None):
    if email is None:
        email = user.email

    token = generate_token(user.pk)
    
    verification_link = f"http://127.0.0.1:8000/api/verify/{token}/"

    subject = "Verify your email"
    from_email = "yourgmail@gmail.com"
    to = [email]

    text_content = f"Please click the link to verify your email: {verification_link}"

    html_content = f"""
    <html>
    <body>
        <p>Welcome! Please verify your email by clicking the button below:</p>
        <p>
        <a href="{verification_link}" target="_blank"
            style="display:inline-block;
                    background-color:#4CAF50;
                    color:white;
                    padding:10px 20px;
                    text-decoration:none;
                    border-radius:5px;
                    font-weight:bold;">
            ✅ Verify Email
        </a>
        </p>
        <p>If the button doesn't work, copy and paste this link into your browser:</p>
        <p><a href="{verification_link}">{verification_link}</a></p>
    </body>
    </html>
    """


    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@api_view(['POST'])
def register_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return JsonResponse({"error": "Email and password are required"}, status=400)

    # ✅ Check if email already exists
    if sailor_users.objects.filter(email=email).exists():
        return JsonResponse({"msg": "User with this email already exists"}, status=208)

    
    user = sailor_users.objects.create(email=email)
    user.set_password(password)
    user.save()

    send_verification_email(user, email)

    return JsonResponse({"message": "Verification email sent. Please check your inbox."})

def verify_user(request, token):
    user_id = verify_token(token)
    if user_id:
        user = sailor_users.objects.get(pk=user_id)
        user.is_verified = True
        user.save()
        return HttpResponse("Email verified successfully")
    return HttpResponse("Invalid or expired link")


class sailorlist(generics.ListAPIView):
    queryset = sailor_users.objects.all()
    serializer_class = sailoruseserializer
    


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
        email = sailor_user,
        rank=rank,
        experience_years=experience_years,
        spouse_name=spouse_name,
        childern_names=childern_names,
        home_location=home_location,
        hobbies=hobbies,
        company_name=company_name
    )
    return Response({'msg':"created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST',"GET"])
def login_for_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = sailor_users.objects.get(email=email)
        except sailor_users.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, 
                            status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"error": "Incorrect password"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.is_verified:
            return Response({"error": "Email not verified"}, 
                            status=status.HTTP_403_FORBIDDEN)

        # Update last login time
        user.last_login = timezone.now()
        user.save()

        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)

    return Response({"message": "Use POST method to login"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



    
    



