from django import forms
from .models import Cliente
from .models import Empleado

class ClienteForm(forms.ModelForm):   
    senia = forms.DecimalField(
        label="Seña ($)",
        required=False,
        initial=0,
        min_value=0
    )
    
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.filter(activo=True),
        label="Empleado que toma el pedido",
        required=True)
    
    
    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'email', 'telefono', 'direccion','senia']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
            'telefono': forms.TextInput(attrs={'required': True}),
            'direccion': forms.TextInput(attrs={'required': True}),
        }