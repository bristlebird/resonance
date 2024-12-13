from django.db import models
from cloudinary.models import CloudinaryField



class About(models.Model):
    """
    Stores single entry of content for the about page
    """
    title = models.CharField(max_length=200)
    about_image = CloudinaryField('image', default='placeholder', folder='resonance/images')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.title}"
