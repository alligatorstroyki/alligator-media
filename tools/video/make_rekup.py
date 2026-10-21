"""Спецификация ролика «Рекуперация» для render_video.py."""
import json

DEFS = """<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2236"/><stop offset=".75" stop-color="#7d4f5a"/><stop offset="1" stop-color="#8f5f5f"/></linearGradient>
<linearGradient id="warmup" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="920" y2="0"><stop offset="0" stop-color="#5aa9ff"/><stop offset="1" stop-color="#ffd27a"/></linearGradient>
<linearGradient id="cooldown" gradientUnits="userSpaceOnUse" x1="0" y1="30" x2="0" y2="610"><stop offset="0" stop-color="#ff9a3c"/><stop offset="1" stop-color="#a7adb4"/></linearGradient>
<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""

LABEL = 'font-size="30" fill="#fff" stroke="#1a1a1a" stroke-width="5" paint-order="stroke"'


def house(dim_rooms=False, window_open=False):
    room_op = "0.55" if dim_rooms else "1"
    win_left_ground = (
        '<rect x="190" y="410" width="18" height="92" fill="#1d2228"/>'
        '<polygon points="190,410 150,398 150,512 190,502" fill="#ffe7a3" stroke="#3a3530" stroke-width="3"/>'
        if window_open else
        '<rect x="190" y="410" width="18" height="92" fill="#ffe08a"/>'
    )
    return f"""
<rect width="960" height="630" fill="url(#sky)"/>
<g fill="#1b2620"><circle cx="70" cy="470" r="70"/><circle cx="140" cy="440" r="60"/><circle cx="880" cy="460" r="75"/><circle cx="820" cy="430" r="55"/></g>
<rect y="540" width="960" height="90" fill="#24402a"/>
<rect x="170" y="118" width="620" height="26" fill="#22252b"/>
<rect x="190" y="144" width="580" height="52" fill="#3b3631"/>
<rect x="190" y="340" width="580" height="32" fill="#3b3631"/>
<g opacity="{room_op}">
 <rect x="208" y="196" width="262" height="144" fill="#f2d9a6"/>
 <rect x="482" y="196" width="270" height="144" fill="#dde6e8"/>
 <rect x="208" y="372" width="262" height="168" fill="#f2d9a6"/>
 <rect x="482" y="372" width="270" height="168" fill="#efdcb8"/>
 <rect x="232" y="296" width="170" height="36" rx="6" fill="#8e6b4e"/><rect x="236" y="286" width="54" height="18" rx="6" fill="#efe8da"/>
 <rect x="540" y="300" width="150" height="34" rx="14" fill="#ffffff" stroke="#b9c3c6" stroke-width="3"/>
 <rect x="600" y="222" width="46" height="56" rx="6" fill="#bfd3dc"/>
 <rect x="236" y="486" width="170" height="46" rx="10" fill="#6d7f8c"/><rect x="236" y="470" width="170" height="22" rx="8" fill="#7f93a0"/>
 <rect x="540" y="470" width="196" height="64" fill="#7a6a5a"/><rect x="536" y="462" width="204" height="10" fill="#cbbfa9"/>
 <polygon points="640,400 700,400 712,430 628,430" fill="#9aa3aa"/>
</g>
<rect x="190" y="144" width="18" height="396" fill="#ddd5c6"/><rect x="752" y="144" width="18" height="396" fill="#ddd5c6"/>
<rect x="470" y="196" width="12" height="144" fill="#ddd5c6"/><rect x="470" y="372" width="12" height="168" fill="#ddd5c6"/>
<rect x="190" y="220" width="18" height="80" fill="#ffe08a"/>
{win_left_ground}
<rect x="752" y="230" width="18" height="70" fill="#ffe08a"/><rect x="752" y="420" width="18" height="70" fill="#ffe08a"/>
<rect x="592" y="150" width="112" height="40" rx="6" fill="#cfd6dc" stroke="#8a949c" stroke-width="3"/>
<circle cx="620" cy="170" r="11" fill="none" stroke="#6b757d" stroke-width="3"/>
"""


def ducts(op="1", labels=False, glow=False):
    f = ' filter="url(#glow)"' if glow else ""
    lab = ""
    if labels:
        lab = f"""<text x="250" y="232" {LABEL}>приток</text><text x="250" y="406" {LABEL}>приток</text>
<text x="500" y="232" {LABEL}>вытяжка</text><text x="560" y="452" {LABEL}>вытяжка</text>
<text x="690" y="112" {LABEL}>с улицы →</text><text x="700" y="240" {LABEL}>на улицу</text>"""
    return f"""<g opacity="{op}"{f}>
 <path d="M592 160 H300 V206" fill="none" stroke="#6ec6ff" stroke-width="9" stroke-linecap="round" class="flow" stroke-dasharray="18 14"/>
 <path d="M455 160 V356 H300 V392" fill="none" stroke="#6ec6ff" stroke-width="9" stroke-linecap="round" class="flow" stroke-dasharray="18 14"/>
 <path d="M640 214 V190" fill="none" stroke="#ff9a3c" stroke-width="9" stroke-linecap="round" class="flow" stroke-dasharray="14 10"/>
 <path d="M670 398 V364 H730 V176 H704" fill="none" stroke="#ff9a3c" stroke-width="9" stroke-linecap="round" class="flow" stroke-dasharray="18 14"/>
 <path d="M900 160 H704" fill="none" stroke="#4a90ff" stroke-width="9" stroke-linecap="round" class="flow" stroke-dasharray="18 14"/>
 <path d="M704 182 H900" fill="none" stroke="#a7adb4" stroke-width="9" stroke-linecap="round" class="flow" stroke-dasharray="18 14"/>
</g>{lab}"""


def svg(body, vb="60 85 790 520"):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


S1 = svg(house() + ducts(op="0.55"))

stale = "".join(
    f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#8b8f95" opacity=".5" filter="url(#blur8)" class="pulse"/>'
    for x, y, rx, ry in [(320, 260, 90, 40), (600, 260, 90, 40), (330, 450, 100, 48), (610, 440, 100, 48)])
co2 = "".join(f'<text x="{x}" y="{y}" font-size="34" fill="#4f545a" class="rise">CO₂</text>'
              for x, y in [(300, 330), (380, 320), (590, 330), (310, 530), (620, 520), (400, 520)])
drops = "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#7cc4ff"/>'
                for x, y in [(199, 235), (198, 258), (200, 282), (199, 428), (198, 455), (200, 480), (761, 250), (760, 440)])
S2 = svg(house() + stale + co2 + drops +
         f'<text x="215" y="112" {LABEL}>окна закрыты — воздух стоит</text>')

waves = "".join(
    f'<path d="M150 {y} q-18 -14 -26 0 t-26 0 t-26 0" fill="none" stroke="#ff9a3c" stroke-width="7" stroke-linecap="round" class="flowr" stroke-dasharray="14 10"/>'
    for y in (420, 455, 490))
snow = "".join(f'<text x="{x}" y="{y}" font-size="30" fill="#e8f4ff" class="rise">✻</text>'
               for x, y in [(80, 330), (120, 360), (95, 410), (140, 290), (75, 250)])
S3 = svg(house(window_open=True) + waves + snow +
         f'<text x="230" y="585" {LABEL}>тепло уходит вместе с воздухом</text>')

S4 = svg(house() + ducts(labels=True))

core = """
<rect width="960" height="630" fill="#1c1f25"/>
<g stroke="rgba(255,255,255,.05)" stroke-width="2">""" + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="630"/>' for x in range(0, 960, 60)) + "".join(f'<line x1="0" y1="{y}" x2="960" y2="{y}"/>' for y in range(0, 630, 60)) + """</g>
<rect x="250" y="140" width="460" height="360" rx="22" fill="#cfd6dc" stroke="#8a949c" stroke-width="5"/>
<g transform="translate(480 320) rotate(45)"><rect x="-110" y="-110" width="220" height="220" fill="#e9eef1" stroke="#7c868e" stroke-width="4"/>
""" + "".join(f'<line x1="-110" y1="{y}" x2="110" y2="{y}" stroke="#9aa5ad" stroke-width="3"/>' for y in range(-90, 110, 22)) + """</g>
<path d="M40 320 H920" fill="none" stroke="url(#warmup)" stroke-width="16" stroke-linecap="round" class="flow" stroke-dasharray="26 18"/>
<path d="M480 30 V610" fill="none" stroke="url(#cooldown)" stroke-width="16" stroke-linecap="round" class="flow" stroke-dasharray="26 18"/>
""" + f"""<text x="40" y="290" {LABEL} font-size="30">с улицы</text>
<text x="770" y="290" {LABEL} font-size="30">в комнаты</text>
<text x="500" y="70" {LABEL} font-size="30">из комнат</text>
<text x="500" y="590" {LABEL} font-size="30">на улицу</text>"""
S5 = svg(core, vb="0 0 960 630")

late = f"""<line x1="208" y1="410" x2="470" y2="410" stroke="#ff5a4a" stroke-width="5" stroke-dasharray="14 10" class="pulse"/>
<text x="226" y="446" {LABEL}>потолок ниже</text>
<text x="215" y="112" {LABEL}>воздуховоды — в перекрытиях</text>"""
S6 = svg(house(dim_rooms=True) + ducts(glow=True) + late)

spec = {"scenes": [
    {"pill": "ИНЖЕНЕРИЯ ДОМА", "title": "Рекуперация", "sub": "Зачем она тёплому герметичному дому?", "dur": 6.5, "svg": S1},
    {"pill": "ПРОБЛЕМА", "title": "Дом не дышит сам", "sub": "Герметичные окна и пароизоляция почти не пускают воздух", "dur": 7.0, "svg": S2},
    {"pill": "А ЕСЛИ ОТКРЫТЬ ОКНО?", "title": "Тепло уходит на улицу", "sub": "Зимой вместе с воздухом теряешь отопление", "dur": 6.5, "svg": S3},
    {"pill": "РЕШЕНИЕ", "title": "Приток и вытяжка", "sub": "Свежий воздух — в комнаты, вытяжка — из кухни и санузлов", "dur": 7.0, "svg": S4},
    {"pill": "КАК РАБОТАЕТ", "title": "Рекуператор", "sub": "Уходящий воздух греет входящий, потоки не смешиваются", "dur": 7.0, "svg": S5},
    {"pill": "НО ЕСТЬ НЮАНС", "title": "Закладывают в проект", "sub": "Воздуховоды прячут в перекрытиях — после отделки поздно", "dur": 7.0, "svg": S6},
    {"cta": True, "pill": "БОЛЬШЕ РАЗБОРОВ", "title": "Сохрани ролик", "sub": "и подпишись. Разбираем инженерию премиум-домов", "dur": 7.0},
]}
json.dump(spec, open("rekuperaciya.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok", sum(s["dur"] for s in spec["scenes"]))
