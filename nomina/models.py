from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    emp_no     = models.AutoField(primary_key=True)
    ci         = models.CharField(max_length=50, unique=True)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    gender     = models.CharField(max_length=1, choices=GENDER_CHOICES)
    hire_date  = models.DateField()
    correo     = models.EmailField(max_length=100, null=True, blank=True)
    activo     = models.BooleanField(default=True)

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Department(models.Model):
    dept_no   = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=50, unique=True)
    activo    = models.BooleanField(default=True)

    class Meta:
        db_table = 'departments'
        ordering = ['dept_name']

    def __str__(self):
        return self.dept_name
    
class DeptEmp(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE)
    dept      = models.ForeignKey(Department, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date   = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'dept_emp'

    def __str__(self):
        return f'{self.employee} - {self.dept}'

class DeptManager(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE)
    dept      = models.ForeignKey(Department, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date   = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'dept_manager'

    def __str__(self):
        return f'{self.employee} - {self.dept}'
    
class Title(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title     = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date   = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'titles'

    def __str__(self):
        return f'{self.employee} - {self.title}'

class Salary(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary    = models.BigIntegerField()
    from_date = models.DateField()
    to_date   = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'salaries'

    def __str__(self):
        return f'{self.employee} - {self.salary}'
    
class SalaryAuditLog(models.Model):
    usuario             = models.CharField(max_length=50)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    detalle_cambio      = models.CharField(max_length=250)
    salario             = models.BigIntegerField()
    employee            = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'log_auditoria_salarios'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f'{self.usuario} - {self.fecha_actualizacion}'

class UserProfile(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('rrhh', 'RRHH'),
    ]

    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    rol      = models.CharField(max_length=10, choices=ROL_CHOICES, default='rrhh')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.user.username} ({self.rol})'

class DeptEmp(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE)
    dept      = models.ForeignKey(Department, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date   = models.DateField(null=True, blank=True)