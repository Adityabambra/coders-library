from django.contrib import admin
from .models import Book, ReadingHistory


admin.site.register(Book)
admin.site.register(ReadingHistory)