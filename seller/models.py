from django.db import models
from django.contrib.auth.models import User


#class Category(models.Model):
#  name = models.CharField(max_length=200)

class Food(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)      # 상품 판매자
  name = models.CharField(max_length=20)
  price = models.IntegerField()
  description = models.TextField()
  image_url = models.URLField()

  def __str__(self) -> str:
    return self.name