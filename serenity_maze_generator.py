from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String, Circle
from reportlab.graphics import renderPDF
import qrcode, os, textwrap

outdir='output'
os.makedirs(outdir, exist_ok=True)

html='''<!doctype html>
<html lang="ar" dir="rtl" data-theme="dark">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>serenity-maze</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0b132b;--surface:#111b3b;--surface2:#16244f;--text:#f7f8fc;--muted:#b8c2e0;--gold:#c5a059;--teal:#87d6d1;--ok:#8de0a8;--warn:#ffd27d;--radius:22px;--shadow:0 20px 60px rgba(0,0,0,.35)}
*{box-sizing:border-box} html,body{margin:0;padding:0;background:radial-gradient(circle at top,#16244f 0%,#0b132b 55%,#081022 100%);color:var(--text);font-family:'Tajawal',sans-serif;min-height:100%}
body{display:flex;align-items:center;justify-content:center;padding:24px}
.app{width:min(980px,100%);background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.02));backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.08);box-shadow:var(--shadow);border-radius:28px;overflow:hidden}
.hero{padding:28px;border-bottom:1px solid rgba(255,255,255,.08);background:linear-gradient(135deg,rgba(197,160,89,.16),rgba(135,214,209,.06))}
.brand{display:flex;align-items:center;gap:14px}.logo{width:54px;height:54px;border-radius:16px;background:linear-gradient(135deg,var(--gold),#e7d1a4);display:grid;place-items:center;color:#0b132b;font-weight:800;font-size:24px}.title{font-size:34px;font-weight:800;margin:0}.sub{margin:6px 0 0;color:var(--muted);font-size:18px}
.grid{display:grid;grid-template-columns:1.15fr .85fr;gap:0}@media(max-width:860px){.grid{grid-template-columns:1fr}}
.main,.side{padding:24px}.card{background:linear-gradient(180deg,var(--surface),var(--surface2));border:1px solid rgba(255,255,255,.07);border-radius:var(--radius);padding:20px}.stack{display:grid;gap:16px}.timer{display:grid;place-items:center;padding:18px;border-radius:24px;background:radial-gradient(circle at center,rgba(197,160,89,.18),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.08)}.time{font-size:74px;font-weight:800;line-height:1;color:#fff}.hint{color:var(--muted);font-size:17px;margin-top:10px;text-align:center}
.btns{display:flex;flex-wrap:wrap;gap:12px}.btn{appearance:none;border:none;border-radius:999px;padding:14px 18px;font-size:17px;font-weight:700;cursor:pointer}.primary{background:var(--gold);color:#0b132b}.ghost{background:transparent;border:1px solid rgba(255,255,255,.16);color:#fff}.ok{background:var(--ok);color:#0b132b}.badge{display:inline-block;padding:8px 12px;border-radius:999px;background:rgba(135,214,209,.12);border:1px solid rgba(135,214,209,.24);color:var(--teal);font-weight:700}
.q{font-size:23px;font-weight:800;margin:0 0 12px}.answers{display:grid;gap:10px}.answer{padding:14px 16px;border-radius:16px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);cursor:pointer}.answer:hover{border-color:rgba(197,160,89,.5)} .answer.active{border-color:var(--gold);background:rgba(197,160,89,.12)}
.tip{font-size:18px;line-height:1.8;color:#f2f4fb}.list{margin:0;padding:0 18px 0 0}.list li{margin:0 0 10px;color:var(--muted);line-height:1.8}.reward{display:none}.reward.show{display:block}.pill{display:inline-block;padding:7px 10px;border-radius:999px;background:rgba(255,210,125,.12);color:var(--warn);border:1px solid rgba(255,210,125,.25);margin:4px 0}
.footer{padding:18px 24px;border-top:1px solid rgba(255,255,255,.08);color:var(--muted);font-size:15px}
</style>
</head>
<body>
<div class="app">
  <section class="hero">
    <div class="brand"><div class="logo">س</div><div><h1 class="title">متاهة الـ 15 دقيقة</h1><p class="sub">تجربة ليلية تفاعلية لفصل العقل عن التشتيت والانتقال إلى هدوء ما قبل النوم</p></div></div>
  </section>
  <div class="grid">
    <main class="main stack">
      <div class="card">
        <span class="badge">المهمة الآن</span>
        <h2 class="q" style="margin-top:12px">ضع الهاتف بعيدًا وابدأ طقسًا هادئًا</h2>
        <ul class="list">
          <li>حضّر مشروبًا دافئًا خفيفًا أو كوب ماء</li>
          <li>رتّب الوسادة أو أطفئ الإشعارات</li>
          <li>خذ 10 أنفاس بطيئة ثم عد إلى الصفحة</li>
        </ul>
        <div class="btns" style="margin-top:16px"><button class="btn primary" id="startBtn">ابدأ التحدي</button><button class="btn ghost" id="resetBtn">إعادة</button><button class="btn ok" id="doneBtn">أنهيت المهمة</button></div>
      </div>
      <div class="card">
        <h2 class="q">هل تشعر بالقلق الآن؟</h2>
        <div class="answers" id="answers">
          <button class="answer" data-mode="yes">نعم، عقلي مزدحم</button>
          <button class="answer" data-mode="medium">قليلًا، أحتاج تهدئة</button>
          <button class="answer" data-mode="no">لا، أريد فقط الاستمرار</button>
        </div>
        <div id="tip" class="tip" style="margin-top:16px">اختر حالتك لتظهر لك رسالة هادئة مناسبة لهذه اللحظة.</div>
      </div>
      <div class="card reward" id="reward">
        <span class="pill">المكافأة انفتحت</span>
        <h2 class="q" style="margin-top:10px">مكافأتك الهادئة</h2>
        <p class="tip">أحسنت. التزامك بهذه الدقائق هو بداية الانفصال عن دوامة التحفيز. افتح الآن صوت المطر الهادئ أو شغّل قائمة النوم المقترحة.</p>
        <div class="btns" style="margin-top:14px">
          <a class="btn primary" target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/watch?v=mPZkdNFkNps">صوت مطر هادئ</a>
          <a class="btn ghost" target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/watch?v=1ZYbU82GVz4">قائمة تشغيل للنوم</a>
        </div>
      </div>
    </main>
    <aside class="side stack">
      <div class="timer">
        <div id="time" class="time">15:00</div>
        <div class="hint">لا نطارد النوم بالقوة؛ نحن فقط نخفف الضوضاء التي تمنعه.</div>
      </div>
      <div class="card">
        <h2 class="q">مكاسبك من 15 دقيقة هادئة</h2>
        <ul class="list">
          <li>خفض التحفيز الذهني قبل النوم</li>
          <li>تخفيف تعلق العقل بالشاشة</li>
          <li>تهيئة أفضل للنوم العميق</li>
          <li>بداية روتين يمكن تكراره كل ليلة</li>
        </ul>
      </div>
      <div class="card">
        <h2 class="q">حقيقة سريعة</h2>
        <p id="fact" class="tip">تقليل الضوء والشاشات قبل النوم يساعد على منح الدماغ إشارة أوضح بأن وقت الراحة قد بدأ.</p>
      </div>
    </aside>
  </div>
  <div class="footer">صُممت هذه التجربة لتُلحق بكتابك الرقمي عبر QR Code في نهاية فصل الخطة أو كهدية تفاعلية مستقلة.</div>
</div>
<script>
const timeEl=document.getElementById('time');
const startBtn=document.getElementById('startBtn');
const resetBtn=document.getElementById('resetBtn');
const doneBtn=document.getElementById('doneBtn');
const reward=document.getElementById('reward');
const fact=document.getElementById('fact');
const facts=[
'تقليل الضوء والشاشات قبل النوم يساعد على منح الدماغ إشارة أوضح بأن وقت الراحة قد بدأ.',
'القلق لا يُحل دائمًا ليلًا؛ أحيانًا يحتاج فقط ورقة وقلم وحدودًا واضحة للغد.',
'الروتين الهادئ قبل النوم أهم من محاولة النوم بالقوة.',
'بعض الأرق يبدأ من كثرة التحفيز لا من قلة التعب.'
];
fact.textContent=facts[Math.floor(Math.random()*facts.length)];
let total=15*60, left=total, timer=null;
function render(){const m=String(Math.floor(left/60)).padStart(2,'0');const s=String(left%60).padStart(2,'0');timeEl.textContent=`${m}:${s}`}
function reveal(){reward.classList.add('show');reward.scrollIntoView({behavior:'smooth',block:'start'})}
startBtn.onclick=()=>{if(timer)return;timer=setInterval(()=>{left--;render();if(left<=0){clearInterval(timer);timer=null;reveal()}},1000)};
resetBtn.onclick=()=>{clearInterval(timer);timer=null;left=total;render();reward.classList.remove('show')};
doneBtn.onclick=()=>reveal();
render();
const tips={yes:'إذا كان عقلك مزدحمًا: لا تحاول إسكاته بالقوة. اكتب فكرة واحدة فقط تؤلمك الآن، ثم قل لنفسك: سأعود لها غدًا، لا الليلة.',medium:'إذا كنت تحتاج تهدئة: خفف الإضاءة، رخِّ كتفيك، وخذ شهيقًا لأربع ثوانٍ ثم زفيرًا لست ثوانٍ لخمس مرات.',no:'ممتاز. استمر على نفس الهدوء، ولا تبحث عن محفز جديد. الليلة تربح بالبساطة.'};
document.querySelectorAll('.answer').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.answer').forEach(b=>b.classList.remove('active'));btn.classList.add('active');document.getElementById('tip').textContent=tips[btn.dataset.mode]}));
</script>
</body></html>'''

html_path=os.path.join(outdir,'serenity-maze.html')
open(html_path,'w',encoding='utf-8').write(html)

# PDF
try:
    font_candidates=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
    font_path=next(p for p in font_candidates if os.path.exists(p))
    pdfmetrics.registerFont(TTFont('BaseFont', font_path))
    fname='BaseFont'
except:
    fname='Helvetica'

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleAr', fontName=fname, fontSize=22, leading=28, alignment=TA_CENTER, textColor=colors.HexColor('#0b132b')))
styles.add(ParagraphStyle(name='HeadAr', fontName=fname, fontSize=16, leading=22, alignment=TA_RIGHT, textColor=colors.HexColor('#0b132b')))
styles.add(ParagraphStyle(name='BodyAr', fontName=fname, fontSize=11, leading=18, alignment=TA_RIGHT, textColor=colors.HexColor('#1a1a1a')))
styles.add(ParagraphStyle(name='SmallAr', fontName=fname, fontSize=9, leading=14, alignment=TA_RIGHT, textColor=colors.HexColor('#444444')))

pdf_path=os.path.join(outdir,'sleep-qr-pack.pdf')
doc=SimpleDocTemplate(pdf_path,pagesize=A4,rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36)
story=[]

# QR code to html file path (works locally after opening shared artifact page path not guaranteed; provide editable field too)
qr_url='serenity-maze.html'
img=qrcode.make(qr_url)
qr_png=os.path.join(outdir,'qr.png')
img.save(qr_png)

from reportlab.platypus import Image

story.append(Paragraph('بطاقة الدخول إلى متاهة الـ 15 دقيقة', styles['TitleAr']))
story.append(Spacer(1,14))
story.append(Paragraph('ملف مكمّل لكتاب النوم الرقمي: يتضمن صفحة هبوط تفاعلية + كود QR + وصف جاهز للاستخدام داخل المنتج أو المتجر.', styles['BodyAr']))
story.append(Spacer(1,18))
story.append(Image(qr_png, width=180, height=180))
story.append(Spacer(1,12))
story.append(Paragraph('مهم: هذا الكود موجّه حاليًا إلى ملف الصفحة التفاعلية المرفق معك ضمن نفس الحزمة. إذا أردت استخدامه للبيع الفعلي، ارفع صفحة HTML على رابطك النهائي ثم أعد توليد QR بالرابط العام.', styles['SmallAr']))
story.append(Spacer(1,18))

rows=[['العنصر','الوصف'],['اسم التجربة','متاهة الـ 15 دقيقة'],['نوعها','صفحة تفاعلية ليلية تعمل على الجوال والمتصفح'],['فكرتها','عداد 15 دقيقة + سؤال تفاعلي + رسالة تهدئة + مكافأة صوتية'],['أفضل مكان لها','نهاية فصل الخطة أو كهدية إضافية داخل المنتج'],['هوية الألوان','كحلي داكن + ذهبي هادئ + لمسة تركواز مطمئنة']]
t=Table(rows,colWidths=[130,360])
t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),fname),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#0b132b')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.6,colors.HexColor('#c5a059')),('BACKGROUND',(0,1),(-1,-1),colors.HexColor('#f8f4ec')),('ALIGN',(0,0),(-1,-1),'RIGHT'),('LEADING',(0,0),(-1,-1),16)]))
story.append(t)
story.append(Spacer(1,18))

for title, body in [
('النص الجاهز داخل كتابك','امسح الكود وادخل تحدي الهدوء الليلي. لديك 15 دقيقة فقط لتفصل عقلك عن التشتيت، ترتّب مكان نومك، وتهيئ نفسك لعبور هادئ نحو النوم.'),
('وصف تسويقي مختصر','هذه ليست صفحة عادية، بل تجربة صغيرة مصممة لتدريب العقل على الانفصال عن الضجيج الليلي. عدّاد، تهدئة، ومكافأة نهائية تجعل القارئ يشعر أنه داخل منتج حي لا مجرد ملف جامد.'),
('طريقة الاستخدام','1) ضع QR في نهاية الكتاب. 2) ارفع ملف HTML على استضافة عامة. 3) استبدل الرابط داخل QR النهائي. 4) اختبره من الجوال. 5) اجعل المكافأة صوتًا خاصًا بك لاحقًا لرفع قيمة المنتج.')
]:
    story.append(Paragraph(title, styles['HeadAr']))
    story.append(Spacer(1,6))
    story.append(Paragraph(body, styles['BodyAr']))
    story.append(Spacer(1,12))

doc.build(story)
print({'html':html_path,'pdf':pdf_path})
