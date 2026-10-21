"""Генератор роликов «Аллигатор стройки» в стиле референса (1080x1920, 30 fps).

Использование: python3 render_video.py spec.json out.mp4 [--preview out_dir]
spec.json:
{
  "scenes": [
    {"pill": "ИНЖЕНЕРИЯ ДОМА", "title": "Рекуперация", "sub": "Зачем она…", "dur": 6.5,
     "svg": "<svg viewBox='0 0 960 630'>…</svg>"},
    …,
    {"cta": true, "pill": "БОЛЬШЕ РАЗБОРОВ", "title": "Сохрани ролик", "sub": "…", "dur": 7}
  ]
}
Анимация внутри SVG по классам:
  .flow  — бегущий пунктир (stroke-dasharray задайте сами, например "18 14")
  .flowr — бегущий пунктир в обратную сторону
  .pulse — мерцание прозрачности
  .rise  — медленно всплывает вверх и появляется заново
  .spin  — вращение вокруг своего центра (задайте style="transform-box:fill-box;transform-origin:center")
Маскот: mascot.png рядом со скриптом.
"""
import base64, json, pathlib, subprocess, sys, html
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
FPS = 30


def build_html(spec):
    mascot = base64.b64encode((HERE / "mascot.png").read_bytes()).decode()
    scenes = spec["scenes"]
    layers = []
    for i, s in enumerate(scenes):
        e = lambda k: html.escape(s.get(k, ""))
        if s.get("cta"):
            layers.append(f"""<div class="scene cta" id="s{i}">
  <img class="m-big" src="data:image/png;base64,{mascot}">
  <div class="pill p">{e('pill')}</div>
  <div class="title t">{e('title')}</div>
  <div class="sub u">{e('sub')}</div>
</div>""")
        else:
            layers.append(f"""<div class="scene" id="s{i}">
  <div class="pill p">{e('pill')}</div>
  <div class="title t" style="{'font-size:74px' if len(s.get('title',''))>18 else ''}">{e('title')}</div>
  <div class="sub u">{e('sub')}</div>
  <div class="card c">{s.get('svg', '')}</div>
</div>""")
    segs = "".join(f'<div class="seg"><i id="g{i}"></i></div>' for i in range(len(scenes)))
    durs = json.dumps([float(s["dur"]) for s in scenes])
    ctas = json.dumps([bool(s.get("cta")) for s in scenes])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{font-family:'Liberation Sans','Arial',sans-serif;font-weight:700;color:#fff;
 background:radial-gradient(ellipse 760px 900px at 540px 520px,rgba(214,150,30,.42),rgba(214,150,30,0) 70%),
 linear-gradient(#2a2d33,#16181d 70%,#0e1014);position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.035) 2px,transparent 2px);background-size:90px 90px}}
.hz{{position:absolute;left:0;right:0;height:36px;background:repeating-linear-gradient(-45deg,#f5c21b 0 26px,#141414 26px 52px)}}
.hz.top{{top:0}} .hz.bot{{bottom:0}}
.mascot{{position:absolute;left:399px;top:95px;width:284px;height:284px}}
.scene{{position:absolute;inset:0;opacity:0}}
.pill{{position:absolute;left:50%;top:416px;transform:translateX(-50%);background:#ffc61e;color:#111;font-size:38px;padding:14px 34px;border-radius:40px;white-space:nowrap;letter-spacing:.01em}}
.title{{position:absolute;left:40px;right:40px;top:500px;text-align:center;color:#ffc72c;font-size:88px;line-height:1.05;text-shadow:5px 5px 0 rgba(0,0,0,.55)}}
.sub{{position:absolute;left:90px;right:90px;top:670px;text-align:center;font-size:56px;line-height:1.36;text-shadow:4px 4px 0 rgba(0,0,0,.55)}}
.card{{position:absolute;left:55px;top:980px;width:970px;height:640px;border:5px solid #f5c21b;border-radius:24px;overflow:hidden;background:#20232a}}
.card svg{{width:100%;height:100%;display:block}}
.cta .m-big{{position:absolute;left:350px;top:150px;width:380px;height:380px}}
.cta .pill{{top:610px}} .cta .title{{top:720px;font-size:100px}} .cta .sub{{top:880px}}
.prog{{position:absolute;left:70px;right:70px;top:1640px;display:flex;gap:11px}}
.seg{{flex:1;height:13px;border-radius:7px;background:#3a3d44;overflow:hidden}}
.seg i{{display:block;height:100%;width:0;background:#f5c21b}}
svg text{{font-family:'Liberation Sans',Arial,sans-serif;font-weight:700}}
</style></head><body>
<div class="grid"></div>
<img class="mascot" id="mascot" src="data:image/png;base64,{mascot}">
{''.join(layers)}
<div class="prog">{segs}</div>
<div class="hz top"></div><div class="hz bot"></div>
<script>
const D={durs}, CTA={ctas};
const starts=[];let acc=0;for(const d of D){{starts.push(acc);acc+=d;}}
const TOTAL=acc;
const clamp=(x)=>Math.max(0,Math.min(1,x));
const ease=(x)=>1-Math.pow(1-clamp(x),3);
const scenes=D.map((_,i)=>document.getElementById('s'+i));
function render(t){{
  let idx=0;for(let i=0;i<D.length;i++){{if(t>=starts[i])idx=i;}}
  for(let i=0;i<D.length;i++){{
    const el=scenes[i];const lt=t-starts[i];
    let op=0;
    if(i===idx){{op=clamp(lt/0.35);const rem=D[i]-lt;if(i<D.length-1)op*=clamp(rem/0.25);}}
    el.style.opacity=op;
    if(op<=0)continue;
    const p=el.querySelector('.p'),ti=el.querySelector('.t'),u=el.querySelector('.u'),c=el.querySelector('.c');
    if(p)p.style.opacity=ease((lt-0.05)/0.3);
    if(ti){{const k=ease((lt-0.2)/0.4);ti.style.opacity=k;ti.style.transform=`translateY(${{(1-k)*36}}px)`;}}
    if(u){{const k=ease((lt-0.5)/0.4);u.style.opacity=k;u.style.transform=`translateY(${{(1-k)*24}}px)`;}}
    if(c){{const k=ease(lt/0.45);c.style.opacity=k;c.style.transform=`scale(${{0.965+0.035*k}})`;}}
    el.querySelectorAll('.flow').forEach(f=>f.style.strokeDashoffset=(-t*70).toFixed(1));
    el.querySelectorAll('.flowr').forEach(f=>f.style.strokeDashoffset=(t*70).toFixed(1));
    el.querySelectorAll('.pulse').forEach((f,j)=>f.style.opacity=(0.55+0.45*Math.sin(t*3+j)).toFixed(3));
    el.querySelectorAll('.rise').forEach((f,j)=>{{const ph=((t*28+j*37)%90);f.style.transform=`translateY(${{-ph}}px)`;f.style.opacity=(Math.sin(Math.PI*ph/90)).toFixed(3);}});
    el.querySelectorAll('.spin').forEach(f=>f.style.transform=`rotate(${{(t*120)%360}}deg)`);
  }}
  const m=document.getElementById('mascot');
  m.style.opacity=CTA[idx]?(1-clamp((t-starts[idx])/0.3)):1;
  m.style.transform=`scale(${{1+0.012*Math.sin(t*2.2)}})`;
  for(let i=0;i<D.length;i++){{
    const g=document.getElementById('g'+i);
    g.style.width=(i<idx?100:(i===idx?clamp((t-starts[i])/D[i])*100:0))+'%';
  }}
}}
window.TOTAL=TOTAL;
</script></body></html>"""


def main():
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = sys.argv[2]
    preview = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--preview" else None
    doc = build_html(spec)
    total = sum(float(s["dur"]) for s in spec["scenes"])
    n = int(round(total * FPS))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(doc)
        pg.wait_for_timeout(300)
        if preview:
            pathlib.Path(preview).mkdir(parents=True, exist_ok=True)
            starts, acc = [], 0.0
            for s in spec["scenes"]:
                starts.append(acc); acc += float(s["dur"])
            for i, st in enumerate(starts):
                pg.evaluate(f"render({st + float(spec['scenes'][i]['dur']) * 0.6})")
                pg.screenshot(path=f"{preview}/scene-{i+1:02d}.png")
            b.close(); return
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                               "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
                               "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                               "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
        for fr in range(n):
            pg.evaluate(f"render({fr / FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close(); ff.wait()
        b.close()
    print(f"{out}: {n} frames, {total:.1f}s")


if __name__ == "__main__":
    main()
