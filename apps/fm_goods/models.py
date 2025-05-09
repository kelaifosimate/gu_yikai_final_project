from datetime import datetime

from django.db import models
from tinymce.models import HTMLField  # Using rich text editor requires installation in settings file


class TypeInfo(models.Model):
    # Product category information: Books, Electronics, etc.
    isDelete = models.BooleanField(default=False)
    ttitle = models.CharField(max_length=20, verbose_name="Category")

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    # Specific product information
    isDelete = models.BooleanField(default=False)  # Logical deletion
    gtitle = models.CharField(max_length=20, verbose_name="Product Name", unique=True)
    gpic = models.ImageField(verbose_name='Product Image', upload_to='fm_goods/image/%Y/%m', null=True, blank=True)
    gprice = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Product Price")  # Product price with 2 decimal places, integer up to 7 digits
    gunit = models.CharField(max_length=20, verbose_name="Seller Username")
    gclick = models.IntegerField(verbose_name="Click Count", default=0, null=False)
    gjianjie = models.CharField(max_length=200, verbose_name="Brief Introduction")
    gkucun = models.IntegerField(verbose_name="Inventory", default=0)
    gcontent = HTMLField(max_length=200, verbose_name="Details")
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE, verbose_name="Category")  # Foreign key relationship with TypeInfo table

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.gtitle


class GoodsContent(models.Model):
    # User comments
    isDelete = models.BooleanField(default=False)  # Logical deletion
    ctitle = models.CharField(max_length=20, verbose_name="Product Name")
    cpic = models.ImageField(verbose_name='Upload Image', upload_to='fm_goods/image/%Y/%m', null=True, blank=True)
    cusername = models.CharField(max_length=20, verbose_name="Buyer Username")
    clogo = models.CharField(verbose_name='Buyer Avatar', max_length=200, default=None)
    cuser_content = HTMLField(max_length=200, verbose_name="User Comment")
    date_publish = models.DateTimeField(verbose_name="Publication Time", default=datetime.now)
    cgoodsname = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="Related Product")  # Foreign key relationship with GoodsInfo table

    class Meta:
        verbose_name = "Product Comment"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ctitle


class ContentChart(models.Model):
    # Comment replies
    isDelete = models.BooleanField(default=False)  # Logical deletion
    ctitle = models.CharField(max_length=20, verbose_name="Product Name")
    cusername = models.CharField(max_length=20, verbose_name="Commenter Username")
    cusername1 = models.CharField(max_length=20, verbose_name="Replier Username")
    ccontent_chart = HTMLField(max_length=200, verbose_name="Comment Reply")
    date_publish = models.DateTimeField(verbose_name="Publication Time", default=datetime.now)
    ccontent = models.ForeignKey(GoodsContent, on_delete=models.CASCADE, verbose_name="Comment ID")  # Foreign key relationship with GoodsContent table

    class Meta:
        verbose_name = "Comment Reply"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ctitle