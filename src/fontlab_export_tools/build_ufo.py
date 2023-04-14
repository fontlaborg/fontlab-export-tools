#!/usr/bin/env python3

from .utils import read_config
from pathlib import Path
from fontTools.ttLib import TTFont
from ufoLib2 import Font as UFont
from defcon import Font as DFont, UnicodeData, Glyph
from extractor.formats.opentype import extractFontFromOpenType


class FontBuilder:
    def __init__(self, config_path):
        self.config = read_config(config_path)
        self.copy_info = [
            "unitsPerEm",
            "descender",
            "xHeight",
            "capHeight",
            "ascender",
            "italicAngle",
            "openTypeHeadFlags",
            "openTypeHheaAscender",
            "openTypeHheaDescender",
            "openTypeHheaLineGap",
            "openTypeHheaCaretSlopeRise",
            "openTypeHheaCaretSlopeRun",
            "openTypeHheaCaretOffset",
            "openTypeOS2WeightClass",
            "openTypeOS2Selection",
            "openTypeOS2Panose",
            "openTypeOS2FamilyClass",
            "openTypeOS2UnicodeRanges",
            "openTypeOS2CodePageRanges",
            "openTypeOS2TypoAscender",
            "openTypeOS2TypoDescender",
            "openTypeOS2TypoLineGap",
            "openTypeOS2WinAscent",
            "openTypeOS2WinDescent",
            "openTypeOS2SubscriptXSize",
            "openTypeOS2SubscriptYSize",
            "openTypeOS2SubscriptXOffset",
            "openTypeOS2SubscriptYOffset",
            "openTypeOS2SuperscriptXSize",
            "openTypeOS2SuperscriptYSize",
            "openTypeOS2SuperscriptXOffset",
            "openTypeOS2SuperscriptYOffset",
            "openTypeOS2StrikeoutSize",
            "openTypeOS2StrikeoutPosition",
            "openTypeVheaVertTypoAscender",
            "openTypeVheaVertTypoDescender",
            "openTypeVheaVertTypoLineGap",
            "openTypeVheaCaretSlopeRise",
            "openTypeVheaCaretSlopeRun",
            "openTypeVheaCaretOffset",
            "postscriptSlantAngle",
            "postscriptUnderlineThickness",
            "postscriptUnderlinePosition",
            "postscriptIsFixedPitch",
            "postscriptDefaultWidthX",
            "postscriptNominalWidthX",
            "postscriptDefaultCharacter",
            "postscriptWindowsCharacterSet",
            "_openTypeOS2WidthClass",
            "styleMapStyleName",
        ]

    def load_fonts(self, mod_path, ref_path):
        self.mod_path = Path(mod_path)
        self.mod_ufo = DFont(self.mod_path)
        self.mod_info = self.mod_ufo.info
        self.mod_cmap = self.get_cmap(self.mod_ufo)
        self.ref_path = Path(ref_path)
        self.ref_ttx = TTFont(self.ref_path)
        self.ref_ufo = DFont()
        extractFontFromOpenType(
            self.ref_path,
            self.ref_ufo,
            doInfo=True,
            doGlyphs=True,
            doKerning=True,
            doGlyphOrder=True,
            doInstructions=False,
        )
        self.ref_info = self.ref_ufo.info
        self.ref_cmap = self.get_cmap(self.ref_ufo)
        self.stem = self.mod_path.stem

    def get_cmap(self, ufo):
        return {
            uni: mod_glyph.name
            for mod_glyph in ufo
            for uni in mod_glyph.unicodes
        }

    def save_font(self):
        self.mod_ufo.save()

    def update_font_info(self, patch=None):
        for copy_attr in self.copy_info:
            rattr = getattr(self.ref_ufo.info, copy_attr)
            attr = getattr(self.mod_info, copy_attr)
            if (type(rattr) == type(attr)) and attr != rattr:
                print(
                    f"{self.stem}: Updating family fontinfo `{copy_attr}`\n  from `{attr}`\n    to `{rattr}`"
                )
                setattr(self.mod_info, copy_attr, rattr)
        for copy_attr, rattr in self.config.get("fontinfo", {}).items():
            attr = getattr(self.mod_info, copy_attr)
            if attr != rattr:
                print(
                    f"{self.stem}: Updating family fontinfo `{copy_attr}`\n  from `{attr}`\n    to `{rattr}`"
                )
                setattr(self.mod_info, copy_attr, rattr)
        self.mod_info.openTypeOS2Type = []
        if patch:
            for copy_attr, rattr in patch.get("fontinfo", {}).items():
                attr = getattr(self.mod_info, copy_attr)
                if attr != rattr:
                    print(
                        f"{self.stem}: Updating master fontinfo `{copy_attr}`\n  from `{attr}`\n    to `{rattr}`"
                    )
                    setattr(self.mod_info, copy_attr, rattr)        

    def update_unicodes(self, patch=None):
        for uni, name in self.ref_cmap.items():
            ref_glyph = self.ref_ufo[name]
            if name in self.mod_ufo.keys():
                mod_glyph = self.mod_ufo[name]
                if mod_glyph.unicodes != ref_glyph.unicodes:
                    print(
                        f"{self.stem}: Updating unicodes for {name} from {mod_glyph.unicodes} to {ref_glyph.unicodes}"
                    )
                    mod_glyph.unicodes = ref_glyph.unicodes
        self.mod_cmap = self.get_cmap(self.mod_ufo)

    def update_widths(self, patch=None):
        for uni, name in self.ref_cmap.items():
            ref_glyph = self.ref_ufo[name]
            if uni in self.mod_cmap:
                mod_glyph = self.mod_ufo[self.mod_cmap[uni]]
                if mod_glyph.width != ref_glyph.width:
                    print(
                        f"{self.stem}: Updating `{name}` width from `{mod_glyph.width}` to `{ref_glyph.width}`"
                    )
                    mod_glyph.width = ref_glyph.width

    def add_glyphs(self, patch=None):
        for uni, name in self.ref_cmap.items():
            ref_glyph = self.ref_ufo[name]
            if name not in self.mod_ufo.keys() and uni not in self.mod_cmap:
                mod_glyph = Glyph()
                mod_glyph.name = name
                mod_glyph.unicodes = ref_glyph.unicodes
                mod_glyph.width = ref_glyph.width
                print(f"{self.stem}: Adding mod_glyph `{name}`")
                self.mod_ufo.insertGlyph(mod_glyph)

    def update_glyphs(self, patch=None):
        self.update_unicodes(patch)
        self.update_widths(patch)
        self.add_glyphs(patch)

    def fixes(self, patch=None):
        fixes = self.config.get("fixes", {})
        for fix_name, fix_value in fixes.items():
            if (
                fix_name == "nbspace"
                and fix_value
                and self.mod_cmap.get(0x00A0, None)
                and self.mod_cmap.get(0x0020, None)
            ):
                self.mod_ufo[self.mod_cmap[0x00A0]].width = self.mod_ufo[
                    self.mod_cmap[0x0020]
                ].width

    def patch(self, mod_path, ref_path, patch):
        self.load_fonts(mod_path, ref_path)
        self.update_font_info(patch)
        self.update_glyphs(patch)
        if self.config.get("fixes", None):
            self.fixes(patch)
        self.save_font()

    def apply_patches(self):
        for patch in self.config.fonts:
            self.patch(mod_path=patch["ufo_path"], ref_path=patch["ref_path"], patch=patch)


def build_ufo(config_path):
    b = FontBuilder(config_path)
    b.apply_patches()
