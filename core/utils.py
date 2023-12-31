from django import forms
from django.db.models import Q, Model
from django.http import HttpResponse
from decimal import Decimal
from datetime import date
from django.views.generic.list import ListView
import csv


def filter_query_by(filtros_dict, queryset, form = None):
    for attr, value in filtros_dict.items():
        if not value:
            continue
        if form is not None and hasattr(form, f"get_{attr}"):
            func = getattr(form, f"get_{attr}")
            if callable(func):
                queryset = func(queryset, value)
        elif type(value) == str:
            if value.isdigit():
                prev_value = value
                value = int(value)
                queryset = queryset.filter(Q(**{attr: value}) | Q(**
                                                 {f'{attr}__icontains': prev_value}))
            else:
                attr = f'{attr}__icontains'
                #print(f"{attr=} {value=}")
                queryset = queryset.filter(Q(**{attr: value}))
        # elif isinstance(value, Model) or isinstance(value, int) or isinstance(value, Decimal):
        elif isinstance(value, (Model, int, Decimal, date)):
            queryset = queryset.filter(Q(**{attr: value}))
    return queryset

# Filtros - Form

class FiltrosForm(forms.Form):
    ORDEN_CHOICES = [] # Choices para ordenamiento
    ATTR_CHOICES = [] # Choices del listado para el listado a exportar
    orden = forms.CharField(required=False)

    def filter(self, qs, filters):
        return filter_query_by(filters, qs, self)
        
    def sort(self, qs, ordering):
        for o in ordering.split(','):
            if o != '':
                qs = qs.order_by(o)  # aplicamos ordenamiento
        return qs

    def apply(self, qs):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            ordering = cleaned_data.pop("orden", None)
            if len(cleaned_data) > 0:
                qs = self.filter(qs, cleaned_data)
            if ordering:
                qs = self.sort(qs, ordering)
        return qs

    def sortables(self):
        return self.ORDEN_CHOICES
    
    def get_attrs(self):
        return self.ATTR_CHOICES
    
    def serialize_query_params(self):
        #print("data: ", self.data)
        if self.is_valid():
            return "&".join([f"{k}={v}" for k,v in self.data.items() if v]) 

# Lista Filtros - ListView

class ListFilterView(ListView):
    filtros = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtros = self.get_filtros(self.request.GET)
        if filtros is not None: 
            context['filtros'] = filtros
            context['serialized_query_params'] = filtros.serialize_query_params()
        context['query'] = self.get_queryset()

        """if self.filtros:
            filtros = self.filtros(self.request.GET)
            context['filtros'] = filtros
            context['serialized_query_params'] = filtros.serialize_query_params()
            context['query'] = self.get_queryset()"""

        return context

    def get_queryset(self):
        qs = super().get_queryset()
        #print(f"{qs=}")
        qs = self.apply_filters_to_qs(qs)
        return qs

    def get_filtros(self, *args, **kwargs):
        return self.filtros(*args, **kwargs) if self.filtros is not None else None

    def apply_filters_to_qs(self, qs):

        filtros = self.get_filtros(self.request.GET)
        if filtros is not None:
        # if self.filtros:
        #     filtros = self.filtros(self.request.GET)
        #     print(f"{filtros=}")
            return filtros.apply(qs)

        """if self.filtros:
            filtros = self.filtros(self.request.GET)
            results = filtros.apply(qs)
            return results"""

        return qs
    


def export_list(request, Modelo, Filtros): # Metodo utilizado para la exportar listados a formato .csv

    qs = Modelo.objects.all() # Modelo del listado
    filtros = Filtros(request.GET) # Filtros del listado, el GET obtiene los criterios de filtros
    if filtros.is_valid():
        qs = filtros.apply(qs) # aplicamos filtros
    
        encabezados = filtros.get_attrs() # attrs definidos en filtros
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename=filename.csv'
        
        writer = csv.writer(response, delimiter=";") # comienzo a escribrir

        fields_nombre = [v for k,v in encabezados] 
        fields_clave = [k for k,v in encabezados]
        writer.writerow(fields_nombre)


        for fila in qs: # por cada fila...
            valores = []
            for f in fields_clave: #escribo el valor de la celda que corresponde hasta llenar la fila
                valor = getattr(fila, f)
                if callable(valor): 
                    
                    try: #intento ejecutarla
                        valor = valor()
                        if valor is True or valor is False:
                            valor = ("No","Si")[valor is True]
     

                    except: 
                        valor =  ''.join([str(v)+'\n' for v in valor.all()]) #formateando valores

                if valor is None: #si el valor es nulo...
                    valor = 'n/a'


                valores.append(valor) # adjunto el valor justo con los demas valores que conforman la fila
            writer.writerow(valores) # escribo la fila

        return response