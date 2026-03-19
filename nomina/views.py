from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Employee, Department, Salary
from .forms import EmpleadoForm

# Create your views here.
# Vista para el login
def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'nomina/login.html')

# Vista para el dashboard
def dashboard(request):
    context = { 
            'total_empleados': Employee.objects.filter(activo=True).count(),
            'total_departamentos': Department.objects.filter(activo=True).count(),
            'total_salarios': Salary.objects.filter(to_date__isnull=True).count(),   
            }
    return render(request, 'nomina/dashboard.html', context)

# Vistas para empleados
def empleado_lista(request):
    query = request.GET.get('q', '')
    empleados = Employee.objects.filter(activo=True, first_name__icontains=query)
    
    if query:
        empleados = empleados.filter(
            first_name__icontains=query
        ) | empleados.filter(
            last_name__icontains=query
        ) | empleados.filter(
            ci__icontains=query
        )
    return render(request, 'nomina/empleados/lista.html', {
        'empleados': empleados,
        'query': query
    })
    
def empleado_crear(request):
    if request.method == 'POST':
            form = EmpleadoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/empleados/')
    else:
        form = EmpleadoForm()
    return render(request, 'nomina/empleados/formulario.html', {
        'form': form
        })
        
def empleado_editar(request, pk):
    empleado = Employee.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('/empleados/')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'nomina/empleados/formulario.html', {
        'form': form,
    })

def empleado_desactivar(request, pk):
    empleado = Employee.objects.get(pk=pk)
    empleado.activo = False
    empleado.save()
    return redirect('/empleados/')