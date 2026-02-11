from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    desc = models.TextField()
    cover_img = models.ImageField(upload_to='covers/')
    pdf_file = models.FileField(upload_to='books/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','book')
    def __str__(self):
        return f"{self.user.username} read {self.book.title}"
    

