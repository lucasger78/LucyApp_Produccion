from django.db import models
from django.utils import timezone
from decimal import Decimal

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=60, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
            return self.nombre_completo      
        


class Pedido(models.Model):    
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seña = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completado = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        """Calcula automáticamente el total_final antes de guardar"""
        self.total_final = max(Decimal('0'), self.total - self.senia)  # Evita valores negativos
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente} ({'Completado' if self.completado else 'Pendiente'})"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (${self.subtotal})"