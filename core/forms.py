from django import forms
from django.forms import ModelForm
from .models import Producto, Cliente


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


