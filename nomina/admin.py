from django.contrib import admin
from .models import Employee, Department, DeptEmp,DeptManager, Title, Salary, SalaryAuditLog, UserProfile

# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(DeptEmp)
admin.site.register(DeptManager)
admin.site.register(Title)
admin.site.register(Salary)
admin.site.register(SalaryAuditLog)
admin.site.register(UserProfile)    
