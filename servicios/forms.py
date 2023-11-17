
from django import forms 
from .models import TipoServicio, TipoServicioProducto
from core.utils import FiltrosForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML



class TipoServicioForm(forms.ModelForm):
    class Meta:
        model= TipoServicio
        exclude= ('productos',)

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


