from django.db import models

class Picture(models.Model):
    title = models.CharField(max_length = 255)
    artist = models.CharField(max_length = 255)
    url = models.CharField(max_length = 255)

    def __str__(self):
        return self.title
