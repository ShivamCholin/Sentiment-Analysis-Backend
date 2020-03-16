from django.contrib import admin
from .models import Searchres
from .models import Detailed


class SearchresAdmin(admin.ModelAdmin):
    list_display = ('hashtag','positive','negative','time')

class DetailedResAdmin(admin.ModelAdmin):
    list_display = ('hashtag','label')

admin.site.register(Searchres,SearchresAdmin)
admin.site.register(Detailed,DetailedResAdmin)
# Register your models here.
