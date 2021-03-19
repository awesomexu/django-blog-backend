import datetime
import simplejson
import jwt
import bcrypt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from user.models import User
from django_blog import settings


AUTH_EXPIRE = 36000

# Create your views here.


def gen_token(user_id):
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE
        }
    , settings.SECRET_KEY, 'HS256')


def reg(request):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        query = User.objects.filter(email=email)
        print(query)
        if query:
            return HttpResponseBadRequest()

        name = payload['name']
        password = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt()).decode()
        print(f'email:{email},name:{name},password:{password}')

        user = User()
        user.email = email
        user.name = name
        user.password = password

        try:
            user.save()
            return HttpResponse()
        except:
            # 这里可用于标记数据库保存过程中产生的异常
            raise

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def login(request):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password']

        user = User.objects.filter(email=email).first()
        if not user:
            return HttpResponseBadRequest()
        if not bcrypt.checkpw(password.encode(), user.password.encode()):

            return HttpResponseBadRequest()
        return JsonResponse({
            'user': {
                'user_id': user.id,
                'user_email': user.email,
                'user_name': user.name
            },
            'token': gen_token(user.id)
        })

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def authentication(view):
    def wrapper(request):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # 过期处理（手动处理），使用exp字段，若过期decode时自动抛出异常
            # if (datetime.datetime.now().timestamp()-payload['timestamp']) > AUTH_EXPIRE:
            #     return HttpResponse(status=401)
            user_id = payload['user_id']
            user = User.objects.get(pk=user_id)
            request.user = user
        except Exception as e:
            print(e)
            return HttpResponse(status=401)
        return view(request)
    return wrapper


@authentication
def test(request):
    print(request.user.id)
    print(request.user.email)
    print(request.user.name)
    return HttpResponse()
