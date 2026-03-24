from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Employee, Department, Salary, SalaryAuditLog, DeptEmp
from .forms import EmpleadoForm, DepartamentoForm, SalarioForm, AsignacionForm
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import openpyxl
import io
from django.http import HttpResponse

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
@login_required
def dashboard(request):
    context = { 
            'total_empleados': Employee.objects.filter(activo=True).count(),
            'total_departamentos': Department.objects.filter(activo=True).count(),
            'total_salarios': Salary.objects.filter(to_date__isnull=True).count(),   
            }
    return render(request, 'nomina/dashboard.html', context)

# Vistas para empleados
@login_required
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
    
@login_required
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

@login_required
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
@login_required
def empleado_desactivar(request, pk):
    empleado = Employee.objects.get(pk=pk)
    empleado.activo = False
    empleado.save()
    return redirect('/empleados/')

# vistas para departamentos
def departamento_lista(request):
    departamentos = Department.objects.filter(activo=True)
    return render(request, 'nomina/departamentos/lista.html', {
        'departamentos': departamentos
    })
@login_required
def departamento_crear(request): 
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('/departamentos/')
        
    else: 
        form = DepartamentoForm()
    return render(request, 'nomina/departamentos/formulario.html', {
        'form': form
    })
@login_required
def departamento_editar(request, pk):
    departamento = Department.objects.get(pk=pk)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect('/departamentos/')
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'nomina/departamentos/formulario.html', {
        'form': form
        })
@login_required
def departamento_desactivar(request, pk):
    departamento = Department.objects.get(pk=pk)
    departamento.activo = False 
    departamento.save()
    return redirect('/departamentos/')

# Vistas para salarios
def salario_lista(request):
    salarios = Salary.objects.filter(to_date__isnull=True).select_related('employee')
    return render(request, 'nomina/salarios/lista.html', {
        'salarios': salarios
    })
    
@login_required
def salario_crear(request): 
    if request.method == 'POST': 
        form = SalarioForm(request.POST)
        if form.is_valid():
            empleado = form.cleaned_data['employee']
            # cerrar salario anterior
            Salary.objects.filter(
                employee=empleado,
                to_date__isnull=True
            ).update(to_date=form.cleaned_data['from_date'])
            
            salario = form.save()
            
            SalaryAuditLog.objects.create(
                usuario = request.user.username,
                detalle_cambio = f"Nuevo salario registrado: {salario.salary} ",
                salario = salario.salary, 
                employee = empleado
                
            )
            
            return redirect('/salarios/')
            
    else:
        form = SalarioForm()
    return render(request, 'nomina/salarios/formulario.html', {
        'form': form 
    })


def salario_editar(request, pk): 
    salario = Salary.objects.get(pk=pk)
    if request.method == 'POST':
        form = SalarioForm(request.POST, instance=salario)
        if form.is_valid():
            form.save()
            return redirect('/salarios/')
    
    else: 
        form = SalarioForm(instance=salario)
    return render(request, 'nomina/salarios/formulario.html', {
        'form': form
    })
@login_required
def auditoria_lista(request):
    registros = SalaryAuditLog.objects.all()
    return render(request, 'nomina/auditoria/lista.html', {
        'registros': registros
    })

# vista para asiganaciones
@login_required
def asignacion_lista(request):
    asignaciones = DeptEmp.objects.filter(
        to_date__isnull=True
    ).select_related('employee', 'dept')
    return render(request, 'nomina/asignaciones/lista.html', {
        'asignaciones': asignaciones
    })
    
@login_required
def asignacion_crear(request):
    if request.method == 'POST':
        form = AsignacionForm(request.POST)
        if form.is_valid():
            empleado = form.cleaned_data['employee']
            # Cerrar asignación anterior
            DeptEmp.objects.filter(
                employee=empleado,
                to_date__isnull=True
            ).update(to_date=form.cleaned_data['from_date'])
            form.save()
            return redirect('/asignaciones/')
    else:
        form = AsignacionForm()
    return render(request, 'nomina/asignaciones/formulario.html', {'form': form})

@login_required
def asignacion_terminar(request, pk):
    asignacion = DeptEmp.objects.get(pk=pk)
    asignacion.to_date = asignacion.from_date
    asignacion.save()
    return redirect('/asignaciones/')

# reportes 

@login_required
def reportes(request):
    return render(request, 'nomina/reportes/index.html')

@login_required
def reporte_nomina_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Nómina Vigente")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 760, "Empleado")
    p.drawString(250, 760, "Salario")
    p.drawString(400, 760, "Desde")
    
    salarios = Salary.objects.filter(
        to_date__isnull=True
    ).select_related('employee')
    
    y = 740
    p.setFont("Helvetica", 11)
    for s in salarios:
        p.drawString(50, y, str(s.employee))
        p.drawString(250, y, str(s.salary))
        p.drawString(400, y, str(s.from_date))
        y -= 20
    
    p.save()
    buffer.seek(0)
    
    return HttpResponse(
        buffer,
        content_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename="nomina.pdf"'}
    )

@login_required
def reporte_nomina_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Nómina Vigente'
    
    ws.append(['Empleado', 'Salario', 'Desde'])
    
    salarios = Salary.objects.filter(
        to_date__isnull=True
    ).select_related('employee')
    
    for s in salarios:
        ws.append([str(s.employee), s.salary, str(s.from_date)])
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    return HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="nomina.xlsx"'}
    )