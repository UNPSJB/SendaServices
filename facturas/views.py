from django.shortcuts import render, get_object_or_404
from .models import Factura
from core.utils import ListFilterView
from servicios.models import Servicio
from .forms import (
    FacturasFiltrosForm,)

def detalle_factura(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)
    return render(request, 'facturas/factura.html', {'factura': factura})

# Create your views here.s
class FacturaListView(ListFilterView):
    #Cantidad de elementos por lista
    paginate_by = 5
    #Filtros de la lista
    filtros = FacturasFiltrosForm
    model = Factura #Nombre del modelo
    template_name = "facturas/facturas_list.html" #Ruta del template
    context_object_name = 'facturas' #Nombre de la lista usar ''
  
    def get_servicio(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return Servicio.objects.get(pk=pk)
        else:
            return None
        
    def get_queryset(self):
        servicio = self.get_servicio()
        if servicio:
            # Filtrar las facturas por el servicio
            return Factura.objects.filter(servicio=servicio)
        else:
            # Si no hay servicio, mostrar todas las facturas
            return Factura.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = self.get_servicio()
        context['tnav'] = "Gestion de Facturas" if not servicio else f"Gestion de Facturas: {servicio}"
        context["servicio"] = servicio
        return context

