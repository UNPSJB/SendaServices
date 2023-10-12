from django import forms
from django.forms import ModelForm
from .models import Producto, Cliente,Empleado
from crispy_forms.helper import FormHelper

class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'cuil_cuit': 'Cuit/Cuil',
            'apellido': 'Apellido',
            'nombre': 'Nombre',
            'correo': 'Correo',
            'habitual': 'Habitual',
            'gubernamental': 'Gubernamental',
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'cuil_cuit': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el cuit/cuit del cliente',
                }
            ),
            'apellido': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el apellido del cliente',
                }
            ),
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre del cliente',

                }
            ),
            'correo': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el correo del cliente',
                }
            ),
            'habitual': forms.CheckboxInput(
                attrs= {
                    'class': 'form-check-input'
                }
            ),
            'gubernamental': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input'
                }
            ),
        }

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'


class EmpleadoForm(ModelForm):

    class Meta:
        model = Empleado
        fields = '__all__'
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'legajo': 'Legajo',
            'apellido': 'Apellido',
            'nombre': 'Nombre',
            'cuil': 'Cuil',
            'correo': 'Correo',
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'legajo': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el legajo del empleado',
                }
            ),
            'apellido': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el apellido del empleado',
                }
            ),
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre del empleado',

                }
            ),
            'cuil': forms.NumberInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el cuil del empleado',
                }
            ),
            'correo': forms.EmailInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder':'Ingrese el correo del empelado',
                }
            ),
        
        }
