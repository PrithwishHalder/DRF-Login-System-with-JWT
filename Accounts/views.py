from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_205_RESET_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from Task1.settings import EMAIL_HOST_USER
import secrets
import string
from Accounts.serializers import *
from Accounts.models import *


@api_view(['GET', ])
@permission_classes([AllowAny, ])
def index(request):
  routes = [
      'login/',
      'token/refresh/',
      'register/',
      'reset/',
      'forget/',
      'passReset/',
      'pages/',
      'logout/',
  ]

  return Response(routes)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def logout(request):
  try:
    refresh_token = request.data["refresh"]
    token = RefreshToken(refresh_token)
    token.blacklist()

    return Response(status=HTTP_205_RESET_CONTENT, data="Logout Successful")
  except Exception as e:
    return Response(status=HTTP_400_BAD_REQUEST, data="Logout Unsuccessful")


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def pages(request):

  data = {
      "username": request.user.username,
      "email": request.user.email
  }

  return Response(data)


@api_view(['POST'])
# Permission method for the function
@permission_classes([AllowAny, ])
def Register(request):

  if request.method == "POST":
    # Register User
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
      password = request.data['password']
      user = User.objects.create_user(
          email=request.data['email'], username=request.data['username'])
      user.set_password(password)
      user.save()
      # return data if validated
      data = serializer.data
    else:
      # return error if not validated
      data = serializer.errors

    return Response(data)


@api_view(['POST'])
# Permission method for the function
@permission_classes([IsAuthenticated, ])
def Reset(request):

  if request.method == "POST":

    # Check Data
    serializer = ResetSerializer(data=request.data)

    if serializer.is_valid():
      old_password = request.data['old_password']
      new_password = request.data['new_password']
      user = request.user
      obj = User.objects.get(username=user.username)
      if(obj.check_password(old_password)):
        obj.set_password(new_password)
        obj.save()
      # return data if validated
      data = serializer.data
    else:
      # return error if not validated
      data = serializer.errors

    return Response(data)


@api_view(['POST'])
# Permission method for the function
@permission_classes([AllowAny, ])
def ForgotPass(request):

  if request.method == "POST":
    username = request.data['username']
    email = request.data['email']
    user = User.objects.get(username=username, email=email)
    alphabet = string.ascii_letters + string.digits
    otp = ''.join(secrets.choice(alphabet) for i in range(12))
    Message = "Hello " + username + ",\n\tWe are sending you this email because you requested a forget password. \nUse "\
        "the given OTP to reset your password.\n\nYour OTP : " + \
        otp + "\n\nWith Regards,\nCelebal"

    try:
      data = {
          "user": user.id,
          "otp": otp
      }

      try:
        obj = OTP.objects.get(user=user)
        serializer = OTPSerializer(instance=obj, data=data)

      except Exception:

        serializer = OTPSerializer(data=data)
      finally:

        if serializer.is_valid():
          serializer.save()
          send_mail("Forget Password!", Message,
                    EMAIL_HOST_USER, [email, ])
          return Response(status=HTTP_200_OK, data=Message)
        else:
          return Response(serializer.errors)

    except Exception as e:
      return Response(e)


@api_view(['POST'])
# Permission method for the function
@permission_classes([AllowAny, ])
def ForgetPassReset(request):

  if request.method == "POST":
    username = request.data['username']
    email = request.data['email']
    user = User.objects.get(username=username, email=email)  # Get User info
    data = {
        "otp": request.data['otp'],
        "user": user.id
    }
    obj = OTP.objects.get(user=user)  # Get OTP info of user
    serializer = OTPSerializer(instance=obj, data=data)

    if serializer.is_valid():  # Validate the OTP and user info
      password = request.data['new_password']
      user.set_password(password)
      user.save()  # Save new Password
      obj.delete()  # Delete the OTP from DB
      return Response(status=HTTP_200_OK, data="Password Updated")

    else:
      return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)
