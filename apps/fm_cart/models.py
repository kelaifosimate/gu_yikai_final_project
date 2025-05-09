from django.db import models
from apps.fm_user.models import UserInfo
from apps.fm_goods.models import GoodsInfo


class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='User')
    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name='Product')
    count = models.IntegerField(default=1, verbose_name='Quantity')

    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = verbose_name
        ordering = ['user', 'goods']
        constraints = [
            models.UniqueConstraint(fields=['user', 'goods'], name='unique_cart_item')
        ]

    def __str__(self):
        return f"{self.user.uname}'s cart: {self.goods.gtitle} ({self.count})"

    def get_absolute_url(self):
        return reverse('fm_cart:cart')