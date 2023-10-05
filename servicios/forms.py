
from django import forms
from .models import Cliente

class ClienteCreateForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=('cuil_cuit','apellido_y_nombre','correo','habitual','gubernamental')


