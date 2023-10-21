from django import forms
from django.forms import ModelForm
from .models import Producto, Cliente, Inmueble
from .utils import FiltrosForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML



class ClienteFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("cuil_cuit", "CUIL/CUIT"),
        ("apellido", "Apellido"),
        ("nombre", "Nombre"),
        ("correo", "Correo"),
        ("habitual", "Habitual"),
        ("gubernamental", "Gubernamental"),
    ]
    ATTR_CHOICES = [

        ("cuil_cuit", "CUIL/CUIT"),
        ("apellido", "Apellido"),
        ("nombre", "Nombre"),
        ("correo", "Correo"),
        ("habitual", "Habitual"),
        ("gubernamental", "Gubernamental"),

    ]

    #Formulario de filtrado
    cuil_cuit = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Cuil/Cuit'}), max_length=45)
    apellido = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}), max_length=45)
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}), max_length=45)
    correo = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Correo'}))
        
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "cuil_cuit","nombre", "apellido", "correo", #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )

class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'

class ClienteModForm(ModelForm):

    class Meta:
        model = Cliente
        exclude = ('cuil_cuit',)
    

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
        exclude = ["domicilio", "cliente"]


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


class ProductoUpdateForm(ProductoForm):

    class Meta(ProductoForm.Meta):
        exclude = ["stock", "codigo"]
