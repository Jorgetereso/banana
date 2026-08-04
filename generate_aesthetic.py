"""Generate 10 aesthetic/lighting variations of a Banana Airways cabin frame.

Image-to-image via OpenAI gpt-image-1 (images.edit): keeps the SAME characters,
composition, camera and objects — only changes lighting / mood / style.

Usage:
    export OPENAI_API_KEY=sk-...            # never commit this
    python3 generate_aesthetic.py [source_image]

Source defaults to assets/FRAMES/cabin.png. Outputs to assets/AESTHETIC/NN-name.png.
"""
import os, sys, json, base64, mimetypes, threading, traceback
import urllib.request

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("ERROR: OPENAI_API_KEY not set in env"); sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "assets", "FRAMES", "cabin.png")
OUT_DIR = os.path.join(HERE, "assets", "AESTHETIC")
os.makedirs(OUT_DIR, exist_ok=True)

if not os.path.exists(SRC):
    print(f"ERROR: source frame not found at {SRC}"); sys.exit(1)

URL = "https://api.openai.com/v1/images/edits"
MODEL = "gpt-image-2"   # Jorge's rule: ALWAYS gpt-image-2, NEVER gpt-image-1
SIZE = "1536x1024"   # landscape, close to the cabin's 16:9

KEEP = (
    "Keep the EXACT same characters, their exact designs, poses, positions, the exact "
    "camera angle, framing, seats, luggage and every object identical to the input image. "
    "Do NOT redesign, move, add or remove anything. This is a relight / restyle only — "
    "change ONLY the lighting, mood, color grade and surface rendering as described. "
    "First-person cabin view of the BANANA AIRWAYS low-cost airline. No UI, no text overlays."
)

LOOKS = [
    ("01-fotorrealista", "Photorealistic relight: physically-based materials, soft realistic global illumination, "
        "natural window daylight, subtle ambient occlusion, believable fabric and plastic surfaces, gentle depth of field."),
    ("02-golden-hour", "Warm golden-hour sunrise pouring through the cabin windows, long soft orange light, "
        "dust motes in the sunbeams, cozy amber glow, gentle lens flare."),
    ("03-terror", "Horror version: dark, desaturated, thick volumetric fog, a single pulsing red emergency light, "
        "deep shadows, eerie cold rim light, a sense of dread, cinematic low-key lighting."),
    ("04-noir", "Film-noir black and white, hard high-contrast key light, dramatic venetian shadows, "
        "deep blacks, glossy speculars, moody 1940s cinematography."),
    ("05-neon-cyberpunk", "Neon cyberpunk lighting: magenta and cyan light sources, wet reflective surfaces, "
        "glowing signage bounce light, hazy atmosphere, Blade Runner mood."),
    ("06-comic-cel", "Comic / cel-shaded style: bold black outlines, flat vibrant colors, halftone shading, "
        "graphic-novel ink look, punchy saturated palette."),
    ("07-claymation", "Premium claymation / stop-motion look: soft studio lighting, visible fingerprints and "
        "clay texture, shallow macro depth of field, Aardman-quality tactile handcrafted surfaces."),
    ("08-chernobyl", "Toxic Chernobyl atmosphere: sickly green-yellow radioactive haze, floating dust, peeling "
        "decayed surfaces, grimy overcast light, unsettling abandoned mood."),
    ("09-tormenta", "Electric night thunderstorm outside the windows: hard intermittent lightning flashes lighting "
        "the cabin in stark bursts, cold blue ambient, rain streaks on the glass, dramatic contrast."),
    ("10-aaa-sobrio", "Clean AAA studio render: balanced neutral three-point studio lighting, crisp materials, "
        "polished professional game-cinematic presentation, tasteful bloom, no gimmicks."),
]


def build_multipart(fields, files):
    boundary = "----bananaform7f3b2a"
    body = b""
    for k, v in fields.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    for k, path in files.items():
        fn = os.path.basename(path)
        ctype = mimetypes.guess_type(path)[0] or "image/png"
        with open(path, "rb") as f:
            data = f.read()
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fn}\"\r\n"
                 f"Content-Type: {ctype}\r\n\r\n").encode()
        body += data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, boundary


def generate(slug, style, results):
    prompt = style + "\n\n" + KEEP
    fields = {"model": MODEL, "prompt": prompt, "size": SIZE, "n": "1"}
    files = {"image": SRC}
    body, boundary = build_multipart(fields, files)
    req = urllib.request.Request(URL, data=body, method="POST", headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    })
    try:
        print(f"  [{slug}] generating…", flush=True)
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.loads(r.read())
        b64 = resp["data"][0]["b64_json"]
        out = os.path.join(OUT_DIR, slug + ".png")
        with open(out, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  [{slug}] ✓ saved → {out}", flush=True)
        results[slug] = "ok"
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")[:400]
        print(f"  [{slug}] HTTP {e.code}: {msg}", flush=True)
        results[slug] = f"http{e.code}"
    except Exception:
        traceback.print_exc()
        results[slug] = "exception"


def main():
    print(f"Source: {SRC}")
    print(f"Generating {len(LOOKS)} looks → {OUT_DIR}\n")
    results = {}
    # Run in small batches of 3 to respect rate limits
    threads = []
    for i, (slug, style) in enumerate(LOOKS):
        t = threading.Thread(target=generate, args=(slug, style, results), daemon=True)
        threads.append(t)
    running = []
    for t in threads:
        t.start(); running.append(t)
        if len(running) >= 3:
            running[0].join(); running.pop(0)
    for t in running:
        t.join()
    print("\n===== SUMMARY =====")
    for slug, _ in LOOKS:
        print(f"  {slug:22s} {results.get(slug, 'missing')}")


if __name__ == "__main__":
    main()
