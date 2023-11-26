
from django import forms 
from servicios.models import Servicio
from .models import Horario, Periodo,Asistencia
from django.forms import ModelForm, ValidationError, Select
from django.urls import reverse_lazy
from core.utils import FiltrosForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML



class HorarioForm(ModelForm):

    class Meta:
        model = Horario
        fields = '__all__'
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'turno': 'Turno',
            'diaSemana': 'Dia de la semana',
            'servicio': 'Servicio',
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'turno': forms.CheckboxInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el turno del turno',
                }
            ),
            'diaSemana': forms.CheckboxInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el dia de la semana del turno',
                }
            ),
            'servicio': forms.CheckboxInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el servicio del turno',

                }
            ),
        
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-horarioForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Guardar'))


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
    turno = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Turno'}), max_length=30)
    diaSemana = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'dia de la semana'}), max_length=30)
    #servicio = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Servicio'}))
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), required=False, label='Propietario')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "turno","diaSemana",  #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


class HorarioModForm(ModelForm):

    class Meta:
        model = Horario
        fields = '__all__'

        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'turno': 'Turno',
            'diaSemana': 'Dia de la semana',
            'servicio': 'Servicio',
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'turno': forms.CheckboxInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el turno del horario',
                }
            ),
            'diaServicio': forms.CheckboxInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el dia de la semana del turno',

                }
            ),
            'servicio.pk': forms.TextInput(
                attrs = {           
                    'class': 'form-control',
                    'placeholder':'Ingrese el servicio del turno',
                }
            ),
                 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-horarioForm'
        self.helper.form_method = 'post'
        horario = kwargs["instance"] 
        self.helper.form_action = reverse_lazy("modificarHorario", kwargs={"pk": horario.pk})
        self.helper.add_input(Submit('submit', 'Guardar'))


class PeriodoForm(forms.ModelForm):

    class Meta:
        model = Periodo
        fields = '__all__'
 
        widgets = {
            'producto': forms.Select(attrs={'autocomplete': 'off'}),
            'cantidad': forms.NumberInput(attrs={'min': 1})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()



class AsistenciForm(forms.ModelForm):
    class Meta:
        model= Asistencia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

"""
    
class TipoServicioFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("codigo", "Codigo"),
        ("descripcion", "Descripcion"),
        ("costo", "Costo"),
        ("unidadDeMedida", "Unidad de medida"),
    ]
    ATTR_CHOICES = [
        ("codigo", "Codigo"),
        ("descripcion", "Descripcion"),
        ("costo", "Costo"),
        ("unidadDeMedida", "Unidad de medida"),

    ]

    #Formulario de filtrado
    codigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '12345'}), max_length=30)
    descripcion = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'limpieza'}), max_length=250)
    costo = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'placeholder': '10000'}), decimal_places=2,max_digits=14)
    unidadDeMedida = forms.CharField(label="Unidad de Medida",required=False, widget=forms.TextInput(attrs={'placeholder': 'M2'}), max_length=30)
        
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "codigo","descripcion", "costo", "unidadDeMedida", #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


"""