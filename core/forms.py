from django import forms
from django.forms import ModelForm, ValidationError, Select
from django.urls import reverse_lazy
from .models import Producto, Cliente, Inmueble, Empleado,Categoria
from .utils import FiltrosForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML



class ClienteFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("cuil_cuit", "CUIL/CUIT"),
        ("apellido", "Apellido"),
        ("nombre", "Nombre"),
        ("correo", "Correo"),
        ("habitual", "Habitual"),
        ("gubernamental", "Gubernamental"),
    ]
    ATTR_CHOICES = [

        ("cuil_cuit", "CUIL/CUIT"),
        ("apellido", "Apellido"),
        ("nombre", "Nombre"),
        ("correo", "Correo"),
        ("habitual", "Habitual"),
        ("gubernamental", "Gubernamental"),

    ]

    #Formulario de filtrado
    cuil_cuit = forms.CharField(label="CUIL/CUIT",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cuil/Cuit'}), max_length=45)
    apellido = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}), max_length=45)
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}), max_length=45)
    correo = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Correo'}))
        
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "cuil_cuit","nombre", "apellido", "correo", #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'cuil_cuit': 'Cuil/Cuit',
            'apellido': 'Apellido',
            'nombre': 'Nombre',
            'correo': 'Correo',
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'cuil_cuit': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el cuil/cuit del cliente',
                    'pattern': '([0-9]{11})', 'placeholder': '###########',
                    #'pattern': '([0-9]{2}-([0-9]{8}|[0-9]{7})-[0-9]{1})', 'placeholder': '##-########-#',
                }
            ),
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre del cliente',
                }
            ),
            'apellido': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el apellido del cliente',
                }
            ),
            'correo': forms.EmailInput(
                attrs = {           
                    'class': 'form-control',
                    'placeholder':'Ingrese el correo del cliente',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-clienteForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Guardar'))


class ClienteModForm(ModelForm):

    class Meta:
        model = Cliente
        exclude = ('cuil_cuit',)

        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'apellido': 'Apellido',
            'nombre': 'Nombre',
            'correo': 'Correo',
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre del cliente',
                }
            ),
            'apellido': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el apellido del cliente',

                }
            ),
            'correo': forms.EmailInput(
                attrs = {           
                    'class': 'form-control',
                    'placeholder':'Ingrese el correo del cliente',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-clienteForm'
        self.helper.form_method = 'post'
        cliente = kwargs["instance"] # nos da el modelo Inmueble
        self.helper.form_action = reverse_lazy("modificarCliente", kwargs={"pk": cliente.pk})
        self.helper.add_input(Submit('submit', 'Guardar'))


class EmpleadoForm(ModelForm):

    class Meta:
        model = Empleado
        fields = '__all__'
        exclude = ["baja"]
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'legajo': 'Legajo',
            'apellido': 'Apellido',
            'nombre': 'Nombre',
            'cuil': 'Cuil',
            'correo': 'Correo',
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'legajo': forms.NumberInput(
                #Permite estilizar los formularios
                attrs = {
                    'min':0,
                    'class': 'form-control',
                    'placeholder':'Ingrese el legajo del empleado',
                }
            ),
            'apellido': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el apellido del empleado',
                }
            ),
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre del empleado',

                }
            ),
            'cuil': forms.NumberInput(
                attrs = {
                    'min':0,
                    'class': 'form-control',
                    'placeholder':'Ingrese el cuil del empleado',
                    'pattern': '([0-9]{11})', 'placeholder': '###########',
                }
            ),
            'correo': forms.EmailInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder':'Ingrese el correo del empelado',
                }
            ),
        
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-empleadoForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Guardar'))


class EmpleadoFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("legajo", "Legajo"),
        ("apellido", "Apellido"),
        ("nombre", "Nombre"),
        ("correo", "Correo"),
        ("cuil", "Cuil"),
        ("categoria", "Categoria"),
    ]
    ATTR_CHOICES = [

        ("legajo", "Legajo"),
        ("apellido", "Apellido"),
        ("nombre", "Nombre"),
        ("correo", "Correo"),
        ("cuil", "Cuil"),
        ("categoria", "Categoria"),

    ]

    #Formulario de filtrado
    legajo = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Legajo'}), max_length=45)
    apellido = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}), max_length=45)
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}), max_length=45)
    correo = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Correo'}))
    cuil = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Cuil'}), max_length=45)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False, label='Categoria') 
  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "legajo","nombre", "apellido", "correo","cuil","categoria" #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


class EmpleadoModForm(ModelForm):

    class Meta:
        model = Empleado
        exclude= ("legajo", "baja","cuil",)

        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'apellido': 'Apellido',
            'nombre': 'Nombre',
            'correo': 'Correo',
            'cuil': 'Cuil',
            'categoria': 'Categoria',
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre del empleado',
                }
            ),
            'apellido': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el apellido del empleado',

                }
            ),
            'correo': forms.EmailInput(
                attrs = {           
                    'class': 'form-control',
                    'placeholder':'Ingrese el correo del empleado',
                }
            ),
                 
            'cuil': forms.NumberInput(
                attrs = {           
                    'class': 'form-control',
                    'placeholder':'Ingrese el cuil del empleado',
                }
            ),
            'Categoria.numero': forms.NumberInput(
                attrs = {           
                    'class': 'form-control',
                    'placeholder':'Ingrese el numero de la categoria',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'legajo-empleadoForm'
        self.helper.form_method = 'post'
        empleado = kwargs["instance"] 
        self.helper.form_action = reverse_lazy("modificarEmpleado", kwargs={"pk": empleado.legajo})
        self.helper.add_input(Submit('submit', 'Guardar'))

            

class CategoriaForm(ModelForm):

    class Meta:
        model = Categoria
        fields = '__all__'
        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'nombre':'Nombre',
            'sueldoBase': 'Sueldo Base',
            'empleado.legajo': 'Empleado',
           
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'nombre': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre de la categoria',
                }
            ),
            'sueldoBase': forms.NumberInput(
                attrs = {
                    'min': 0,
                    'class': 'form-control',
                    'placeholder':'Ingrese el sueldo base de la categoria',
                }
            )
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-categoriaForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Guardar'))


class CategoriaUpdateForm(CategoriaForm):

    class Meta(CategoriaForm.Meta):
        pass
        #model = Categoria
        #fields = '__all__'
        #exclude = ["baja", "empleado.legajo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-categoriaForm'
        self.helper.form_method = 'post'
        categoria = kwargs["instance"] # nos da el modelo Inmueble
        self.helper.form_action = reverse_lazy("modificarCategoria", kwargs={"pk": categoria.pk})
        self.helper.add_input(Submit('submit', 'Guardar'))



class CategoriaFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("sueldoBase", "Sueldo Base"),
    ]
    ATTR_CHOICES = [
        ("nombre", "Nombre"),
        ("sueldoBase", "Sueldo Base"),
    ]

    #Formulario de filtrado

    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    sueldoBase = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Sueldo Base'}))
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "nombre", "sueldoBase"
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )



class InmuebleFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("domicilio", "Domicilio"),
        ("metrosCuadrados", "Metros Cuadrados"),
        ("nroAmbientes", "Cantidad de Ambientes"),
        ("tipo", "Tipo"),
        ("cliente", "Propietario"),
    ]
    ATTR_CHOICES = [
        ("domicilio", "Domicilio"),
        ("metrosCuadrados", "Metros Cuadrados"),
        ("nroAmbientes", "Cantidad de Ambientes"),
        ("tipo", "Tipo"),
        ("cliente", "Propietario"),
    ]

    #Formulario de filtrado
    domicilio = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Domicilio'}), max_length=90)
    metrosCuadrados = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Metros Cuadrados'}))
    nroAmbientes = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de Ambientes'}))
    tipo = forms.ChoiceField(required=False, choices=Inmueble.TIPOS)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False, label='Propietario') #filtrar inmuebles por cliente

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "domicilio","metrosCuadrados", "nroAmbientes", "tipo", "cliente", #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


class InmuebleCustomFiltrosForm(InmuebleFiltrosForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "domicilio","metrosCuadrados", "nroAmbientes", "tipo", #Remplazar campos formulario
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


InmuebleCustomFiltrosForm.base_fields.pop("cliente")


def InmuebleForm(selected_client=None):  

    class InmuebleForm(ModelForm):

        #if not selected_client:
            #cliente = forms.ModelChoiceField(
            #    queryset=Cliente.objects.all(),
            #    widget=forms.Select(attrs={'disabled':'disabled' if selected_client else False})
            #    )

        #print(selected_client is None)

        class Meta:
            model = Inmueble
            fields = '__all__'
            exclude = ["cliente", ] if selected_client else []
            #Label se refiere la descripcion que esta al lado del formulario.
            labels = { 
                'codigo': 'Domicilio',
                'metrosCuadrados': 'Metros Cuadrados',
                'nroAmbientes': 'Cantidad de Ambientes',
            }

            #Referencia a los estilos con los que se renderizan los campos
            widgets = {
                'domicilio': forms.TextInput(
                    #Permite estilizar los formularios
                    attrs = {
                        'class': 'form-control',
                        'placeholder':'Ingrese el domicilio del inmueble',
                    }
                ),
                'metrosCuadrados': forms.NumberInput(
                    attrs = {
                        'min': 0,
                        'class': 'form-control',
                        'placeholder':'Ingrese los metros cuadrados del inmueble',
                    }
                ),
                'nroAmbientes': forms.NumberInput(
                    attrs = {
                        'min': 0,
                        'class': 'form-control',
                        'placeholder':'Ingrese la cantidad de ambientes del inmueble',

                    }
                ),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'id-inmuebleForm'
            self.helper.form_method = 'post'
            if selected_client:
                self.helper.form_action = reverse_lazy("crearInmuebleParaCliente", kwargs={"pk": selected_client.pk})
            self.helper.add_input(Submit('btn-submit-form', 'Guardar', css_class="btn btn-primary btn-block text-white w-100", css_id="save-inmueble"))

    return InmuebleForm


class InmuebleUpdateForm(InmuebleForm()):

    class Meta(InmuebleForm().Meta):
        exclude = ["domicilio","cliente"]

        widgets = {
            'domicilio': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'readonly': 'readonly',
                }
            ), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        inmueble = kwargs["instance"] # nos da el modelo Inmueble
        url_kwargs = {'pk': inmueble.pk}
        url = "modificarInmueble"
        if "initial" in kwargs:
            if "cliente" in kwargs["initial"]:
                cliente = kwargs["initial"]["cliente"] # nos da el modelo Inmueble
                url = "modificarInmuebleParaCliente"
                url_kwargs.update({'cliente_pk': cliente.pk})

        self.helper.form_action = reverse_lazy(url, kwargs=url_kwargs)


if "cliente" in InmuebleUpdateForm.base_fields:
    InmuebleUpdateForm.base_fields.pop("cliente")


class ProductoFiltrosForm(FiltrosForm):
    #Campos del modelo
    ORDEN_CHOICES = [
        ("codigo", "Código"),
        ("descripcion", "Descripción"),
        ("stock", "Stock"),
        ("precioUnitario", "Precio Unitario"),
    ]
    ATTR_CHOICES = ORDEN_CHOICES

    #Formulario de filtrado
    codigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'EJ000'}), max_length=45)
    descripcion = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Lavandina'}), max_length=45)
    stock__gte = forms.DecimalField(label="", widget=forms.NumberInput(attrs={'placeholder': 'Mínimo', 'min': 1}), required=False)
    stock__lte = forms.DecimalField(label="", widget=forms.NumberInput(attrs={'placeholder': 'Máximo', 'min': 1}), required=False)
    precioUnitario__gte = forms.DecimalField(label="", widget=forms.NumberInput(attrs={'placeholder': 'Mínimo', 'min': 1}), required=False)
    precioUnitario__lte = forms.DecimalField(label="", widget=forms.NumberInput(attrs={'placeholder': 'Máximo', 'min': 1}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<i class="fas fa-filter"></i> <h4>Filtrar</h4>'),
                "codigo",
                "descripcion", 
                HTML(
                    '<label class="form-label">Stock</label>'),
                Div("stock__gte", "stock__lte", css_class="custom-range-form"),
                HTML(
                    '<label class="form-label">Precio Unitario</label>'),
                Div("precioUnitario__gte", "precioUnitario__lte", css_class="custom-range-form"),
            ),
            Div(Submit('submit', 'Filtrar'), css_class="d-grid gap-2")
        )


class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ["baja"] 

        #Label se refiere la descripcion que esta al lado del formulario.
        labels = { 
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'stock': 'Stock',
            'precioUnitario': 'Precio Unitario',
           
        }
        #Referencia a los estilos con los que se renderizan los campos
        widgets = {
            'codigo': forms.TextInput(
                #Permite estilizar los formularios
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese el codigo del producto',
                }
            ),
            'descripcion': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder':'Ingrese descripcion del producto',
                }
            ),
            'stock': forms.NumberInput(
                attrs = {
                    'min': 0,
                    'class': 'form-control',
                    'placeholder':'Ingrese el stock del producto',

                }
            ),
            'precioUnitario': forms.NumberInput(
                attrs = {
                    'min': 0,                    
                    'class': 'form-control',
                    'placeholder':'Ingrese el precio del producto',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-productoForm'

        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Guardar'))



class ProductoUpdateForm(ProductoForm):

    class Meta(ProductoForm.Meta):
        exclude = ["stock", "codigo", "baja"]
    
