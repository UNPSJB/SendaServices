
from django import forms 
from .models import TipoServicio, TipoServicioProducto
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
            'cantidad': forms.NumberInput(attrs={'min': 1})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


# Presupuesto - Material - Inlines

def TipoServicioProductoInline(extra=1):
    return forms.inlineformset_factory(
        TipoServicio,
        TipoServicioProducto,
        form=TipoServicioProductoForm,
        extra=extra,
    )

# Presupuesto - Material - Form Helper

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


    


    


