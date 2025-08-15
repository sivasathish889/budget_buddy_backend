from django.contrib import admin
from .models import Users,Expense,Catagory

class UserAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','DOB','goal']

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['user','amount','description','category','date',]

class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
# Register your models here.
admin.site.register(Users, UserAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Catagory,CatagoryAdmin)

admin.site.site_header = "Budget Buddy"
admin.site.site_title = "Budget Buddy"
