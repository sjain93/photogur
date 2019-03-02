from django.db import models

class Picture(models.Model):
    title = models.CharField(max_length = 255)
    artist = models.CharField(max_length = 255)
    url = models.CharField(max_length = 255)

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name ='comments')

    def __str__(self):
        return self.name
