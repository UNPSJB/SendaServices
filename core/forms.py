from django import forms
from django.forms import ModelForm
from .models import Producto, Cliente, Inmueble, Empleado,Categoria
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'stock': 'Stock',
            'precioUnitario': 'Precio Unitario',
           
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
            'stock': forms.NumberInput(
                attrs = {
                    'min': 0,
                    'class': 'form-control',
                    'placeholder':'Ingrese el stock del producto',

                }
            ),
            'precioUnitario': forms.NumberInput(
                attrs = {
                    'min': 0,                    
                    'class': 'form-control',
                    'placeholder':'Ingrese el precio del producto',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-productoForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Guardar'))


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

class ProductoUpdateForm(ProductoForm):

    class Meta(ProductoForm.Meta):
        exclude = ["stock", "codigo"]


class InmuebleForm(ModelForm):

    class Meta:
        model = Inmueble
        fields = '__all__'
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'codigo': 'Domicilio',
            'metrosCuadrados': 'Metros Cuadrados',
            'nroAmbientes': 'Cantidad de Ambientes',
            'tipo': 'Tipo',
            'cliente.cuil_cuit': 'Cliente',
           
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'domicilio': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el domicilio del inmueble',
                }
            ),
            'metrosCuadrados': forms.NumberInput(
                attrs = {
                    'min': 0,
                    'class': 'form-control',
                    'placeholder':'Ingrese los metros cuadrados del inmueble',
                }
            ),
            'nroAmbientes': forms.NumberInput(
                attrs = {
                    'min': 0,
                    'class': 'form-control',
                    'placeholder':'Ingrese la cantidad de ambientes del inmueble',

                }
            ),
            'tipo': forms.TextInput(
                attrs = {                    
                    'class': 'form-control',
                    'placeholder':'Ingrese el tipo del inmueble',
                }
            ),
            'cliente.cuil_cuit': forms.NumberInput(
                attrs = {                    
                    'class': 'form-control',
                    'placeholder':'Ingrese el cuil/cuit del inmueble',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-inmuebleForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Guardar'))


class InmuebleUpdateForm(InmuebleForm):

    class Meta(InmuebleForm.Meta):
        exclude = ["domicilio", "cliente.cuil_cuit"]



class CategoriaForm(ModelForm):

    class Meta:
        model = Categoria
        fields = '__all__'
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'nombre':'Nombre',
            'sueldoBase': 'Sueldo Base',
            'empleado.legajo': 'Empleado',
           
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'nombre': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre de la categoria',
                }
            ),
            'sueldoBase': forms.NumberInput(
                attrs = {
                    'min': 0,
                    'class': 'form-control',
                    'placeholder':'Ingrese el sueldo base de la categoria',
                }
            )
            
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-inmuebleForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Guardar'))

