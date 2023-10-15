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
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'codigo': 'Codigo',
            'descripcion': 'Descripcion',
            'stock': 'Stock',
            'precioUnitario': 'Precio',
           
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'codigo': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el codigo del producto',
                }
            ),
            'descripcion': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese descripcion del producto',
                }
            ),
            'stock': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el stock del producto',

                }
            ),
            'precioUnitario': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el precio del producto',
                }
            ),
        }

