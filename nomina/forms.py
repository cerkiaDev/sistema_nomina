from django import forms
from .models import Employee, Department, Salary

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['ci', 'birth_date', 'first_name', 'last_name',                   'gender', 'hire_date', 'correo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'ci': 'Cédula',
            'birth_date': 'Fecha de Nacimiento',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'gender': 'Género',
            'hire_date': 'Fecha de Contrato',
            'correo': 'Correo',
        }

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']
        labels = {
            'dept_name': 'Nombre del Departamento',
        }

class SalarioForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['employee', 'salary', 'from_date', 'to_date']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'employee': 'Empleado',
            'salary': 'Salario',
            'from_date': 'Fecha de Inicio',
            'to_date': 'Fecha de Fin',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_date'].required = False