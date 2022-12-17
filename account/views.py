from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ( RegisterESLR, RegisterPSLR, LoginESLR, LoginPSLR, 
                           ProfileSLR, ChangeP_SLR, SefcpSLR, ResetP_SLR,
                           ActivateEmailSLR, ActivatePhoneSLR, Activate2factorSLR,
                           Send2factorSLR )
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

    
def jwt(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Register With Email
class RegisterEVIEW(GenericAPIView):
    serializer_class = RegisterESLR
    def post(self, request):
        slr = self.serializer_class(data=request.data, context={'domain':request.META['HTTP_HOST']})
        slr.is_valid(raise_exception=True)
        slr.save()
        return Response({'message':'register with email successfully, please activate your user'}, status=HTTP_201_CREATED)

class ActivateEmailVIEW(GenericAPIView):
    serializer_class = ActivateEmailSLR
    def post(self, request):
        slr = self.serializer_class(data=request.data)
        slr.is_valid(raise_exception=True)
        return Response({'message':'user with email activate successfully'}, status=HTTP_200_OK)

# Register With Phone
class RegisterPVIEW(GenericAPIView):
    serializer_class = RegisterPSLR
    def post(self, request):
        slr = self.serializer_class(data=request.data, context={'domain':request.META['HTTP_HOST']})
        slr.is_valid(raise_exception=True)
        user = slr.save()
        return Response({'message':'register with phone successfully, please activate your user'}, status=HTTP_201_CREATED)

class ActivatePhoneVIEW(GenericAPIView):
    serializer_class = ActivatePhoneSLR
    def post(self, request):
        slr = self.serializer_class(data=request.data)
        slr.is_valid(raise_exception=True)
        return Response({'message':'user with phone activate successfully'}, status=HTTP_201_CREATED)
        
# Login With Email
class LoginEVIEW(GenericAPIView):
    serializer_class = LoginESLR
    def post(self, request):
        slr = self.serializer_class(data=request.data)
        slr.is_valid(raise_exception=True)
        email=slr.data['email'].lower()
        user = authenticate(email, password=slr.data['password'])
        if user is not None:
            return Response({'message':'login with email successfully','tokens':jwt(user)}, status=HTTP_200_OK)
        return Response({'error':"you've entered an incorrect password"}, status=HTTP_400_BAD_REQUEST)

# Login With Phone
class LoginPVIEW(GenericAPIView):
    serializer_class = LoginPSLR
    def post(self, request):
        slr = self.serializer_class(data=request.data)
        slr.is_valid(raise_exception=True)
        phone_no=slr.data['phone_no']
        user = authenticate(phone_no, password=slr.data['password'])
        if user is not None:
            return Response({'message':'login with phone successfully', 'tokens':jwt(user)}, status=HTTP_200_OK)
        return Response({'error':"you've entered an incorrect password"}, status=HTTP_400_BAD_REQUEST)

# Fatch Profile
class ProfileVIEW(RetrieveAPIView):
    serializer_class = ProfileSLR
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        slr = self.serializer_class(request.user)
        return Response({'message':'fatch profile successfully', 'data':slr.data}, status=HTTP_200_OK)

# for change password if you're alrealy loged in 
class ChangeP_VIEW(GenericAPIView):
    serializer_class = ChangeP_SLR
    throttle_classes = (UserRateThrottle,)
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        slr = self.serializer_class(data=request.data, context={'user':request.user})
        slr.is_valid(raise_exception=True)
        return Response({'message':'change password successfully'}, status=HTTP_200_OK)

# send email for change password
class SefcpVIEW(GenericAPIView):
    serializer_class = SefcpSLR
    throttle_classes = (UserRateThrottle,)
    def post(self, request):
        slr = self.serializer_class(data=request.data, context={'domain':request.META['HTTP_HOST']})
        slr.is_valid(raise_exception=True)
        return Response({'message':'email sent'}, status=HTTP_200_OK)

# change password view
class ResetP_VIEW(GenericAPIView):
    serializer_class = ResetP_SLR
    def post(self, request, uid, token):
        slr = self.serializer_class(data=request.data, context={'id':uid, 'token':token})
        slr.is_valid(raise_exception=True)
        return Response({'message':'reset password successfully'}, status=HTTP_200_OK)

class Send2factorVIEW(GenericAPIView):
    serializer_class = Send2factorSLR
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        slr = self.serializer_class(data=request.data, context={'user':request.user})
        slr.is_valid(raise_exception=True)
        return Response({'message':'send otp successfully'}, status=HTTP_200_OK)

class Activate2factorVIEW(GenericAPIView):
    serializer_class = Activate2factorSLR
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        slr = self.serializer_class(data=request.data, context={'user':request.user})
        slr.is_valid(raise_exception=True)
        return Response({'message':'activate 2-factor authentication successfully'}, status=HTTP_200_OK)