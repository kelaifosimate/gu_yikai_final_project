from django.db import models
from django.urls import reverse


class UserInfo(models.Model):
    uname = models.CharField(max_length=20, verbose_name="Username", unique=True)
    upwd = models.CharField(max_length=40, verbose_name="Password", blank=False)
    uemail = models.EmailField(verbose_name="Email", unique=True, null=True, blank=True)
    usex = models.CharField(max_length=10, default="", verbose_name="Gender")
    ushou = models.CharField(max_length=20, default="", verbose_name="Recipient Name")
    uaddress = models.CharField(max_length=100, default="", verbose_name="Address")
    uyoubian = models.CharField(max_length=6, default="", verbose_name="Postal Code")
    uphone = models.CharField(max_length=11, default="", verbose_name="Phone Number")

    class Meta:
        verbose_name = "User Information"
        verbose_name_plural = verbose_name
        ordering = ['uname']

    def __str__(self):
        return self.uname

    def get_absolute_url(self):
        return reverse('fm_user:info')