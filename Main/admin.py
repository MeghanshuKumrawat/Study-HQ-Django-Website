from django.contrib import admin
from .models import *




@admin.register(Student_Details)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('your_name', 'email', 'phone_no', 'batch', 'batch_time', 'serial_no')
    list_filter = ('your_name', 'email', 'phone_no', 'batch', 'batch_time', 'serial_no')
    search_fields = ('your_name__startswith', 'email__startswith', 'phone_no__startswith', 'batch__startswith', 'batch_time__startswith', 'serial_no__startswith')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered', 'ordered_date')
    list_filter = ('user', 'ordered', 'ordered_date')
    
@admin.register(OrderCourse)
class OrderCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    list_filter = ('user', 'course')
    

admin.site.register(Comment)
admin.site.register(Coupon)
admin.site.register(Courses)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(ContactUs)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)

