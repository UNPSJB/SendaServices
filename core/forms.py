from django.forms import ModelForm
from .models import Producto, Cliente


class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'



