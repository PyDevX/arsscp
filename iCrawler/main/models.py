from django.db import models

class arsProduct(models.Model):
    urunlink = models.CharField(max_length = 500 )
    stokkod = models.CharField(max_length = 20) 
    birim = models.CharField(max_length = 10)
    name=models.CharField(max_length = 500)
    stok = models.IntegerField()
    fiyat = models.DecimalField(max_digits = 10 ,decimal_places=2)
    ozellik = models.TextField(null=True , blank = True)
    imglink = models.CharField(max_length = 500,null=True , blank = True)    
    anakategori = models.CharField(max_length = 50) 
    altkategori = models.CharField(max_length = 50)
    sonkategori = models.CharField(max_length = 50)
    published = models.BooleanField(default = False )
    checkCount = models.IntegerField(default = 0)
    stokislem  = models.CharField(max_length = 20 , null=True , blank = True) 
    fiyatislem = models.CharField(max_length = 20 , null=True , blank = True) 
    kcreated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class seleniumpages(models.Model):
    url = models.CharField(max_length = 500)