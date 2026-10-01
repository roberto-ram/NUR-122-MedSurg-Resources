"""Generate the corrected, quality-checked electrolyte relationship table.

The original Electrolyte_Relationship_Table.pdf and its generator are intentionally
left unchanged. This corrected copy keeps the one-page landscape study-sheet design
while improving clinical precision, spacing, alignment, and text rendering.
"""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Electrolyte_Relationship_Table_CORRECTED.pdf"

for font_name, filename in (("Body", "arial.ttf"), ("Bold", "arialbd.ttf")):
    pdfmetrics.registerFont(
        TTFont(font_name, str(Path("C:/Windows/Fonts") / filename))
    )
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Bold")

INK = "#26343B"
MUTED = "#53636A"
BLUE = "#EAF0F4"
SAGE = "#EEF3EE"
PALE = "#F7F9F9"
LINE = "#CCD6D9"
GUIDE = "#DCE4E6"


ROWS = [
    [
        "<b>Ca ↔ phosphate</b><br/>OPPOSITE - often",
        "<b>↓ Ca often ↔ ↑ phosphate</b><br/><b>↑ Ca often ↔ ↓ phosphate</b>",
        "Phosphate binds Ca. PTH raises serum Ca and increases renal phosphate excretion.",
        "High phosphate can lower Ca → tingling, spasms, <b>hyperreflexia</b>, tetany.",
        "<b>Trousseau:</b> BP cuff → hand spasm.<br/><b>Chvostek:</b> face tap → twitch.<br/>Severe: <b>SEIZURE / LARYNGOSPASM</b> risk. Assess neuro + <b>ECG</b>.",
    ],
    [
        "<b>Mg ↔ Ca</b><br/>NEUROMUSCULAR / REFLEXES",
        "<b>↓ Mg may cause ↓ Ca → excitability ↑</b><br/><b>↑ Mg → CNS / muscle depression</b>",
        "Both affect nerve/muscle stability. Severe Mg deficiency can impair PTH release or action, lowering Ca.",
        "Low: tremors, cramps, hyperreflexia, tetany.<br/>High: ↓ DTRs, lethargy, weakness, low BP/HR, <b>RESPIRATORY DEPRESSION</b>.",
        "<b>Check DTRs</b>, breathing + <b>ECG</b>.<br/>LOW = too excitable.<br/>HIGH = too relaxed/depressed.",
    ],
    [
        "<b>K ↔ acid-base</b><br/>MAINLY METABOLIC",
        "<b>Metabolic acidosis → K tends OUT → serum K ↑</b><br/><b>Metabolic alkalosis → K tends IN → serum K ↓</b>",
        "pH and HCO3 changes influence K shifts. Respiratory effects are usually smaller.",
        "Either K extreme → weakness + <b>DYSRHYTHMIA</b> risk.<br/>Alkalosis may ↓ ionized Ca → cramps/tetany.",
        "<b>WATCH K + ECG.</b> This is a tendency. Cause matters: GI loss can lower K; in DKA, insulin lack is a major reason serum K shifts out.",
    ],
    [
        "<b>K ↔ insulin / glucose</b><br/>EXAM 1 - DIABETES",
        "<b>INSULIN → GLUCOSE + K INTO CELLS</b><br/>→ serum K can fall",
        "DKA causes osmotic diuresis → total-body K loss. Insulin then moves K into cells.",
        "Serum K may start normal/high, then fall during treatment → weakness + ECG/rhythm changes.",
        "Trend K before/during insulin; monitor rhythm as indicated.<br/><b>SERUM K ≠ TOTAL-BODY K.</b>",
    ],
    [
        "<b>Cl ↔ bicarbonate</b><br/>ACID-BASE",
        "<b>Vomiting / NG:</b> lose H+ + Cl → hypochloremic alkalosis; K often ↓.<br/><b>Diarrhea:</b> lose HCO3 → metabolic acidosis; Cl may ↑ and K often ↓.",
        "Gastric loss removes acid + Cl. Intestinal loss removes HCO3. Interpret Cl and HCO3 together.",
        "Vomiting/NG: weakness, cramps, alkalosis.<br/>Diarrhea: dehydration, acidosis; deep/fast breathing may occur.",
        "<b>READ TOGETHER: Cl + HCO3 + K + FLUID STATUS.</b>",
    ],
    [
        "<b>Na ↔ water</b><br/>WATER ↔ BRAIN",
        "<b>Water excess vs Na → dilution → Na ↓</b><br/><b>Water deficit vs Na → concentration → Na ↑</b>",
        "Serum Na reflects water relative to Na, not total-body Na. Water moves toward higher osmolality.",
        "Brain cells swell or shrink. Significant changes → confusion, LOC change, <b>SEIZURES</b>.",
        "<b>SODIUM = NEURO + FLUID.</b> Check neuro, I/O, weight.<br/><b>USE CONTROLLED CORRECTION</b> → rapid shifts can cause neurologic injury.",
    ],
    [
        "<b>Na ↔ hormones</b><br/>ADH / ALDOSTERONE",
        "<b>↑ ADH:</b> retain water → dilute Na ↓<br/><b>↓ / ineffective ADH (DI):</b> water loss → Na may ↑<br/><b>Aldosterone:</b> retain Na; water follows; excrete K",
        "ADH controls water retention. Aldosterone promotes Na retention and K excretion.",
        "SIADH → dilutional hyponatremia.<br/>DI → high urine output, water loss, hypernatremia risk.<br/>Excess aldosterone → K may fall.",
        "Compare <b>Na + K + I/O + urine output + BP + daily weight.</b>",
    ],
    [
        "<b>Phosphate ↔ energy</b><br/>ATP / MUSCLE / RESPIRATORY",
        "<b>↓ phosphate → ↓ cellular energy / ATP</b><br/>→ muscle function ↓",
        "Phosphate is needed for cellular energy production and muscle function.",
        "General weakness, weak respiratory muscles, poor activity tolerance, ↓ cardiac performance, fall risk.",
        "<b>LOW PHOSPHATE = THINK WEAK.</b><br/>Check breathing strength, mobility, fall/cardiac risk + <b>RENAL FUNCTION</b>.",
    ],
    [
        "<b>Mg ↔ K</b><br/>CORRECTION CLUE",
        "<b>↓ Mg → kidney K wasting</b><br/>→ low K may persist",
        "Mg deficiency makes it harder for the kidneys to retain K.",
        "K stays low despite replacement; combined deficits increase rhythm risk.",
        "<b>K not improving? CHECK Mg.</b><br/>Monitor <b>ECG + kidney function</b>.",
    ],
    [
        "<b>Kidneys ↔ all</b><br/>PUT IT TOGETHER",
        "<b>Impaired regulation / excretion</b><br/>→ several abnormalities at once",
        "Kidneys regulate electrolytes, acid-base and fluid. With kidney failure, K, Mg and phosphate may rise; Ca may fall.",
        "Rhythm, reflex, weakness, fluid and pH changes may occur together.",
        "<b>THINK: KIDNEYS + GI LOSSES + MEDS + FLUIDS.</b><br/>Review BUN/Cr, urine output, I/O, meds, orders + trends.",
    ],
]


PATTERNS = [
    ("METABOLIC ACIDOSIS", "K tends OUT; effect depends on cause<br/>DKA: total-body K is depleted"),
    ("METABOLIC ALKALOSIS", "K tends IN → K ↓<br/>Ionized Ca ↓ → tetany risk"),
    ("Ca / PHOSPHATE", "Often opposite<br/>High phosphate can produce low-Ca findings"),
    ("LOW Mg + LOW Ca", "Excitability ↑<br/>Cramps / hyperreflexia / tetany"),
    ("VOMITING / NG", "H+ + Cl lost → alkalosis<br/>K often ↓"),
    ("DIARRHEA", "HCO3 lost → acidosis<br/>Cl may ↑; K often ↓ from GI loss"),
    ("INSULIN / DKA", "Insulin moves K into cells<br/>Serum K may fall; trend closely"),
    ("RENAL DYSFUNCTION", "K / Mg / phosphate may build up<br/>Check creatinine + urine output"),
]


def paragraph(c, text, x, top, width, size=7.25, color=INK, bold=False, leading=None):
    style = ParagraphStyle(
        "cell",
        fontName="Bold" if bold else "Body",
        fontSize=size,
        leading=leading or size + 0.95,
        textColor=HexColor(color),
        spaceAfter=0,
        spaceBefore=0,
    )
    p = Paragraph(text, style)
    _, height = p.wrap(width, 600)
    p.drawOn(c, x, top - height)
    return height


def measure(text, width, size=7.25, leading=None):
    style = ParagraphStyle(
        "measure",
        fontName="Body",
        fontSize=size,
        leading=leading or size + 0.95,
        spaceAfter=0,
        spaceBefore=0,
    )
    p = Paragraph(text, style)
    return p.wrap(width, 600)[1]


def main():
    c = canvas.Canvas(str(OUTPUT), pagesize=(792, 612))
    c.setTitle("ELECTROLYTE RELATIONSHIP TABLE - CORRECTED QC COPY")
    c.setAuthor("NUR 122 Study Reference")
    c.setSubject("Corrected and quality-checked electrolyte relationship study table")
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, 792, 612, fill=1, stroke=0)

    paragraph(c, "ELECTROLYTE RELATIONSHIP TABLE", 26, 589, 610, 19, bold=True)
    c.setFillColor(HexColor(SAGE))
    c.roundRect(648, 574, 118, 18, 5, fill=1, stroke=0)
    paragraph(c, "CORRECTED - QC COPY", 657, 587, 100, 7.3, INK, True)
    paragraph(
        c,
        "How the major electrolytes interact and what those relationships mean clinically",
        26,
        563,
        740,
        10,
        MUTED,
    )
    paragraph(
        c,
        "↑ increases   ↓ decreases   ↔ closely related   •   Opposite = often inverse   •   Relationships are tendencies; the cause and the patient determine the meaning",
        26,
        546,
        740,
        8,
        MUTED,
    )

    widths = [105, 185, 145, 140, 165]
    x0 = 26
    table_top = 527
    y = table_top
    header_height = 24
    c.setFillColor(HexColor(INK))
    c.rect(x0, y - header_height, 740, header_height, fill=1, stroke=0)
    x = x0
    for label, width in zip(
        [
            "RELATIONSHIP",
            "WHAT HAPPENS?",
            "WHY / PHYSIOLOGY",
            "WHAT YOU MAY SEE",
            "NURSING / EXAM CONNECTION",
        ],
        widths,
    ):
        paragraph(c, label, x + 7, y - 7, width - 14, 7.5, "#FFFFFF", True)
        x += width
    y -= header_height

    row_fills = [SAGE, "#F5F8F5", BLUE, "#F4F7F9", BLUE, "#F4F7F9", PALE, "#FFFFFF", PALE, "#FFFFFF"]
    row_font = 7.25
    row_leading = 8.15
    top_padding = 3.4
    bottom_padding = 2.9
    row_boundaries = [y]

    for index, row in enumerate(ROWS):
        heights = [
            measure(text, width - 14, row_font, row_leading)
            for text, width in zip(row, widths)
        ]
        row_height = max(heights) + top_padding + bottom_padding
        c.setFillColor(HexColor(row_fills[index]))
        c.rect(x0, y - row_height, 740, row_height, fill=1, stroke=0)
        x = x0
        for text, width in zip(row, widths):
            paragraph(
                c,
                text,
                x + 7,
                y - top_padding,
                width - 14,
                row_font,
                INK,
                False,
                row_leading,
            )
            x += width
        c.setStrokeColor(HexColor(LINE))
        c.setLineWidth(0.45)
        c.line(x0, y - row_height, 766, y - row_height)
        y -= row_height
        row_boundaries.append(y)

    # Subtle column guides make heading-to-cell association unambiguous.
    c.setStrokeColor(HexColor(GUIDE))
    c.setLineWidth(0.35)
    x = x0
    for width in widths[:-1]:
        x += width
        c.line(x, table_top - header_height, x, y)

    if y < 137:
        raise ValueError(f"Table exceeds its reserved area: bottom={y:.1f}")

    paragraph(c, "PATTERNS TO RECOGNIZE ON AN EXAM", 26, y - 7, 740, 8, MUTED, True)
    pattern_top = y - 20
    gap = 6
    box_width = (740 - 3 * gap) / 4
    box_height = 34
    row_gap = 4
    for index, (title, body) in enumerate(PATTERNS):
        column = index % 4
        row = index // 4
        x = 26 + column * (box_width + gap)
        box_top = pattern_top - row * (box_height + row_gap)
        c.setFillColor(HexColor(SAGE if index in (2, 3) else BLUE))
        c.roundRect(x, box_top - box_height, box_width, box_height, 4, fill=1, stroke=0)
        paragraph(c, title, x + 7, box_top - 5, box_width - 14, 7.2, INK, True)
        paragraph(c, body, x + 7, box_top - 17, box_width - 14, 7.15, INK, False, 8.0)

    pattern_bottom = pattern_top - box_height - row_gap - box_height
    if pattern_bottom < 45:
        raise ValueError(f"Pattern boxes exceed their reserved area: bottom={pattern_bottom:.1f}")

    paragraph(
        c,
        "Course basis: NUR 122 electrolyte and acid-base lectures/objectives. Clinical clarifications preserve course intent while distinguishing metabolic K shifts and total-body K loss in DKA.",
        26,
        34,
        740,
        6.6,
        MUTED,
    )
    paragraph(
        c,
        "Review: Lippincott Ch. 10, 17 and 48 • ATI Ch. 45-46 • Exam 1: Days 1-2 exemplars.",
        26,
        23,
        740,
        6.6,
        MUTED,
    )

    c.showPage()
    c.save()
    print(OUTPUT)
    print(f"Table bottom: {y:.1f}; pattern bottom: {pattern_bottom:.1f}")


if __name__ == "__main__":
    main()
