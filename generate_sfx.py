"""Generate Banana Airways sound effects via ElevenLabs API.

Reads sfx_list.txt, generates one mp3 per entry into assets/SFX/,
and rebuilds sfx.html with grouped <audio> players.

Usage:
    python generate_sfx.py                 # generate any missing mp3s + rebuild html
    python generate_sfx.py --force         # regenerate every mp3 from scratch
    python generate_sfx.py --only <id>     # regenerate a single entry by id
    python generate_sfx.py --html-only     # skip API calls, just rebuild html
"""
import os
import sys
import json
import html
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.abspath(__file__))
LIST_PATH = os.path.join(ROOT, "sfx_list.txt")
OUT_DIR = os.path.join(ROOT, "assets", "SFX")
HTML_PATH = os.path.join(ROOT, "sfx.html")

API_URL = "https://api.elevenlabs.io/v1/sound-generation"
API_KEY = os.environ.get("ELEVENLABS_API_KEY")
MAX_CONCURRENT = 3

os.makedirs(OUT_DIR, exist_ok=True)


def parse_list(path):
    entries = []
    with open(path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                print(f"  warn: line {line_no} has {len(parts)} fields, skipping: {line[:60]}")
                continue
            cat, sfx_id, prompt, dur = parts
            try:
                dur_f = float(dur)
            except ValueError:
                print(f"  warn: line {line_no} bad duration '{dur}', skipping")
                continue
            entries.append({
                "category": cat,
                "id": sfx_id,
                "prompt": prompt,
                "duration": dur_f,
                "filename": f"{cat}_{sfx_id}.mp3",
            })
    return entries


def generate_one(entry, force=False):
    out_path = os.path.join(OUT_DIR, entry["filename"])
    if os.path.exists(out_path) and not force:
        return entry["id"], "skip (exists)"
    if not API_KEY:
        return entry["id"], "FAIL (no ELEVENLABS_API_KEY in env)"
    body = json.dumps({
        "text": entry["prompt"],
        "duration_seconds": entry["duration"],
        "prompt_influence": 0.5,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        return entry["id"], f"FAIL HTTP {e.code} — {e.read()[:200].decode('utf-8','ignore')}"
    except Exception as e:
        return entry["id"], f"FAIL {type(e).__name__}: {e}"
    with open(out_path, "wb") as f:
        f.write(data)
    return entry["id"], f"ok ({len(data)//1024} KB, {time.time()-t0:.1f}s)"


def render_html(entries):
    by_cat = {}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)

    cat_sections = []
    for cat in sorted(by_cat):
        items_html = []
        for e in by_cat[cat]:
            mp3_rel = f"assets/SFX/{e['filename']}"
            exists = os.path.exists(os.path.join(OUT_DIR, e["filename"]))
            missing_badge = "" if exists else '<span class="sfx__missing">no audio yet</span>'
            items_html.append(f"""
        <article class="sfx" data-id="{html.escape(e['id'])}">
          <div class="sfx__head">
            <span class="sfx__id">{html.escape(e['id'])}</span>
            <span class="sfx__dur">{e['duration']:g}s</span>
          </div>
          <pre class="sfx__prompt" tabindex="0" title="Click to copy">{html.escape(e['prompt'])}</pre>
          <audio controls preload="none" src="{mp3_rel}"></audio>
          {missing_badge}
        </article>""")
        cat_sections.append(f"""
    <section class="cat">
      <h2 class="cat__h">{html.escape(cat)}</h2>
      <div class="sfx-grid">{''.join(items_html)}
      </div>
    </section>""")

    total = len(entries)
    cats = len(by_cat)
    body = "".join(cat_sections) or '<p class="empty">Lista vacía — agregá entradas en <code>sfx_list.txt</code>.</p>'

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>SFX Library · Banana Airways</title>
<meta name="robots" content="noindex, nofollow" />
<meta name="description" content="Librería interna de sound effects para Banana Airways." />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Bungee&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />

<link rel="stylesheet" href="sfx.css" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%94%8A%3C/text%3E%3C/svg%3E" />
</head>
<body>

<header class="topbar">
  <a class="topbar__brand" href="https://3dar.com" target="_blank" rel="noopener" title="3DAR">
    <span class="topbar__b">B</span>
    <span class="topbar__txt">BANANA<br>AIRWAYS</span>
  </a>
  <span class="topbar__tag">INTERNO · SFX LIBRARY</span>
  <span class="topbar__stats">{total} sfx · {cats} categorías</span>
</header>

<main class="memo">
  <article>
    <div class="memo__meta">ElevenLabs Sound Effects · auto-generated</div>
    <h1 class="memo__h1">SFX<br>Library</h1>
    <p class="memo__lead">
      Catálogo interno de sound effects generados con
      <a href="https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert" target="_blank" rel="noopener">ElevenLabs Sound Effects API</a>.
      Edita <code>sfx_list.txt</code> y corré <code>python generate_sfx.py</code> para agregar o regenerar.
      Click en el prompt para copiarlo.
    </p>
    {body}

    <footer class="memo__foot">
      <span>Interno · Banana Airways · by <a href="https://3dar.com" target="_blank" rel="noopener">3DAR</a></span>
      <span>noindex · nofollow</span>
    </footer>
  </article>
</main>

<script>
  document.querySelectorAll('.sfx__prompt').forEach(el => {{
    el.addEventListener('click', () => {{
      navigator.clipboard.writeText(el.textContent).then(() => {{
        el.classList.add('sfx__prompt--copied');
        setTimeout(() => el.classList.remove('sfx__prompt--copied'), 1100);
      }});
    }});
  }});
</script>

</body>
</html>
"""


def main():
    args = sys.argv[1:]
    force = "--force" in args
    html_only = "--html-only" in args
    only_id = None
    if "--only" in args:
        i = args.index("--only")
        if i + 1 < len(args):
            only_id = args[i + 1]

    entries = parse_list(LIST_PATH)
    print(f"loaded {len(entries)} entries from sfx_list.txt")

    if not html_only:
        targets = entries if only_id is None else [e for e in entries if e["id"] == only_id]
        if only_id and not targets:
            print(f"  warn: no entry with id '{only_id}'")
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as ex:
            futures = {ex.submit(generate_one, e, force or only_id is not None): e for e in targets}
            for fut in as_completed(futures):
                e = futures[fut]
                try:
                    sfx_id, status = fut.result()
                except Exception as exc:
                    sfx_id, status = e["id"], f"FAIL exception: {exc}"
                print(f"  [{e['category']}] {sfx_id:<28} {status}")

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(render_html(entries))
    print(f"wrote {HTML_PATH}")


if __name__ == "__main__":
    main()
