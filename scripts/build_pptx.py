"""High-fidelity OpenXML (.pptx) generator matching the HTML presentation deck 1-for-1.

Generates `docs/Cloud_Next_27_Agents_CLI_LangGraph.pptx` (16:9 widescreen, 960x540 pt) with:
- Exact visual parity with `docs/slides.html` across all 10 slides
- Multi-color syntax-highlighted terminal code blocks (#8AB4F8, #81C995, #FDD663, #F28B82)
- Giant 52pt metric counters on Slide 2 (18+, 6, 0%)
- Pill badges and footer dividers on Slide 3
- Full 3-Layer Stack Cake on Slide 4 (Authoring Layer + 6 vs 18 Split + Dark Cloud Foundation)
- 4-Stage Pipeline Cards with top colored accent bars on Slide 7
- 6-Tile Bento Grid + bottom CTA bar on Slide 10
"""

from __future__ import annotations

from pathlib import Path
from typing import Union
from xml.sax.saxutils import escape
import zipfile

PT = 12700  # 1 point = 12,700 EMUs
SLIDE_W = 960 * PT
SLIDE_H = 540 * PT

# A Run is (text, font_family, size_pt, color_hex, is_bold)
RunSpec = tuple[str, str, float, str, bool]
# A Paragraph is either a single RunSpec or a list of RunSpecs on the same line
ParaSpec = Union[RunSpec, list[RunSpec]]


def _hex(color: str) -> str:
    return color.lstrip("#").upper()


class SlideBuilder:
    def __init__(self, bg_hex: str) -> None:
        self.bg_hex = _hex(bg_hex)
        self.shapes: list[str] = []
        self.animated_spids: list[tuple[int, str, int]] = []  # (spid, effect_type, delay_ms)
        self._id = 2

    def _next_id(self, animate: str | None = "fly_up", delay_ms: int = 180) -> int:
        val = self._id
        self._id += 1
        if animate:
            self.animated_spids.append((val, animate, delay_ms))
        return val

    def add_rect(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        fill_hex: str,
        border_hex: str | None = None,
        border_w_pt: float = 1.0,
        rounded: bool = False,
        adj: int = 5000,
        animate: str | None = None,
    ) -> None:
        sid = self._next_id(animate=animate)
        x, y, w, h = int(x_pt * PT), int(y_pt * PT), int(w_pt * PT), int(h_pt * PT)
        geom = "roundRect" if rounded else "rect"
        av = f'<a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>' if rounded else "<a:avLst/>"
        bw = int(border_w_pt * PT)
        ln_xml = (
            f'<a:ln w="{bw}"><a:solidFill><a:srgbClr val="{_hex(border_hex)}"/></a:solidFill></a:ln>'
            if border_hex
            else "<a:ln><a:noFill/></a:ln>"
        )
        self.shapes.append(
            f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="Rect {sid}"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
    <a:prstGeom prst="{geom}">{av}</a:prstGeom>
    <a:solidFill><a:srgbClr val="{_hex(fill_hex)}"/></a:solidFill>
    {ln_xml}
  </p:spPr>
</p:sp>"""
        )

    def add_box(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        paragraphs: list[ParaSpec],
        fill_hex: str | None = None,
        border_hex: str | None = None,
        border_w_pt: float = 1.0,
        rounded: bool = False,
        adj: int = 4500,
        pad_l: float = 12.0,
        pad_t: float = 10.0,
        pad_r: float = 12.0,
        pad_b: float = 10.0,
        align: str = "l",
        valign: str = "t",
        line_spacing_pct: int = 118000,
        animate: str | None = "fly_up",
        delay_ms: int = 180,
    ) -> None:
        sid = self._next_id(animate=animate, delay_ms=delay_ms)
        x, y, w, h = int(x_pt * PT), int(y_pt * PT), int(w_pt * PT), int(h_pt * PT)
        geom = "roundRect" if rounded else "rect"
        av = f'<a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>' if rounded else "<a:avLst/>"
        fill_xml = (
            f'<a:solidFill><a:srgbClr val="{_hex(fill_hex)}"/></a:solidFill>'
            if fill_hex
            else "<a:noFill/>"
        )
        bw = int(border_w_pt * PT)
        ln_xml = (
            f'<a:ln w="{bw}"><a:solidFill><a:srgbClr val="{_hex(border_hex)}"/></a:solidFill></a:ln>'
            if border_hex
            else "<a:ln><a:noFill/></a:ln>"
        )
        l_ins, t_ins, r_ins, b_ins = int(pad_l * PT), int(pad_t * PT), int(pad_r * PT), int(pad_b * PT)

        p_xml_list: list[str] = []
        for para in paragraphs:
            runs: list[RunSpec] = [para] if isinstance(para, tuple) else para
            # If a single run contains newlines, split into multiple paragraphs
            if len(runs) == 1 and "\n" in runs[0][0]:
                text, font, size_pt, color_hex, is_bold = runs[0]
                for line in text.split("\n"):
                    sz = int(size_pt * 100)
                    b_attr = ' b="1"' if is_bold else ' b="0"'
                    p_xml_list.append(
                        f"""<a:p>
  <a:pPr algn="{align}"><a:lnSpc><a:spcPct val="{line_spacing_pct}"/></a:lnSpc></a:pPr>
  <a:r>
    <a:rPr lang="en-US" sz="{sz}"{b_attr} dirty="0">
      <a:solidFill><a:srgbClr val="{_hex(color_hex)}"/></a:solidFill>
      <a:latin typeface="{escape(font)}"/>
      <a:cs typeface="{escape(font)}"/>
    </a:rPr>
    <a:t>{escape(line)}</a:t>
  </a:r>
</a:p>"""
                    )
            else:
                r_xml_parts: list[str] = []
                for text, font, size_pt, color_hex, is_bold in runs:
                    sz = int(size_pt * 100)
                    b_attr = ' b="1"' if is_bold else ' b="0"'
                    r_xml_parts.append(
                        f"""  <a:r>
    <a:rPr lang="en-US" sz="{sz}"{b_attr} dirty="0">
      <a:solidFill><a:srgbClr val="{_hex(color_hex)}"/></a:solidFill>
      <a:latin typeface="{escape(font)}"/>
      <a:cs typeface="{escape(font)}"/>
    </a:rPr>
    <a:t>{escape(text)}</a:t>
  </a:r>"""
                    )
                p_xml_list.append(
                    f"""<a:p>
  <a:pPr algn="{align}"><a:lnSpc><a:spcPct val="{line_spacing_pct}"/></a:lnSpc></a:pPr>
{chr(10).join(r_xml_parts)}
</a:p>"""
                )

        body_p = "\n".join(p_xml_list)
        self.shapes.append(
            f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="Box {sid}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
    <a:prstGeom prst="{geom}">{av}</a:prstGeom>
    {fill_xml}
    {ln_xml}
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" lIns="{l_ins}" tIns="{t_ins}" rIns="{r_ins}" bIns="{b_ins}" anchor="{valign}"/>
    <a:lstStyle/>
    {body_p}
  </p:txBody>
</p:sp>"""
        )

    def add_four_color_bar(self) -> None:
        sid = self._next_id(animate="fade", delay_ms=80)
        w = int(960 * PT)
        h = int(6 * PT)
        self.shapes.append(
            f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="GradientBar {sid}"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="0" y="0"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:gradFill flip="none" rotWithShape="1">
      <a:gsLst>
        <a:gs pos="0"><a:srgbClr val="4285F4"/></a:gs>
        <a:gs pos="33000"><a:srgbClr val="EA4335"/></a:gs>
        <a:gs pos="66000"><a:srgbClr val="FBBC04"/></a:gs>
        <a:gs pos="100000"><a:srgbClr val="34A853"/></a:gs>
      </a:gsLst>
      <a:lin ang="0" scaled="1"/>
    </a:gradFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
</p:sp>"""
        )

    def add_header(
        self,
        is_dark: bool,
        eyebrow: str,
        eyebrow_color: str,
        title: str,
        subtitle: str,
        slide_num: str,
    ) -> None:
        self.add_four_color_bar()
        self.add_box(
            48, 20, 680, 22,
            [(eyebrow.upper(), "Google Sans", 9.5, eyebrow_color, True)],
            pad_l=0, pad_t=0, pad_r=0, pad_b=0,
        )
        self.add_box(
            850, 20, 62, 22,
            [(slide_num, "Google Sans Mono", 9.5, "9AA0A6" if is_dark else "5F6368", False)],
            pad_l=0, pad_t=0, pad_r=0, pad_b=0, align="r",
        )
        self.add_box(
            48, 42, 864, 42,
            [(title, "Google Sans Display", 26, "FFFFFF" if is_dark else "202124", True)],
            pad_l=0, pad_t=0, pad_r=0, pad_b=0,
        )
        if subtitle:
            self.add_box(
                48, 82, 864, 28,
                [(subtitle, "Google Sans Text", 12.5, "BDC1C6" if is_dark else "5F6368", False)],
                pad_l=0, pad_t=0, pad_r=0, pad_b=0,
            )

    def add_footer(self, is_dark: bool, left_text: str, right_text: str, right_color: str | None = None) -> None:
        line_color = "2D3343" if is_dark else "DADCE0"
        txt_color = "9AA0A6" if is_dark else "5F6368"
        r_color = right_color or txt_color
        self.add_rect(48, 492, 864, 1, line_color)
        self.add_box(
            48, 498, 560, 24,
            [(left_text, "Google Sans Text", 9.5, txt_color, False)],
            pad_l=0, pad_t=0, pad_r=0, pad_b=0,
        )
        self.add_box(
            610, 498, 302, 24,
            [(right_text, "Google Sans Mono", 9.5, r_color, True)],
            pad_l=0, pad_t=0, pad_r=0, pad_b=0, align="r",
        )

    def to_xml(self) -> str:
        shapes_xml = "\n".join(self.shapes)
        par_xml_list: list[str] = []
        bld_xml_list: list[str] = []
        ctn_id = 4
        for idx, (spid, effect_type, delay_ms) in enumerate(self.animated_spids):
            node_type = "withEffect" if idx == 0 else "afterEffect"
            actual_delay = 100 if idx == 0 else delay_ms
            c_mid = ctn_id
            c_inner = ctn_id + 1
            c_set = ctn_id + 2
            c_anim = ctn_id + 3
            ctn_id += 4

            if effect_type == "fly_up":
                preset_id = 2
                preset_sub = 4
                motion_xml = f"""                              <p:animEffect transition="in" filter="fade">
                                <p:cBhvr>
                                  <p:cTn id="{c_anim}" dur="450"/>
                                  <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                                </p:cBhvr>
                              </p:animEffect>"""
            else:
                preset_id = 10
                preset_sub = 0
                motion_xml = f"""                              <p:animEffect transition="in" filter="fade">
                                <p:cBhvr>
                                  <p:cTn id="{c_anim}" dur="450"/>
                                  <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                                </p:cBhvr>
                              </p:animEffect>"""

            par_xml_list.append(
                f"""                      <p:par>
                        <p:cTn id="{c_mid}" fill="hold">
                          <p:stCondLst><p:cond delay="{actual_delay}"/></p:stCondLst>
                          <p:childTnLst>
                            <p:par>
                              <p:cTn id="{c_inner}" presetID="{preset_id}" presetClass="entr" presetSubtype="{preset_sub}" fill="hold" grpId="0" nodeType="{node_type}">
                                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                <p:childTnLst>
                                  <p:set>
                                    <p:cBhvr>
                                      <p:cTn id="{c_set}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
                                      <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                                      <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
                                    </p:cBhvr>
                                    <p:to><p:strVal val="visible"/></p:to>
                                  </p:set>
{motion_xml}
                                </p:childTnLst>
                              </p:cTn>
                            </p:par>
                          </p:childTnLst>
                        </p:cTn>
                      </p:par>"""
            )
            bld_xml_list.append(f'    <p:bldP spid="{spid}" grpId="0"/>')

        children_timing = "\n".join(par_xml_list)
        bld_lst_xml = "\n".join(bld_xml_list)

        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgPr>
        <a:solidFill><a:srgbClr val="{self.bg_hex}"/></a:solidFill>
        <a:effectLst/>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {shapes_xml}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
  <p:transition spd="med" advClick="1"><p:fade/></p:transition>
  <p:timing>
    <p:tnLst>
      <p:par>
        <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
          <p:childTnLst>
            <p:seq concurrent="1" nextAc="seek">
              <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                <p:childTnLst>
                  <p:par>
                    <p:cTn id="3" fill="hold">
                      <p:stCondLst>
                        <p:cond delay="0"/>
                      </p:stCondLst>
                      <p:childTnLst>
{children_timing}
                      </p:childTnLst>
                    </p:cTn>
                  </p:par>
                </p:childTnLst>
              </p:cTn>
              <p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
              <p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
            </p:seq>
          </p:childTnLst>
        </p:cTn>
      </p:par>
    </p:tnLst>
    <p:bldLst>
{bld_lst_xml}
    </p:bldLst>
  </p:timing>
</p:sld>"""


def build_slides() -> list[SlideBuilder]:
    slides: list[SlideBuilder] = []

    # =========================================================================
    # SLIDE 01: Hero Opening (Dark Stage #0E1015)
    # =========================================================================
    s1 = SlideBuilder("0E1015")
    s1.add_four_color_bar()
    # Top Pill Badge
    s1.add_box(
        56, 36, 290, 26,
        [("Google Cloud Next '27  •  Developer Session", "Google Sans", 9.5, "8AB4F8", True)],
        fill_hex="162038", border_hex="3B5998", rounded=True, adj=50000,
        pad_l=12, pad_t=4, pad_r=12, pad_b=4, align="c", valign="ctr",
    )
    s1.add_box(
        358, 36, 130, 26,
        [("agents-cli v1.8+", "Google Sans Mono", 9.5, "9AA0A6", False)],
        pad_l=4, pad_t=4, pad_r=4, pad_b=4, valign="ctr",
    )
    s1.add_box(
        840, 36, 64, 26,
        [("01 / 10", "Google Sans Mono", 9.5, "9AA0A6", False)],
        pad_l=0, pad_t=4, pad_r=0, pad_b=4, align="r", valign="ctr",
    )
    s1.add_box(
        56, 118, 600, 24,
        [("POWERING THE AGENT DEVELOPMENT LIFECYCLE", "Google Sans", 11, "8AB4F8", True)],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    s1.add_box(
        56, 148, 848, 135,
        [
            ("Every agent framework.", "Google Sans Display", 44, "FFFFFF", True),
            [
                ("One ", "Google Sans Display", 44, "4285F4", True),
                ("production ", "Google Sans Display", 44, "9B72CB", True),
                ("lifecycle.", "Google Sans Display", 44, "D96570", True),
            ],
        ],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0, line_spacing_pct=110000,
    )
    s1.add_box(
        56, 295, 760, 70,
        [
            (
                "Running LangChain, LangGraph, and custom enterprise governance policies natively on Google Cloud with the Agents CLI Extension System.",
                "Google Sans Text",
                16,
                "BDC1C6",
                False,
            )
        ],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0, line_spacing_pct=130000,
    )
    s1.add_rect(56, 465, 848, 1, "2D3343")
    s1.add_box(
        56, 480, 430, 30,
        [("github.com/sanketbisne/scalfod-langgraph-agentscli", "Google Sans Mono", 10, "FFFFFF", False)],
        fill_hex="1F2430", border_hex="2D3343", rounded=True, adj=20000,
        pad_l=12, pad_t=5, pad_r=12, pad_b=5, valign="ctr",
    )
    s1.add_box(
        600, 480, 304, 30,
        [("Google Cloud AI & Developer Platform", "Google Sans", 10, "9AA0A6", False)],
        pad_l=0, pad_t=6, pad_r=0, pad_b=4, align="r", valign="ctr",
    )
    slides.append(s1)

    # =========================================================================
    # SLIDE 02: By The Numbers (Dark Stage #0E1015)
    # =========================================================================
    s2 = SlideBuilder("0E1015")
    s2.add_header(
        True,
        "By The Numbers",
        "8AB4F8",
        "Decoupling the lifecycle from the runtime.",
        "Out of 24 CLI commands, 18 are framework-agnostic and only 6 touch the agent runtime.",
        "02 / 10",
    )
    # 3 Big Number Cards
    s2.add_box(
        48, 130, 276, 340,
        [
            ("18+", "Google Sans Display", 52, "8AB4F8", True),
            ("", "Google Sans Text", 6, "FFFFFF", False),
            ("Framework-Agnostic Commands", "Google Sans", 14, "FFFFFF", True),
            ("", "Google Sans Text", 6, "9AA0A6", False),
            (
                "deploy, eval grade, eval compare, infra, scaffold, lint, and login work unchanged across ADK, LangChain, and LangGraph.",
                "Google Sans Text",
                11,
                "9AA0A6",
                False,
            ),
        ],
        fill_hex="161922", border_hex="2D3343", rounded=True, pad_l=20, pad_t=22, pad_r=20, pad_b=20,
    )
    s2.add_box(
        342, 130, 276, 340,
        [
            ("6", "Google Sans Display", 52, "81C995", True),
            ("", "Google Sans Text", 6, "FFFFFF", False),
            ("Runtime Overrides", "Google Sans", 14, "FFFFFF", True),
            ("", "Google Sans Text", 6, "9AA0A6", False),
            (
                "run, playground, and eval.generate hot-swap via a single agents-cli-extension.yaml manifest at the project root.",
                "Google Sans Text",
                11,
                "9AA0A6",
                False,
            ),
        ],
        fill_hex="161922", border_hex="2D3343", rounded=True, pad_l=20, pad_t=22, pad_r=20, pad_b=20,
    )
    s2.add_box(
        636, 130, 276, 340,
        [
            ("0%", "Google Sans Display", 52, "FDD663", True),
            ("", "Google Sans Text", 6, "FFFFFF", False),
            ("Framework Lock-In", "Google Sans", 14, "FFFFFF", True),
            ("", "Google Sans Text", 6, "9AA0A6", False),
            (
                "Zero google-adk dependency required in pyproject.toml. Pure LangChain and LangGraph code in production.",
                "Google Sans Text",
                11,
                "9AA0A6",
                False,
            ),
        ],
        fill_hex="161922", border_hex="2D3343", rounded=True, pad_l=20, pad_t=22, pad_r=20, pad_b=20,
    )
    s2.add_footer(
        True,
        "Available starting in Agents CLI v1.5+ (Extension System) & v1.8+ (LangChain Template)",
        "google/agents-cli",
        "8AB4F8",
    )
    slides.append(s2)

    # =========================================================================
    # SLIDE 03: The Framework Lock-In Problem (Light Stage #FFFFFF)
    # =========================================================================
    s3 = SlideBuilder("FFFFFF")
    s3.add_header(
        False,
        "The Framework Lock-In Problem",
        "1A73E8",
        "Ending the tradeoff between velocity and choice.",
        "How teams previously adapted opinionated agent toolchains vs. the Agents CLI Extension System:",
        "03 / 10",
    )
    # Card 1
    s3.add_rect(48, 130, 276, 340, "F8F9FA", "DADCE0", rounded=True)
    s3.add_box(
        66, 150, 110, 24,
        [("Legacy Path 1", "Google Sans", 9.5, "C5221F", True)],
        fill_hex="FCE8E6", rounded=True, adj=20000, pad_l=8, pad_t=3, pad_r=8, pad_b=3, align="c", valign="ctr",
    )
    s3.add_box(
        66, 186, 240, 200,
        [
            ("Forking the CLI", "Google Sans", 16, "202124", True),
            ("", "Google Sans Text", 6, "5F6368", False),
            (
                "Maintain a divergent internal copy and manually rebase on every upstream release.",
                "Google Sans Text",
                11,
                "5F6368",
                False,
            ),
        ],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    s3.add_rect(66, 412, 240, 1, "DADCE0")
    s3.add_box(
        66, 422, 240, 28,
        [("Result: Permanent maintenance tax", "Google Sans Mono", 9.5, "C5221F", True)],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )

    # Card 2
    s3.add_rect(342, 130, 276, 340, "F8F9FA", "DADCE0", rounded=True)
    s3.add_box(
        360, 150, 110, 24,
        [("Legacy Path 2", "Google Sans", 9.5, "B06000", True)],
        fill_hex="FEF7E0", rounded=True, adj=20000, pad_l=8, pad_t=3, pad_r=8, pad_b=3, align="c", valign="ctr",
    )
    s3.add_box(
        360, 186, 240, 200,
        [
            ("Custom Wrapper Scripts", "Google Sans", 16, "202124", True),
            ("", "Google Sans Text", 6, "5F6368", False),
            (
                "Build parallel shell scripts around the CLI. Developers and coding agents call the native CLI directly and bypass policies.",
                "Google Sans Text",
                11,
                "5F6368",
                False,
            ),
        ],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    s3.add_rect(360, 412, 240, 1, "DADCE0")
    s3.add_box(
        360, 422, 240, 28,
        [("Result: Bypassed governance gates", "Google Sans Mono", 9.5, "B06000", True)],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )

    # Card 3 (Highlighted Blue)
    s3.add_rect(636, 130, 276, 340, "E8F0FE", "1A73E8", border_w_pt=2.0, rounded=True)
    s3.add_box(
        654, 150, 155, 24,
        [("Cloud Next '27 Standard", "Google Sans", 9.5, "FFFFFF", True)],
        fill_hex="1A73E8", rounded=True, adj=20000, pad_l=8, pad_t=3, pad_r=8, pad_b=3, align="c", valign="ctr",
    )
    s3.add_box(
        654, 186, 240, 200,
        [
            ("Agents CLI Extensions", "Google Sans", 16, "202124", True),
            ("", "Google Sans Text", 6, "3C4043", False),
            (
                "Declarative agents-cli-extension.yaml overrides commands in-place, pinned by Git commit SHA.",
                "Google Sans Text",
                11,
                "3C4043",
                False,
            ),
        ],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    s3.add_rect(654, 412, 240, 1, "AECBFA")
    s3.add_box(
        654, 422, 240, 28,
        [("Result: Zero fork + 100% enforcement", "Google Sans Mono", 9.5, "137333", True)],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    s3.add_footer(
        False,
        "Distributed directly via Git repositories with zero external registry required",
        "schema: agents-cli-extension/v1alpha1",
    )
    slides.append(s3)

    # =========================================================================
    # SLIDE 04: 3-Layer Stack Cake - 6 vs 18 Split (Light Stage #FFFFFF)
    # =========================================================================
    s4 = SlideBuilder("FFFFFF")
    s4.add_header(
        False,
        "Inside the Command Surface (6 vs. 18 Split)",
        "137333",
        "One unified command surface across the stack.",
        "A single agents-cli-extension.yaml swaps only the 6 runtime commands and keeps the 18 production commands intact.",
        "04 / 10",
    )
    # Layer 1: Authoring Layer
    s4.add_rect(48, 122, 864, 92, "F8F9FA", "DADCE0", rounded=True, adj=8000)
    s4.add_box(
        64, 130, 500, 20,
        [("1. AGENT AUTHORING LAYER (BRING YOUR OWN FRAMEWORK)", "Google Sans", 9, "5F6368", True)],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    fw_items = [
        ("LangChain 1.0+", "E8F0FE", "1A73E8", "1967D2"),
        ("LangGraph StateGraph", "E8F0FE", "1A73E8", "1967D2"),
        ("Deep Agents", "FFFFFF", "DADCE0", "202124"),
        ("Google ADK (Python / Go)", "FFFFFF", "DADCE0", "202124"),
    ]
    for i, (label, bg, brd, col) in enumerate(fw_items):
        s4.add_box(
            64 + i * 210, 156, 198, 42,
            [(label, "Google Sans", 10.5, col, True)],
            fill_hex=bg, border_hex=brd, border_w_pt=1.5, rounded=True, adj=15000,
            align="c", valign="ctr",
        )

    # Layer 2: 6 Overridden vs 18+ Native
    s4.add_box(
        48, 226, 424, 140,
        [
            ("6 Overridden Runtime Commands", "Google Sans", 11.5, "1967D2", True),
            ("", "Google Sans Text", 8, "3C4043", False),
            (
                "run • playground (LangGraph Studio) • eval.generate • publish.gemini-enterprise • eval.dataset • eval.optimize",
                "Google Sans Mono",
                10,
                "3C4043",
                False,
            ),
        ],
        fill_hex="F8FAFF", border_hex="4285F4", border_w_pt=2.0, rounded=True, adj=8000,
        pad_l=18, pad_t=16, pad_r=18, pad_b=16,
    )
    # Right-aligned pill badge inside Left Card
    s4.add_box(
        352, 238, 104, 24,
        [("[↑ langchain]", "Google Sans Mono", 9, "1967D2", True)],
        fill_hex="E8F0FE", rounded=True, adj=25000, align="c", valign="ctr",
        pad_l=4, pad_t=2, pad_r=4, pad_b=2,
    )

    s4.add_box(
        488, 226, 424, 140,
        [
            ("18+ Native Production Commands", "Google Sans", 11.5, "137333", True),
            ("", "Google Sans Text", 8, "3C4043", False),
            (
                "deploy • eval grade • eval compare • infra (Terraform) • scaffold • extension • install • lint",
                "Google Sans Mono",
                10,
                "3C4043",
                False,
            ),
        ],
        fill_hex="F6FEF8", border_hex="34A853", border_w_pt=2.0, rounded=True, adj=8000,
        pad_l=18, pad_t=16, pad_r=18, pad_b=16,
    )
    # Right-aligned pill badge inside Right Card
    s4.add_box(
        822, 238, 74, 24,
        [("Built-In", "Google Sans Mono", 9, "137333", True)],
        fill_hex="E6F4EA", rounded=True, adj=25000, align="c", valign="ctr",
        pad_l=4, pad_t=2, pad_r=4, pad_b=2,
    )

    # Layer 3: Google Cloud Production Foundation
    s4.add_rect(48, 378, 864, 96, "202124", rounded=True, adj=8000)
    s4.add_box(
        64, 386, 500, 20,
        [("3. GOOGLE CLOUD PRODUCTION FOUNDATION", "Google Sans", 9, "8AB4F8", True)],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    foundation_items = [
        "Cloud Run (FastAPI A2A)",
        "Vertex AI Eval Service",
        "Gemini on Vertex AI",
        "Cloud Trace & Logging",
    ]
    for i, label in enumerate(foundation_items):
        s4.add_box(
            64 + i * 210, 412, 198, 44,
            [(label, "Google Sans Mono", 9.5, "FFFFFF", False)],
            fill_hex="2D3136", rounded=True, adj=15000, align="c", valign="ctr",
        )
    s4.add_footer(
        False,
        "Same Dockerfile CMD & FastAPI A2A contract across every framework",
        "app.fast_api_app:app",
    )
    slides.append(s4)

    # =========================================================================
    # SLIDE 05: Live Demo Act 1 - Scaffolding (Dark Stage #0E1015)
    # =========================================================================
    s5 = SlideBuilder("0E1015")
    s5.add_header(
        True,
        "Live Demo  •  Act 1",
        "8AB4F8",
        "Scaffold a pure LangGraph project in one command.",
        "Scaffolding and extension installation happen together. Nothing needs to be installed globally.",
        "05 / 10",
    )
    s5.add_rect(48, 130, 864, 340, "131314", "3C4043", rounded=True, adj=6000)
    # Terminal Window Header Bar
    s5.add_rect(48, 130, 864, 32, "1E1F22", "3C4043", rounded=True, adj=6000)
    s5.add_rect(64, 141, 10, 10, "EA4335", rounded=True, adj=50000)
    s5.add_rect(80, 141, 10, 10, "FBBC04", rounded=True, adj=50000)
    s5.add_rect(96, 141, 10, 10, "34A853", rounded=True, adj=50000)
    s5.add_box(
        118, 134, 420, 24,
        [("zsh — scalfod-langgraph-agentscli", "Google Sans Mono", 9.5, "9AA0A6", False)],
        pad_l=0, pad_t=2, pad_r=0, pad_b=2, valign="ctr",
    )
    # Sequential Terminal Block 1: Scaffold command
    s5.add_box(
        68, 174, 824, 92,
        [
            ("# 1. Scaffold directly from the first-party LangChain template", "Google Sans Mono", 11, "8AB4F8", False),
            ("$ agents-cli create scalfod-langgraph-agentscli \\", "Google Sans Mono", 11, "E8EAED", False),
            ("    --agent google/agents-cli/extensions/langchain/template@v1.8.0 \\", "Google Sans Mono", 11, "E8EAED", False),
            ("    -d cloud_run", "Google Sans Mono", 11, "E8EAED", False),
        ],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    # Sequential Terminal Block 2: Install & output
    s5.add_box(
        68, 276, 824, 78,
        [
            ("$ cd scalfod-langgraph-agentscli && agents-cli install", "Google Sans Mono", 11, "E8EAED", False),
            ("Agents CLI v1.8.0 • Fetching remote template: google/agents-cli/extensions/langchain/template@v1.8.0", "Google Sans Mono", 10.5, "81C995", False),
            ("> ✓ Connected to project: your-project • Your agent project is ready.", "Google Sans Mono", 10.5, "81C995", True),
        ],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    # Sequential Terminal Block 3: Verify zero ADK dependency
    s5.add_box(
        68, 366, 824, 84,
        [
            ("# 2. Prove zero google-adk dependency in pyproject.toml and app/", "Google Sans Mono", 11, "8AB4F8", False),
            ('$ grep -r "google.adk\\|google-adk" pyproject.toml app/ ; echo "exit: $?"', "Google Sans Mono", 11, "E8EAED", False),
            ("exit: 1   # Zero google-adk dependency verified!", "Google Sans Mono", 11, "FDD663", True),
        ],
        pad_l=0, pad_t=0, pad_r=0, pad_b=0,
    )
    s5.add_footer(
        True,
        "Auto-loaded via ./agents-cli-extension.yaml at project root",
        "Zero ADK Dependency Verified",
        "81C995",
    )
    slides.append(s5)

    # =========================================================================
    # SLIDE 06: Project Structure & CompiledStateGraph (Light Stage #FFFFFF)
    # =========================================================================
    s6 = SlideBuilder("FFFFFF")
    s6.add_header(
        False,
        "Codebase Architecture",
        "B06000",
        "One graph representation: CompiledStateGraph",
        "In LangChain 1.0+, create_agent compiles directly into a LangGraph CompiledStateGraph.",
        "06 / 10",
    )
    s6.add_box(
        48, 130, 420, 340,
        [
            ("Project Tree", "Google Sans", 11, "8AB4F8", True),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("scalfod-langgraph-agentscli/", "Google Sans Mono", 10, "E8EAED", False),
            ([("├── ", "Google Sans Mono", 10, "E8EAED", False), ("agents-cli-extension.yaml", "Google Sans Mono", 10, "FDD663", True), ("  # Overrides", "Google Sans Mono", 10, "9AA0A6", False)]),
            ("├── agents-cli-manifest.yaml   # cloud_run", "Google Sans Mono", 10, "E8EAED", False),
            ([("├── ", "Google Sans Mono", 10, "E8EAED", False), ("langgraph.json", "Google Sans Mono", 10, "FDD663", True), ("             # Studio config", "Google Sans Mono", 10, "9AA0A6", False)]),
            ("├── pyproject.toml             # langchain", "Google Sans Mono", 10, "E8EAED", False),
            ("├── Dockerfile                 # FastAPI :8080", "Google Sans Mono", 10, "E8EAED", False),
            ("├── app/", "Google Sans Mono", 10, "E8EAED", False),
            ([("│   ├── ", "Google Sans Mono", 10, "E8EAED", False), ("agent.py", "Google Sans Mono", 10, "81C995", True), ("               # StateGraph", "Google Sans Mono", 10, "9AA0A6", False)]),
            ([("│   ├── ", "Google Sans Mono", 10, "E8EAED", False), ("tools.py", "Google Sans Mono", 10, "81C995", True), ("               # DeepCite tools", "Google Sans Mono", 10, "9AA0A6", False)]),
            ("│   ├── fast_api_app.py        # A2A server", "Google Sans Mono", 10, "E8EAED", False),
            ("│   └── app_utils/a2a.py       # agent.json", "Google Sans Mono", 10, "E8EAED", False),
            ("└── extensions/sbom-deploy/    # SBOM gate", "Google Sans Mono", 10, "E8EAED", False),
        ],
        fill_hex="131314", border_hex="3C4043", rounded=True, pad_l=18, pad_t=16, pad_r=18, pad_b=16,
    )
    s6.add_box(
        492, 130, 420, 340,
        [
            ("app/agent.py", "Google Sans", 11, "81C995", True),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("from langchain.agents import create_agent", "Google Sans Mono", 10, "8AB4F8", False),
            ("from langchain_google_genai import ChatGoogleGenerativeAI", "Google Sans Mono", 10, "8AB4F8", False),
            ("from langgraph.graph.state import CompiledStateGraph", "Google Sans Mono", 10, "8AB4F8", False),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("llm = ChatGoogleGenerativeAI(", "Google Sans Mono", 10, "E8EAED", False),
            ('    model="gemini-2.5-flash", temperature=0', "Google Sans Mono", 10, "FDD663", False),
            (")", "Google Sans Mono", 10, "E8EAED", False),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("root_agent: CompiledStateGraph = create_agent(", "Google Sans Mono", 10, "81C995", True),
            ("    model=llm,", "Google Sans Mono", 10, "E8EAED", False),
            ("    tools=[create_research_plan, search_curated_kb,", "Google Sans Mono", 10, "E8EAED", False),
            ("           search_arxiv_papers, critique_research_draft],", "Google Sans Mono", 10, "E8EAED", False),
            ("    system_prompt=SYSTEM_PROMPT,", "Google Sans Mono", 10, "E8EAED", False),
            (")", "Google Sans Mono", 10, "81C995", True),
        ],
        fill_hex="131314", border_hex="3C4043", rounded=True, pad_l=18, pad_t=16, pad_r=18, pad_b=16,
    )
    s6.add_footer(
        False,
        "Authenticates automatically via Application Default Credentials (ADC) on Vertex AI",
        "GOOGLE_GENAI_USE_VERTEXAI=True",
    )
    slides.append(s6)

    # =========================================================================
    # SLIDE 07: DeepCite Research & Critique Loop (Light Stage #FFFFFF)
    # =========================================================================
    s7 = SlideBuilder("FFFFFF")
    s7.add_header(
        False,
        "DeepCite Reference Workload",
        "1A73E8",
        "Iterative Research & Self-Critique Loop",
        "Grounded retrieval and mandatory citation verification before generating the final technical report:",
        "07 / 10",
    )
    stages = [
        ("01 • PLAN", "1A73E8", "4285F4", "create_research_plan", "Decomposes complex prompts into structured sub-questions and targeted search queries."),
        ("02 • SEARCH", "B06000", "FBBC04", "search_curated_kb / arxiv", "Retrieves evidence with explicit IDs ([KB-...], [ARXIV-...], [WIKI-...]) and offline fallbacks."),
        ("03 • CRITIQUE", "C5221F", "EA4335", "critique_research_draft", "Audits draft claims for >= 2 distinct citations and depth; triggers revision if incomplete."),
        ("04 • REPORT", "137333", "34A853", "research-report CLI", "Outputs Markdown with inline [SOURCE_ID] citations and a verified ## References section."),
    ]
    for i, (kicker, kcol, bar_col, fn_name, desc) in enumerate(stages):
        cx = 48 + i * 220
        s7.add_box(
            cx, 136, 204, 330,
            [
                (kicker, "Google Sans", 10, kcol, True),
                ("", "Google Sans Text", 4, "202124", False),
                (fn_name, "Google Sans Mono", 11, "202124", True),
                ("", "Google Sans Text", 8, "5F6368", False),
                (desc, "Google Sans Text", 11, "5F6368", False),
            ],
            fill_hex="F8F9FA", border_hex="DADCE0", rounded=True, pad_l=16, pad_t=22, pad_r=16, pad_b=16,
        )
        # Top colored accent bar on each stage card
        s7.add_rect(cx + 2, 136, 200, 6, bar_col)

    s7.add_footer(
        False,
        "Deterministic offline fallbacks guarantee reproducible runs in CI/CD and sandboxed environments",
        "app/tools.py",
        "1A73E8",
    )
    slides.append(s7)

    # =========================================================================
    # SLIDE 08: LangGraph Studio & Vertex AI Evaluations (Dark Stage #0E1015)
    # =========================================================================
    s8 = SlideBuilder("0E1015")
    s8.add_header(
        True,
        "Live Demo  •  Act 2 & Act 3",
        "81C995",
        "LangGraph Studio & Vertex AI Evaluations.",
        "Boot LangGraph Studio via agents-cli playground and grade traces with Vertex AI Eval Service.",
        "08 / 10",
    )
    s8.add_box(
        48, 130, 420, 340,
        [
            ("1. RUN & INSPECT IN LANGGRAPH STUDIO", "Google Sans", 10, "8AB4F8", True),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ('$ agents-cli --help | grep -E "playground|run "', "Google Sans Mono", 9.5, "E8EAED", False),
            ([("  playground  Start LangGraph server. ", "Google Sans Mono", 9.5, "E8EAED", False), ("[↑ langchain]", "Google Sans Mono", 9.5, "81C995", True)]),
            ([("  run         Run compiled graph.     ", "Google Sans Mono", 9.5, "E8EAED", False), ("[↑ langchain]", "Google Sans Mono", 9.5, "81C995", True)]),
            ("", "Google Sans Mono", 6, "E8EAED", False),
            ('$ agents-cli run "How do Agents CLI extensions work?"', "Google Sans Mono", 9.5, "E8EAED", False),
            ("WARNING:root:agents-cli: applying 6 extension command(s)", "Google Sans Mono", 9.5, "FDD663", False),
            ("", "Google Sans Mono", 6, "E8EAED", False),
            ("$ agents-cli playground", "Google Sans Mono", 9.5, "E8EAED", False),
            ("> Boots LangGraph Studio on http://localhost:8080", "Google Sans Mono", 9.5, "81C995", True),
        ],
        fill_hex="131314", border_hex="3C4043", rounded=True, pad_l=18, pad_t=16, pad_r=18, pad_b=16,
    )
    s8.add_box(
        492, 130, 420, 340,
        [
            ("2. OVERRIDDEN GENERATE + NATIVE GRADE", "Google Sans", 10, "81C995", True),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("# Overridden: Drives LangGraph CompiledStateGraph", "Google Sans Mono", 9.5, "8AB4F8", False),
            ("$ agents-cli eval generate \\", "Google Sans Mono", 9.5, "E8EAED", False),
            ("    --dataset tests/eval/datasets/basic-dataset.json \\", "Google Sans Mono", 9.5, "E8EAED", False),
            ("    -o tests/eval/output/", "Google Sans Mono", 9.5, "E8EAED", False),
            ("", "Google Sans Mono", 6, "E8EAED", False),
            ("# Native: Scores traces via Vertex AI Eval Service", "Google Sans Mono", 9.5, "81C995", False),
            ("$ agents-cli eval grade \\", "Google Sans Mono", 9.5, "E8EAED", False),
            ("    --traces tests/eval/output/basic-dataset.json \\", "Google Sans Mono", 9.5, "E8EAED", False),
            ("    --config tests/eval/eval_config.yaml", "Google Sans Mono", 9.5, "E8EAED", False),
        ],
        fill_hex="131314", border_hex="3C4043", rounded=True, pad_l=18, pad_t=16, pad_r=18, pad_b=16,
    )
    s8.add_footer(
        True,
        "Unsupported ADK-simulator commands (eval dataset) exit cleanly with an explanation",
        "Standard EvaluationDataset Schema",
        "81C995",
    )
    slides.append(s8)

    # =========================================================================
    # SLIDE 09: Custom Enterprise Governance Extension (Dark Stage #0E1015)
    # =========================================================================
    s9 = SlideBuilder("0E1015")
    s9.add_header(
        True,
        "Live Demo  •  Act 4",
        "F28B82",
        "Policy-as-Code: Custom sbom-deploy Gate",
        "AGENTS_CLI_DISABLE_OVERRIDES=1 lets wrapper scripts run Syft + Grype checks and call native deploy without recursion.",
        "09 / 10",
    )
    s9.add_box(
        48, 130, 420, 340,
        [
            ("AGENTS-CLI-EXTENSION.YAML", "Google Sans", 10, "FDD663", True),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("schema: agents-cli-extension/v1alpha1", "Google Sans Mono", 9.5, "E8EAED", False),
            ("name: sbom-deploy", "Google Sans Mono", 9.5, "81C995", False),
            ("description: Scan project SBOM, then run native deploy.", "Google Sans Mono", 9.5, "E8EAED", False),
            ("requires:", "Google Sans Mono", 9.5, "E8EAED", False),
            ('  agents_cli: ">=1.5,<2"', "Google Sans Mono", 9.5, "FDD663", False),
            ("  on_incompatible: warn", "Google Sans Mono", 9.5, "E8EAED", False),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("commands:", "Google Sans Mono", 9.5, "E8EAED", False),
            ("  override:", "Google Sans Mono", 9.5, "8AB4F8", False),
            ("    deploy:", "Google Sans Mono", 9.5, "E8EAED", False),
            ('      run: ["bash", "scripts/sbom_then_deploy.sh"]', "Google Sans Mono", 9.5, "81C995", False),
            ("  add:", "Google Sans Mono", 9.5, "8AB4F8", False),
            ("    sbom-report:", "Google Sans Mono", 9.5, "E8EAED", False),
            ('      run: ["bash", "scripts/sbom_report.sh"]', "Google Sans Mono", 9.5, "81C995", False),
        ],
        fill_hex="131314", border_hex="3C4043", rounded=True, pad_l=18, pad_t=16, pad_r=18, pad_b=16,
    )
    s9.add_box(
        492, 130, 420, 340,
        [
            ("SCRIPTS/SBOM_THEN_DEPLOY.SH", "Google Sans", 10, "81C995", True),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("#!/usr/bin/env bash", "Google Sans Mono", 9.5, "9AA0A6", False),
            ("set -euo pipefail", "Google Sans Mono", 9.5, "E8EAED", False),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ('echo "[sbom-deploy] Generating CycloneDX SBOM..."', "Google Sans Mono", 9.5, "E8EAED", False),
            ("syft dir:. -o cyclonedx-json > /tmp/sbom.cdx.json", "Google Sans Mono", 9.5, "FDD663", False),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ('echo "[sbom-deploy] Scanning for critical CVEs..."', "Google Sans Mono", 9.5, "E8EAED", False),
            ("grype sbom:/tmp/sbom.cdx.json --fail-on critical", "Google Sans Mono", 9.5, "FDD663", False),
            ("", "Google Sans Mono", 4, "E8EAED", False),
            ("# Loader sets AGENTS_CLI_DISABLE_OVERRIDES=1", "Google Sans Mono", 9.5, "8AB4F8", True),
            ("# Delegates to built-in deploy with zero recursion!", "Google Sans Mono", 9.5, "8AB4F8", True),
            ('exec agents-cli deploy "$@"', "Google Sans Mono", 9.5, "81C995", True),
        ],
        fill_hex="131314", border_hex="3C4043", rounded=True, pad_l=18, pad_t=16, pad_r=18, pad_b=16,
    )
    s9.add_footer(
        True,
        "$ agents-cli extension add local@./extensions/sbom-deploy --yes",
        "AGENTS_CLI_DISABLE_OVERRIDES=1",
        "81C995",
    )
    slides.append(s9)

    # =========================================================================
    # SLIDE 10: Closing Bento Grid Summary + Bottom CTA Bar (Dark Stage #0E1015)
    # =========================================================================
    s10 = SlideBuilder("0E1015")
    s10.add_header(
        True,
        "Google Cloud Next '27 Summary",
        "8AB4F8",
        "The Open Agent Development Lifecycle",
        "",
        "10 / 10",
    )
    bento_tiles = [
        (48, 100, "01 • OPEN FRAMEWORKS", "8AB4F8", "LangChain & LangGraph", "First-party template with zero google-adk dependency and unified CompiledStateGraph."),
        (342, 100, "02 • LOCAL DEVELOPER EXPERIENCE", "81C995", "LangGraph Studio", "agents-cli playground boots LangGraph dev server on port 8080 for visual graph inspection."),
        (636, 100, "03 • QUALITY FLYWHEEL", "FDD663", "Vertex AI Evaluations", "Overridden eval generate pairs seamlessly with native eval grade and eval compare."),
        (48, 255, "04 • ENTERPRISE GOVERNANCE", "F28B82", "SBOM Pre-Deploy Gates", "Wrap deploy with Syft + Grype checks and delegate safely via AGENTS_CLI_DISABLE_OVERRIDES=1."),
        (342, 255, "05 • SUPPLY-CHAIN SECURITY", "8AB4F8", "SHA Lockfile Discipline", "Pinned commit SHAs in agents-cli-extensions.yaml ensure bit-for-bit reproducible CI builds."),
        (636, 255, "06 • SERVERLESS PRODUCTION", "81C995", "Cloud Run + A2A Protocol", "Exposes /.well-known/agent.json and /a2a/tasks/send over FastAPI on port 8080."),
    ]
    for bx, by, kicker, kcol, heading, desc in bento_tiles:
        s10.add_box(
            bx, by, 276, 140,
            [
                (kicker, "Google Sans Mono", 8.5, kcol, True),
                (heading, "Google Sans Display", 15, "FFFFFF", True),
                ("", "Google Sans Text", 4, "9AA0A6", False),
                (desc, "Google Sans Text", 10, "9AA0A6", False),
            ],
            fill_hex="161922", border_hex="2D3343", rounded=True, pad_l=16, pad_t=14, pad_r=16, pad_b=12,
        )

    # Bottom Callout Bar matching HTML Slide 10
    s10.add_rect(48, 415, 864, 72, "131C31", "4285F4", border_w_pt=1.5, rounded=True, adj=12000)
    s10.add_box(
        68, 425, 560, 52,
        [
            ("GET STARTED TODAY", "Google Sans", 9, "8AB4F8", True),
            ("https://github.com/sanketbisne/scalfod-langgraph-agentscli", "Google Sans Mono", 14, "FFFFFF", True),
        ],
        pad_l=0, pad_t=2, pad_r=0, pad_b=2,
    )
    s10.add_box(
        675, 433, 215, 36,
        [("uvx google-agents-cli setup", "Google Sans Mono", 10, "FFFFFF", True)],
        fill_hex="1A73E8", rounded=True, adj=20000, align="c", valign="ctr",
    )
    slides.append(s10)

    return slides


def write_pptx(output_path: Path) -> None:
    slides = build_slides()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    slide_ct_overrides = "\n".join(
        f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, len(slides) + 1)
    )
    content_types_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
{slide_ct_overrides}
</Types>"""

    root_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""

    sld_id_entries = "\n".join(
        f'    <p:sldId id="{255 + i}" r:id="rId{i + 2}"/>'
        for i in range(1, len(slides) + 1)
    )
    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
{sld_id_entries}
  </p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="screen16x9"/>
  <p:notesSz cx="{SLIDE_H}" cy="{SLIDE_W}"/>
</p:presentation>"""

    pres_rels_entries = "\n".join(
        f'  <Relationship Id="rId{i + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, len(slides) + 1)
    )
    pres_rels_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
{pres_rels_entries}
</Relationships>"""

    slide_master_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
  </p:sldLayoutIdLst>
</p:sldMaster>"""

    slide_master_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""

    slide_layout_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
             type="blank" preserve="1">
  <p:cSld name="Blank">
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""

    slide_layout_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""

    slide_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""

    theme_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="GoogleCloudNext27">
  <a:themeElements>
    <a:clrScheme name="GoogleCloud">
      <a:dk1><a:srgbClr val="202124"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="0E1015"/></a:dk2>
      <a:lt2><a:srgbClr val="F8F9FA"/></a:lt2>
      <a:accent1><a:srgbClr val="4285F4"/></a:accent1>
      <a:accent2><a:srgbClr val="EA4335"/></a:accent2>
      <a:accent3><a:srgbClr val="FBBC04"/></a:accent3>
      <a:accent4><a:srgbClr val="34A853"/></a:accent4>
      <a:accent5><a:srgbClr val="8AB4F8"/></a:accent5>
      <a:accent6><a:srgbClr val="81C995"/></a:accent6>
      <a:hlink><a:srgbClr val="4285F4"/></a:hlink>
      <a:folHlink><a:srgbClr val="9B72CB"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="GoogleSansScheme">
      <a:majorFont>
        <a:latin typeface="Google Sans Display"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:majorFont>
      <a:minorFont>
        <a:latin typeface="Google Sans Text"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="GoogleFormat">
      <a:fillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:fillStyleLst>
      <a:lnStyleLst>
        <a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="25400"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="38100"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
      </a:lnStyleLst>
      <a:effectStyleLst>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
      </a:effectStyleLst>
      <a:bgFillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>"""

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", root_rels_xml)
        zf.writestr("ppt/presentation.xml", presentation_xml)
        zf.writestr("ppt/_rels/presentation.xml.rels", pres_rels_xml)
        zf.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml)
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels_xml)
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml)
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels_xml)
        zf.writestr("ppt/theme/theme1.xml", theme_xml)

        for idx, slide in enumerate(slides, start=1):
            zf.writestr(f"ppt/slides/slide{idx}.xml", slide.to_xml())
            zf.writestr(f"ppt/slides/_rels/slide{idx}.xml.rels", slide_rels_xml)

    print(f"Generated 1-to-1 high-fidelity {len(slides)}-slide PPTX at: {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "docs" / "Cloud_Next_27_Agents_CLI_LangGraph.pptx"
    write_pptx(out)
