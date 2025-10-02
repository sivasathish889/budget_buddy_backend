from django.contrib import admin
from .models import Users,Expense,Catagory,Social

class UserAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','DOB','goal']

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','description','category','date',]

class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
# Register your models here.
admin.site.register(Users, UserAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Catagory,CatagoryAdmin)
admin.site.register(Social)

admin.site.site_header = "Budget Buddy"
admin.site.site_title = "Budget Buddy"
