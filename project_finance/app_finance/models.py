from django.db import models

#Stockモデルクラスを作成
class Stock(models.Model):
    code = models.CharField(max_length=100)    
    start = models.DateField()
    end = models.DateField()
    button = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')        #日付
