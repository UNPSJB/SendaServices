from io import BytesIO
import os
import base64
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage

def generar_pdf_factura_en_memoria(factura):
    html = render_factura_html(factura)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    result.seek(0)
    return result

def render_factura_html(factura):
    template = get_template('pdf/factura_individual.html')
    
    # Ruta base64 o local para evitar errores de xhtml2pdf
    logo_path = os.path.join(settings.BASE_DIR, "static/img/senda.png")
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    
    html = template.render({
        'factura': factura,
        'servicio': factura.servicio,
        'logo_base64': f"data:image/png;base64,{logo_base64}"
    })
    return html


def enviar_factura_por_email(factura):
    cliente = factura.servicio.inmueble.cliente
    correo_destino = cliente.correo

    pdf_file = generar_pdf_factura_en_memoria(factura)

    mail = EmailMessage(
        subject=f"📄 Factura #{factura.pk} - Senda Services",
        body=f"Hola {cliente},\n\nAdjuntamos tu factura correspondiente al servicio realizado.\n\nSaludos,\nEquipo Senda",
        from_email=os.getenv('DEFAULT_FROM_EMAIL'),
        to=[correo_destino],
    )
    mail.attach(f"factura_{factura.pk}.pdf", pdf_file.read(), "application/pdf")
    mail.send()
