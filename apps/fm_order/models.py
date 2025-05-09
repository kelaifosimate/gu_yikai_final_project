from django.db import models
from datetime import datetime

from apps.fm_goods.models import GoodsInfo
from apps.fm_user.models import UserInfo

class OrderInfo(models.Model):  # Main order
    oid = models.CharField(max_length=20, primary_key=True, verbose_name="Order Number")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="Order User")
    odate = models.DateTimeField(auto_now=True, verbose_name="Time")
    oIsPay = models.BooleanField(default=False, verbose_name="Is Paid")
    ototal = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Total Price")
    oaddress = models.CharField(max_length=150, verbose_name="Order Address")
    # Although total price can be calculated from the price and quantity of multiple products,
    # considering the frequent use of order total price, we ignore the redundancy of total

    class Meta:
        verbose_name = "Unpaid Order"
        verbose_name_plural = verbose_name

    def __str__(self):
        # return self.user.uname + " at " + str(self.odate) + " order"
        return "{0}'s order at {1}".format(self.user.uname, self.odate)


# Unable to implement: Real payment, logistics information
class OrderDetailInfo(models.Model):  # Specific product order in a main order

    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="Product")
    username = models.CharField(max_length=20, verbose_name="Buyer Username", default=None)
    shopername = models.CharField(max_length=20, verbose_name="Seller Username", default="")
    datatime = models.DateTimeField(verbose_name="Transaction Time", default=datetime.now)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="Order")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Product Price")
    count = models.IntegerField(verbose_name="Product Quantity")

    class Meta:
        verbose_name = "Paid Order"
        verbose_name_plural = verbose_name

    def __str__(self):
        # return self.goods.gtitle + "(quantity is " + str(self.count)  + ")"
        return "{0}(quantity: {1})".format(self.goods.gtitle, self.count)