from django.contrib import admin
from api.models import State, City, Pincode, Subscriber, Contact, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email','date_joined', 'role')
    list_filter = ('role',)
    ordering =('-date_joined',)


admin.site.register(User, UserAdmin)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Pincode)
admin.site.register(Subscriber)
admin.site.register(Contact)
