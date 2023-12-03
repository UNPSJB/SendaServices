from django import forms 
from servicios.models import Servicio
from .models import Factura
from django.forms import ModelForm, ValidationError, Select
from django.urls import reverse_lazy
from core.utils import FiltrosForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from datetime import datetime


class FacturasFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("pago", "Pago"),
        
    ]
    ATTR_CHOICES = [
        ("pago", "Pago"),
    ]

    #Formulario de filtrado
    servicio = forms.TextInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.initial['turno'] = '' 
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "turno","diaSemana","servicio",  #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )
