# from django.urls import path, include
# from django.views.generic.base import RedirectView
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('catalogo/', views.catalogo, name='catalogo'),
#     path('guardar-carrito/', views.guardar_carrito, name='guardar_carrito'),
#     path('formulario-cliente/', views.formulario_cliente, name='formulario_cliente'),
#     # path('resumen_pedido/', views.resumen_pedido, name='resumen_pedido'),
#     path('verificar-pedido/', views.verificar_pedido, name='verificar_pedido'),
#     path('pedido/<int:pedido_id>/pdf/', views.generar_pdf_pedido, name='generar_pdf_pedido'),
#     path('gracias/', views.gracias, name='gracias'),
#     path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('accounts/', include('django.contrib.auth.urls')),  # Incluye todas las URLs de autenticación
    
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'), 
    path('guardar-carrito/', views.guardar_carrito, name='guardar_carrito'),
    path('formulario-cliente/', views.formulario_cliente, name='formulario_cliente'),
    path('verificar-pedido/', views.verificar_pedido, name='verificar_pedido'),
    path('pedido/<int:pedido_id>/pdf/', views.generar_pdf_pedido, name='generar_pdf_pedido'),
    path('gracias/', views.gracias, name='gracias'),
]