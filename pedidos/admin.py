from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Producto, Cliente, Pedido, ItemPedido, Empleado
from django.utils.html import format_html

# Configuración para Producto
class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto

class ProductoAdmin(ImportExportModelAdmin):
    resource_class = ProductoResource
    list_display = ('nombre', 'categoria', 'precio')

# Configuración para ItemPedido (inline en Pedido)
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('get_nombre_producto', 'cantidad', 'subtotal')
    
    def get_nombre_producto(self, obj):
        return obj.producto.nombre
    get_nombre_producto.short_description = 'Producto'

# Configuración para Pedido
class PedidoResource(resources.ModelResource):
    class Meta:
        model = Pedido
        fields = ('id', 'cliente__nombre_completo', 'fecha', 'total', 'seña', 'total_final')

class PedidoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'total', 'seña', 'total_final', 'completado')
    inlines = [ItemPedidoInline]
    list_filter = ('completado', 'fecha')
    readonly_fields = ('fecha',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')

# Configuración para Cliente
class ClienteAdmin(ImportExportModelAdmin):
    list_display = ('nombre_completo', 'email', 'telefono', 'direccion', 'fecha_registro')
    search_fields = ('nombre_completo', 'email')
    list_per_page = 20

# Configuración para Empleado (si aún lo necesitas)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',)
    


# Personalización del admin
admin.site.site_header = format_html(
    '<img src="{}" height="60" style="margin-right:15px; vertical-align:middle;">'
    '<span style="color: #fff; font-size: 24px; vertical-align:middle; line-height:60px;">Lucy Cosas Ricas</span>',
    '/static/pedidos/img/logo-white.png'
)

admin.site.site_title = "Administración Lucy Cosas Ricas"
admin.site.index_title = "Panel de Control"

# Registro de modelos
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Empleado, EmpleadoAdmin)  