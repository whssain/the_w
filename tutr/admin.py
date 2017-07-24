from django.contrib import admin
from .models import Musician 
admin.site.register(Musician) 
# Register your models here.

class TutrModelAdmin(admin.ModelAdmin):
	last_name = ["last_name"]
	search_fields = ["instrument"]
	
    
	list_display_links = ["last_name"]
	list_editable = ["first_name"]
	class Meta:
		model = Musician 
