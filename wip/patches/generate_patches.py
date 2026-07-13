#!/usr/bin/env python3
"""Generate Part V chapter .vl files (text layer + live-element placeholders)
from wip/part-v-chapter-drafts.md.

Parses the drafts' position markers (H1/H2/H3/Body/Link/Live element) and emits
one .vl document per chapter into wip/patches/, using the house scaffold cloned
from the existing help chapters (top strip, dependencies, Application process).

Run:  python3 generate_patches.py
"""

import re
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # wip/
DRAFTS = ROOT / "part-v-chapter-drafts.md"
OUTDIR = Path(__file__).resolve().parent

LANG_VERSION = "2025.7.2"

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
    """Estimate IOBox height for wrapped comment text."""
    px_per_char = {7: 4.6, 9: 5.9, 12: 7.6, 15: 9.4, 22: 13.5}[font]
    line_h = {7: 15, 9: 20, 12: 25, 15: 31, 22: 46}[font]
    cpl = max(10, int(width / px_per_char))
    lines = 0
    for para in text.split("\n"):
        if not para.strip():
            lines += 1
        else:
            lines += max(1, -(-len(para) // cpl))
    return max(line_h, lines * line_h)


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

def ch38_live_elements(doc_filename: str):
    """The Thing record definition + a wired Create call site (column 3).

    Structure cloned from the vvvv-serialized MyRecord in wip/The Origin of
    Life.vl: RecordDefinition node with Slots, an empty-canvas Create patch
    whose input pins wire (hidden link -> ControlPoint -> slot pad) into the
    properties; call site references the type via RecordType CategoryReference.
    Returns (canvas_xml, patch_xml) to inject into the Application.
    """
    ids = {k: new_id() for k in (
        "defNode defPatch defCanvas padPos cpPos padSize cpSize createPatch "
        "procDef frag slotPos slotSize l1 l2 l3 l4 ioPos ioSize createNode "
        "ncPin cposPin csizePin coutPin dposPin dsizePin thingPad appSlot "
        "la lb lc note"
    ).split()}
    canvas = f"""          <Node Name="Thing" Bounds="1300,762" Id="{ids['defNode']}">
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
          <Pad Id="{ids['ioPos']}" Comment="Position" Bounds="1104,752,45,28" ShowValueBox="true" isIOBox="true" Value="0, 0">
            <p:TypeAnnotation LastCategoryFullName="2D" LastDependency="VL.CoreLib.vl">
              <Choice Kind="TypeFlag" Name="Vector2" />
            </p:TypeAnnotation>
          </Pad>
          <Pad Id="{ids['ioSize']}" Comment="Size" Bounds="1176,790,35,15" ShowValueBox="true" isIOBox="true" Value="0.5">
            <p:TypeAnnotation LastCategoryFullName="Primitive" LastDependency="VL.CoreLib.vl">
              <Choice Kind="TypeFlag" Name="Float32" />
            </p:TypeAnnotation>
          </Pad>
          <Node Bounds="1102,838,51,26" Id="{ids['createNode']}">
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
          <Pad Id="{ids['thingPad']}" SlotId="{ids['appSlot']}" Bounds="1104,894" />
{comment_pad(1230, 894, 260, 40, "< a Thing stored in a pad. Hover the link above to see the type in the tooltip.", 9)}"""
    patch = f"""        <Slot Id="{ids['appSlot']}" Name="Thing" />
        <Link Id="{ids['la']}" Ids="{ids['ioPos']},{ids['cposPin']}" />
        <Link Id="{ids['lb']}" Ids="{ids['ioSize']},{ids['csizePin']}" />
        <Link Id="{ids['lc']}" Ids="{ids['coutPin']},{ids['thingPad']}" />"""
    return canvas, patch


def document(title: str, pads: list, canvas_extra: str = "", patch_extra: str = "") -> str:
    pads_xml = "\n".join(pads)
    patch_extra = patch_extra + "\n" if patch_extra else ""
    if canvas_extra:
        pads_xml += "\n" + canvas_extra
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
    chapters = []  # (num, title, blocks)
    cur = None
    i = 0
    skip_mode = False  # inside ## Notes
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
                _, i2 = read_fence(i + 1)  # discard the map fence
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
            # live-element descriptions continue on the same line only
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


# ---------------------------------------------------------------- emit

def emit_chapter(ch):
    title_text = None
    pads = []
    for b in ch["blocks"]:
        kind, text = b["kind"], b["text"]
        if kind == "H1":
            title_text = text.replace(" & ", " and ")
            continue
        x, y, font = b["x"], b["y"], b["font"]
        if y is None:
            continue
        if kind == "Opening paragraph" or (kind == "Body" and "\n" in text) or kind == "Body":
            w = b["width"] or (430 if font == 9 else 346)
            if b["link"]:
                pads.append(comment_pad(x, y, max(140, len(text) * 6 + 15), 19, text, 9, "Link"))
            else:
                h = est_height(text, w, font)
                pads.append(comment_pad(x, y, w, h, text, font))
        elif kind == "H2":
            pads.append(comment_pad(x, y, max(200, len(text) * 10 + 30), 31, text, 15))
        elif kind == "H3":
            pads.append(comment_pad(x, y, max(150, len(text) * 8 + 20), 25, text, 12))
        elif kind == "Link":
            pads.append(comment_pad(x, y, max(140, len(text) * 6 + 15), 19, text, 9, "Link"))
        elif kind == "Live element":
            if ch["num"] == 38 and x == 1092 and y == 750:
                continue  # replaced by the built pilot elements
            w = b["width"] or 430
            placeholder = "< LIVE ELEMENT — build by hand:\n\n" + text
            h = est_height(placeholder, w, 9)
            pads.append(comment_pad(x, y, w, h, placeholder, 9))

    if title_text is None:
        title_text = f"{ch['num']}. {ch['title'].replace(' & ', ' and ')}"
    all_pads = top_strip(title_text) + pads
    fname_title = re.sub(r"^\d+\.\s*", "", title_text).replace(": ", " - ")
    fname = f"Explanation {ch['num']}. {fname_title}.vl"
    canvas_extra = patch_extra = ""
    if ch["num"] == 38:
        canvas_extra, patch_extra = ch38_live_elements(fname)
    return fname, document(title_text, all_pads, canvas_extra, patch_extra), len(pads)


def main():
    lines = DRAFTS.read_text(encoding="utf-8").splitlines()
    chapters, warnings = parse_chapters(lines)
    print(f"Parsed {len(chapters)} chapters from {DRAFTS.name}\n")
    for ch in chapters:
        fname, xml, npads = emit_chapter(ch)
        (OUTDIR / fname).write_text(xml, encoding="utf-8")
        kinds = {}
        for b in ch["blocks"]:
            kinds[b["kind"]] = kinds.get(b["kind"], 0) + 1
        print(f"  {fname}  ({npads} content pads; {kinds})")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print("  " + w)
    else:
        print("\nNo parser warnings.")


if __name__ == "__main__":
    main()
