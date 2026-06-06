from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
from reportlab.graphics import renderPDF
import os, math

# ─── Colores corporativos ───
PRIMARY = HexColor("#8b5cf6")
PRIMARY_DARK = HexColor("#7c3aed")
PRIMARY_LIGHT = HexColor("#a78bfa")
BG_DARK = HexColor("#0a0a12")
BG_CARD = HexColor("#111122")
BG_CARD2 = HexColor("#15152a")
TEXT_MAIN = HexColor("#e2e8f0")
TEXT_SEC = HexColor("#94a3b8")
TEXT_MUTED = HexColor("#64748b")
BORDER = HexColor("#1e1e3a")
GREEN = HexColor("#22c55e")
YELLOW = HexColor("#eab308")
RED = HexColor("#ef4444")
GRADIENT_TOP = HexColor("#0d0d1a")
GRADIENT_BOT = HexColor("#0a0a12")

WIDTH, HEIGHT = A4

# ─── Estilos ───
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "BrochureTitle", parent=styles["Title"],
    fontSize=28, leading=34, textColor=white,
    fontName="Helvetica-Bold", alignment=TA_CENTER,
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    "BrochureSubtitle", parent=styles["Normal"],
    fontSize=13, leading=18, textColor=TEXT_SEC,
    fontName="Helvetica", alignment=TA_CENTER,
    spaceAfter=16
)

heading_style = ParagraphStyle(
    "BrochureHeading", parent=styles["Heading2"],
    fontSize=18, leading=22, textColor=PRIMARY_LIGHT,
    fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=8,
    alignment=TA_LEFT
)

heading2_style = ParagraphStyle(
    "BrochureHeading2", parent=styles["Heading2"],
    fontSize=14, leading=18, textColor=white,
    fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=6,
    alignment=TA_LEFT
)

body_style = ParagraphStyle(
    "BrochureBody", parent=styles["Normal"],
    fontSize=9.5, leading=14, textColor=TEXT_SEC,
    fontName="Helvetica", alignment=TA_JUSTIFY,
    spaceAfter=6
)

body_small = ParagraphStyle(
    "BodySmall", parent=body_style,
    fontSize=8.5, leading=12, textColor=TEXT_SEC
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

footer_style = ParagraphStyle(
    "Footer", parent=styles["Normal"],
    fontSize=7, leading=9, textColor=TEXT_MUTED,
    fontName="Helvetica", alignment=TA_CENTER
)

cta_style = ParagraphStyle(
    "CTA", parent=body_style,
    fontSize=11, leading=15, textColor=white,
    fontName="Helvetica-Bold", alignment=TA_CENTER
)

# ─── Decoraciones ───
class GradientRect(Flowable):
    """Rectángulo con gradiente vertical"""
    def __init__(self, width, height, color1, color2):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2

    def draw(self):
        d = Drawing(self.width, self.height)
        steps = 20
        for i in range(steps):
            y = self.height * i / steps
            h = self.height / steps + 1
            r, g, b = self._lerp_color(self.color1, self.color2, i/steps)
            d.add(Rect(0, y, self.width, h, fillColor=HexColor(f"#{r:02x}{g:02x}{b:02x}"), strokeColor=None))
        renderPDF.draw(d, self.canv, 0, 0)

    def _lerp_color(self, c1, c2, t):
        r = int(c1.red * 255 * (1-t) + c2.red * 255 * t)
        g = int(c1.green * 255 * (1-t) + c2.green * 255 * t)
        b = int(c1.blue * 255 * (1-t) + c2.blue * 255 * t)
        return r, g, b

class AccentLine(Flowable):
    """Línea decorativa con gradiente"""
    def __init__(self, width, height=2):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        d = Drawing(self.width, self.height)
        steps = 30
        seg_w = self.width / steps
        for i in range(steps):
            t = i / steps
            r = int(139 * (1-t) + 99 * t)
            g = int(92 * (1-t) + 102 * t)
            b = int(246 * (1-t) + 241 * t)
            d.add(Rect(i*seg_w, 0, seg_w+1, self.height,
                       fillColor=HexColor(f"#{r:02x}{g:02x}{b:02x}"), strokeColor=None))
        renderPDF.draw(d, self.canv, 0, 0)

def draw_bg(canvas, doc):
    """Fondo oscuro con detalles"""
    canvas.saveState()
    # Fondo principal
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    # Línea superior sutil
    canvas.setStrokeColor(HexColor("#8b5cf640"))
    canvas.setLineWidth(0.5)
    canvas.line(0, HEIGHT - 1, WIDTH, HEIGHT - 1)
    # Esquinas decorativas
    canvas.setStrokeColor(HexColor("#8b5cf620"))
    canvas.setLineWidth(0.3)
    # Esquina superior derecha
    canvas.line(WIDTH - 30, HEIGHT - 10, WIDTH - 10, HEIGHT - 10)
    canvas.line(WIDTH - 10, HEIGHT - 30, WIDTH - 10, HEIGHT - 10)
    # Esquina inferior izquierda
    canvas.line(10, 10, 30, 10)
    canvas.line(10, 10, 10, 30)
    canvas.restoreState()

def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawCentredString(WIDTH / 2, 12, f"GuLIN AI — Brochure Corporativo — Pág. {doc.page}")
    canvas.restoreState()

def spacer(h=6):
    return Spacer(1, h)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=10, spaceBefore=10)

def accent_hr():
    return AccentLine(WIDTH - 40*mm, 2)

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", bullet_style)

def card_table(title, items, cols=2):
    """Crea una tabla tipo card con título y items"""
    data = []
    row = []
    for i, (t, d) in enumerate(items):
        cell = [
            [Paragraph(f"<b>{t}</b>", ParagraphStyle("ct", parent=body_style, fontSize=10, textColor=white))],
            [Paragraph(d, ParagraphStyle("cd", parent=body_style, fontSize=8, leading=11, textColor=TEXT_SEC))]
        ]
        inner = Table(cell, colWidths=[(WIDTH - 40*mm) / cols - 8])
        inner.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), BG_CARD2),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        row.append(inner)
        if len(row) == cols or i == len(items) - 1:
            while len(row) < cols:
                row.append(Paragraph("", body_style))
            data.append(row)
            row = []
    t = Table(data, colWidths=[(WIDTH - 40*mm) / cols] * cols)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t

# ─── Construcción del PDF ───
output_path = os.path.join(os.path.dirname(__file__), "brochure_gulin.pdf")
logo_path = os.path.join(os.path.dirname(__file__), "GULIN_LOGO_3.jpeg")

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=20*mm,
    rightMargin=20*mm,
    topMargin=16*mm,
    bottomMargin=20*mm,
    title="Brochure GuLIN AI - Agente Inteligente de TI",
    author="GuLIN AI"
)

story = []

# ============================================================
# PÁGINA 1 - PORTADA
# ============================================================
story.append(spacer(50))

# Logo
if os.path.exists(logo_path):
    im = Image(logo_path, width=60*mm, height=60*mm)
    story.append(im)

story.append(spacer(8))
story.append(Paragraph("GuLIN <font color='#8b5cf6'>IA</font>", title_style))
story.append(Paragraph("Agente Inteligente Autónomo para TI Empresarial", subtitle_style))
story.append(spacer(6))
story.append(accent_hr())
story.append(spacer(8))

story.append(Paragraph(
    "Detecta, diagnostica y mitiga incidentes de infraestructura<br/>antes de que afecten a tus clientes.",
    ParagraphStyle("PortadaDesc", parent=body_style, fontSize=12, leading=17,
                   textColor=TEXT_SEC, alignment=TA_CENTER)
))
story.append(spacer(25))

# ─── Highlights mejorados ───
highlight_items = [
    ("-40%", "Reducción MTTR", "en tiempo de resolución de incidentes"),
    ("3x", "Velocidad Entrega", "mayor velocidad de deploy"),
    ("$50K+", "Ahorro Anual", "en optimización de costos cloud"),
]

h_data = []
for num, label, desc in highlight_items:
    h_data.append([
        Paragraph(f"<font color='#8b5cf6' size='22'><b>{num}</b></font>",
                  ParagraphStyle("hn", parent=body_style, alignment=TA_CENTER)),
        Paragraph(f"<b>{label}</b>",
                  ParagraphStyle("hl", parent=body_style, fontSize=10, textColor=white, alignment=TA_CENTER)),
        Paragraph(desc,
                  ParagraphStyle("hd", parent=body_style, fontSize=7.5, alignment=TA_CENTER)),
    ])

ht = Table(h_data, colWidths=[(WIDTH - 40*mm)/3]*3)
ht.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
    ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('ROUNDEDCORNERS', [6, 6, 6, 6]),
]))
story.append(ht)

story.append(spacer(30))

# ─── Info de contacto en portada ───
contact_data = [[
    Paragraph("contacto@gulin-ai.com", ParagraphStyle("c1", parent=body_style, fontSize=8, textColor=TEXT_MUTED, alignment=TA_CENTER)),
]]
ct = Table(contact_data, colWidths=[WIDTH - 40*mm])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
    ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(ct)

story.append(PageBreak())

# ============================================================
# PÁGINA 2 - PROBLEMA + SOLUCIÓN + CARACTERÍSTICAS
# ============================================================
story.append(Paragraph("El Problema", heading_style))
story.append(Paragraph(
    "Las operaciones tradicionales de TI están al límite. Los ingenieros pasan el <b>60% de su tiempo</b> "
    "respondiendo a falsas alertas y apagando fuegos manualmente en lugar de construir valor para el producto.",
    body_style
))
story.append(spacer(4))

# Cards de problemas
problem_items = [
    ("🔔 Fatiga extrema por Alertas",
     "Miles de notificaciones confusas al día. Imposible identificar qué es crítico antes de una caída."),
    ("⏱️ Resolución Lenta (MTTR Elevado)",
     "Horas de análisis de logs, llamadas de emergencia a las 3 a.m. y costosos tiempos muertos."),
    ("☁️ Desperdicio y Costes Cloud",
     "Recursos sobre-dimensionados y licencias SaaS inactivas por falta de previsión inteligente."),
]
story.append(card_table("Problemas", problem_items, cols=1))

story.append(spacer(8))
story.append(accent_hr())
story.append(spacer(4))

story.append(Paragraph("La Solución", heading_style))
story.append(Paragraph(
    "GuLIN es el <b>primer agente inteligente autónomo de TI</b> para empresas. Se integra de forma segura en tu stack "
    "tecnológico para diagnosticar anomalías, predecir problemas de infraestructura y mitigar incidentes "
    "de forma totalmente autónoma, <b>24/7</b>.",
    body_style
))
story.append(spacer(4))

# Caja de solución destacada
sol_data = [[
    Paragraph(
        "<b>⚡ Automatización Inteligente:</b> Correlaciona logs, métricas y trazas en tiempo real.<br/>"
        "<b>🛡️ Seguridad Enterprise:</b> Aislamiento absoluto. SOC2 e ISO 27001.<br/>"
        "<b>☁️ Multicloud:</b> AWS, Azure, GCP, Jira, ServiceNow.",
        ParagraphStyle("sol_text", parent=body_style, fontSize=9, leading=14, textColor=TEXT_SEC)
    )
]]
st = Table(sol_data, colWidths=[WIDTH - 40*mm])
st.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), BG_CARD2),
    ('BOX', (0, 0), (-1, -1), 0.5, HexColor("#8b5cf640")),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ('ROUNDEDCORNERS', [6, 6, 6, 6]),
]))
story.append(st)

story.append(spacer(10))
story.append(accent_hr())
story.append(spacer(4))

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
story.append(card_table("Características", features, cols=2))

story.append(spacer(8))
story.append(accent_hr())
story.append(spacer(4))

# ─── Casos por Rol ───
story.append(Paragraph("Casos de Uso por Rol", heading_style))

roles = [
    ("👨‍💻 Desarrolladores & DevOps", "Generación de pipelines CI/CD seguros, refactorización automatizada, soporte para despliegues complejos sin intervención manual."),
    ("🗄️ DBAs & Data Engineers", "Optimización de consultas lentas, sugerencias de índices, monitoreo de cuellos de botella en bases de datos."),
    ("🏗️ Arquitectos de Soluciones", "Validación de arquitectura contra principios de diseño, detección de deuda técnica, generación de diagramas."),
    ("🖥️ SysAdmins e Infraestructura", "Monitoreo proactivo de servidores, rotación automatizada de certificados, gestión de parches de seguridad."),
    ("📈 Monitoreo & AIOps", "Correlación inteligente de alertas, reducción de falsos positivos, dashboards unificados de salud del sistema."),
    ("🏷️ Gestión de Activos (SAM)", "Auditorías automatizadas de licencias, detección de software no autorizado, optimización de costos SaaS."),
]
story.append(card_table("Roles", roles, cols=2))

story.append(PageBreak())

# ============================================================
# PÁGINA 3 - IMPACTO + SEGURIDAD + CTA
# ============================================================
story.append(Paragraph("Impacto de Negocio", heading_style))
story.append(spacer(4))

# Tabla de impacto mejorada
impact_data = [
    [Paragraph("<b>Métrica</b>", ParagraphStyle("ih", parent=body_style, fontSize=9, textColor=PRIMARY_LIGHT)),
     Paragraph("<b>Resultado</b>", ParagraphStyle("ih2", parent=body_style, fontSize=9, textColor=PRIMARY_LIGHT)),
     Paragraph("<b>Descripción</b>", ParagraphStyle("ih3", parent=body_style, fontSize=9, textColor=PRIMARY_LIGHT))],
    [Paragraph("MTTR (Tiempo de Resolución)", body_small),
     Paragraph("<font color='#22c55e'><b>-40%</b></font>", body_small),
     Paragraph("Reducción del tiempo medio de resolución de incidentes críticos", body_small)],
    [Paragraph("Velocidad de Entrega", body_small),
     Paragraph("<font color='#22c55e'><b>3x</b></font>", body_small),
     Paragraph("Aceleración en despliegues y resolución de impedimentos", body_small)],
    [Paragraph("Costos Cloud", body_small),
     Paragraph("<font color='#22c55e'><b>-30%</b></font>", body_small),
     Paragraph("Optimización de recursos y licencias SaaS", body_small)],
    [Paragraph("Disponibilidad (SLA)", body_small),
     Paragraph("<font color='#22c55e'><b>99.9%</b></font>", body_small),
     Paragraph("Disponibilidad garantizada con respuesta autónoma inmediata", body_small)],
    [Paragraph("Productividad Equipo", body_small),
     Paragraph("<font color='#22c55e'><b>+60%</b></font>", body_small),
     Paragraph("Más tiempo para construir valor en lugar de apagar fuegos", body_small)],
]

t2 = Table(impact_data, colWidths=[doc.width*0.28, doc.width*0.17, doc.width*0.55])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1a1a30")),
    ('BACKGROUND', (0, 1), (-1, -1), BG_CARD),
    ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('ROUNDEDCORNERS', [6, 6, 6, 6]),
]))
story.append(t2)

story.append(spacer(16))
story.append(accent_hr())
story.append(spacer(8))

# ─── Seguridad ───
story.append(Paragraph("Seguridad y Cumplimiento", heading_style))

sec_items = [
    ("🔐 Autonomía con Control Humano", "Define permisos específicos de acción para la IA. Desde sugerencias hasta ejecución automatizada en entornos no críticos."),
    ("🛡️ Seguridad Nivel Enterprise", "Aislamiento absoluto de contextos. Cumplimiento SOC2 e ISO 27001. Tus datos nunca se usan para entrenar modelos públicos."),
    ("🔗 Integración Multicloud", "AWS, Azure, GCP, Jira, ServiceNow y más. Conexión mediante APIs seguras con autenticación OAuth 2.0 y tokens efímeros."),
    ("🔒 Encriptación Total", "Todo el tráfico encriptado TLS 1.3. Puedes revocar el acceso en cualquier momento desde nuestro panel de control."),
]
story.append(card_table("Seguridad", sec_items, cols=2))

story.append(spacer(20))
story.append(accent_hr())
story.append(spacer(10))

# ─── CTA Final ───
story.append(Paragraph(
    "Lleva la eficiencia de tu equipo de TI al siguiente nivel",
    ParagraphStyle("cta_title", parent=title_style, fontSize=20, leading=24)
))
story.append(spacer(4))
story.append(Paragraph(
    "Elimina la fatiga de alertas, asegura el tiempo de actividad y optimiza tus costos en nube "
    "con la primera solución TI autónoma.",
    subtitle_style
))
story.append(spacer(12))

# Botón CTA
cta_data = [[Paragraph("<b>SOLICITAR DEMO →</b>", cta_style)]]
cta_table = Table(cta_data, colWidths=[180])
cta_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
    ('BOX', (0, 0), (-1, -1), 0, PRIMARY),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('LEFTPADDING', (0, 0), (-1, -1), 24),
    ('RIGHTPADDING', (0, 0), (-1, -1), 24),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ROUNDEDCORNERS', [8, 8, 8, 8]),
]))
story.append(cta_table)

story.append(spacer(12))
story.append(Paragraph("contacto@gulin-ai.com  |  www.gulin-ai.com", footer_style))
story.append(Paragraph("© 2026 GuLIN AI. Todos los derechos reservados.", footer_style))

# ─── Generar PDF ───
doc.build(story, onFirstPage=draw_bg, onLaterPages=lambda c, d: (draw_bg(c, d), draw_page_number(c, d)))
print(f"✅ Brochure PDF generado exitosamente: {output_path}")
