from django.db import models
from datetime import datetime
from apps.fm_goods.models import GoodsInfo
from apps.fm_user.models import UserInfo

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True, verbose_name="Order Number")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="Order User")
    odate = models.DateTimeField(auto_now=True, verbose_name="Time")
    oIsPay = models.BooleanField(default=False, verbose_name="Is Paid")
    ototal = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Total Price")
    oaddress = models.CharField(max_length=150, verbose_name="Order Address")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.uname}'s order at {self.odate.strftime('%Y-%m-%d %H:%M')}"

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="Product")
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="Order")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Product Price")
    count = models.IntegerField(verbose_name="Product Quantity")

    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.goods.gtitle} (quantity: {self.count})"