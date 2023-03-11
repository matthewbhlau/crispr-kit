import os
import uuid
from django.db import models

def get_image_filename(instance, filename):
    """
    Returns a randomly generated filename for the uploaded image with the
    original extension.
    """
    extension = os.path.splitext(filename)[1]
    new_filename = f"{uuid.uuid4().hex}{extension}"
    return new_filename


class DataModel(models.Model):
    COLOR_CHOICES = (
        ("red", "Red"),
        ("yellow", "Yellow"),
        ("blue", "Blue"),
        ("green", "Green"),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, choices=COLOR_CHOICES)
    image = models.ImageField(upload_to="images/")
    
    def save(self, *args, **kwargs):
        filename = self.image.name
        new_filename = get_image_filename(self, filename)
        self.image.name = new_filename
        super().save(*args, **kwargs)


class ExpressionPlot(models.Model):
    related_data = models.OneToOneField(DataModel, on_delete=models.CASCADE)
    nc = models.CharField(max_length=25, verbose_name="NC")
    pc = models.CharField(max_length=25, verbose_name="PC")
    nt = models.CharField(max_length=25, verbose_name="NT")
    t = models.CharField(max_length=25, verbose_name="T")
    ng = models.CharField(max_length=25, verbose_name="NG")
