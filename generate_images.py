#!/usr/bin/env python3
"""Generate landing-page images via Gemini 2.5 Flash Image (Nano Banana) on OpenRouter."""
import base64, json, os, sys, urllib.request, urllib.error
from pathlib import Path

KEY = os.environ.get("OPENROUTER_API_KEY")
if not KEY:
    sys.exit("Missing OPENROUTER_API_KEY")

OUT = Path(__file__).parent / "photos"
OUT.mkdir(exist_ok=True)

PROMPTS = {
    "hero": (
        "Architectural editorial photograph of a contemporary smart office building interior in Europe, "
        "expansive floor-to-ceiling glazing, polished concrete floor, soft late-afternoon sun raking across "
        "minimalist furniture, designer pendant lighting, warm wood and matte black detailing, calm composition, "
        "deep tonal range, no people, no text, no logos, premium real-estate photography, 16:9 aspect ratio."
    ),
    "energie": (
        "Industrial editorial photograph of a modern mechanical plant room in a contemporary building, "
        "exposed silver HVAC ducting on a concrete ceiling, recessed LED strip lighting, clean polished concrete floor, "
        "geometric symmetry, soft cool daylight, no people, no text, no logos, premium architectural photography, 4:3 aspect ratio."
    ),
    "komfort": (
        "Architectural exterior photograph of a contemporary residential apartment building facade in Vienna, "
        "rhythmic balconies with floor-to-ceiling glass doors, clean horizontal lines, warm golden-hour sunlight, "
        "subtle reflections in the glazing, no people, no text, no logos, premium real-estate photography, 4:3 aspect ratio."
    ),
    "wartung": (
        "Editorial close-up photograph of a building maintenance engineer's hands holding a modern tablet showing a "
        "technical schematic of a heating system; in soft focus background a row of building utility equipment; "
        "warm directional industrial lighting; no faces visible, no text on screen, no logos, "
        "premium editorial photography, 4:3 aspect ratio."
    ),
    "luft": (
        "Architectural interior photograph of a calm modern living room with abundant natural daylight filtered through "
        "sheer linen curtains; healthy indoor plants on a low oak sideboard; minimalist neutral palette of warm beige and "
        "soft white; polished oak floor; no people, no text, no logos, premium interior magazine photography, 4:3 aspect ratio."
    ),
    "belegung": (
        "Architectural interior photograph of a contemporary open-plan coworking space, empty mid-morning, "
        "row of designer desks with laptops closed, beams of sunlight crossing the polished floor, "
        "warm wood and white walls, ceiling-mounted occupancy sensors visible discreetly, "
        "no people, no text, no logos, premium architectural photography, 4:3 aspect ratio."
    ),
    "sicherheit": (
        "Editorial product photograph of a modern keyless smart access pad mounted next to a sleek glass and brushed-steel office door, "
        "soft moody side lighting, shallow depth of field, subtle reflections, no people, no text, no logos, no buttons readable, "
        "premium product photography, 4:3 aspect ratio."
    ),
}

API = "https://openrouter.ai/api/v1/chat/completions"

def gen(name: str, prompt: str) -> Path:
    body = json.dumps({
        "model": "google/gemini-3.1-flash-image-preview",
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
    }).encode()

    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nichtagentur.github.io/enlivion/",
        "X-Title": "Enlivion landing page",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:400]}", file=sys.stderr)
        raise

    msg = data["choices"][0]["message"]
    images = msg.get("images") or []
    if not images:
        print(f"  no images in response. content={msg.get('content','')[:200]}", file=sys.stderr)
        raise RuntimeError("no image returned")

    img_url = images[0]["image_url"]["url"]
    if not img_url.startswith("data:"):
        raise RuntimeError(f"unexpected image url: {img_url[:100]}")
    header, b64 = img_url.split(",", 1)
    ext = "png" if "png" in header else "jpg"
    out = OUT / f"{name}.{ext}"
    out.write_bytes(base64.b64decode(b64))
    return out

if __name__ == "__main__":
    targets = sys.argv[1:] or list(PROMPTS.keys())
    for name in targets:
        if name not in PROMPTS:
            print(f"skip unknown: {name}")
            continue
        print(f"generating {name}...", flush=True)
        try:
            p = gen(name, PROMPTS[name])
            print(f"  -> {p} ({p.stat().st_size // 1024} KB)")
        except Exception as e:
            print(f"  FAILED: {e}")
