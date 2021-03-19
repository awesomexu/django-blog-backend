from django.db import models
from user.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200, null=False)
    pub_date = models.DateTimeField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Post <{self.pk}><{self.title}>'

    __str__ = __repr__


class Content(models.Model):
    post = models.OneToOneField(Post,on_delete=models.CASCADE)
    content = models.TextField(null=False)

    def __repr__(self):
        return f'Content <{self.pk}><{self.content[:20]}>'

    __str__ = __repr__