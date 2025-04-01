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


class HorarioForm(ModelForm):

    class Meta:
        model = Horario
        fields = ("turno", "diaSemana", "servicio")

        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'turno': 'Turno',
            'diaSemana': 'Dia de la semana',
            'servicio': 'Servicio',
        }

        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'turno': forms.Select(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el turno del turno',
                }
            ),
            'diaSemana': forms.Select(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el dia de la semana del turno',
                }
            ),
            "servicio": forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese el dia de la semana del turno',
                }
            ), 
        }

    def __init__(self, *args, **kwargs):
        empleado = kwargs.pop("empleado", None)  # Extraemos el servicio de los kwargs
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-horarioForm'
        self.helper.form_method = 'post'
        self.helper.form_tag = False


class HorarioFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("turno", "Turno"),
        ("diaSemana", "dia de la semana"),
        ("servicio", "Servicio"),
        
    ]
    ATTR_CHOICES = [

        ("turno", "Turno"),
        ("diaSemana", "dia de la semana"),
        ("servicio", "Servicio"),
    ]

    #Formulario de filtrado
    turno = forms.ChoiceField(required=False, choices=Horario.Turno.choices)
    diaSemana = forms.ChoiceField(required=False, choices=Horario.DiaSemana.choices)
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
                "turno","diaSemana","servicio",  #Remplazar campos formulario
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
                "turno","diaSemana", #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


HorarioCustomFiltrosForm.base_fields.pop("servicio")


class HorarioModForm(ModelForm):

    class Meta:
        model = Horario
        #fields = "__all__"
        exclude = ('turno', 'diaSemana', 'servicio',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-horarioForm'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
