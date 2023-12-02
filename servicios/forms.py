
from django import forms 
from .models import TipoServicio, TipoServicioProducto, Servicio, DetalleServicio, TipoEstado, Estado
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


class ServiciosFiltrosForm(FiltrosForm):
    # Campos del modelo
    ORDEN_CHOICES = [
        ("estado", "Estado"),
        ("desde", "Fecha Inicio"),
        ("hasta", "Fecha Fin"),
        ("cantidadEstimadaEmpleados", "Empleados Estimados"),
        ("totalEstimado", "Total Estimado"),
    ]

    ATTR_CHOICES = [
        ("estado", "Estado"),
        ("desde", "Fecha Inicio"),
        ("hasta", "Fecha Fin"),
        ("cantidadEstimadaEmpleados", "Empleados Estimados"),
        ("totalEstimado", "Total Estimado"),
    ]

    # ESTADO_CHOICES = [
    #     ("presupuestado", _("Presupuestado 👽")),
    #     ("contratado", _("Contratado 🛸")),
    #     ("vencido", _("Vencido 💀")),
    #     ("cancelado", _("Cancelado 💩")),
    #     ("pagado", _("Pagado 🤑")),
    #     ("iniciado", _("Iniciado 😊")),
    #     ("finalizado", _("Finalizado 😴")),
    # ]

    # Formulario de filtrado
    estado = forms.ChoiceField(
        label=_("Estado"),
        choices=TipoEstado.choices,
        required=False  # Ajusta esto según tus necesidades
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

    cantidadEstimadaEmpleados = forms.DecimalField(
        label=_("Empleados Estimados"),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '10000'}),
        decimal_places=2,
        max_digits=14
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
                "codigo", "estado", "hasta", "desde", "cantidadEstimadaEmpleados", "totalEstimado",  # Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )

    def get_estado(self, qs, value):
        q = Q(estados__timestamp=Subquery(
            Estado.objects.filter(servicio=OuterRef("id"), timestamp__lte=datetime.now())
            .order_by("-timestamp")
            .values("timestamp")[:1]
        )) & Q(estados__tipo=value)
        return qs.filter(q)
      
class ServicioForm(forms.ModelForm):
    class Meta:
        model= Servicio
        exclude = ('estado',)

        widgets = {
            'desde': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'hasta': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desde'].widget.attrs['min'] = datetime.today().strftime('%Y-%m-%d')
        self.fields['hasta'].widget.attrs['min'] = datetime.today().strftime('%Y-%m-%d')

        inmuebles = Inmueble.objects.all()

        if "initial" in kwargs:
            if "cliente" in kwargs["initial"]:
                cliente = kwargs["initial"]["cliente"] # nos da el Cliente del Inmueble
                inmuebles = Inmueble.objects.filter(cliente = cliente)
      
        self.fields['inmueble'].queryset = inmuebles
        self.helper = FormHelper()
        self.helper.form_tag = False

        #self.helper.form_action = reverse_lazy(url, kwargs=url_kwargs)

    def clean(self):
        cleaned_data = super().clean()
        desde = cleaned_data.get('desde')
        hasta = cleaned_data.get('hasta')

        if desde and hasta and hasta < desde:
            raise ValidationError("La fecha 'FIN' debe ser mayor o igual a la fecha 'INICIO'.")

        return cleaned_data
    

from django import forms
from django.core.exceptions import ValidationError
from .models import Servicio
from datetime import datetime
from crispy_forms.helper import FormHelper

class ServicioUpdateForm(forms.ModelForm):

    class Meta:
        model = Servicio
        exclude = ('estado', 'inmueble', )

    desde = forms.DateField(widget=forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'text'}))
    hasta = forms.DateField(widget=forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'text'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desde'].widget.attrs['min'] = datetime.today().strftime('%d/%m/%Y')
        self.fields['hasta'].widget.attrs['min'] = datetime.today().strftime('%d/%m/%Y')
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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     inmueble = kwargs["instance"] # nos da el modelo Inmueble
    #     url_kwargs = {'pk': inmueble.pk}
    #     url = "modificarInmueble"
    #     if "initial" in kwargs:
    #         if "cliente" in kwargs["initial"]:
    #             cliente = kwargs["initial"]["cliente"] # nos da el Cliente del Inmueble
    #             url = "modificarInmuebleParaCliente"
    #             url_kwargs.update({'cliente_pk': cliente.pk})

    #     self.helper.form_action = reverse_lazy(url, kwargs=url_kwargs)

    def clean(self):
        cleaned_data = super().clean()
        desde = cleaned_data.get('desde')
        hasta = cleaned_data.get('hasta')

        if desde and hasta and hasta < desde:
            raise ValidationError("La fecha 'FIN' debe ser mayor o igual a la fecha 'INICIO'.")

        return cleaned_data

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
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


