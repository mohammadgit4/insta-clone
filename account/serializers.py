from .models import User
from .sms import send_sms
from random import randint
from django.core.mail import send_mail
from rest_framework import serializers
from django.conf import settings
from django.core.validators import MinLengthValidator
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError

# E called for EMAIL
class RegisterESLR(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'password', 'confirm_password')

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('this email has already been registered.')
        elif attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("you must enter the same password ( password and confirm_password ) twice in order to confirm it")
        else:
            link = f'http://{self.context["domain"]}/user/activate/'
            send_mail('activate your user', f'click link below and follow instruction to activate your user\n link ---> {link}', settings.EMAIL_HOST, (attrs['email'],))
            return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

class ActivateEmailSLR(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(style={'input_type_type':'password'})
    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists() and User.objects.get(email=attrs['email']).check_password(attrs['password']):
            user = User.objects.get(email=attrs['email'])
            if user.is_active:
                raise serializers.ValidationError('user is already activated')
            else:
                user.is_active = True
                user.save()
                return attrs
        else:
            raise AuthenticationFailed('the email or password that you entered does not match an account')

# P called for PHONE NO
class RegisterPSLR(serializers.ModelSerializer):
    phone_no = serializers.CharField(validators =[MinLengthValidator(9)], max_length=10)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('country_code', 'phone_no', 'username', 'full_name', 'password', 'confirm_password')

    def validate(self, attrs):
        if User.objects.filter(phone_no=attrs['phone_no']).exists():
            raise serializers.ValidationError("a user with that phone-no already exists.")
        elif attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("you must enter the same password ( password and confirm_password ) twice in order to confirm it")
        else:
            link = f'http://{self.context["domain"]}/user/activate-phone/'
            phone_no = f'+{attrs["country_code"]} {attrs["phone_no"]}'
            send_sms(f'click link below and follow instruction to activate your user\n link ---> {link}', phone_no)
            return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)
        
class ActivatePhoneSLR(serializers.Serializer):
    country_code = serializers.CharField(validators =[MinLengthValidator(2)], max_length=4)
    phone_no = serializers.CharField(validators =[MinLengthValidator(9)], max_length=10)
    password = serializers.CharField(style={'input_type_type':'password'})
    def validate(self, attrs):
        if User.objects.filter(country_code=attrs['country_code'], phone_no=attrs['phone_no']).exists() and User.objects.get(phone_no=attrs['phone_no']).check_password(attrs['password']):
            user = User.objects.get(phone_no=attrs['phone_no'])
            if user.is_active:
                raise serializers.ValidationError('user is already activated')
            else:
                user.is_active = True
                user.save()
                return attrs
        else:
            raise AuthenticationFailed('the phone_no or password that you entered does not match an account')


class LoginESLR(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ('email', 'password')
    
    def validate(self, attrs):
        if not User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('the email that you entered does not match an account')
        return attrs

class LoginPSLR(serializers.ModelSerializer):
    phone_no = serializers.CharField(validators =[MinLengthValidator(9)], max_length=10)
    class Meta:
        model = User
        fields = ('country_code', 'phone_no', 'password')
    
    def validate(self, attrs):
        if not User.objects.filter(phone_no=attrs['phone_no'] , country_code=attrs['country_code']).exists():
            raise serializers.ValidationError('the phone number that you entered does not match an account')
        return attrs

class ProfileSLR(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'phone_no', 'profile', 'date_of_birth', 'gender')

class ChangeP_SLR(serializers.ModelSerializer):
    current_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('current_password', 'password', 'confirm_password')

    def validate(self, attrs): 
        user = self.context.get('user')
        password = attrs['password']
        current_password = attrs['current_password']
        if user.check_password(current_password):
            if current_password == password:
                raise serializers.ValidationError('new password must be different from current password')
            elif password != attrs['confirm_password']:
                raise serializers.ValidationError("you must enter the same password ( password and confirm_password ) twice in order to confirm it")
            else:
                user.set_password(password)
                user.save()
                return attrs
        else:
            raise AuthenticationFailed("current password is not valid")

class SefcpSLR(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            user = User.objects.get(email=attrs['email'])
            link = f'http://{self.context["domain"]}/user/reset-password/{urlsafe_base64_encode(force_bytes(user.id))}/{PasswordResetTokenGenerator().make_token(user)}/'
            send_mail('password reset request', f'hey {user.full_name} we got a request to reset your password if you wish to change your password, please click the link below and follow the instructions to create a new one. \nlink ---> {link}', settings.EMAIL_HOST, (user.email, ))
            return attrs
        else:
            raise serializers.ValidationError("this email address that you've entered doesn't match an account")
        
class ResetP_SLR(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)

    def validate(self, attrs):
        id = smart_str(urlsafe_base64_decode(self.context['id']))
        token = self.context['token']
        user = User.objects.get(pk=id)
        password = attrs['password']
        if PasswordResetTokenGenerator().check_token(user, token):
            if user.check_password(attrs['password']):
                raise serializers.ValidationError('new password must be different from current password')
            elif password != attrs['confirm_password']:
                raise serializers.ValidationError("you must enter the same password ( password and confirm_password ) twice in order to confirm it")
            else:
                user.set_password(password)
                user.save()
                return attrs
        else:
            raise serializers.ValidationError("invalid token or expired!")

class Send2factorSLR(serializers.Serializer):
    def validate(self, attrs):
        otp = randint(100000, 999999)
        user = self.context['user']
        phone_no = f'+{user.country_code} {user.phone_no}'
        send_sms_to_phone = send_sms(f'your 2-factor verification code is \n otp = {otp}', phone_no),
        send_email = send_mail('otp for on 2-factor authentication', f'your 2-factor verification code is \n otp = {otp}', EMAIL_HOST, (user.email, ))
        if user.email and user.phone_no:
            send_sms_to_phone and send_email
        elif user.email:
            send_email
        elif user.phone_no:
            send_sms_to_phone
        user.otp = otp
        user.save()
        return attrs

class Activate2factorSLR(serializers.Serializer):
    otp = serializers.CharField(validators=[MinLengthValidator(6)], max_length=6)
    def validate(self, attrs):
        user = self.context['user']
        if user.otp != attrs['otp']:
            raise serializers.ValidationError('otp is not valid!')
        else:
            user.tfa = True
            user.save()
        return attrs