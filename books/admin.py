from django.contrib import admin

from .models import Author, Book, BookCopy

# Register your models here.


# class CustomBookRequestAdmin(admin.ModelAdmin):
#     list_display = ["book", "requester", "approved", "date_time_requested"]

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)
