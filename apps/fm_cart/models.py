from django.db import models

from apps.fm_user.models import UserInfo
from apps.fm_goods.models import GoodsInfo
# When there is a one-to-many relationship, such as product category to specific product,
# maintain the relationship in the "many" table, i.e., in the specific product table
# When there is a many-to-many relationship, create a new table and maintain the table relationship in a third table
# The relationship between user table and product table is maintained in the shopping cart table

# For the shopping cart, choose physical deletion rather than logical deletion,
# Products in the shopping cart are not important information and can be deleted directly


class CartInfo(models.Model):

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="User")
    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="Product")
    count = models.IntegerField(verbose_name="", default=0)  # Record how many units of a product the user bought

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.uname + "'s shopping cart"