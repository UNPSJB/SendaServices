
from django import forms 
from .models import Servicio, TipoServicio, TipoServicioProducto, Servicio, DetalleServicio, TipoEstado, Estado
from core.utils import FiltrosForm
from core.models import Inmueble
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from datetime import datetime
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Subquery, OuterRef
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from datetime import datetime
from turnos.models import Horario

class ServiciosFiltrosForm(FiltrosForm):
    # Campos del modelo
    ORDEN_CHOICES = [
        ("estado", "Estado del servicio"),
        ("desde", "Fecha Inicio"),
        ("hasta", "Fecha Fin"),
        ("totalEstimado", "Total"),
    ]

    ATTR_CHOICES = [
        ("estado", "Estado del servicio"),
        ("desde", "Fecha Inicio"),
        ("hasta", "Fecha Fin"),
        ("totalEstimado", "Total"),
    ]

    ES_EVENTUAL_CHOICES = [
        ("", "Todos"),  # Opción vacía para no filtrar
        ("1", "Sí"),
        ("0", "No"),
    ]


    # Formulario de filtrado
    estado = forms.ChoiceField(
        label=_("Estado del servicio"),
        choices=[("", "Todos los estados")] + list(TipoEstado.choices),
        required=False
    )

    es_eventual = forms.ChoiceField(
    label=_("Servicio Eventual"),
    choices=ES_EVENTUAL_CHOICES,
    required=False,
    )

    desde = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label=_("Fecha Inicio")
    )

    hasta = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label=_("Fecha Fin")
    )

    totalEstimado = forms.DecimalField(
        label=_("Total estimado"),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '10000'}),
        decimal_places=2,
        max_digits=14
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML('<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "estado", "es_eventual","desde", "hasta", "totalEstimado",  # Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'),
                Submit('clear', 'Borrar filtros', css_class='btn btn-secondary'),
                css_class="d-grid gap-2")
        )

    def get_es_eventual(self, qs, value):
        if value == "1":
            return qs.filter(desde=models.F("hasta"))  # Es eventual
        elif value == "0":
            return qs.exclude(desde=models.F("hasta"))  # No es eventual
        return qs  # Sin filtro


    def get_estado(self, qs, value):
        q = Q(estados__timestamp=Subquery(
            Estado.objects.filter(servicio=OuterRef("id"), timestamp__lte=datetime.now())
            .order_by("-timestamp")
            .values("timestamp")[:1]
        )) & Q(estados__tipo=value)
        return qs.filter(q)
      
from core.models import Categoria
from .models import ServicioCantidadEmpleado
from django.forms import inlineformset_factory

class ServicioCantidadEmpleadoForm(forms.ModelForm):
    class Meta:
        model = ServicioCantidadEmpleado
        fields = ['categoria', 'cantidad']

        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1, 'max': 200}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


# FORMSET DE EMPLEADOS POR SERVICIO
def ServicioCantidadEmpleadoInline(extra=1):
    return inlineformset_factory(
        Servicio,
        ServicioCantidadEmpleado,
        form=ServicioCantidadEmpleadoForm,
        extra=extra,
        can_delete=True
    )


class ServicioCantidadEmpleadoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'
        self.layout = Layout(
            'categoria',
            'cantidad'
        )
        self.render_required_fields = True


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        exclude = ('estado', 'total')
        widgets = {
            'desde': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'hasta': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['desde'].widget.attrs['min'] = datetime.today().strftime('%Y-%m-%d')
        self.fields['hasta'].widget.attrs['min'] = datetime.today().strftime('%Y-%m-%d')

        self.fields['inmueble'].widget.attrs.update({
            'class': 'select2-inmueble form-select',
            'data-placeholder': 'Buscar inmueble por domicilio o cliente'
        })

        inmuebles = Inmueble.objects.none()

        if "initial" in kwargs and "cliente" in kwargs["initial"]:
            cliente = kwargs["initial"]["cliente"]
            inmuebles = Inmueble.objects.filter(cliente=cliente)

        if self.instance and self.instance.pk:
            inmuebles = Inmueble.objects.filter(pk=self.instance.inmueble.pk) | inmuebles
        elif 'inmueble' in self.data:
            try:
                inmueble_id = int(self.data.get('inmueble'))
                inmuebles = Inmueble.objects.filter(pk=inmueble_id) | inmuebles
            except (ValueError, TypeError):
                pass

        self.fields['inmueble'].queryset = inmuebles.distinct()

        self.helper = FormHelper()
        self.helper.form_tag = False


    def save(self, commit=True):
        servicio = super().save(commit)
        servicio.total = servicio.totalEstimado()
        servicio.save()
        return servicio

    def clean(self):
        cleaned_data = super().clean()
        desde = cleaned_data.get('desde')
        hasta = cleaned_data.get('hasta')

        if desde and hasta and hasta < desde:
            raise ValidationError("La fecha 'FIN' debe ser mayor o igual a la fecha 'INICIO'.")

        return cleaned_data


class ServicioUpdateForm(forms.ModelForm):

    class Meta:
        model = Servicio
        exclude = ('estado', 'inmueble', )
    
    desde = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))
    hasta = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        #print(f"{kwargs=}")
        servicio = kwargs["instance"] # nos da el modelo Inmueble
        url_kwargs = {'pk': servicio.pk}
        url = "servicios:modificarServicio"
        #if "initial" in kwargs:
            #if "cliente" in kwargs["initial"]:
                #servicio = kwargs["initial"] # nos da el Servicio
        inmueble = servicio.inmueble
        #print(f"{inmueble=}")
        url = "servicios:modificarServicioParaCliente"
        url_kwargs.update({'cliente_pk': inmueble.cliente.pk})
        #print(f"{url=}, {url_kwargs=}")
        self.helper.form_action = reverse_lazy(url, kwargs=url_kwargs)
        
class ServicioContratarForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['desde', 'hasta', 'inmueble']
        widgets = {
            'desde': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'hasta': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



        self.fields['desde'].widget.attrs['min'] = datetime.today().strftime('%Y-%m-%d')
        self.fields['hasta'].widget.attrs['min'] = datetime.today().strftime('%Y-%m-%d')

        # Mostrar inmueble como solo lectura (disabled), pero también mantenerlo oculto para el POST
        self.fields['inmueble'].disabled = True
        self.fields['inmueble_hidden'] = forms.ModelChoiceField(
            queryset=Inmueble.objects.all(),
            initial=self.instance.inmueble,
            widget=forms.HiddenInput()
        )

        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super().clean()
        desde = cleaned_data.get('desde')
        hasta = cleaned_data.get('hasta')
        if desde and hasta and hasta < desde:
            raise forms.ValidationError("La fecha 'hasta' debe ser posterior a 'desde'.")
        return cleaned_data

    def save(self, commit=True):
        self.instance.inmueble = self.cleaned_data.get('inmueble_hidden')
        return super().save(commit)


class DetalleServicioForm(forms.ModelForm):

    class Meta:
        model = DetalleServicio
        fields = ("tipoServicio",
                  "cantidad",
                  )

        widgets = {
            'tipoServicio': forms.Select(attrs={'autocomplete': 'off'}),
            'cantidad': forms.NumberInput(attrs={'min': 1})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


# Tipo Servicio - Producto - Inlines

def DetalleServicioInline(extra=1):
    return forms.inlineformset_factory(
        Servicio,
        DetalleServicio,
        form=DetalleServicioForm,
        extra=extra,
    )


# Tipo Servicio - Producto - Form Helper

class DetalleServicioFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'
        self.layout = Layout(
            'tipoServicio',
            'cantidad'
        )
        self.render_required_fields = True



class TipoServicioForm(forms.ModelForm):
    class Meta:
        model= TipoServicio
        exclude= ('productos',)

        widgets= {
            'ganancia': forms.NumberInput(attrs={'min':1,'max':100})
        }
        
        labels = {
            'ganancia': 'Ganancia (%)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class TipoServicioUpdateForm(forms.ModelForm):

    class Meta:
        model = TipoServicio
        exclude= ('productos',)

        widgets= {
            'ganancia': forms.NumberInput(attrs={'min':1,'max':100})
        }
        
        labels = {
            'ganancia': 'Ganancia (%)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class TipoServicioProductoForm(forms.ModelForm):

    class Meta:
        model = TipoServicioProducto
        fields = ("producto",
                  "cantidad",
                  )

        widgets = {
            'producto': forms.Select(attrs={'autocomplete': 'off'}),
            'cantidad': forms.NumberInput(attrs={'min': 0})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


# Tipo Servicio - Producto - Inlines

def TipoServicioProductoInline(extra=1):
    return forms.inlineformset_factory(
        TipoServicio,
        TipoServicioProducto,
        form=TipoServicioProductoForm,
        extra=extra,
    )

# Tipo Servicio - Producto - Form Helper

class TipoServicioProductoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'
        self.layout = Layout(
            'producto',
            'cantidad'
        )
        self.render_required_fields = True


    


    

class TipoServicioFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("descripcion", "Descripcion"),
        ("ganancia", "Ganancia"),
    ]
    ATTR_CHOICES = [
        ("descripcion", "Descripcion"),
        ("ganancia", "Ganancia"),

    ]

    #Formulario de filtrado
    descripcion = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'limpieza'}), max_length=250)
    ganancia = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'placeholder': '15'}), decimal_places=2,max_digits=14)
        
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "descripcion", "ganancia"
            ),
            Div(Submit('submit', 'Filtrar'),
                Submit('clear', 'Borrar filtros', css_class='btn btn-secondary'),
                css_class="d-grid gap-2")
        )


