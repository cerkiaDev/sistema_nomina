"""
URL configuration for sistema_nomina project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from nomina import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view),
    path('dashboard/', views.dashboard),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('empleados/', views.empleado_lista, name='empleado-lista'),
    path('empleados/nuevo/', views.empleado_crear, name='empleado-crear'),
    path('empleados/<int:pk>/editar/', views.empleado_editar, name='empleado-editar'),
    path('empleados/<int:pk>/desactivar/', views.empleado_desactivar, name='empleado-desactivar'),
    path('departamentos/', views.departamento_lista, name='departamento-lista'),
    path('departamentos/nuevo/', views.departamento_crear, name='departamento-crear'),
    path('departamentos/<int:pk>/editar/', views.departamento_editar, name='departamento-editar'),
    path('departamentos/<int:pk>/desactivar/', views.departamento_desactivar, name='departamento-desactivar'), 
    path('salarios/', views.salario_lista, name='salario-lista'),
    path('salarios/nuevo/', views.salario_crear, name='salario-crear'),
    path('salarios/<int:pk>/editar/', views.salario_editar, name='salario-editar'),
    path('auditoria/', views.auditoria_lista, name='auditoria-lista'),
    path('asignaciones/', views.asignacion_lista, name='asignacion-lista'),
    path('asignaciones/nueva/', views.asignacion_crear, name='asignacion-crear'),
    path('asignaciones/<int:pk>/terminar/', views.asignacion_terminar, name='asignacion-terminar'),
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/nomina-pdf/', views.reporte_nomina_pdf, name='reporte-nomina-pdf'),
    path('reportes/nomina-excel/', views.reporte_nomina_excel, name='reporte-nomina-excel'),
]
