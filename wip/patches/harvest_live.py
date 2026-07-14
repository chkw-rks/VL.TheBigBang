"""Harvest live-element subgraphs from wip/The Origin of Life.vl.

The prototype document contains one hand-built demo zone per (old-structure)
chapter, stacked vertically on the Application canvas, plus the type
definitions (MyRecord, MyClass, Particle*, ColoredCircle, ...). This module
extracts a zone's elements, pulls the type definitions it references
(transitively), keeps the links whose endpoints both survive, remaps every ID
to a fresh one, rewrites self-references to the target document name, and
translates coordinates to a target position.

Everything extracted was serialized by vvvv itself, so the structures are
known-good; only placement and identity change.
"""

import re
import uuid
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "The Origin of Life.vl"

# prototype zones by canvas y (from the per-chapter "Role:" pads);
# 39 and 40 split what was one combined mechanics chapter in the prototype
ZONES = {
    38: (-99999, 8400),
    39: (8400, 11800),
    40: (8400, 11800),
    41: (11800, 13900),
    42: (13900, 16900),
    43: (16900, 19800),
    44: (19800, 21900),
    45: (21900, 24400),
    46: (24400, 99999),
}

# LastDependency values that are real libraries and must NOT be rewritten
_LIB_DEPS = {"CoreLibBasics.vl", "Builtin", "Nodes.vl"}

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def _new_id() -> str:
    n = uuid.uuid4().int
    chars = []
    for _ in range(22):
        n, r = divmod(n, 62)
        chars.append(ALPHABET[r])
    return "".join(reversed(chars))


_BOUNDS = re.compile(r'Bounds="(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)((?:,-?\d+(?:\.\d+)?){0,2})"')


def _first_xy(text):
    m = _BOUNDS.search(text)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def _translate(text, dx, dy, first_line_only=False):
    def repl(m):
        x = int(round(float(m.group(1)) + dx))
        y = int(round(float(m.group(2)) + dy))
        return f'Bounds="{x},{y}{m.group(3)}"'
    if first_line_only:
        head, _, tail = text.partition("\n")
        return _BOUNDS.sub(repl, head, count=1) + ("\n" + tail if tail else "")
    return _BOUNDS.sub(repl, text)


class _Block:
    def __init__(self, text):
        self.text = text
        head, _, tail = text.lstrip().partition("\n")
        # definition = named Node whose NodeReference (before its inner Patch)
        # declares a *Definition choice
        pre_patch = text.split("<Patch", 1)[0]
        self.is_def = bool(re.search(
            r'Kind="(Record|Class|Container|Interface|Forward)Definition"', pre_patch))
        m = re.search(r'<Node Name="([^"]+)"', head)
        self.name = m.group(1) if self.is_def and m else None
        xy = _first_xy(text)
        self.x, self.y = xy if xy else (None, None)
        self.ids = set(re.findall(r'Id="([0-9A-Za-z]{22})"', text))
        self.is_role_pad = 'Value="Role:' in text
        # prototype-era prose (long comment IOBoxes) is superseded by the
        # drafts' text layer; short labels/annotations are kept
        vm = re.search(r'Value="([^"]*)"', text)
        self.is_prose_pad = (
            text.lstrip().startswith("<Pad ")
            and 'VL.Core.StringType">Comment<' in text
            and vm is not None and len(vm.group(1)) > 200
        )


def _scan_blocks(lines, start, end, indent):
    sp = " " * indent
    out = []
    i = start
    while i < end:
        ln = lines[i]
        if ln.startswith(sp + "<!--"):
            while i < end and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        if ln.startswith(sp + "<") and not ln.startswith(sp + "</"):
            tag = re.match(r"^\s*<([A-Za-z:._]+)", ln).group(1)
            if ln.rstrip().endswith("/>"):
                out.append("\n".join(lines[i:i + 1]))
                i += 1
                continue
            close = sp + f"</{tag}>"
            j = i + 1
            while j < end and lines[j].rstrip() != close:
                j += 1
            out.append("\n".join(lines[i:j + 1]))
            i = j + 1
            continue
        i += 1
    return out


def _load():
    lines = SRC.read_text(encoding="utf-8").splitlines()
    app = next(i for i, l in enumerate(lines) if '<Node Name="Application"' in l)
    app_indent = len(lines[app]) - len(lines[app].lstrip())
    patch_i = next(i for i in range(app, len(lines))
                   if lines[i].lstrip().startswith("<Patch "))
    canvas_i = next(i for i in range(patch_i, len(lines))
                    if lines[i].lstrip().startswith("<Canvas "))
    canvas_indent = len(lines[canvas_i]) - len(lines[canvas_i].lstrip())
    canvas_end = next(i for i in range(canvas_i, len(lines))
                      if lines[i].rstrip() == " " * canvas_indent + "</Canvas>")
    patch_end = next(i for i in range(canvas_end, len(lines))
                     if lines[i].rstrip() == " " * (canvas_indent - 2) + "</Patch>")

    blocks = [_Block(t) for t in
              _scan_blocks(lines, canvas_i + 1, canvas_end, canvas_indent + 2)]
    tail = _scan_blocks(lines, canvas_end + 1, patch_end, canvas_indent)
    links, slots = [], {}
    for t in tail:
        s = t.lstrip()
        if s.startswith("<Link "):
            m = re.search(r'Ids="([0-9A-Za-z]{22}),([0-9A-Za-z]{22})"', t)
            if m:
                links.append((t, m.group(1), m.group(2)))
        elif s.startswith("<Slot "):
            m = re.search(r'<Slot Id="([0-9A-Za-z]{22})"', t)
            if m:
                slots[m.group(1)] = t
    defs = {b.name: b for b in blocks if b.is_def and b.name}
    return blocks, links, slots, defs


def _refs(text, def_names):
    found = set()
    for n in def_names:
        if re.search(rf'Kind="(?:Record|Class)Type" Name="{re.escape(n)}"', text) \
           or re.search(rf'Kind="ProcessAppFlag" Name="{re.escape(n)}"', text):
            found.add(n)
    return found


def _remap_ids(text):
    tokens = set(re.findall(r'Id="([0-9A-Za-z]{22})"', text))
    for tok in tokens:
        text = text.replace(tok, _new_id())
    return text


def _rewrite_deps(text, target_fname):
    def repl(m):
        dep = m.group(1)
        if dep.startswith("VL.") or dep in _LIB_DEPS:
            return m.group(0)
        return f'LastDependency="{target_fname}"'
    return re.sub(r'LastDependency="([^"]+)"', repl, text)


def harvest(chnum, x0, y0, target_fname):
    """Return (canvas_xml, patch_xml, info) for the chapter's prototype zone."""
    if chnum not in ZONES or not SRC.exists():
        return "", "", None
    blocks, links, slots, defs = _load()
    lo, hi = ZONES[chnum]
    in_range = [b for b in blocks
                if not b.is_def and not b.is_role_pad
                and b.y is not None and lo <= b.y < hi]
    zone = [b for b in in_range if not b.is_prose_pad]
    prose_dropped = len(in_range) - len(zone)
    if not zone:
        return "", "", None

    # transitive closure of referenced local type definitions
    def_names = set(defs)
    needed, frontier = set(), set()
    for b in zone:
        frontier |= _refs(b.text, def_names)
    while frontier:
        n = frontier.pop()
        if n in needed:
            continue
        needed.add(n)
        frontier |= _refs(defs[n].text, def_names) - needed

    # translate zone to target position, stack defs to the right of it
    minx = min(b.x for b in zone)
    miny = min(b.y for b in zone)
    maxx = max(b.x for b in zone)
    dx, dy = x0 - minx, y0 - miny
    parts = [_translate(b.text, dx, dy) for b in zone]
    def_x = int(x0 + (maxx - minx) + 260)
    for i, n in enumerate(sorted(needed)):
        parts.append(_translate(defs[n].text, def_x - defs[n].x,
                                y0 + i * 60 - defs[n].y, first_line_only=True))

    kept_ids = set()
    for b in zone:
        kept_ids |= b.ids
    for n in needed:
        kept_ids |= defs[n].ids

    # app slots referenced by surviving pads
    slot_parts = []
    for sid, stext in slots.items():
        if re.search(rf'SlotId="{sid}"', "\n".join(parts)):
            slot_parts.append(stext)
            kept_ids |= set(re.findall(r'Id="([0-9A-Za-z]{22})"', stext))

    link_parts = [t for (t, a, b) in links if a in kept_ids and b in kept_ids]
    dropped = sum(1 for (t, a, b) in links
                  if (a in kept_ids) != (b in kept_ids))

    combined = _remap_ids("\n".join(parts + ["---SPLIT---"] + slot_parts + link_parts))
    combined = _rewrite_deps(combined, target_fname)
    # house typography: the published chapters never use em-dashes
    combined = combined.replace(" — ", " - ").replace("—", " - ")
    canvas_xml, _, patch_xml = combined.partition("---SPLIT---")
    info = {"elements": len(zone), "defs": sorted(needed),
            "links": len(link_parts), "links_dropped": dropped,
            "slots": len(slot_parts), "prose_dropped": prose_dropped}
    return canvas_xml.strip("\n"), patch_xml.strip("\n"), info
