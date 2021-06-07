from django.db import models
from django.contrib.auth.models import User,UserManager
from django.urls import reverse

class Post(models.Model):
    content = models.TextField(max_length='400',blank=False)
    conimage = models.ImageField(blank=False, upload_to = 'images')
    date_post = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("confessions-home")  

class Home(models.Model):
    image = models.ImageField(blank=False)
    likes = models.ManyToManyField(User, blank=True,related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_post = models.DateField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("detail", kwargs={'id': self.pk})  
 
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userImage = models.ImageField(upload_to = "Profiles", default = "default/default.jpg")
    bio = models.TextField(max_length='200', blank=True)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)


    def __str__(self):
        return str(self.user)
 

class Following(models.Model):
    """ Following of the user """
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    followed = models.ManyToManyField(User, related_name="followed")
    follower = models.ManyToManyField(User, related_name="follower")

    @classmethod
    def follow(cls, user, another_account):
        obj,vcreate = cls.objects.get_or_create(user = user)
        obj.followed.add(another_account)

    @classmethod
    def unfollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.remove(another_account)
        print("unfollowed")

    def __str__(self):
        return str(self.user)

