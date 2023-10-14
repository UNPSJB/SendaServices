from django import forms
from django.forms import ModelForm
from .models import Producto, Cliente

class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        #Label se refiere la descripcion que esta al lado del formulario.
        

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'


