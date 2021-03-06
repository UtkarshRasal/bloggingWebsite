from django.db import models
from accounts.models import User
import datetime, uuid

class Tags(models.Model):
    id              = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, unique=True)
    name            = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
        
class Blogs(models.Model):
    id              = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, unique=True)
    user            = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title           = models.CharField(max_length=255)
    content         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    tags            = models.ManyToManyField(Tags)
    media_file      = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

class Comments(models.Model):
    id              = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, unique=True) 
    blog            = models.ForeignKey(Blogs, null=True, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comment         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Comments'

    def __all__(self):
        return self.id 

class Likes(models.Model):
    id              = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, unique=True)
    blog            = models.ForeignKey(Blogs, null=True, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural='Likes'

    def __all__(self):
        return self.user
