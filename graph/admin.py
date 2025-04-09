from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Node, Edge

admin.site.register(Node)
admin.site.register(Edge)