import math
import simplejson
import datetime
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
from user.views import authentication
from .models import Post, Content
# Create your views here.


def get_all(request):
    try:
        try:
            page = request.GET.get('page')
            page = int(page)
            page = page if page>0 else 1
        except:
            page = 1

        try:
            size = request.GET.get('size')
            size = int(size)
            size = size if size>0 and size<101 else 20
        except:
            size = 20

        start = (page-1)*size
        result = Post.objects
        count = result.count()
        posts = result.order_by('-pk')[start:start+size]
        return JsonResponse({
            'posts': [{
                'post_id': post.id,
                'title': post.title
            } for post in posts],
            'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages': math.ceil(count/size)
            }
        })

    except Exception as e:
        print(e)
        return HttpResponseNotFound()


def get_one(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        return JsonResponse({
            'post': {
                'post_id': post.pk,
                'title': post.title,
                'pub_date': int(post.pub_date.timestamp()),
                'author': post.author.name,
                'author_id': post.author.pk,
                'content': post.content.content
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()


@authentication
def publish(request):
    try:
        payload = simplejson.loads(request.body)

        post = Post()
        post.title = payload['title']
        post.pub_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.author = request.user
        post.save()

        content = Content()
        content.post = post
        content.content = payload['content']
        content.save()

        return JsonResponse({
            'post_id': post.pk
        })

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()