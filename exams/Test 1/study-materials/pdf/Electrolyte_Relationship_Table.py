"""Editable source: edit ROWS and PATTERNS, then run with Python + reportlab.
Course basis: Electrolytes_CMcCain.pdf pp. 5-10,12-14,16-22;
ABGs_CMcCain_Spring2026.pdf pp. 2,4-7,13,17;
NUR122 Fall26 MS ReadingListObjectives.pdf pp. 2-4.
Standard clarification: Mg deficiency and persistent low K/Ca, renal K loss:
https://www.merckmanuals.com/professional/nephrology/electrolyte-disorders/hypomagnesemia
https://www.ncbi.nlm.nih.gov/books/NBK500003/
Acid-base context: https://www.merckmanuals.com/professional/nephrology/acid-base-regulation-and-disorders/metabolic-acidosis
No ATI or Brunner full textbook was available locally; reading locations are from objectives.
Course cautions: Ca/phosphate inverse pairing is common, not universal. ABG p.7
contains an inconsistent respiratory-acidosis calcium statement; this sheet uses
the consistent alkalosis/ionized-calcium teaching and does not reproduce that claim.
H+/K+ exchange is a simplified tendency, not a universal or fixed exchange ratio.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
for name, file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold')
INK='#26343B'; MUTED='#53636A'; BLUE='#EAF0F4'; SAGE='#EEF3EE'; LINE='#CDD5D8'
ROWS = [
['<b>Ca ↔ phosphate</b><br/>OPPOSITE • often',
 '<b>↓ Ca ↔ ↑ phosphate</b><br/><b>↑ Ca ↔ ↓ phosphate</b>',
 'Phosphate binds Ca. PTH raises serum Ca and promotes phosphate loss in urine.',
 'High phosphate may look like low Ca: tingling, spasms, <b>hyperreflexia</b>, tetany.',
 '<b>Trousseau:</b> BP cuff → hand spasm.<br/><b>Chvostek:</b> face tap → twitch.<br/>Severe: <b>SEIZURE / LARYNGOSPASM</b> risk. Assess neuro + <b>ECG</b>.'],
['<b>Mg ↔ Ca</b><br/>NEUROMUSCULAR / REFLEXES',
 '<b>↓ Mg + ↓ Ca → excitability ↑</b><br/><b>↑ Mg → CNS / muscle depression</b>',
 'Both stabilize nerve/muscle activity. Severe Mg lack can impair Ca regulation.',
 'Low: tremors, cramps, hyperreflexia, tetany.<br/>High: ↓ DTRs, lethargy, weakness, low BP/HR, <b>RESPIRATORY DEPRESSION</b>.',
 '<b>Check DTRs</b>, breathing + <b>ECG</b>.<br/>LOW = too excitable.<br/>HIGH = too relaxed/depressed.'],
['<b>K ↔ acid-base</b><br/>HEART / MUSCLE',
 '<b>ACIDOSIS → K tends OUT → serum K ↑</b><br/><b>ALKALOSIS → K tends IN → serum K ↓</b>',
 'H+ and K shift across cell membranes as the body responds to pH.',
 'Either K extreme → weakness + <b>DYRHYTHMIA</b> risk.<br/>Alkalosis may ↓ ionized Ca → cramps/tetany.',
 '<b>WATCH K + ECG.</b> A tendency, not a rule. Cause matters; GI loss can still lower K.'],
['<b>K ↔ insulin / glucose</b><br/>EXAM 1 • DIABETES',
 '<b>INSULIN → GLUCOSE + K INTO CELLS</b><br/>→ serum K can fall',
 'Insulin stimulates K uptake. DKA causes fluid/electrolyte loss; treatment can lower serum K further.',
 'K may drop during insulin therapy → weakness + ECG/rhythm changes.',
 'Trend K before/during insulin; monitor rhythm as indicated.<br/><b>SERUM K ≠ TOTAL-BODY K.</b>'],
['<b>Cl ↔ bicarbonate</b><br/>ACID-BASE',
 '<b>Vomiting / NG:</b> lose H+ + Cl → ↓ Cl → alkalosis; K often ↓.<br/><b>Diarrhea:</b> lose HCO3 → acidosis; Cl may ↑.',
 'Gastric fluid contains acid + Cl. Intestinal loss removes HCO3. Read Cl and HCO3 together.',
 'Vomiting/NG: weakness, cramps, alkalosis.<br/>Diarrhea: fluid loss, acidosis; deep/fast breathing may occur.',
 '<b>READ TOGETHER: Cl + HCO3 + K + FLUID STATUS.</b>'],
['<b>Na ↔ water</b><br/>WATER ↔ BRAIN',
 '<b>Water excess vs Na → dilution → Na ↓</b><br/><b>Water deficit vs Na → concentration → Na ↑</b>',
 'Serum Na depends strongly on water relative to Na. Water shifts toward higher osmolality.',
 'Brain cells swell or shrink. Significant changes → confusion, LOC change, <b>SEIZURES</b>.',
 '<b>SODIUM = NEURO + FLUID.</b> Check neuro, I&O, weight.<br/><b>AVOID RAPID Na CORRECTION</b> → neurologic injury.'],
['<b>Na ↔ hormones</b><br/>ADH / ALDOSTERONE',
 '<b>↑ ADH:</b> retain water → dilute Na ↓<br/><b>↓ / ineffective ADH (DI):</b> water loss → Na may ↑<br/><b>Aldosterone:</b> retain Na/water; excrete K',
 'ADH controls water retention. Aldosterone promotes Na retention and K loss.',
 'SIADH → dilutional hyponatremia.<br/>DI → high urine output, water loss, hypernatremia risk.<br/>Excess aldosterone → K may fall.',
 'Compare <b>Na + K + I&O + urine output + BP + daily weight.</b>'],
['<b>Phosphate ↔ energy</b><br/>ATP / MUSCLE / RESPIRATORY',
 '<b>↓ phosphate → ↓ cellular energy / ATP</b><br/>→ muscle function ↓',
 'Phosphate is needed for cellular energy production and muscle function.',
 'General weakness, weak respiratory muscles, poor activity tolerance, ↓ cardiac performance, fall risk.',
 '<b>LOW PHOSPHATE = THINK WEAK.</b><br/>Check breathing strength, mobility, fall/cardiac risk + <b>RENAL FUNCTION</b>.'],
['<b>Mg ↔ K</b><br/>CORRECTION CLUE',
 '<b>↓ Mg → kidney K wasting</b><br/>→ low K may persist',
 'Mg deficiency makes it harder for the kidneys to retain K.',
 'K stays low despite replacement; combined deficits increase rhythm risk.',
 '<b>K not improving? CHECK Mg.</b><br/>Monitor <b>ECG + kidney function</b>.'],
['<b>Kidneys ↔ all</b><br/>PUT IT TOGETHER',
 '<b>Impaired regulation / excretion</b><br/>→ several abnormalities at once',
 'Kidneys regulate electrolytes, acid-base and fluid. K, Mg and phosphate may accumulate when excretion falls.',
 'Rhythm, reflex, weakness, fluid and pH changes may occur together.',
 '<b>THINK: KIDNEYS + GI LOSSES + MEDS + FLUIDS.</b><br/>Review BUN/Cr, urine output, I&O, meds, orders + trends.'],
]
PATTERNS = [
 ('ACIDOSIS','K tends OUT → serum K ↑<br/>Check actual K + ECG'),
 ('ALKALOSIS','K tends IN → K ↓<br/>Ionized Ca ↓ → tetany risk'),
 ('Ca / PHOSPHATE','Often opposite<br/>High phosphate can look like low Ca'),
 ('LOW Mg + LOW Ca','Excitability ↑<br/>Cramps / hyperreflexia / tetany'),
 ('VOMITING / NG','H+ + Cl lost → alkalosis<br/>K often ↓'),
 ('DIARRHEA','HCO3 lost → acidosis<br/>Cl may ↑; K may ↓ from GI loss'),
 ('INSULIN / DKA','Insulin moves K into cells<br/>Serum K may fall; trend closely'),
 ('RENAL FAILURE','K / Mg / phosphate may build up<br/>Check creatinine + urine output'),
]

def para(c,text,x,top,width,size=8.5,color=INK,bold=False):
    style=ParagraphStyle('cell',fontName='Bold' if bold else 'Body',fontSize=size,
                         leading=size+1,textColor=HexColor(color))
    p=Paragraph(text,style); w,h=p.wrap(width,600)
    p.drawOn(c,x,top-h)
    return h

def main():
    out=ROOT/'Electrolyte_Relationship_Table.pdf'
    c=canvas.Canvas(str(out),pagesize=(792,612))
    c.setTitle('ELECTROLYTE RELATIONSHIP TABLE - How the Major Electrolytes Connect')
    c.setAuthor('NUR 122 Study Reference')
    c.setFillColor(HexColor('#FFFFFF')); c.rect(0,0,792,612,fill=1,stroke=0)
    para(c,'ELECTROLYTE RELATIONSHIP TABLE',26,588,740,19,bold=True)
    para(c,'How the major electrolytes interact and what those relationships mean clinically',26,563,740,10,MUTED)
    para(c,'↑ increases   ↓ decreases   ↔ closely related   •   Opposite = often inverse   •   Together = commonly same clinical direction',26,546,740,8,MUTED)
    widths=[105,185,145,140,165]; x0=26; y=527
    c.setFillColor(HexColor(INK)); c.rect(x0,y-23,740,23,fill=1,stroke=0)
    x=x0
    for label,w in zip(['RELATIONSHIP','WHAT HAPPENS?','WHY / PHYSIOLOGY','WHAT YOU MAY SEE','NURSING / EXAM CONNECTION'],widths):
        para(c,label,x+7,y-6,w-14,7.5,'#FFFFFF',True); x+=w
    y-=23
    for i,row in enumerate(ROWS):
        heights=[]
        for text,w in zip(row,widths):
            p=Paragraph(text,ParagraphStyle('measure',fontName='Body',fontSize=7.3,leading=8.3))
            heights.append(p.wrap(w-14,600)[1])
        height=max(heights)+3
        row_fills=[SAGE,'#F5F8F5',BLUE,'#F4F7F9',BLUE,'#F4F7F9','#F7F8F8','#FFFFFF','#F7F8F8','#FFFFFF']
        c.setFillColor(HexColor(row_fills[i]))
        c.rect(x0,y-height,740,height,fill=1,stroke=0)
        x=x0
        for text,w in zip(row,widths):
            para(c,text,x+7,y-2,w-14,7.3); x+=w
        c.setStrokeColor(HexColor(LINE)); c.setLineWidth(.4); c.line(x0,y-height,766,y-height)
        y-=height
    assert y>148, f'Table too tall: bottom={y}'
    para(c,'PATTERNS TO RECOGNIZE ON AN EXAM',26,y-7,740,8,MUTED,True)
    top=y-20; gap=6; bw=(740-3*gap)/4; bh=35
    for i,(title,body) in enumerate(PATTERNS):
        col=i%4; row=i//4; x=26+col*(bw+gap); box_top=top-row*(bh+5)
        c.setFillColor(HexColor(SAGE if i in (2,3) else BLUE)); c.roundRect(x,box_top-bh,bw,bh,4,fill=1,stroke=0)
        para(c,title,x+7,box_top-5,bw-14,7.4,INK,True)
        para(c,body,x+7,box_top-16,bw-14,7.5,INK)
    para(c,'Built from NUR 122 electrolyte/acid-base course materials. • Relationships are tendencies; interpret labs with the patient’s condition.',26,39,740,7,MUTED)
    para(c,'Read more: Lippincott Ch. 10 + 48 (electrolytes/acid-base); Ch. 17 (respiratory). • ATI Ch. 45-46. • Exam 1: Days 1-2 exemplars.',26,28,740,7,MUTED)
    c.showPage(); c.save(); print(out); print('Table bottom:',y)

if __name__=='__main__': main()
