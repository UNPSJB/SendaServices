from django_cron import CronJobBase, Schedule
from servicios.models import Servicio, TipoEstado
from decimal import Decimal
from servicios.utils import enviar_factura_por_email
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.timezone import make_aware
import threading
import traceback

class VerificarPresupuestosVencidosCron(CronJobBase):
    RUN_EVERY_MINS = 1  # cada 1 minuto para pruebas
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'servicios.verificar_presupuestos_vencidos'

    def do(self):
        try:
            print("📆 Verificando presupuestos vencidos...")
            ahora = timezone.now()

            servicios = Servicio.objects.filter(
                estado=TipoEstado.PRESUPUESTADO
            )

            for servicio in servicios:
                try:
                    fecha = make_aware(datetime.combine(servicio.fecha_presupuesto, datetime.min.time()))
                    if (ahora - fecha) > timedelta(seconds=10):
                        servicio.set_estado(TipoEstado.VENCIDO)
                        print(f"💀 Servicio #{servicio.pk} vencido por presupuesto sin confirmar.")
                except Exception as e:
                    print(f"❌ Error al procesar servicio #{servicio.pk}: {e}")
                    traceback.print_exc()

        except Exception as e:
            print("❌ Error general en el cron de presupuestos vencidos:", str(e))
            traceback.print_exc()


class FacturacionAutomaticaCron(CronJobBase):
    RUN_EVERY_MINS = 60  # cada 24hs
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'servicios.facturacion_automatica'

    def do(self):
        try:
            print("🕒 Ejecutando facturación automática...")

            servicios = Servicio.objects.filter(estado=TipoEstado.EN_CURSO)

            for servicio in servicios:
                try:
                    facturas = servicio.facturas.count()
                    estimado = servicio.cantidad_meses_estimados()

                    if facturas >= estimado:
                        print(f"🔒 Servicio {servicio.pk} ya tiene todas las facturas.")
                        continue

                    total = Decimal(servicio.totalEstimado())
                    if servicio.requiereSeña:
                        total = total / 2

                    monto = total / estimado

                    factura = servicio.facturar(monto=monto)

                    if factura:
                        threading.Thread(
                            target=enviar_factura_por_email,
                            args=(factura,)
                        ).start()

                        print(f"📄 Factura generada y enviada para servicio #{servicio.pk}")

                except Exception as e:
                    print(f"❌ Error procesando servicio {servicio.pk}: {e}")
                    traceback.print_exc()

        except Exception as e:
            print("❌ Error general en el cron:", str(e))
            traceback.print_exc()
