from django.db import models
from datetime import datetime
from django.utils.text import slugify

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=None, unique=True)
    desc = models.TextField()
    date = models.DateTimeField(default=datetime.today)
    creator = models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

class Contact(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    desc = models.TextField()
    
    def __str__(self):
        return str(self.fname)
