
from django import forms 
from servicios.models import Servicio
from core.models import Empleado
from .models import Horario, Periodo,Asistencia
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
        fields = ("turno", "diaSemana",)

        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'turno': 'Turno',
            'diaSemana': 'Dia de la semana',
            #'servicio': 'Servicio',
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
            # 'servicio': forms.Select(
            #     attrs = {
            #         'class': 'form-control',
            #         'placeholder':'Ingrese el servicio del turno',

            #     }
            # ),
        
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-horarioForm'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        #self.helper.add_input(Submit('submit', 'Guardar'))


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
    #servicio = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Servicio'}))
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), required=False, label='Servicio')

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
        #horario = kwargs["horario"] 
        #self.helper.form_action = reverse_lazy("turnos:modificarHorario", kwargs={"pk": horario.pk})
        #self.helper.add_input(Submit('submit', 'Guardar'))


class PeriodoForm(forms.ModelForm):

    class Meta:
        model = Periodo
        fields = '__all__'

        widgets = {
            "fechaDesde": forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            "fechaHasta": forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fechaDesde = cleaned_data.get('fechaDesde')
        fechaHasta = cleaned_data.get('fechaHasta')

        if fechaDesde and fechaHasta and fechaHasta < fechaDesde:
            raise ValidationError("La fecha 'Hasta' debe ser mayor o igual a la fecha 'Desde'.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['fechaDesde'].widget.attrs['min'] = datetime.today().strftime('%Y-%m-%d')
        self.fields['fechaHasta'].widget.attrs['min'] = datetime.today().strftime('%Y-%m-%d')


class PeriodoFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("empleado", "Empleado"),
        ("fechaDesde", "Fecha Desde"),
        ("fechaHasta", "Fecha Hasta"),

    ]
    ATTR_CHOICES = [
        ("empleado", "Empleado"),
        ("fechaDesde", "Fecha Desde"),
        ("fechaHasta", "Fecha Hasta"),
    ]

    #Formulario de filtrado
    fechaDesde = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False,label=("Fecha Inicio"))
    fechaHasta = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False,label=("Fecha Fin"))
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.all(), required=False, label='Empleado')
    #servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), required=False, label='Servicio')

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
                "empleado","fechaDesde","fechaHasta",  #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )

class PeriodoCustomFiltrosForm(PeriodoFiltrosForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "fechaDesde","fechaHasta", #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model= Asistencia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False



# Tipo Servicio - Producto - Inlines
def PeriodoInline(extra=1):
    return forms.inlineformset_factory(
        Horario,
        Periodo,
        form=PeriodoForm,
        extra=extra,
    )

class PeriodoInlineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'
        self.layout = Layout(
            'empleado',
            'fechaDesde',
            'fechaHasta'
        )
        self.render_required_fields = True
