#!/usr/bin/env python3
"""Generate Part V chapter .vl files (text layer + live-element placeholders)
from wip/part-v-chapter-drafts.md.

Parses the drafts' position markers (H1/H2/H3/Body/Link/Live element) and emits
one .vl document per chapter into wip/patches/, using the house scaffold cloned
from the existing help chapters (top strip, dependencies, Application process).

Layout follows the house conventions measured from the finished Part IV
chapters: all body pads are 400 px wide (font 9, ~60 chars/line, 19 px/line);
blocks the drafts mark as full-width are split paragraph-wise across the three
columns; a per-column flow keeps pads from overlapping (the drafts' y values
are treated as minimums, not absolutes).

Run:  python3 generate_patches.py
"""

import re
import uuid
from pathlib import Path

import harvest_live

ROOT = Path(__file__).resolve().parent.parent  # wip/
DRAFTS = ROOT / "part-v-chapter-drafts.md"
OUTDIR = Path(__file__).resolve().parent

LANG_VERSION = "2025.7.3"

BODY_W = 400          # house body width (measured 386-402 in Part IV)
COL_XS = [92, 592, 1092, 1592]
GAP = 40              # vertical gap between flowed blocks
TOP_Y = 175           # first content row (below the title strip)

# ---------------------------------------------------------------- id helpers

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def new_id() -> str:
    n = uuid.uuid4().int
    chars = []
    for _ in range(22):
        n, r = divmod(n, 62)
        chars.append(ALPHABET[r])
    return "".join(reversed(chars))


# ---------------------------------------------------------------- xml helpers

def esc(text: str) -> str:
    """Escape for an XML attribute value, newlines as CRLF char refs."""
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    return text.replace("\n", "&#xD;&#xA;")


def est_height(text: str, width: int, font: int) -> int:
    """Estimate IOBox height, calibrated against the finished chapters."""
    px_per_char = {7: 4.6, 9: 6.7, 12: 8.4, 15: 10.5, 22: 15.0}[font]
    line_h = {7: 15, 9: 19, 12: 25, 15: 31, 22: 46}[font]
    cpl = max(10, int(width / px_per_char))
    lines = 0
    for para in text.split("\n"):
        if not para.strip():
            lines += 1
        else:
            lines += max(1, -(-len(para) // cpl))
    return lines * line_h + 6


def comment_pad(x, y, w, h, text, font, stringtype="Comment", showvalue=False):
    sv = "\n              <p:showvalue p:Type=\"Boolean\">true</p:showvalue>" if showvalue else ""
    return f"""          <Pad Id="{new_id()}" Bounds="{x},{y},{w},{h}" ShowValueBox="true" isIOBox="true" Value="{esc(text)}">
            <p:TypeAnnotation LastCategoryFullName="Primitive" LastDependency="VL.CoreLib.vl">
              <Choice Kind="TypeFlag" Name="String" />
            </p:TypeAnnotation>
            <p:ValueBoxSettings>
              <p:fontsize p:Type="Int32">{font}</p:fontsize>{sv}
              <p:stringtype p:Assembly="VL.Core" p:Type="VL.Core.StringType">{stringtype}</p:stringtype>
            </p:ValueBoxSettings>
          </Pad>"""


def top_strip(title: str):
    """The house header strip, positions cloned from the existing chapters."""
    title_w = max(482, len(title) * 13 + 30)
    return [
        comment_pad(72, 113, title_w, 46, title, 22),
        comment_pad(72, 86, 364, 25, "VL.TheBigBang", 12, showvalue=True),
        comment_pad(552, 86, 66, 15, "Made by chk", 7),
        comment_pad(617, 86, 140, 19, "https://www.3e8.studio", 7, "Link"),
        comment_pad(792, 86, 369, 15,
                    "If you find this material helpful, please consider supporting its development via", 7),
        comment_pad(1160, 86, 140, 19, "https://www.ko-fi.com/chk", 7, "Link"),
    ]


# ------------------------------------------------------- ch. 38 pilot (live)

PILOT_HEIGHT = 240  # vertical space the pilot occupies in the column flow


def ch38_live_elements(doc_filename: str, y0: int):
    """The Thing record definition + a wired Create call site (column 3).

    Structure cloned from the vvvv-serialized MyRecord in wip/The Origin of
    Life.vl. y0 is the flowed top of the block (input IOBox row).
    Returns (canvas_xml, patch_xml) to inject into the Application.
    """
    ids = {k: new_id() for k in (
        "defNode defPatch defCanvas padPos cpPos padSize cpSize createPatch "
        "procDef frag slotPos slotSize l1 l2 l3 l4 ioPos ioSize createNode "
        "ncPin cposPin csizePin coutPin dposPin dsizePin thingPad appSlot "
        "la lb lc"
    ).split()}
    canvas = f"""          <Node Name="Thing" Bounds="1300,{y0 + 10}" Id="{ids['defNode']}">
            <p:NodeReference>
              <Choice Kind="RecordDefinition" />
            </p:NodeReference>
            <Patch Id="{ids['defPatch']}">
              <Canvas Id="{ids['defCanvas']}" CanvasType="Group">
                <Pad Id="{ids['padPos']}" SlotId="{ids['slotPos']}" Bounds="150,210" />
                <ControlPoint Id="{ids['cpPos']}" Bounds="150,180" />
                <Pad Id="{ids['padSize']}" SlotId="{ids['slotSize']}" Bounds="280,210" />
                <ControlPoint Id="{ids['cpSize']}" Bounds="280,180" />
              </Canvas>
              <Patch Id="{ids['createPatch']}" Name="Create">
                <Pin Id="{ids['dposPin']}" Name="Position" Kind="InputPin" />
                <Pin Id="{ids['dsizePin']}" Name="Size" Kind="InputPin" />
              </Patch>
              <ProcessDefinition Id="{ids['procDef']}" IsHidden="true">
                <Fragment Id="{ids['frag']}" Patch="{ids['createPatch']}" Enabled="true" />
              </ProcessDefinition>
              <Slot Id="{ids['slotPos']}" Name="Position">
                <p:TypeAnnotation p:Type="TypeReference">
                  <Choice Kind="TypeFlag" Name="Vector2" />
                </p:TypeAnnotation>
              </Slot>
              <Slot Id="{ids['slotSize']}" Name="Size">
                <p:TypeAnnotation p:Type="TypeReference">
                  <Choice Kind="TypeFlag" Name="Float32" />
                </p:TypeAnnotation>
              </Slot>
              <Link Id="{ids['l1']}" Ids="{ids['dposPin']},{ids['cpPos']}" IsHidden="true" />
              <Link Id="{ids['l2']}" Ids="{ids['cpPos']},{ids['padPos']}" />
              <Link Id="{ids['l3']}" Ids="{ids['dsizePin']},{ids['cpSize']}" IsHidden="true" />
              <Link Id="{ids['l4']}" Ids="{ids['cpSize']},{ids['padSize']}" />
            </Patch>
          </Node>
          <Pad Id="{ids['ioPos']}" Comment="Position" Bounds="1104,{y0},45,28" ShowValueBox="true" isIOBox="true" Value="0, 0">
            <p:TypeAnnotation LastCategoryFullName="2D" LastDependency="VL.CoreLib.vl">
              <Choice Kind="TypeFlag" Name="Vector2" />
            </p:TypeAnnotation>
          </Pad>
          <Pad Id="{ids['ioSize']}" Comment="Size" Bounds="1176,{y0 + 38},35,15" ShowValueBox="true" isIOBox="true" Value="0.5">
            <p:TypeAnnotation LastCategoryFullName="Primitive" LastDependency="VL.CoreLib.vl">
              <Choice Kind="TypeFlag" Name="Float32" />
            </p:TypeAnnotation>
          </Pad>
          <Node Bounds="1102,{y0 + 86},51,26" Id="{ids['createNode']}">
            <p:NodeReference LastCategoryFullName="Main.Thing" LastDependency="{doc_filename}">
              <Choice Kind="NodeFlag" Name="Node" Fixed="true" />
              <CategoryReference Kind="RecordType" Name="Thing" />
              <Choice Kind="OperationCallFlag" Name="Create" />
            </p:NodeReference>
            <Pin Id="{ids['ncPin']}" Name="Node Context" Kind="InputPin" IsHidden="true" />
            <Pin Id="{ids['cposPin']}" Name="Position" Kind="InputPin" />
            <Pin Id="{ids['csizePin']}" Name="Size" Kind="InputPin" />
            <Pin Id="{ids['coutPin']}" Name="Output" Kind="StateOutputPin" />
          </Node>
          <Pad Id="{ids['thingPad']}" SlotId="{ids['appSlot']}" Bounds="1104,{y0 + 142}" />
{comment_pad(1180, y0 + 142, 300, 40, "< a Thing stored in a pad. Hover the link above to see the type in the tooltip.", 9)}"""
    patch = f"""        <Slot Id="{ids['appSlot']}" Name="Thing" />
        <Link Id="{ids['la']}" Ids="{ids['ioPos']},{ids['cposPin']}" />
        <Link Id="{ids['lb']}" Ids="{ids['ioSize']},{ids['csizePin']}" />
        <Link Id="{ids['lc']}" Ids="{ids['coutPin']},{ids['thingPad']}" />"""
    return canvas, patch


def document(title: str, pads: list, canvas_extra: str = "", patch_extra: str = "") -> str:
    pads_xml = "\n".join(pads)
    if canvas_extra:
        pads_xml += "\n" + canvas_extra
    patch_extra = patch_extra + "\n" if patch_extra else ""
    create_id, update_id = new_id(), new_id()
    return f"""<?xml version="1.0" encoding="utf-8"?>
<Document xmlns:p="property" xmlns:r="reflection" Id="{new_id()}" LanguageVersion="{LANG_VERSION}" Version="0.128">
  <NugetDependency Id="{new_id()}" Location="VL.CoreLib" Version="{LANG_VERSION}" />
  <Patch Id="{new_id()}">
    <Canvas Id="{new_id()}" DefaultCategory="Main" CanvasType="FullCategory" />
    <Node Name="Application" Bounds="100,100" Id="{new_id()}">
      <p:NodeReference>
        <Choice Kind="ContainerDefinition" Name="Process" />
        <CategoryReference Kind="Category" Name="Primitive" />
      </p:NodeReference>
      <Patch Id="{new_id()}">
        <Canvas Id="{new_id()}" CanvasType="Group">
{pads_xml}
        </Canvas>
        <Patch Id="{create_id}" Name="Create" />
        <Patch Id="{update_id}" Name="Update" />
        <ProcessDefinition Id="{new_id()}">
          <Fragment Id="{new_id()}" Patch="{create_id}" Enabled="true" />
          <Fragment Id="{new_id()}" Patch="{update_id}" Enabled="true" />
        </ProcessDefinition>
{patch_extra}      </Patch>
    </Node>
  </Patch>
  <NugetDependency Id="{new_id()}" Location="VL.Stride" Version="{LANG_VERSION}" />
  <NugetDependency Id="{new_id()}" Location="VL.Skia" Version="{LANG_VERSION}" />
  <DocumentDependency Id="{new_id()}" Location="../../include/Nodes.vl" />
  <DocumentDependency Id="{new_id()}" Location="../../VL.TheBigBang.vl" />
  <NugetDependency Id="{new_id()}" Location="VL.Stride.TextureFX" Version="{LANG_VERSION}" />
</Document>
"""


# ---------------------------------------------------------------- draft parser

MARKER = re.compile(
    r"^(?:\*\*|###\s*)(H1|H2|H3|Body|Link|Live element|Opening paragraph)\s*"
    r"\(([^)]*)\)\s*(?:\*\*|:\*\*|)\s*:?\s*(.*)$"
)
ATTR = re.compile(r"(font|x|y|width)\s*[=~ ]\s*~?(\d+)")


def parse_attrs(s: str) -> dict:
    return {k: int(v) for k, v in ATTR.findall(s)}


def parse_chapters(lines):
    chapters = []
    cur = None
    i = 0
    skip_mode = False
    warnings = []
    cur_x = 92

    def read_fence(j):
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and lines[j].strip().startswith("```"):
            body = []
            j += 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                body.append(lines[j].rstrip())
                j += 1
            return "\n".join(body).strip("\n"), j + 1
        return None, j

    while i < len(lines):
        line = lines[i]
        h = re.match(r"^# Chapter (\d+) — (.+)$", line)
        if h:
            cur = {"num": int(h.group(1)), "title": h.group(2).strip(), "blocks": []}
            chapters.append(cur)
            skip_mode = False
            cur_x = 92
            i += 1
            continue
        if cur is None:
            i += 1
            continue
        if line.startswith("## Notes"):
            skip_mode = True
            i += 1
            continue
        if line.startswith("## "):
            skip_mode = False
            if line.startswith("## Layout map"):
                _, i2 = read_fence(i + 1)
                i = i2
                continue
            i += 1
            continue
        if skip_mode:
            i += 1
            continue

        m = MARKER.match(line)
        if not m:
            if re.match(r"^\*\*(H\d|Body|Link|Live)", line):
                warnings.append(f"ch{cur['num']}: unparsed marker line {i+1}: {line[:90]}")
            i += 1
            continue

        kind, attrstr, rest = m.group(1), m.group(2), m.group(3).strip()
        attrs = parse_attrs(attrstr)
        if "x" in attrs:
            cur_x = attrs["x"]
        x = attrs.get("x", cur_x)
        y = attrs.get("y")
        width = attrs.get("width")
        font = attrs.get("font", 9)
        is_link = "Link" in attrstr

        inline = None
        im = re.match(r"^`(.*)`$", rest)
        if im:
            inline = im.group(1)

        i += 1
        if kind in ("H1", "Opening paragraph") or (kind == "Body" and inline is None):
            text, i = read_fence(i)
            if text is None:
                warnings.append(f"ch{cur['num']}: no fence after {kind} near line {i+1}")
                continue
        elif kind == "Live element":
            text = rest
        else:
            text = inline if inline is not None else rest
            if not text:
                warnings.append(f"ch{cur['num']}: empty {kind} at line {i}")
                continue

        cur["blocks"].append({
            "kind": kind, "x": x, "y": y, "width": width,
            "font": font, "link": is_link, "text": text,
        })
    return chapters, warnings


# ---------------------------------------------------------------- layout flow

def col_of(x: int) -> int:
    return min(range(len(COL_XS)), key=lambda i: abs(COL_XS[i] - x))


def split_paragraphs(text: str, n: int = 3):
    """Split multi-paragraph text into up to n consecutive groups."""
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    n = min(n, len(paras))
    if n <= 1:
        return [text]
    base, extra = divmod(len(paras), n)
    groups, idx = [], 0
    for g in range(n):
        take = base + (1 if g < extra else 0)
        groups.append("\n\n".join(paras[idx:idx + take]))
        idx += take
    return groups


def emit_chapter(ch):
    title_text = None
    items = []  # (draft_y, seq, col, span_groups | single item)
    seq = 0
    pilot = None

    for b in ch["blocks"]:
        kind, text = b["kind"], b["text"]
        if kind == "H1":
            title_text = text.replace(" & ", " and ")
            continue
        if b["y"] is None:
            continue
        seq += 1
        col = col_of(b["x"])
        full_width = (b["width"] or 0) > 600

        if kind == "Live element" and ch["num"] == 38 and b["x"] == 1092 and b["y"] == 750:
            items.append((b["y"], seq, [("PILOT", col, None, None)]))
            continue

        if kind in ("Opening paragraph", "Body") and not b["link"] and full_width:
            groups = split_paragraphs(text, 3)
            row = []
            for gi, g in enumerate(groups):
                c = min(col + gi, len(COL_XS) - 1)
                row.append(("body", c, g, b["font"]))
            items.append((b["y"], seq, row))
        elif kind in ("Opening paragraph", "Body") and not b["link"]:
            items.append((b["y"], seq, [("body", col, text, b["font"])]))
        elif kind == "H2":
            items.append((b["y"], seq, [("h2", col, text, 15)]))
        elif kind == "H3":
            items.append((b["y"], seq, [("h3", col, text, 12)]))
        elif kind == "Link" or b["link"]:
            items.append((b["y"], seq, [("link", col, text, 9)]))
        elif kind == "Live element":
            placeholder = "< LIVE ELEMENT — build by hand:\n\n" + text
            if full_width:
                groups = split_paragraphs(placeholder, 3)
                row = [("body", min(col + gi, len(COL_XS) - 1), g, 9)
                       for gi, g in enumerate(groups)]
                items.append((b["y"], seq, row))
            else:
                items.append((b["y"], seq, [("body", col, placeholder, 9)]))

    if title_text is None:
        title_text = f"{ch['num']}. {ch['title'].replace(' & ', ' and ')}"
    fname_title = re.sub(r"^\d+\.\s*", "", title_text).replace(": ", " - ")
    fname = f"Explanation {ch['num']}. {fname_title}.vl"

    # per-column flow: draft y is a minimum, cursors prevent overlap.
    # Items sharing the same draft y form one row and stay Y-aligned across
    # columns (house convention). Gaps: tight under headings and between a
    # resource title and its link, airy otherwise.
    from itertools import groupby

    cursors = [TOP_Y] * len(COL_XS)
    last_kind = {}
    pads = []
    pilot_y = None

    def gap_for(c, kind):
        prev = last_kind.get(c)
        if prev in ("h2", "h3"):
            return 8
        if kind == "link" and prev == "body":
            return 2
        return GAP

    ordered = sorted(items, key=lambda t: (t[0], t[1]))
    for draft_y, group in groupby(ordered, key=lambda t: t[0]):
        rowitems = [r for (_y, _s, row) in group for r in row]
        first_kind = {}
        for r in rowitems:
            first_kind.setdefault(r[1], r[0])
        y_row = max([draft_y] + [cursors[c] + gap_for(c, k)
                                 for c, k in first_kind.items()])
        placed = set()
        for r in rowitems:
            kind, c = r[0], r[1]
            x = COL_XS[c]
            y = y_row if c not in placed else cursors[c] + gap_for(c, kind)
            placed.add(c)
            if kind == "PILOT":
                pilot_y = y
                cursors[c] = y + PILOT_HEIGHT
                last_kind[c] = "body"
                continue
            text, font = r[2], r[3]
            if kind == "h2":
                w, h = max(200, min(BODY_W, len(text) * 10 + 30)), 31
            elif kind == "h3":
                w, h = max(150, min(BODY_W, len(text) * 8 + 20)), 25
            elif kind == "link":
                w, h = min(BODY_W, len(text) * 6 + 15), 19
                pads.append(comment_pad(x, y, w, h, text, 9, "Link"))
                cursors[c] = y + h
                last_kind[c] = "link"
                continue
            else:
                w = BODY_W
                h = est_height(text, w, font)
            pads.append(comment_pad(x, y, w, h, text, font))
            cursors[c] = y + h
            last_kind[c] = kind

    canvas_extra = patch_extra = ""
    if ch["num"] == 38 and pilot_y is not None:
        canvas_extra, patch_extra = ch38_live_elements(fname, pilot_y)

    # harvested prototype zone below the text content
    bottom = max(cursors)
    hv_canvas, hv_patch, info = harvest_live.harvest(ch["num"], 92, bottom + 190, fname)
    if hv_canvas:
        pads.append(comment_pad(
            92, bottom + 110, 400, 44,
            "Prototype patches below — harvested from wip/The Origin of Life.vl. "
            "Arrange them into the live-element slots marked above.", 12))
        canvas_extra = (canvas_extra + "\n" + hv_canvas) if canvas_extra else hv_canvas
        patch_extra = (patch_extra + "\n" + hv_patch) if patch_extra else hv_patch

    all_pads = top_strip(title_text) + pads
    return fname, document(title_text, all_pads, canvas_extra, patch_extra), len(pads), info


def main():
    lines = DRAFTS.read_text(encoding="utf-8").splitlines()
    chapters, warnings = parse_chapters(lines)
    print(f"Parsed {len(chapters)} chapters from {DRAFTS.name}\n")
    for ch in chapters:
        fname, xml, npads, info = emit_chapter(ch)
        (OUTDIR / fname).write_text(xml, encoding="utf-8")
        hv = (f"  + harvested {info['elements']} elements, {info['links']} links "
              f"({info['links_dropped']} cross-zone dropped), {info['slots']} slots, "
              f"defs: {', '.join(info['defs']) or 'none'}") if info else "  (no prototype zone)"
        print(f"  {fname}  ({npads} content pads)\n  {hv}")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print("  " + w)
    else:
        print("\nNo parser warnings.")


if __name__ == "__main__":
    main()
