from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, Flowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Wedge
from reportlab.graphics import renderPDF
import os

# ─── Colores ───
PURPLE = "#8b5cf6"
PURPLE_DARK = "#7c3aed"
PURPLE_LIGHT = "#a78bfa"
PINK = "#ec4899"
CYAN = "#06b6d4"
GREEN = "#22c55e"
YELLOW = "#eab308"
ORANGE = "#f97316"
RED = "#ef4444"
BG_DARK = "#0a0a12"
BG_CARD = "#111122"
BG_CARD2 = "#15152a"
TEXT_MAIN = "#e2e8f0"
TEXT_SEC = "#94a3b8"
TEXT_MUTED = "#64748b"
BORDER = "#1e1e3a"
WHITE = "#ffffff"

WIDTH, HEIGHT = A4

# ─── Flowables decorativos ───
class GradientBar(Flowable):
    """Barra de gradiente horizontal"""
    def __init__(self, width, height=3, colors=[PURPLE, PINK]):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.colors = colors

    def draw(self):
        d = Drawing(self.width, self.height)
        steps = 40
        seg_w = self.width / steps
        n = len(self.colors) - 1
        for i in range(steps):
            t = i / steps
            idx = min(int(t * n), n - 1)
            local_t = (t * n) - idx
            c1 = self.colors[idx]
            c2 = self.colors[min(idx + 1, n - 1)]
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            r = int(r1 * (1-local_t) + r2 * local_t)
            g = int(g1 * (1-local_t) + g2 * local_t)
            b = int(b1 * (1-local_t) + b2 * local_t)
            d.add(Rect(i*seg_w, 0, seg_w+1, self.height,
                       fillColor=HexColor(f"#{r:02x}{g:02x}{b:02x}"), strokeColor=None))
        renderPDF.draw(d, self.canv, 0, 0)

class MetricCircle(Flowable):
    """Círculo con métrica"""
    def __init__(self, size, number, label, color=PURPLE):
        Flowable.__init__(self)
        self.size = size
        self.number = number
        self.label = label
        self.color = color

    def draw(self):
        d = Drawing(self.size, self.size + 20)
        cx, cy = self.size/2, self.size/2 + 10
        # Círculo exterior
        d.add(Circle(cx, cy, self.size/2 - 2,
                     fillColor=HexColor(BG_CARD2),
                     strokeColor=HexColor(self.color),
                     strokeWidth=2))
        # Número
        from reportlab.graphics.charts.textlabels import Label
        num_label = Label()
        num_label.setOrigin(cx, cy + 4)
        num_label.setText(self.number)
        num_label.fontName = 'Helvetica-Bold'
        num_label.fontSize = self.size * 0.28
        num_label.fillColor = HexColor(self.color)
        num_label.textAnchor = 'middle'
        d.add(num_label)
        # Label debajo
        txt_label = Label()
        txt_label.setOrigin(cx, cy - self.size/2 + 2)
        txt_label.setText(self.label)
        txt_label.fontName = 'Helvetica'
        txt_label.fontSize = 7
        txt_label.fillColor = HexColor(TEXT_SEC)
        txt_label.textAnchor = 'middle'
        d.add(txt_label)
        renderPDF.draw(d, self.canv, 0, 0)

class IconBox(Flowable):
    """Caja con icono y texto"""
    def __init__(self, width, height, icon, title, desc, color=PURPLE):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.icon = icon
        self.title = title
        self.desc = desc
        self.color = color

    def draw(self):
        d = Drawing(self.width, self.height)
        # Fondo
        d.add(Rect(0, 0, self.width, self.height,
                   fillColor=HexColor(BG_CARD2),
                   strokeColor=HexColor(BORDER),
                   strokeWidth=0.5,
                   rx=6, ry=6))
        # Círculo icono
        d.add(Circle(18, self.height - 18, 10,
                     fillColor=HexColor(f"{self.color}20"),
                     strokeColor=HexColor(self.color),
                     strokeWidth=1))
        # Icono (texto)
        icon_label = self._make_label(self.icon, 18, self.height - 18, 9, WHITE)
        d.add(icon_label)
        # Título
        title_label = self._make_label(self.title, 36, self.height - 14, 8, WHITE, 'Helvetica-Bold')
        d.add(title_label)
        # Descripción
        desc_label = self._make_label(self.desc, 10, self.height - 36, 6.5, TEXT_SEC)
        d.add(desc_label)
        renderPDF.draw(d, self.canv, 0, 0)

    def _make_label(self, text, x, y, size, color, font='Helvetica'):
        from reportlab.graphics.charts.textlabels import Label
        l = Label()
        l.setOrigin(x, y)
        l.setText(text)
        l.fontName = font
        l.fontSize = size
        l.fillColor = HexColor(color)
        return l

def draw_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(HexColor(BG_DARK))
    canvas.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    # Barra superior
    canvas.setStrokeColor(HexColor(f"{PURPLE}40"))
    canvas.setLineWidth(0.5)
    canvas.line(0, HEIGHT - 1, WIDTH, HEIGHT - 1)
    canvas.restoreState()

def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(HexColor(TEXT_MUTED))
    canvas.drawCentredString(WIDTH / 2, 12, f"GuLIN AI — Brochure Corporativo — Pág. {doc.page}")
    canvas.restoreState()

def spacer(h=6):
    return Spacer(1, h)

def gradient_hr():
    return GradientBar(WIDTH - 40*mm, 2, [PURPLE, PINK, CYAN])

def make_table(data, col_widths, style_list=None):
    t = Table(data, colWidths=col_widths)
    base_style = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    if style_list:
        base_style.extend(style_list)
    t.setStyle(TableStyle(base_style))
    return t

# ─── Estilos de texto ───
styles = getSampleStyleSheet()

s_title = ParagraphStyle("T1", parent=styles["Title"], fontSize=30, leading=36,
                         textColor=HexColor(WHITE), fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
s_subtitle = ParagraphStyle("T2", parent=styles["Normal"], fontSize=14, leading=19,
                            textColor=HexColor(TEXT_SEC), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=12)
s_heading = ParagraphStyle("H1", parent=styles["Heading2"], fontSize=20, leading=24,
                           textColor=HexColor(PURPLE_LIGHT), fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=8)
s_subheading = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14, leading=18,
                              textColor=HexColor(WHITE), fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=6)
s_body = ParagraphStyle("B1", parent=styles["Normal"], fontSize=9.5, leading=14,
                        textColor=HexColor(TEXT_SEC), fontName="Helvetica", alignment=TA_JUSTIFY, spaceAfter=6)
s_body_small = ParagraphStyle("B2", parent=s_body, fontSize=8.5, leading=12)
s_bullet = ParagraphStyle("BL", parent=s_body, fontSize=9, leading=13,
                          leftIndent=14, bulletIndent=0, spaceAfter=3)
s_footer = ParagraphStyle("F1", parent=styles["Normal"], fontSize=7, leading=9,
                          textColor=HexColor(TEXT_MUTED), fontName="Helvetica", alignment=TA_CENTER)
s_cta = ParagraphStyle("CTA", parent=s_body, fontSize=12, leading=16,
                       textColor=HexColor(WHITE), fontName="Helvetica-Bold", alignment=TA_CENTER)

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", s_bullet)

# ─── Construcción ───
output_path = os.path.join(os.path.dirname(__file__), "brochure_gulin.pdf")
logo_path = os.path.join(os.path.dirname(__file__), "GULIN_LOGO_3.jpeg")

doc = SimpleDocTemplate(output_path, pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=16*mm, bottomMargin=20*mm,
    title="Brochure GuLIN AI - Agente Inteligente de TI",
    author="GuLIN AI")

story = []

# ============================================================
# PÁGINA 1 - PORTADA
# ============================================================
story.append(spacer(40))

# Logo
if os.path.exists(logo_path):
    im = Image(logo_path, width=65*mm, height=65*mm)
    story.append(im)

story.append(spacer(6))
story.append(Paragraph("GuLIN <font color='#8b5cf6'>IA</font>", s_title))
story.append(Paragraph("Agente Inteligente Autónomo para TI Empresarial", s_subtitle))
story.append(spacer(4))
story.append(gradient_hr())
story.append(spacer(6))

story.append(Paragraph(
    "Detecta, diagnostica y mitiga incidentes de infraestructura<br/>"
    "<b>antes de que afecten a tus clientes</b>",
    ParagraphStyle("PD", parent=s_body, fontSize=12, leading=17,
                   textColor=HexColor(TEXT_SEC), alignment=TA_CENTER)
))
story.append(spacer(20))

# ─── Métricas circulares ───
metric_row = []
metrics = [
    ("-40%", "MTTR", PURPLE),
    ("3x", "Velocidad", PINK),
    ("$50K+", "Ahorro/año", CYAN),
    ("99.9%", "SLA", GREEN),
]
for num, label, color in metrics:
    metric_row.append(MetricCircle(50, num, label, color))

metric_table = Table([metric_row], colWidths=[(WIDTH-40*mm)/4]*4)
metric_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(metric_table)

story.append(spacer(20))

# ─── Caja de valor ───
value_data = [[
    Paragraph(
        "<b>⚡ Automatización Inteligente 24/7</b><br/>"
        "Correlaciona logs, métricas y trazas en tiempo real.<br/>"
        "<b>🛡️ Seguridad Enterprise</b> — SOC2, ISO 27001<br/>"
        "<b>☁️ Multicloud</b> — AWS, Azure, GCP, Jira, ServiceNow",
        ParagraphStyle("VB", parent=s_body, fontSize=9.5, leading=15, textColor=HexColor(TEXT_SEC))
    )
]]
vt = Table(value_data, colWidths=[WIDTH - 40*mm])
vt.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), HexColor(BG_CARD2)),
    ('BOX', (0, 0), (-1, -1), 0.5, HexColor(f"{PURPLE}40")),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 14),
    ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ('ROUNDEDCORNERS', [8, 8, 8, 8]),
]))
story.append(vt)

story.append(spacer(25))

# Contacto
contact = [[
    Paragraph("contacto@gulin-ai.com  |  www.gulin-ai.com",
              ParagraphStyle("CT", parent=s_body, fontSize=8, textColor=HexColor(TEXT_MUTED), alignment=TA_CENTER))
]]
ct = Table(contact, colWidths=[WIDTH - 40*mm])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), HexColor(BG_CARD)),
    ('BOX', (0, 0), (-1, -1), 0.5, HexColor(BORDER)),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROUNDEDCORNERS', [6, 6, 6, 6]),
]))
story.append(ct)

story.append(PageBreak())

# ============================================================
# PÁGINA 2 - PROBLEMA + SOLUCIÓN + CARACTERÍSTICAS
# ============================================================
story.append(Paragraph("⚡ El Problema que Resolvemos", s_heading))
story.append(Paragraph(
    "Las operaciones tradicionales de TI están al límite. Los ingenieros pasan el <b>60% de su tiempo</b> "
    "respondiendo a falsas alertas y apagando fuegos manualmente en lugar de construir valor para el producto.",
    s_body
))
story.append(spacer(4))

# Problemas en cards visuales
problems = [
    ("🔔", "Fatiga por Alertas", "Miles de notificaciones confusas al día. Imposible identificar qué es crítico."),
    ("⏱️", "MTTR Elevado", "Horas de análisis de logs y llamadas de emergencia a las 3 a.m."),
    ("☁️", "Costos Cloud", "Recursos sobre-dimensionados y licencias SaaS inactivas."),
]

prob_data = []
for icon, title, desc in problems:
    prob_data.append([
        Paragraph(f"<font size='14'>{icon}</font>", ParagraphStyle("PI", parent=s_body, alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b>", ParagraphStyle("PT", parent=s_body, fontSize=10, textColor=HexColor(WHITE))),
        Paragraph(desc, ParagraphStyle("PD2", parent=s_body, fontSize=8.5, leading=12, textColor=HexColor(TEXT_SEC))),
    ])

pt = Table(prob_data, colWidths=[20, (WIDTH-40*mm)*0.3, (WIDTH-40*mm)*0.55])
pt.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), HexColor(BG_CARD2)),
    ('BOX', (0, 0), (-1, -1), 0.5, HexColor(BORDER)),
    ('INNERGRID', (0, 0), (-1, -1), 0.3, HexColor(BORDER)),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('ROUNDEDCORNERS', [6, 6, 6, 6]),
]))
story.append(pt)

story.append(spacer(10))
story.append(gradient_hr())
story.append(spacer(6))

# ─── Solución ───
story.append(Paragraph("💡 Nuestra Solución", s_heading))
story.append(Paragraph(
    "GuLIN es el <b>primer agente inteligente autónomo de TI</b> para empresas. Se integra de forma segura en tu stack "
    "tecnológico para diagnosticar anomalías, predecir problemas de infraestructura y mitigar incidentes "
    "de forma totalmente autónoma, <b>24/7</b>.",
    s_body
))
story.append(spacer(6))

# ─── Características Clave ───
story.append(Paragraph("🚀 Características Clave", s_heading))

features = [
    ("🤖", "Diagnóstico Autónomo", "Correlaciona logs, métricas y trazas en tiempo real. Identifica causa raíz en segundos."),
    ("🛡️", "Seguridad Enterprise", "Aislamiento absoluto. SOC2, ISO 27001. Tus datos nunca se usan para entrenar modelos públicos."),
    ("☁️", "Multicloud", "AWS, Azure, GCP, Jira, ServiceNow. Conexión mediante APIs seguras OAuth 2.0."),
    ("📊", "Optimización Costos", "Identifica recursos infrautilizados. Reduce hasta un 30% la factura cloud."),
    ("🔔", "Alertas Inteligentes", "Filtra ruido y prioriza incidentes críticos con análisis contextual de impacto al negocio."),
    ("⚡", "Automatización Segura", "Desde modo sugerencia hasta ejecución autónoma con permisos granulares."),
]

feat_data = []
for icon, title, desc in features:
    feat_data.append([
        Paragraph(f"<font size='12'>{icon}</font>", ParagraphStyle("FI", parent=s_body, alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b>", ParagraphStyle("FT", parent=s_body, fontSize=10, textColor=HexColor(WHITE))),
        Paragraph(desc, ParagraphStyle("FD", parent=s_body, fontSize=8, leading=11, textColor=HexColor(TEXT_SEC))),
    ])

# Grid 2 columnas
feat_table_data = []
row = []
for i, f in enumerate(feat_data):
    inner = Table([f], colWidths=[18, (WIDTH-40*mm)/2 - 30, (WIDTH-40*mm)/2 - 18])
    inner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(BG_CARD2)),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor(BORDER)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    row.append(inner)
    if len(row) == 2 or i == len(features) - 1:
        while len(row) < 2:
            row.append(Paragraph("", s_body))
        feat_table_data.append(row)
        row = []

ft = Table(feat_table_data, colWidths=[(WIDTH-40*mm)/2]*2)
ft.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(ft)

story.append(spacer(8))
story.append(gradient_hr())
story.append(spacer(4))

# ─── Casos por Rol ───
story.append(Paragraph("👥 Casos de Uso por Rol", s_heading))

roles = [
    ("👨‍💻", "DevOps", "Pipelines CI/CD seguros, refactorización automatizada, despliegues sin intervención manual."),
    ("🗄️", "DBAs", "Optimización de queries lentas, sugerencias de índices, monitoreo de cuellos de botella."),
    ("🏗️", "Arquitectos", "Validación de arquitectura, detección de deuda técnica, generación de diagramas."),
    ("🖥️", "SysAdmins", "Monitoreo proactivo, rotación de certificados, gestión de parches de seguridad."),
    ("📈", "AIOps", "Correlación de alertas, reducción de falsos positivos, dashboards unificados."),
    ("🏷️", "SAM", "Auditorías de licencias, detección de software no autorizado, optimización SaaS."),
]

roles_data = []
for icon, title, desc in roles:
    roles_data.append([
        Paragraph(f"<font size='10'>{icon}</font>", ParagraphStyle("RI", parent=s_body, alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b>", ParagraphStyle("RT", parent=s_body, fontSize=9, textColor=HexColor(WHITE))),
        Paragraph(desc, ParagraphStyle("RD", parent=s_body, fontSize=7.5, leading=10, textColor=HexColor(TEXT_SEC))),
    ])

roles_table_data = []
row = []
for i, r in enumerate(roles_data):
    inner = Table([r], colWidths=[16, (WIDTH-40*mm)/2 - 28, (WIDTH-40*mm)/2 - 16])
    inner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(BG_CARD2)),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor(BORDER)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    row.append(inner)
    if len(row) == 2 or i == len(roles) - 1:
        while len(row) < 2:
            row.append(Paragraph("", s_body))
        roles_table_data.append(row)
        row = []

rt = Table(roles_table_data, colWidths=[(WIDTH-40*mm)/2]*2)
rt.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(rt)

story.append(PageBreak())

# ============================================================
# PÁGINA 3 - IMPACTO + SEGURIDAD + CTA
# ============================================================
story.append(Paragraph("📈 Impacto de Negocio", s_heading))
story.append(spacer(4))

# Tabla de impacto
impact_data = [
    [Paragraph("<b>Métrica</b>", ParagraphStyle("IH", parent=s_body, fontSize=9, textColor=HexColor(PURPLE_LIGHT))),
     Paragraph("<b>Resultado</b>", ParagraphStyle("IH2", parent=s_body, fontSize=9, textColor=HexColor(PURPLE_LIGHT))),
     Paragraph("<b>Descripción</b>", ParagraphStyle("IH3", parent=s_body, fontSize=9, textColor=HexColor(PURPLE_LIGHT)))],
    [Paragraph("MTTR", s_body_small),
     Paragraph(f"<font color='{GREEN}'><b>-40%</b></font>", s_body_small),
     Paragraph("Reducción del tiempo medio de resolución de incidentes críticos", s_body_small)],
    [Paragraph("Velocidad Entrega", s_body_small),
     Paragraph(f"<font color='{GREEN}'><b>3x</b></font>", s_body_small),
     Paragraph("Aceleración en despliegues y resolución de impedimentos", s_body_small)],
    [Paragraph("Costos Cloud", s_body_small),
     Paragraph(f"<font color='{GREEN}'><b>-30%</b></font>", s_body_small),
     Paragraph("Optimización de recursos y licencias SaaS", s_body_small)],
    [Paragraph("Disponibilidad SLA", s_body_small),
     Paragraph(f"<font color='{GREEN}'><b>99.9%</b></font>", s_body_small),
     Paragraph("Disponibilidad garantizada con respuesta autónoma inmediata", s_body_small)],
    [Paragraph("Productividad", s_body_small),
     Paragraph(f"<font color='{GREEN}'><b>+60%</b></font>", s_body_small),
     Paragraph("Más tiempo para construir valor en lugar de apagar fuegos", s_body_small)],
    [Paragraph("ROI Inversión", s_body_small),
     Paragraph(f"<font color='{GREEN}'><b>5x</b></font>", s_body_small),
     Paragraph("Retorno sobre la inversión en el primer año de implementación", s_body_small)],
]

it = Table(impact_data, colWidths=[doc.width*0.25, doc.width*0.17, doc.width*0.58])
it.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1a1a30")),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor(BG_CARD)),
    ('BOX', (0, 0), (-1, -1), 0.5, HexColor(BORDER)),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor(BORDER)),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('ROUNDEDCORNERS', [6, 6, 6, 6]),
]))
story.append(it)

story.append(spacer(14))
story.append(gradient_hr())
story.append(spacer(6))

# ─── Seguridad ───
story.append(Paragraph("🔒 Seguridad y Cumplimiento", s_heading))

sec_items = [
    ("🔐", "Control Humano", "Define permisos específicos. Desde sugerencias hasta ejecución automatizada."),
    ("🛡️", "Nivel Enterprise", "Aislamiento absoluto. SOC2, ISO 27001. Datos nunca usados para entrenar modelos."),
    ("🔗", "Integración Segura", "APIs OAuth 2.0 con tokens efímeros. AWS, Azure, GCP, Jira, ServiceNow."),
    ("🔒", "Encriptación Total", "Tráfico TLS 1.3. Revocación de acceso en cualquier momento."),
]

sec_data = []
for icon, title, desc in sec_items:
    sec_data.append([
        Paragraph(f"<font size='10'>{icon}</font>", ParagraphStyle("SI", parent=s_body, alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b>", ParagraphStyle("ST", parent=s_body, fontSize=9, textColor=HexColor(WHITE))),
        Paragraph(desc, ParagraphStyle("SD", parent=s_body, fontSize=7.5, leading=10, textColor=HexColor(TEXT_SEC))),
    ])

sec_table_data = []
row = []
for i, s in enumerate(sec_data):
    inner = Table([s], colWidths=[16, (WIDTH-40*mm)/2 - 28, (WIDTH-40*mm)/2 - 16])
    inner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(BG_CARD2)),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor(BORDER)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    row.append(inner)
    if len(row) == 2 or i == len(sec_items) - 1:
        while len(row) < 2:
            row.append(Paragraph("", s_body))
        sec_table_data.append(row)
        row = []

st2 = Table(sec_table_data, colWidths=[(WIDTH-40*mm)/2]*2)
st2.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(st2)

story.append(spacer(18))
story.append(gradient_hr())
story.append(spacer(8))

# ─── CTA Final ───
story.append(Paragraph(
    "Lleva la eficiencia de tu equipo de TI al siguiente nivel",
    ParagraphStyle("CTA_TITLE", parent=s_title, fontSize=20, leading=24)
))
story.append(spacer(4))
story.append(Paragraph(
    "Elimina la fatiga de alertas, asegura el tiempo de actividad y optimiza tus costos en nube "
    "con la primera solución TI autónoma.",
    s_subtitle
))
story.append(spacer(10))

# Botón CTA
cta_data = [[Paragraph("<b>SOLICITAR DEMO →</b>", s_cta)]]
cta_table = Table(cta_data, colWidths=[200])
cta_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), HexColor(PURPLE)),
    ('BOX', (0, 0), (-1, -1), 0, HexColor(PURPLE)),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('LEFTPADDING', (0, 0), (-1, -1), 28),
    ('RIGHTPADDING', (0, 0), (-1, -1), 28),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ROUNDEDCORNERS', [8, 8, 8, 8]),
]))
story.append(cta_table)

story.append(spacer(10))
story.append(Paragraph("contacto@gulin-ai.com  |  www.gulin-ai.com", s_footer))
story.append(Paragraph("© 2026 GuLIN AI. Todos los derechos reservados.", s_footer))

# ─── Generar PDF ───
doc.build(story, onFirstPage=draw_bg, onLaterPages=lambda c, d: (draw_bg(c, d), draw_page_number(c, d)))
print(f"✅ Brochure PDF generado exitosamente: {output_path}")
