
from django import forms
from .models import Cliente,TipoServicio

class ClienteCreateForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=('cuil_cuit','apellido_y_nombre','correo','habitual','gubernamental')



class tipoServicioForm(forms.ModelForm):
    model= TipoServicio
    fields=('codigo','descripcion','costo','unidadDeMedida')
    


    


