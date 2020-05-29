from django.db import models


# Create your models here.
class User(models.Model):
    account = models.CharField(max_length=50, unique=True)
    pwd = models.CharField(max_length=32)
    reg_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = "t_user"


class UserInfo(models.Model):
    email = models.EmailField(null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    realname = models.CharField(max_length=100, null=True, blank=True)
    __type_sex = (
        ("m", "男"),
        ("f", "女"),
        ("s", "保密")
    )
    sex = models.CharField(max_length=1, choices=__type_sex)
    photo = models.BinaryField()
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = "t_user_info"
