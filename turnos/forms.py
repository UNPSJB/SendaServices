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
from django_select2.forms import Select2Widget
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
        kwargs.pop("empleado", None)  # Extraemos el servicio de los kwargs
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-horarioForm'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        # En tu Form (Python)
        self.fields['fecha_inicio'].widget.attrs.update({'id': 'fechaInicio'})
        self.fields['fecha_fin'].widget.attrs.update({'id': 'fechaFin'})

        # Si el campo servicio existe (solo cuando no se recibe uno fijo), activamos select2
        self.fields['servicio'].widget.attrs.update({
            'id': 'servicioSelect',
            'class': 'w-100',
            # 'class': 'servicioSelect form-select w-100',
            'data-placeholder': 'Buscar servicio...'
        })

        # self.fields['servicio'].widget.attrs.update({
        #     'id': 'servicioSelect',
        #     'class': 'form-select w-100',
        #     'data-placeholder': 'Buscar servicio...',
        #     'data-url': reverse_lazy('turnos:ajax_servicios'),
        # })

        # self.fields['servicio'].widget = Select2Widget(
        #     attrs={
        #         'data-url': reverse_lazy('turnos:ajax_servicios'),
        #         'data-placeholder': 'Buscar servicio...',
        #         'class': 'form-select w-100'
        #     }
        # )


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
    fecha_inicio = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),required=False,label="Fecha Inicio")
    fecha_fin = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),required=False,label="Fecha Fin")
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
                 "fecha_inicio", "fecha_fin", "servicio",  # ✅ Campos corregidos
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
                 "fecha_inicio", "fecha_fin",  # ✅ Campos corregidos
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


HorarioCustomFiltrosForm.base_fields.pop("servicio")

