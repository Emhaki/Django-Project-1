from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Store(models.Model):
    store_name = models.CharField(max_length=80)
    address = models.CharField(max_length=160)
    phone_num = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE, related_name="mj_menu")


class Menu(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="mj_store")
    menu_name = models.CharField(max_length=80)
    menu_price = models.IntegerField()


class Store_image(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 90},
    )
