from django import forms 
from servicios.models import Servicio
from core.models import Empleado
from .models import Horario
from django.forms import ModelForm, ValidationError, Select
from django.urls import reverse_lazy
from core.utils import FiltrosForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from datetime import datetime
from servicios.forms import Servicio


class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['servicio', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, 
                format="%Y-%m-%dT%H:%M"
            ),
            'fecha_fin': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, 
                format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        empleado = kwargs.pop("empleado", None)  # Extraemos el servicio de los kwargs
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-horarioForm'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        # En tu Form (Python)
        self.fields['fecha_inicio'].widget.attrs.update({'id': 'fechaInicio'})
        self.fields['fecha_fin'].widget.attrs.update({'id': 'fechaFin'})
        self.fields['servicio'].widget.attrs.update({'id': 'servicioSelect'})
        # self.fields["fecha_inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        # self.fields["fecha_fin"].input_formats = ("%Y-%m-%dT%H:%M",)


class HorarioFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("fecha_inicio", "Fecha Inicio"),
        ("fecha_fin", "Fecha Fin"),
        ("servicio", "Servicio"),
        
    ]
    ATTR_CHOICES = [
        ("fecha_inicio", "Fecha Inicio"),
        ("fecha_fin", "Fecha Fin"),
        ("servicio", "Servicio"),
    ]

    #Formulario de filtrado

    desde = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),required=False,label="Fecha Inicio")
    hasta = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),required=False,label="Fecha Fin")
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), required=False, label='Servicio')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                 "desde", "hasta", "servicio",  # ✅ Campos corregidos
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )

class HorarioCustomFiltrosForm(HorarioFiltrosForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                 "desde", "hasta",  # ✅ Campos corregidos
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


HorarioCustomFiltrosForm.base_fields.pop("servicio")

