from django.contrib.gis.db import models
from authe.models import Alborz , User

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    geom_id = models.ForeignKey(Alborz , on_delete=models.CASCADE)
    order_title = models.CharField(max_length=200)
    order_description = models.TextField()
    wrong_predicted = models.MultiPointField(srid=4326 , null=True )
    invest_needed = models.MultiPointField(srid=4326 , null=True )
    before_time = models.DateField()
    after_time = models.DateField()