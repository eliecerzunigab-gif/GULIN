from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ─── Colores corporativos ───
PRIMARY = HexColor("#8b5cf6")
PRIMARY_DARK = HexColor("#7c3aed")
PRIMARY_LIGHT = HexColor("#a78bfa")
BG_DARK = HexColor("#0a0a12")
BG_CARD = HexColor("#111122")
TEXT_MAIN = HexColor("#e2e8f0")
TEXT_SEC = HexColor("#94a3b8")
TEXT_MUTED = HexColor("#64748b")
BORDER = HexColor("#1e1e3a")
GREEN = HexColor("#22c55e")
YELLOW = HexColor("#eab308")
RED = HexColor("#ef4444")

WIDTH, HEIGHT = A4

# ─── Estilos ───
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "BrochureTitle", parent=styles["Title"],
    fontSize=26, leading=32, textColor=white,
    fontName="Helvetica-Bold", alignment=TA_CENTER,
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    "BrochureSubtitle", parent=styles["Normal"],
    fontSize=12, leading=16, textColor=TEXT_SEC,
    fontName="Helvetica", alignment=TA_CENTER,
    spaceAfter=20
)

heading_style = ParagraphStyle(
    "BrochureHeading", parent=styles["Heading2"],
    fontSize=16, leading=20, textColor=PRIMARY_LIGHT,
    fontName="Helvetica-Bold", spaceBefore=16, spaceAfter=8,
    alignment=TA_LEFT
)

body_style = ParagraphStyle(
    "BrochureBody", parent=styles["Normal"],
    fontSize=9.5, leading=14, textColor=TEXT_SEC,
    fontName="Helvetica", alignment=TA_JUSTIFY,
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    "BrochureBullet", parent=body_style,
    fontSize=9, leading=13, textColor=TEXT_SEC,
    leftIndent=14, bulletIndent=0,
    spaceAfter=3
)

feature_title = ParagraphStyle(
    "FeatureTitle", parent=styles["Normal"],
    fontSize=11, leading=14, textColor=white,
    fontName="Helvetica-Bold", spaceAfter=2
)

feature_desc = ParagraphStyle(
    "FeatureDesc", parent=body_style,
    fontSize=8.5, leading=12, textColor=TEXT_SEC
)

footer_style = ParagraphStyle(
    "Footer", parent=styles["Normal"],
    fontSize=7, leading=9, textColor=TEXT_MUTED,
    fontName="Helvetica", alignment=TA_CENTER
)

# ─── Funciones helper ───
def draw_bg(canvas, doc):
    """Fondo oscuro en todas las páginas"""
    canvas.saveState()
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    # Línea decorativa superior
    canvas.setStrokeColor(PRIMARY)
    canvas.setLineWidth(0.5)
    canvas.line(0, HEIGHT - 2, WIDTH, HEIGHT - 2)
    canvas.restoreState()

def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawCentredString(WIDTH / 2, 15, f"GuLIN AI — Brochure Corporativo — Pág. {doc.page}")
    canvas.restoreState()

def spacer(h=6):
    return Spacer(1, h)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8, spaceBefore=8)

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", bullet_style)

def section_box(title, items):
    """Crea una caja con título y lista de items"""
    elements = []
    elements.append(Paragraph(title, heading_style))
    for item in items:
        elements.append(bullet(item))
    elements.append(spacer(4))
    return elements

# ─── Construcción del PDF ───
output_path = os.path.join(os.path.dirname(__file__), "brochure_gulin.pdf")

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=20*mm,
    rightMargin=20*mm,
    topMargin=18*mm,
    bottomMargin=22*mm,
    title="Brochure GuLIN AI - Agente Inteligente de TI",
    author="GuLIN AI"
)

story = []

# ─── PORTADA ───
story.append(spacer(60))

# Logo
logo_path = os.path.join(os.path.dirname(__file__), "GULIN_LOGO_3.jpeg")
if os.path.exists(logo_path):
    im = Image(logo_path, width=55*mm, height=55*mm)
    story.append(im)

story.append(spacer(10))
story.append(Paragraph("GuLIN <font color='#8b5cf6'>IA</font>", title_style))
story.append(Paragraph("Agente Inteligente Autónomo para TI Empresarial", subtitle_style))
story.append(spacer(8))

# Línea decorativa
story.append(HRFlowable(width="60%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=4))

story.append(Paragraph(
    "Detecta, diagnostica y mitiga incidentes de infraestructura antes de que afecten a tus clientes.",
    ParagraphStyle("PortadaDesc", parent=body_style, fontSize=11, leading=16, textColor=TEXT_SEC, alignment=TA_CENTER)
))
story.append(spacer(30))

# Caja de highlights
highlights_data = [
    [Paragraph("<b>Reducción MTTR</b>", feature_title),
     Paragraph("<b>Velocidad Entrega</b>", feature_title),
     Paragraph("<b>Ahorro Anual</b>", feature_title)],
    [Paragraph("<font color='#8b5cf6' size='18'><b>-40%</b></font>", ParagraphStyle("h1", parent=body_style, alignment=TA_CENTER)),
     Paragraph("<font color='#8b5cf6' size='18'><b>3x</b></font>", ParagraphStyle("h2", parent=body_style, alignment=TA_CENTER)),
     Paragraph("<font color='#8b5cf6' size='18'><b>$50K+</b></font>", ParagraphStyle("h3", parent=body_style, alignment=TA_CENTER))],
    [Paragraph("en tiempo de resolución", ParagraphStyle("d1", parent=body_style, fontSize=7.5, alignment=TA_CENTER)),
     Paragraph("mayor velocidad de deploy", ParagraphStyle("d2", parent=body_style, fontSize=7.5, alignment=TA_CENTER)),
     Paragraph("en optimización de costos cloud", ParagraphStyle("d3", parent=body_style, fontSize=7.5, alignment=TA_CENTER))]
]

t = Table(highlights_data, colWidths=[doc.width/3]*3)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
    ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(t)

story.append(PageBreak())

# ─── PÁGINA 2: El Problema ───
story.append(Paragraph("El Problema", heading_style))
story.append(Paragraph(
    "Las operaciones tradicionales de TI están al límite. Los ingenieros pasan el 60% de su tiempo "
    "respondiendo a falsas alertas y apagando fuegos manualmente en lugar de construir valor para el producto.",
    body_style
))
story.append(spacer(4))

problems = [
    ("Fatiga extrema por Alertas", "Miles de notificaciones confusas al día. Imposible identificar qué es crítico antes de una caída."),
    ("Resolución Lenta (MTTR Elevado)", "Horas de análisis de logs, llamadas de emergencia a las 3 a.m. y costosos tiempos muertos."),
    ("Desperdicio y Costes Cloud", "Recursos sobre-dimensionados y licencias SaaS inactivas por falta de previsión inteligente."),
]

for title, desc in problems:
    story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle("p_title", parent=body_style, fontSize=10, textColor=white)))
    story.append(Paragraph(desc, body_style))
    story.append(spacer(2))

story.append(spacer(8))
story.append(Paragraph("La Solución", heading_style))
story.append(Paragraph(
    "GuLIN es el primer agente inteligente autónomo de TI para empresas. Se integra de forma segura en tu stack "
    "tecnológico para diagnosticar anomalías, predecir problemas de infraestructura y mitigar incidentes "
    "de forma totalmente autónoma, 24/7.",
    body_style
))

story.append(spacer(12))
story.append(hr())

# ─── Características Clave ───
story.append(Paragraph("Características Clave", heading_style))

features = [
    ("🤖 Diagnóstico Autónomo", "Correlaciona logs, métricas y trazas en tiempo real para identificar causa raíz en segundos."),
    ("🛡️ Seguridad Enterprise", "Aislamiento absoluto de contextos. Cumplimiento SOC2 e ISO 27001. Tus datos nunca se usan para entrenar modelos públicos."),
    ("☁️ Integración Multicloud", "Conexión fluida con AWS, Azure, GCP, Jira, ServiceNow y herramientas de observabilidad estándar."),
    ("📊 Optimización de Costos", "Identifica recursos infrautilizados y sugiere acciones para reducir hasta un 30% la factura cloud."),
    ("🔔 Alertas Inteligentes", "Filtra el ruido y prioriza incidentes críticos con análisis contextual basado en impacto al negocio."),
    ("⚡ Automatización Segura", "Desde modo sugerencia hasta ejecución autónoma en ventanas de tiempo definidas con permisos granulares."),
]

for title, desc in features:
    story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle("f_title", parent=body_style, fontSize=10, textColor=white)))
    story.append(Paragraph(desc, body_style))
    story.append(spacer(2))

story.append(spacer(8))
story.append(hr())

# ─── Casos por Rol ───
story.append(Paragraph("Casos de Uso por Rol", heading_style))

roles = [
    ("Desarrolladores & DevOps", "Generación de pipelines CI/CD seguros, refactorización automatizada, soporte para despliegues complejos sin intervención manual."),
    ("DBAs & Data Engineers", "Optimización de consultas lentas, sugerencias de índices, monitoreo de cuellos de botella en bases de datos."),
    ("Arquitectos de Soluciones", "Validación de arquitectura contra principios de diseño, detección de deuda técnica, generación de diagramas."),
    ("SysAdmins e Infraestructura", "Monitoreo proactivo de servidores, rotación automatizada de certificados, gestión de parches de seguridad."),
    ("Monitoreo & AIOps", "Correlación inteligente de alertas, reducción de falsos positivos, dashboards unificados de salud del sistema."),
    ("Gestión de Activos (SAM)", "Auditorías automatizadas de licencias, detección de software no autorizado, optimización de costos SaaS."),
]

for role, desc in roles:
    story.append(Paragraph(f"<b>{role}:</b> {desc}", body_style))
    story.append(spacer(2))

story.append(PageBreak())

# ─── PÁGINA 3: ROI y CTA ───
story.append(Paragraph("Impacto de Negocio", heading_style))
story.append(spacer(4))

impact_data = [
    [Paragraph("<b>Métrica</b>", ParagraphStyle("ih", parent=body_style, fontSize=9, textColor=PRIMARY_LIGHT)),
     Paragraph("<b>Resultado</b>", ParagraphStyle("ih2", parent=body_style, fontSize=9, textColor=PRIMARY_LIGHT)),
     Paragraph("<b>Descripción</b>", ParagraphStyle("ih3", parent=body_style, fontSize=9, textColor=PRIMARY_LIGHT))],
    [Paragraph("MTTR", body_style), Paragraph("<font color='#22c55e'><b>-40%</b></font>", body_style),
     Paragraph("Reducción del tiempo medio de resolución de incidentes", body_style)],
    [Paragraph("Velocidad de Entrega", body_style), Paragraph("<font color='#22c55e'><b>3x</b></font>", body_style),
     Paragraph("Aceleración en despliegues y resolución de impedimentos", body_style)],
    [Paragraph("Costos Cloud", body_style), Paragraph("<font color='#22c55e'><b>-30%</b></font>", body_style),
     Paragraph("Optimización de recursos y licencias SaaS", body_style)],
    [Paragraph("SLA", body_style), Paragraph("<font color='#22c55e'><b>99.9%</b></font>", body_style),
     Paragraph("Disponibilidad garantizada con respuesta autónoma inmediata", body_style)],
]

t2 = Table(impact_data, colWidths=[doc.width*0.25, doc.width*0.2, doc.width*0.55])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1a1a30")),
    ('BACKGROUND', (0, 1), (-1, -1), BG_CARD),
    ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(t2)

story.append(spacer(20))
story.append(hr())

# ─── Seguridad ───
story.append(Paragraph("Seguridad y Cumplimiento", heading_style))
story.append(Paragraph(
    "• Autonomía con Control Humano: Define permisos específicos de acción para la IA.<br/>"
    "• Seguridad de Nivel Enterprise: Aislamiento absoluto de contextos. Cumplimiento SOC2 e ISO 27001.<br/>"
    "• Integración Multicloud Completa: AWS, Azure, GCP, Jira, ServiceNow y más.<br/>"
    "• Encriptación TLS 1.3 y autenticación OAuth 2.0 con tokens efímeros.",
    body_style
))

story.append(spacer(20))
story.append(hr())

# ─── CTA Final ───
story.append(spacer(10))
story.append(Paragraph(
    "Lleva la eficiencia de tu equipo de TI al siguiente nivel",
    ParagraphStyle("cta_title", parent=title_style, fontSize=18, leading=22)
))
story.append(spacer(6))
story.append(Paragraph(
    "Elimina la fatiga de alertas, asegura el tiempo de actividad y optimiza tus costos en nube "
    "con la primera solución TI autónoma.",
    subtitle_style
))
story.append(spacer(10))

# Botón visual (simulado con tabla)
cta_data = [[Paragraph(
    "<b>SOLICITAR DEMO →</b>",
    ParagraphStyle("cta_btn", parent=body_style, fontSize=11, textColor=white, alignment=TA_CENTER)
)]]
cta_table = Table(cta_data, colWidths=[160])
cta_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
    ('BOX', (0, 0), (-1, -1), 0, PRIMARY),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 20),
    ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ROUNDEDCORNERS', [8, 8, 8, 8]),
]))
story.append(cta_table)

story.append(spacer(8))
story.append(Paragraph("contacto@gulin-ai.com  |  www.gulin-ai.com", footer_style))
story.append(Paragraph("© 2026 GuLIN AI. Todos los derechos reservados.", footer_style))

# ─── Generar PDF ───
doc.build(story, onFirstPage=draw_bg, onLaterPages=lambda c, d: (draw_bg(c, d), draw_page_number(c, d)))
print(f"✅ Brochure PDF generado exitosamente: {output_path}")
