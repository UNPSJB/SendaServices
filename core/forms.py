from django import forms
from django.forms import ModelForm
from .models import Producto, Cliente
from .utils import FiltrosForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML



class ClienteFiltrosForm(FiltrosForm):
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
                "cuil_cuit","nombre", "apellido", "correo",
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
    

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'


