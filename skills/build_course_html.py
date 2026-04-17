#!/usr/bin/env python3
"""
Rebuild guitar-pedal-course-2 HTML in the tumo2026 style.
Uses pandoc for per-section markdown→HTML conversion, then applies
semantic class transformations matching the tumo2026 document structure.
"""

import os, re, subprocess, tempfile, html as htmllib

COURSE_PATH = "/Users/haigarmen/Documents/Agentic-Skills-Workshop/courses/guitar-pedal-course-2"
OUT_PATH = os.path.join(COURSE_PATH, "guitar-pedal-course-2-course-document.html")

# ── Course metadata ───────────────────────────────────────────────────────────

MODULES = [
    {
        "num": 1, "id": "01-foundations",
        "title": "Foundations — Electricity, Signal & Dirt",
        "desc": "Establish the conceptual and practical foundation: Ohm's Law, guitar signal anatomy, gain vs. distortion, hard vs. soft clipping, and diode forward voltage. Students leave with a working breadboard clipping demo circuit.",
        "lessons": [
            {"slug": "01-electricity-signal-and-dirt",          "title": "Electricity, Signal, and the Nature of Dirt", "type": "reading",     "mins": 30},
            {"slug": "02-session-1-clipping-demo-build",        "title": "Session 1 — The Clipping Demo Build",        "type": "hands-on",    "mins": 180},
        ]
    },
    {
        "num": 2, "id": "02-overdrive",
        "title": "Overdrive — The TS-808 Tubescreamer",
        "desc": "Soft clipping in the feedback path, TL072 op-amp gain, the mid hump, and schematic reading. Students breadboard the core clipping stage and solder a complete PCB clone.",
        "lessons": [
            {"slug": "01-ts808-soft-clipping-and-opamp-gain",   "title": "The TS-808 — Soft Clipping & Op-Amp Gain",  "type": "reading",     "mins": 30},
            {"slug": "02-session-2-build-ts808-clone",          "title": "Session 2 — Build the TS-808 Clone",        "type": "hands-on",    "mins": 180},
        ]
    },
    {
        "num": 3, "id": "03-distortion",
        "title": "Distortion — The ProCo RAT",
        "desc": "Hard clipping to ground, the LM308 op-amp, the reverse-wired filter control, and Dead Pedal Protocol troubleshooting. Students solder a complete RAT clone and leave with two working dirt pedals.",
        "lessons": [
            {"slug": "01-rat-hard-clipping-and-filter-topology","title": "The RAT — Hard Clipping & Filter Topology",  "type": "reading",     "mins": 30},
            {"slug": "02-session-3-build-rat-clone",            "title": "Session 3 — Build the RAT Clone",           "type": "hands-on",    "mins": 180},
        ]
    },
    {
        "num": 4, "id": "04-fuzz",
        "title": "Fuzz — The Tone Bender (Capstone)",
        "desc": "Transistor-based clipping, bias by ear, germanium vs. silicon, and full enclosure wiring. Students leave with a housed, playable Tone Bender fuzz — the course capstone.",
        "lessons": [
            {"slug": "01-tone-bender-transistor-clipping-and-biasing", "title": "The Tone Bender — Transistor Clipping & Biasing", "type": "reading",  "mins": 30},
            {"slug": "02-session-4-build-and-house-tone-bender",       "title": "Session 4 — Build & House the Tone Bender",       "type": "hands-on", "mins": 180},
        ]
    },
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def strip_frontmatter(text):
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            return text[end+4:].lstrip('\n')
    return text

def preprocess_md(md_text):
    """Fix markdown patterns that pandoc mis-parses without a blank line separator."""
    # Insert a blank line between a bold label (e.g. "**Label:**") and a following list,
    # so pandoc treats them as separate block elements instead of inline continuations.
    md_text = re.sub(r'(\*\*[^*]+\*\*:?)\n([-*])', r'\1\n\n\2', md_text)
    return md_text

def md_to_html(md_text):
    """Convert markdown text to HTML fragment via pandoc."""
    md_text = preprocess_md(md_text)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_text)
        tmp = f.name
    result = subprocess.run(
        ['pandoc', tmp, '--from', 'markdown', '--to', 'html', '--highlight-style=pygments'],
        capture_output=True, text=True
    )
    os.unlink(tmp)
    return result.stdout

def fix_mermaid(html):
    """Strip inner <code> wrapper and unescape entities in mermaid blocks."""
    def replacer(m):
        inner = m.group(1)
        inner = inner.replace('&quot;', '"').replace('--&gt;', '-->').replace('&#39;', "'").replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        inner = re.sub(r'^<code[^>]*>', '', inner.strip())
        inner = re.sub(r'</code>$', '', inner.strip())
        return f'<div class="mermaid">{inner}</div>'
    # Handle <pre class="mermaid"><code>...</code></pre>
    html = re.sub(r'<pre class="mermaid"><code>(.*?)</code></pre>', replacer, html, flags=re.DOTALL)
    # Handle <pre class="mermaid">...</pre> (already unwrapped)
    html = re.sub(r'<pre class="mermaid">(.*?)</pre>', lambda m: f'<div class="mermaid">{m.group(1)}</div>', html, flags=re.DOTALL)
    return html

def transform_session_headings(html):
    """Convert ### 0:00–0:20 — Title  headings to time-block layout."""
    def replacer(m):
        time_part = m.group(1).strip()   # e.g. "0:00–0:20"
        title_part = m.group(2).strip()  # e.g. "Introductions and Listening Exercise"
        return (
            f'<div class="time-block">'
            f'<div class="time-stamp">{htmllib.escape(time_part)}</div>'
            f'<div class="time-content"><strong>{htmllib.escape(title_part)}</strong>'
        )
    # Match ### TIME — Title patterns (various dash/dash chars)
    html = re.sub(
        r'<h3[^>]*>(\d+:\d+\s*[–\-—]+\s*\d+:\d+)\s*[–\-—]+\s*([^<]+)</h3>',
        replacer, html
    )
    # Close open time-content/time-block divs before the next time-block,
    # and after the final one.
    parts = re.split(r'(?=<div class="time-block">)', html)
    closed = []
    for i, part in enumerate(parts):
        if i > 0 and part.startswith('<div class="time-block">'):
            # close the previous time-content + time-block
            closed.append('</div></div>\n')
        closed.append(part)
    # Always close the last open time-block (the loop never closes it)
    if len(parts) > 1:
        closed.append('</div></div>\n')
    html = ''.join(closed)
    return html

def wrap_section(heading_id, heading_html, body_html, css_class, heading_override=None):
    """Wrap a heading + body in a semantic div with given CSS class."""
    inner_heading = heading_override or heading_html
    return f'<div class="{css_class}">{inner_heading}{body_html}</div>\n'

def process_lesson_html(raw_html, lesson_meta):
    """Apply all semantic transformations to a pandoc HTML fragment."""
    html = raw_html

    # Fix mermaid first
    html = fix_mermaid(html)

    # Fix task list checkboxes (- [ ] items)
    html = html.replace('<input type="checkbox" disabled="" />', '<input type="checkbox" disabled>')
    html = html.replace('<input type="checkbox" disabled="" checked="checked" />', '<input type="checkbox" disabled checked>')

    # Split into semantic sections by h2 headings
    # We'll process known section types specially
    sections = re.split(r'(<h2[^>]*>.*?</h2>)', html, flags=re.DOTALL)

    output = []
    i = 0
    while i < len(sections):
        chunk = sections[i]

        # Is it an h2 heading?
        h2_match = re.match(r'<h2[^>]*>(.*?)</h2>', chunk, re.DOTALL)
        if h2_match:
            heading_text = re.sub(r'<[^>]+>', '', h2_match.group(1)).strip()
            body = sections[i+1] if i+1 < len(sections) else ''
            i += 2

            slug = heading_text.lower()

            if 'learning objective' in slug:
                output.append(
                    f'<div class="objectives">'
                    f'<h4>Learning Objectives</h4>'
                    f'{body}'
                    f'</div>\n'
                )
            elif 'key takeaway' in slug:
                output.append(
                    f'<div class="takeaways">'
                    f'<h4>Key Takeaways</h4>'
                    f'{body}'
                    f'</div>\n'
                )
            elif slug == 'environment':
                # Convert to env-box paragraph
                output.append(
                    f'<div class="env-box">{body}</div>\n'
                )
            elif slug == 'materials':
                output.append(
                    f'<div class="materials-box">'
                    f'<h4>Materials</h4>'
                    f'{body}'
                    f'</div>\n'
                )
            elif slug == 'session plan':
                session_body = transform_session_headings(body)
                output.append(
                    f'<div class="session-plan">'
                    f'<h2>Session Plan</h2>'
                    f'{session_body}'
                    f'</div>\n'
                )
            elif slug == 'next steps':
                output.append(
                    f'<div class="next-steps">'
                    f'<h4>Next Steps</h4>'
                    f'{body}'
                    f'</div>\n'
                )
            elif slug == 'overview':
                output.append(f'<div class="lesson-overview">{body}</div>\n')
            else:
                # Generic section — keep as-is with h2
                output.append(f'<h2>{heading_text}</h2>\n{body}')
        else:
            output.append(chunk)
            i += 1

    return ''.join(output)

def lesson_path(mod, lesson):
    return os.path.join(COURSE_PATH, "modules", mod["id"], "lessons", lesson["slug"], "lesson.md")

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
  /* ── Fonts & Base ─────────────────────────────────────── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --black:   #0f0f0f;
    --ink:     #1a1a1a;
    --mid:     #555;
    --light:   #888;
    --rule:    #ddd;
    --bg-alt:  #f7f7f7;
    --accent:  #c0392b;
    --accent2: #7b1fa2;
    --green:   #00875a;
    --page-w:  740px;
  }

  html { font-size: 15px; }

  body {
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--ink);
    line-height: 1.65;
    background: #fff;
    max-width: var(--page-w);
    margin: 0 auto;
    padding: 0 2rem 4rem;
  }

  /* ── Cover Page ───────────────────────────────────────── */
  .cover {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4rem 0 6rem;
    border-bottom: 3px solid var(--black);
    margin-bottom: 3rem;
    page-break-after: always;
  }
  .cover-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.5rem;
  }
  .cover h1 {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--black);
    margin-bottom: 1.5rem;
  }
  .cover .subtitle {
    font-size: 1.15rem;
    color: var(--mid);
    max-width: 520px;
    margin-bottom: 3rem;
    line-height: 1.6;
  }
  .cover-meta {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    border-top: 1px solid var(--rule);
    padding-top: 2rem;
  }
  .cover-meta-item .label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--light);
    display: block;
    margin-bottom: 0.25rem;
  }
  .cover-meta-item .value {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--ink);
  }

  /* ── Table of Contents ────────────────────────────────── */
  .toc {
    margin-bottom: 3rem;
    page-break-after: always;
  }
  .toc h2 { margin-bottom: 1.5rem; }
  .toc ol { list-style: none; }
  .toc > ol > li {
    border-bottom: 1px dotted var(--rule);
    padding: 0.5rem 0;
  }
  .toc-module {
    font-weight: 600;
    color: var(--ink);
    font-size: 0.95rem;
  }
  .toc-lessons {
    list-style: none;
    margin-left: 1.5rem;
    margin-top: 0.2rem;
  }
  .toc-lessons li {
    color: var(--mid);
    font-size: 0.88rem;
    padding: 0.15rem 0;
  }
  .toc-lessons li .badge {
    color: var(--accent);
    font-weight: 500;
    font-size: 0.78rem;
    margin-right: 0.4em;
  }

  /* ── Typography ───────────────────────────────────────── */
  h1 { font-size: 2rem; font-weight: 700; line-height: 1.15; color: var(--black); margin-bottom: 0.75rem; }
  h2 { font-size: 1.25rem; font-weight: 600; color: var(--black); margin: 2rem 0 0.75rem; padding-bottom: 0.4rem; border-bottom: 2px solid var(--rule); }
  h3 { font-size: 1rem; font-weight: 600; color: var(--ink); margin: 1.5rem 0 0.4rem; }
  h4 { font-size: 0.88rem; font-weight: 600; color: var(--mid); margin: 1rem 0 0.3rem; text-transform: uppercase; letter-spacing: 0.05em; }

  p { margin-bottom: 0.8rem; }
  em { color: var(--ink); font-style: italic; }
  strong { font-weight: 600; }

  ul, ol { margin: 0.5rem 0 0.8rem 1.4rem; }
  li { margin-bottom: 0.3rem; }
  li::marker { color: var(--accent); }

  a { color: var(--accent2); text-decoration: none; }
  hr { border: none; border-top: 1px solid var(--rule); margin: 2rem 0; }

  /* ── Code ─────────────────────────────────────────────── */
  code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    background: var(--bg-alt);
    padding: 0.1em 0.35em;
    border-radius: 3px;
    color: var(--accent2);
  }
  pre {
    background: #1a1a2e;
    color: #e8e8f0;
    padding: 1.1rem 1.2rem;
    border-radius: 6px;
    overflow-x: auto;
    margin: 0.8rem 0 1rem;
    font-size: 0.82rem;
    line-height: 1.55;
  }
  pre code {
    background: none;
    color: inherit;
    padding: 0;
    font-size: inherit;
  }

  /* ── Callouts / Blockquotes ──────────────────────────── */
  blockquote {
    border-left: 3px solid var(--accent);
    background: #fff5f4;
    padding: 0.8rem 1rem;
    margin: 1rem 0;
    border-radius: 0 4px 4px 0;
    font-size: 0.92rem;
    color: var(--ink);
  }
  blockquote strong { color: var(--accent); }

  /* ── Tables ───────────────────────────────────────────── */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.8rem 0 1rem;
    font-size: 0.88rem;
  }
  th {
    background: var(--black);
    color: #fff;
    font-weight: 600;
    text-align: left;
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
    letter-spacing: 0.04em;
  }
  td {
    padding: 0.45rem 0.75rem;
    border-bottom: 1px solid var(--rule);
    vertical-align: top;
  }
  tr:nth-child(even) td { background: var(--bg-alt); }

  /* ── Mermaid Diagrams ─────────────────────────────────── */
  .mermaid {
    background: var(--bg-alt);
    border: 1px solid var(--rule);
    border-radius: 6px;
    padding: 1rem;
    margin: 0.8rem 0 1rem;
    text-align: center;
  }

  /* ── Module & Lesson Structure ────────────────────────── */
  .module-header {
    background: var(--black);
    color: #fff;
    padding: 2rem 2rem 1.5rem;
    margin: 3rem -2rem 2rem;
    page-break-before: always;
  }
  .module-header .module-number {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    display: block;
    margin-bottom: 0.5rem;
  }
  .module-header h2 {
    font-size: 1.6rem;
    color: #fff;
    border: none;
    margin: 0 0 0.5rem;
    padding: 0;
  }
  .module-header .module-desc {
    color: #aaa;
    font-size: 0.92rem;
    max-width: 560px;
    margin: 0;
  }

  .lesson-header {
    margin: 2.5rem 0 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--rule);
  }
  .lesson-header .type-badge {
    display: inline-block;
    background: var(--accent);
    color: #fff;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2em 0.6em;
    border-radius: 3px;
    margin-bottom: 0.5rem;
  }
  .lesson-header h3 {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--black);
    margin: 0 0 0.4rem;
  }
  .lesson-meta {
    display: flex;
    gap: 1.5rem;
    font-size: 0.8rem;
    color: var(--light);
  }

  /* ── Semantic Boxes ──────────────────────────────────── */
  .lesson-overview {
    font-size: 0.95rem;
    color: var(--mid);
    margin-bottom: 1.5rem;
    line-height: 1.7;
    border-left: 3px solid var(--rule);
    padding-left: 1rem;
  }
  .lesson-overview p { margin-bottom: 0; }

  .objectives {
    background: #f0f4ff;
    border: 1px solid #c0cff7;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
  }
  .objectives h4 { color: var(--accent2); margin-top: 0; }
  .objectives ul { margin-bottom: 0; }
  .objectives li { color: var(--ink); font-size: 0.9rem; }
  .objectives input[type="checkbox"] { accent-color: var(--accent2); margin-right: 0.4em; }

  .env-box {
    background: #f4fef4;
    border: 1px solid #b6e0b6;
    border-left: 3px solid var(--green);
    border-radius: 0 6px 6px 0;
    padding: 0.8rem 1.1rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
  }
  .env-box p:last-child { margin-bottom: 0; }
  .env-box::before {
    content: "Environment";
    display: block;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 0.4rem;
  }

  .materials-box {
    background: #fffbf0;
    border: 1px solid #e8d89e;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
  }
  .materials-box h4 { color: #8a6000; margin-top: 0; }
  .materials-box p:last-child, .materials-box ul:last-child { margin-bottom: 0; }

  .takeaways {
    background: var(--black);
    color: #fff;
    padding: 1rem 1.3rem;
    border-radius: 6px;
    margin: 1.5rem 0 0.5rem;
  }
  .takeaways h4 { color: var(--accent); margin-top: 0; }
  .takeaways li { color: #ddd; font-size: 0.88rem; margin-bottom: 0.4rem; }
  .takeaways li::marker { color: var(--accent); }
  .takeaways strong { color: #fff; }

  .next-steps {
    background: var(--bg-alt);
    border: 1px solid var(--rule);
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.9rem;
  }
  .next-steps h4 { color: var(--mid); margin-top: 0; }
  .next-steps p:last-child { margin-bottom: 0; }

  /* ── Session Plan ─────────────────────────────────────── */
  .session-plan h2 {
    font-size: 1.1rem;
    border-bottom-color: var(--accent);
    color: var(--accent);
  }
  .session-plan h3 { color: var(--ink); font-size: 0.92rem; margin: 1.2rem 0 0.3rem; }

  .time-block {
    display: flex;
    gap: 1rem;
    margin: 0.8rem 0;
    padding: 0.5rem 0;
    border-top: 1px dotted var(--rule);
  }
  .time-stamp {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--accent);
    font-weight: 600;
    white-space: nowrap;
    padding-top: 0.1rem;
    min-width: 86px;
  }
  .time-content { flex: 1; }
  .time-content p:first-child { margin-top: 0; }
  .time-content p:last-child { margin-bottom: 0; }

  /* ── Task lists ───────────────────────────────────────── */
  input[type="checkbox"] { accent-color: var(--accent2); margin-right: 0.4em; }
  .task-list-item { list-style: none; margin-left: -1.4rem; }

  /* ── Print ────────────────────────────────────────────── */
  @media print {
    body { max-width: 100%; padding: 0; font-size: 10.5pt; }
    .cover { min-height: auto; padding: 3rem 2rem 4rem; }
    .cover h1 { font-size: 2.2rem; }
    .module-header { margin: 2rem 0 1.5rem; padding: 1.5rem; page-break-before: always; }
    pre { font-size: 8pt; }
    .mermaid { break-inside: avoid; }
    blockquote { break-inside: avoid; }
    .lesson-header { break-after: avoid; }
    h2, h3 { break-after: avoid; }
    .takeaways { break-inside: avoid; }
  }
"""

# ── Build HTML ────────────────────────────────────────────────────────────────

parts = []

# Head
parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dirt: Build Your Own Overdrive, Distortion &amp; Fuzz — Course Document</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad: true, theme: 'neutral', fontSize: 13 }});</script>
<style>
{CSS}
</style>
</head>
<body>
""")

# Cover
parts.append("""
<div class="cover">
  <div class="cover-label">Course Document · v1.0</div>
  <h1>Dirt:<br>Overdrive,<br>Distortion &amp; Fuzz</h1>
  <p class="subtitle">A 4-week in-person guitar pedal building course. Students build three complete working circuits — a TS-808 Tubescreamer clone, a ProCo RAT clone, and a Tone Bender fuzz — while developing a practical foundation in electronics, signal flow, and circuit topology.</p>
  <div class="cover-meta">
    <div class="cover-meta-item"><span class="label">Format</span><span class="value">In-Person Workshop</span></div>
    <div class="cover-meta-item"><span class="label">Duration</span><span class="value">4 Weeks · 3 hrs/week</span></div>
    <div class="cover-meta-item"><span class="label">Total Hours</span><span class="value">12 hours</span></div>
    <div class="cover-meta-item"><span class="label">Prerequisites</span><span class="value">None — guitar playing only</span></div>
    <div class="cover-meta-item"><span class="label">Disciplines</span><span class="value">Electronics · Guitar · Analog Circuits · Soldering</span></div>
    <div class="cover-meta-item"><span class="label">Final Output</span><span class="value">Housed Tone Bender + 2 PCBs</span></div>
  </div>
</div>
""")

# TOC
parts.append('<div class="toc">\n<h2>Contents</h2>\n<ol>\n')
for mod in MODULES:
    parts.append(f'  <li>\n    <div class="toc-module">Module {mod["num"]} — {htmllib.escape(mod["title"])}</div>\n')
    parts.append('    <ol class="toc-lessons">\n')
    for i, lesson in enumerate(mod["lessons"]):
        badge = "Reading" if lesson["type"] == "reading" else "Hands-On"
        parts.append(f'      <li><span class="badge">{badge}</span>{htmllib.escape(lesson["title"])}</li>\n')
    parts.append('    </ol>\n  </li>\n')
parts.append('</ol>\n</div>\n')

# Modules and lessons
total_lessons = 0
for mod in MODULES:
    # Module header
    parts.append(f"""
<div class="module-header">
  <span class="module-number">Module {mod["num"]}</span>
  <h2>{htmllib.escape(mod["title"])}</h2>
  <p class="module-desc">{htmllib.escape(mod["desc"])}</p>
</div>
""")

    for lesson in mod["lessons"]:
        total_lessons += 1
        lpath = os.path.join(COURSE_PATH, "modules", mod["id"], "lessons", lesson["slug"], "lesson.md")

        with open(lpath) as f:
            raw = f.read()

        body_md = strip_frontmatter(raw)

        # Convert to HTML via pandoc
        body_html = md_to_html(body_md)

        # Apply transformations
        body_html = process_lesson_html(body_html, lesson)

        # Lesson header
        badge_text = "Reading" if lesson["type"] == "reading" else "Hands-On Session"
        mins = lesson["mins"]
        mins_label = f"{mins} min" if mins < 60 else f"{mins//60} hr" + ("s" if mins//60 > 1 else "")

        parts.append(f"""<div class="lesson-header">
  <span class="type-badge">{badge_text}</span>
  <h3>{htmllib.escape(lesson["title"])}</h3>
  <div class="lesson-meta">
    <span>⏱ {mins_label}</span>
    <span>Module {mod["num"]}</span>
  </div>
</div>
""")
        parts.append(body_html)
        parts.append('\n')

# Closing
parts.append("""
<hr>
<p style="text-align:center; color: var(--light); font-size: 0.82rem; margin-top: 3rem;">
  <em>End of course handbook. Dirt: Build Your Own Overdrive, Distortion &amp; Fuzz.</em>
</p>
</body>
</html>
""")

html_out = ''.join(parts)

with open(OUT_PATH, 'w') as f:
    f.write(html_out)

size = os.path.getsize(OUT_PATH)
print(f"Written: {OUT_PATH}")
print(f"Size: {size:,} bytes ({size//1024} KB)")
print(f"Modules: {len(MODULES)}, Lessons: {total_lessons}")
