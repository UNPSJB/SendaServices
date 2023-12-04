from django import forms 
from servicios.models import Servicio
from .models import Factura
from django.forms import ModelForm, ValidationError, Select
from django.urls import reverse_lazy
from core.utils import FiltrosForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from datetime import datetime
from django.utils.translation import gettext_lazy as _


class FacturasFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("emision", "Fecha Emision"),
        ("total", "Total"),
        
    ]
    ATTR_CHOICES = [
        ("emision", "Fecha Emision"),
        ("total", "Total"),
    ]

    #Formulario de filtrado
    emision = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label=_("Fecha Emision"))
    total = forms.DecimalField(label=_("Total de la factura"),
        required=False,)

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
                "emision","total", #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )
