from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

    def get_user_ads(self):
        return Ad.objects.filter(author=self)


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    img_url = models.ImageField(upload_to='img/', null=True)

    # def author_data(self):
    #     return User.objects.get(id=self.author.id)