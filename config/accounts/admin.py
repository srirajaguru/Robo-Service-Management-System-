from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
	list_display = ("name", "user", "phone_number", "is_active")
	search_fields = ("name", "user__username", "phone_number")

	@admin.display(boolean=True, description="Active")
	def is_active(self, obj):
		return obj.user.is_active


# Register your models here.
