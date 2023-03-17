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
            "styleName",
            "styleMapStyleName",
        ]

    def patch(self, ufo_path, ref_path):
        ufo = DFont(ufo_path)
        old_ufo = DFont(ufo_path)
        info = ufo.info
        # print(f"{info=}")
        info.openTypeOS2Type = []
        ref = TTFont(ref_path)
        rufo = DFont()
        # print(f"{rufo=}")
        extractFontFromOpenType(
            ref_path,
            rufo,
            doInfo=True,
            doGlyphs=True,
            doKerning=True,
            doGlyphOrder=True,
            doInstructions=False,
        )
        for copy_attr in self.copy_info:
            rattr = getattr(rufo.info, copy_attr)
            attr = getattr(info, copy_attr)
            if rattr and attr != rattr:
                print(f"Updating `info.{copy_attr}`\n  from `{attr}`\n    to `{rattr}`")
                setattr(info, copy_attr, rattr)
        for copy_attr, rattr in self.config.get("fontinfo", {}).items():
            attr = getattr(info, copy_attr)
            if attr != rattr:
                print(f"Updating `info.{copy_attr}`\n  from `{attr}`\n    to `{rattr}`")
                setattr(info, copy_attr, rattr)

        rcmap = {uni: glyph.name for glyph in rufo for uni in glyph.unicodes}
        cmap = {uni: glyph.name for glyph in ufo for uni in glyph.unicodes}
        for uni, name in rcmap.items():
            rglyph = rufo[name]
            if uni in cmap:
                glyph = ufo[cmap[uni]]
                if glyph.width != rglyph.width:
                    print(
                        f"Updating `{name}` width from `{glyph.width}` to `{rglyph.width}`"
                    )
                    glyph.width = rglyph.width
            elif name in ufo.keys():
                glyph = ufo[name]
                print(
                    f"Updating unicodes for {name} from {glyph.unicodes} to {rglyph.unicodes}"
                )
                glyph.unicodes = rglyph.unicodes
            else:
                glyph = Glyph()
                glyph.name = name
                glyph.unicodes = rglyph.unicodes
                glyph.width = rglyph.width
                print(f"Adding glyph `{name}`")
                ufo.insertGlyph(glyph)
        ufo.save()

    def apply_patches(self):
        for patch in self.config.ufo_patches:
            self.patch(patch["ufo_path"], patch["ref_path"])


def build_ufo(config_path):
    b = FontBuilder(config_path)
    b.apply_patches()
