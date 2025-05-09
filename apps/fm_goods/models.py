from django.db import models
from django.urls import reverse


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20, verbose_name="Product Name", unique=True)
    gpic = models.ImageField(verbose_name='Product Image', upload_to='fm_goods/image/%Y/%m', null=True, blank=True)
    gprice = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Product Price")
    gunit = models.CharField(max_length=20, verbose_name="Seller Username")
    gclick = models.IntegerField(verbose_name="Click Count", default=0, null=False)
    gjianjie = models.CharField(max_length=200, verbose_name="Brief Introduction")
    gkucun = models.IntegerField(verbose_name="Inventory", default=0)
    gcontent = models.TextField(max_length=500, verbose_name="Details")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = verbose_name
        ordering = ['gtitle']

    def __str__(self):
        return self.gtitle

    def get_absolute_url(self):
        return reverse('fm_goods:detail', kwargs={'goods_id': self.pk})

    def get_update_url(self):
        return reverse('fm_goods:edit_product', kwargs={'goods_id': self.pk})

    def get_delete_url(self):
        return reverse('fm_goods:delete_product', kwargs={'goods_id': self.pk})