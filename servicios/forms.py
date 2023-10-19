
from django import forms 
from .models import TipoServicio



class tipoServicioForm(forms.ModelForm):
    class Meta:
        model= TipoServicio
        fields= '__all__'


    


    


