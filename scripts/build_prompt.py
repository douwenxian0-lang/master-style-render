#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
master-style-render 提示词组装引擎

复刻「灵雀AI 大师风格」的核心机制：四参数 -> 生图提示词。

用法:
    python build_prompt.py --space 客厅 --level 重新装修 --master 梁志天 --light 傍晚暖光
    python build_prompt.py -s 主卧 -l 软装更换 -m 如恩 --light 清早晨曦 --json
    python build_prompt.py --list                # 列出所有可选值

参数:
    -s/--space    空间   (默认 客厅)
    -l/--level    改动程度 (默认 中度改造)
    -m/--master   大师风格 (默认 无特定风格)
    --light       光线   (默认 傍晚暖光)
    --mode        模式   txt2img | img2img (默认 txt2img)
    --camera      机位   auto | floor | ceiling | corner | detail
    --json        以 JSON 输出（含参数对照表）
"""

import argparse
import json
import sys

# ---------------------------------------------------------------- 铺贴系统
# 材质品类：纹理母题 + 品类写法
TILE_TYPES = {
    "大理石纹": ("large-format porcelain slab with marble-look veining", "marble-like veining"),
    "洞石":     ("travertine-look porcelain with linear pitting and layered bands", "travertine-like layered pitting"),
    "玉石":     ("jade-look porcelain with translucent cloudy veining", "translucent jade-like veining"),
    "水泥灰":   ("cement-look porcelain with fine subtle mottling", "cement-like fine mottling"),
    "木纹":     ("wood-look porcelain plank with linear grain", "wood grain with linear flow"),
    "水磨石":   ("terrazzo-look porcelain with embedded chips", "terrazzo chips distribution"),
    "仿古":     ("rustic stone-look porcelain with 3D relief texture", "rustic 3D relief texture"),
    "素色岩板": ("solid-color sintered stone slab with uniform tone", "uniform solid tone"),
}

# 表面光泽：行为描述（不用形容词）
GLOSSES = {
    "亮光":   "high-gloss polished surface, sharp specular reflections, wet-look clarity",
    "柔光":   "soft satin sheen, broad diffuse reflection, low glare, no mirror-like gloss",
    "哑光":   "matte surface, minimal reflection, velvety light absorption",
    "肌肤釉": "skin-feel soft-touch glaze, silky matte hand, extremely soft diffuse reflection",
    "浮雕肌理": "dimensional relief surface with tactile ridges, directional texture, subtle self-shadowing",
}

# 缝宽档位
GROUTS = {
    "密缝": ("0.5-1mm", "tight-joint installation, joints under 1mm, almost invisible hairline lines, "
                       "tiles read as one continuous seamless surface"),
    "细缝": ("1.5-2mm", "narrow 1.5mm grout joints, color-matched fine grout, crisp straight joint lines"),
    "常规": ("3mm", "3mm wide cement grout joints, light grey grout, perfectly even joint width"),
    "宽缝": ("6-8mm", "8mm wide deep grout joints, contrasting dark grout, strong grid rhythm"),
    "美缝": ("按规格定", "epoxy grout, matching or contrasting color, glossy smooth joint surface, flush with tile"),
}

# 铺贴方式
BONDS = {
    "对缝": "stack bond, grid layout, joints perfectly aligned",
    "工字": "offset bond, half-tile staggered joints",
    "斜铺": "45-degree diagonal layout",
    "人字": "herringbone pattern",
    "鱼骨": "chevron pattern",
    "大板通铺": "continuous large-format slab layout, layout spans the floor with minimal joints",
}

# 铺贴面
SURFACES = {
    "地面": "floor",
    "墙面": "wall",
    "地面+墙面": "floor and wall",
}

# 材质高保真固定句
TILE_HONEST = ("man-made porcelain tile surface, printed ceramic glazing, uniform industrial finish, "
               "not natural stone slab, no natural stone imperfections")
TILE_REALISM = ("varied veining across each tile, no repeating pattern, vein flow continuing across joints, "
                "grout recessed 0.5mm below the tile surface, subtle shadow line along each joint, "
                "microscopic level differences between adjacent tiles")
TILE_L3_CLEAN = ("clean uninterrupted floor and wall planes, no rugs or carpets covering the tiled floor, "
                 "minimal furniture occlusion of the tiling")
TILE_NEG = ("uneven joint width, wavy joint lines, mismatched grid, random tile sizes, floating misaligned tiles, "
            "inconsistent spacing, bent joint lines around corners")

# ---------------------------------------------------------------- 画质 / 渲染收尾
QUALITY = ("photorealistic interior architectural photography, 8k ultra sharp detail, "
           "physically accurate global illumination, V-Ray render quality")
RENDER = ("professional architectural visualization, natural material response, "
          "subtle film grain, straight uncropped verticals")

NEGATIVE_BASE = ("distorted perspective, tilted verticals, warped walls, duplicated furniture, "
                 "text, watermark, logo, oversaturated, plastic look, cartoon, low-poly, fisheye")

# ---------------------------------------------------------------- 参数一：空间
SPACES = {
    "客厅":  ("spacious modern living room with sofa group, coffee table, TV or feature wall, "
              "floor-to-ceiling window",
              ""),
    "主卧":  ("master bedroom with king bed, bedside tables, wardrobe wall, large window with sheer curtain",
              ""),
    "次卧":  ("secondary bedroom with single or queen bed, desk, compact wardrobe", ""),
    "书房":  ("home study with desk, bookshelf wall, reading chair, task lighting", ""),
    "厨房":  ("modern kitchen with island counter, full-height cabinetry, backsplash, integrated appliances",
              ""),
    "餐厅":  ("dining room with dining table for six, pendant light above, sideboard, decorative wall", ""),
    "玄关":  ("entrance foyer with shoe cabinet, feature wall, mirror, lighting accent", ""),
    "卫生间": ("bathroom with double vanity, mirror, walk-in shower, freestanding tub, "
               "large-format tile wall", ""),
    "阳台":  ("balcony or terrace with lounge seating, planter greenery, glass railing, view beyond", ""),
    "大堂":  ("hotel lobby with reception desk area, double-height volume, feature art wall, lounge seating",
              "luxury five-star hotel"),
    "客房":  ("hotel guest room with bed, work desk, seating chair, minibar console, layered lighting",
              "luxury five-star hotel"),
}

# 空间英文名（用于纯文生图的 from-scratch 指令，保持 prompt 全英文）
SPACE_EN = {
    "客厅": "living room", "主卧": "master bedroom", "次卧": "secondary bedroom",
    "书房": "home study", "厨房": "kitchen", "餐厅": "dining room",
    "玄关": "entrance foyer", "卫生间": "bathroom", "阳台": "balcony",
    "大堂": "hotel lobby", "客房": "hotel guest room",
}

# ---------------------------------------------------------------- 参数二：改动程度
LEVELS = {
    "软装更换": ("preserve existing architecture, wall layout, window positions, floor and ceiling exactly; "
                 "replace only furniture, soft furnishings, textiles, lighting fixtures and decor",
                 "high", 0.85),
    "轻度翻新": ("keep structural layout and window openings unchanged; refresh wall and floor finishes, "
                 "replace furniture, fixtures and lighting",
                 "high", 0.80),
    "中度改造": ("retain overall structural grid and window positions; redesign partitions, wall and floor "
                 "finishes, ceiling design, furniture and lighting",
                 "medium", 0.65),
    "重新装修": ("redesign the entire interior; keep only the room's outer shell, window positions and "
                 "general proportions",
                 "medium", 0.50),
}

# ---------------------------------------------------------------- 参数三：大师风格
MASTERS = {
    "CCD": (
        "luxury five-star hotel lobby aesthetic, restrained modern oriental, symmetrical axial composition, "
        "warm beige travertine walls, grey marble, dark walnut wood veneer, brushed brass details, textured art paint, "
        "leather and linen upholstery, low furniture silhouettes with crisp rectangular lines, "
        "layered ambient lighting with concealed cove strips and precise accent spotlights, warm 2700K low-key glow, "
        "one curated art object as focal point, quiet luxury, generous negative space",
        "gaudy gold, cluttered layout, ornate floral pattern, saturated colors, plastic surface"),

    "如恩": (
        "poetic modernism by Neri&Hu, honest raw materials, exposed concrete and grey brick masonry, "
        "timber slat lattice screen, aged brass, glass block, linen drapery, "
        "geometric grid order, dramatic natural daylight casting sharp diagonal shadows, "
        "narrow slot lighting and a linear ceiling light band carving the space, "
        "muted grey palette with warm wood and matte black, architectural installation feel, contemplative mood",
        "decorative ornament, colorful accents, glossy plastic, ornate ceiling, chintz pattern"),

    "杨邦胜": (
        "oriental artistic conception, site-specific cultural narrative, Zen serenity, "
        "tea-beige palette with ink black and celadon accents, warm wood veneer, natural stone, linen, bamboo, "
        "handcrafted ceramic, soft diffused indirect lighting, luminous ceiling film mimicking skylight, "
        "subtle accent wash on feature wall, landscape-inspired decor, ink-wash painting mood, "
        "serene upscale hotel interior",
        "western classical ornament, neon color, heavy gold, cluttered props"),

    "吴滨": (
        "modern oriental (Modeng Dongfang) by W.DESIGN, poetic abstraction with western minimalism, "
        "smoky grey and greige base palette with muted emerald and oxblood accents as small gestures, "
        "hairline metal trims, silk velvet, honed marble, art plaster wall with subtle texture, "
        "thin-line elegant furniture with simplified oriental forms, "
        "hidden light sources washing walls, soft low-contrast gradient illumination, refined artful living space",
        "high contrast, bright saturated color, heavy ornament, rustic texture"),

    "孙建亚": (
        "quiet luxury minimalism, architectural proportion over decoration, generous negative space, "
        "travertine cladding, pale oak veneer, microcement floor, matte metal details, natural linen, "
        "warm ivory and pale oak palette with charcoal accents, floor-to-ceiling glazing flooding the space "
        "with daylight, soft linear light coves, gentle shadows, restrained elegance, nothing superfluous",
        "busy pattern, shiny chrome, dense furniture arrangement, warm cluttered styling"),

    "戴昆": (
        "bold Art Deco revival, high-saturation color blocking: deep emerald green with brass, burgundy red, "
        "peacock blue, cream base, marble inlay patterned flooring, metal trim moldings, silk velvet upholstery, "
        "antique mirror panels, hand-painted wallpaper, crystal chandelier and theatrical warm golden accent lighting, "
        "rich chiaroscuro, vintage-modern glamour, confident and dramatic, layered decorative detail",
        "minimal empty room, monochrome grey, plain white wall, no pattern"),

    "葛亚曦": (
        "restrained contemporary elegance with subtle oriental undertone by LSD, "
        "taupe and oatmeal palette with charcoal and a single vivid accent color, "
        "layered material subtlety: wood veneer, microcement, natural linen, aged brass, honed stone, "
        "sculptor-designed furniture pieces, gallery-grade art mixed with lived-in objects, "
        "soft indirect daylight, low contrast, quietly sophisticated and livable",
        "loud color blocking, ornate carving, glossy lacquer, cold clinical look"),

    "梁志天": (
        "modern minimalist luxury by Steve Leung, form follows function, clean precise lines and refined proportions, "
        "contrast of polished and matte surfaces: high-gloss wood veneer, marble, mirror panels, satin metal, leather, "
        "ivory and light grey palette with champagne and dark wood accents, "
        "bright even illumination with targeted accent spots and a linear or crystal pendant above the table, "
        "sophisticated hotel-residence elegance, immaculate detailing",
        "rustic texture, excessive ornament, dim moody lighting, industrial exposed concrete"),

    "无特定风格": (
        "clean contemporary interior design, neutral material palette, timeless proportions",
        "dated ornament, heavy pattern, oversaturated color"),
}

# ---------------------------------------------------------------- 参数四：光线
LIGHTS = {
    "清早晨曦": "early morning light, soft cool-white daylight, long gentle shadows, "
                "slightly blue-grey atmospheric cast, fresh and airy",
    "正午阳光": "bright midday sunlight, hard-edged contrast shadows, clear warm-neutral light, "
                "high dynamic range",
    "傍晚暖光": "golden hour warm light 2700K, soft amber glow across surfaces, long warm shadows, "
                "cozy romantic mood",
    "夜晚灯光": "night scene, layered artificial lighting, warm pools of light, dark surrounding, "
                "dramatic contrast, glowing fixtures and concealed strips, "
                "interior exclusively lit by its own fixtures and no daylight entering",
}

# ---------------------------------------------------------------- 机位预设
CAMERAS = {
    "auto":    "one-point perspective, camera at eye level 1.5m, 24mm wide angle, "
               "balanced symmetrical composition, straight verticals",
    "floor":   "low camera angle 0.8m emphasizing the floor plane, wide angle, straight verticals",
    "ceiling": "slightly upward angle showing ceiling and lighting layers, straight verticals",
    "corner":  "elevated 30 degree corner view showing the full room layout, straight verticals",
    "detail":  "close-up detail shot of the feature wall and material junction, shallow depth of field",
}


def build_tile_system(tile, gloss, fmt, grout, bond, surface):
    """组装 [铺贴系统] 段落；全部为 None 时返回空串（不启用该模块）"""
    if not any([tile, gloss, fmt, grout, bond, surface]):
        return "", ""

    if tile and tile not in TILE_TYPES:
        raise ValueError("未知材质品类: %s (可选: %s)" % (tile, "/".join(TILE_TYPES)))
    if gloss and gloss not in GLOSSES:
        raise ValueError("未知表面光泽: %s (可选: %s)" % (gloss, "/".join(GLOSSES)))
    if grout and grout not in GROUTS:
        raise ValueError("未知砖缝档位: %s (可选: %s)" % (grout, "/".join(GROUTS)))
    if bond and bond not in BONDS:
        raise ValueError("未知铺贴方式: %s (可选: %s)" % (bond, "/".join(BONDS)))
    if surface and surface not in SURFACES:
        raise ValueError("未知铺贴面: %s (可选: %s)" % (surface, "/".join(SURFACES)))

    seg = []
    head = "tile installation system: "
    if fmt:
        head += "%s " % fmt
    if tile:
        head += TILE_TYPES[tile][0]
    else:
        head += "large-format porcelain tiles"
    if surface:
        head += " applied on the %s" % SURFACES[surface]
    if bond:
        head += ", laid in %s" % BONDS[bond]
    if grout:
        head += ", %s" % GROUTS[grout][1]
    seg.append(head)

    if gloss:
        seg.append(GLOSSES[gloss])
    seg.append(TILE_HONEST)
    seg.append(TILE_REALISM)
    seg.append(TILE_L3_CLEAN)

    return ",\n".join(seg), TILE_NEG


def grout_mm(grout):
    return GROUTS[grout][0] if grout in GROUTS else "—"


def build(space="客厅", level="中度改造", master="无特定风格", light="傍晚暖光",
          mode="txt2img", camera="auto", tile=None, gloss=None, fmt=None,
          grout=None, bond=None, surface=None):
    """组装提示词，返回 (positive, negative, meta)"""
    if space not in SPACES:
        raise ValueError("未知空间: %s (可选: %s)" % (space, "/".join(SPACES)))
    if level not in LEVELS:
        raise ValueError("未知改动程度: %s (可选: %s)" % (level, "/".join(LEVELS)))
    if master not in MASTERS:
        raise ValueError("未知大师风格: %s (可选: %s)" % (master, "/".join(MASTERS)))
    if light not in LIGHTS:
        raise ValueError("未知光线: %s (可选: %s)" % (light, "/".join(LIGHTS)))
    if camera not in CAMERAS:
        raise ValueError("未知机位: %s (可选: %s)" % (camera, "/".join(CAMERAS)))

    space_desc, space_hint = SPACES[space]
    level_desc, fidelity, denoise = LEVELS[level]
    master_block, master_neg = MASTERS[master]

    try:
        tile_seg, tile_neg = build_tile_system(tile, gloss, fmt, grout, bond, surface)
    except ValueError as e:
        raise e

    parts = [QUALITY]

    if mode == "img2img":
        parts.append(level_desc)
    else:
        parts.append("design a complete %s from scratch" % SPACE_EN[space])

    desc = space_desc
    if space_hint:
        desc = "%s, %s" % (space_hint, desc)
    parts.append(desc)
    parts.append("style: %s" % master_block)
    if tile_seg:
        parts.append(tile_seg)
    parts.append(CAMERAS[camera])
    parts.append(LIGHTS[light])
    parts.append(RENDER)

    positive = ",\n".join(parts)
    negative = "%s, %s" % (NEGATIVE_BASE, master_neg)
    if tile_neg:
        negative = "%s, %s" % (negative, tile_neg)

    meta = {
        "参数": {"空间": space, "改动程度": level, "大师风格": master,
                 "光线": light, "模式": mode, "机位": camera},
        "图生图建议": {"input_fidelity": fidelity, "denoise": denoise,
                       "参考图预处理": "长边 1024px / JPEG q85 / <=500KB"},
    }
    if tile_seg:
        meta["铺贴系统"] = {
            "材质品类": tile or "未定（默认 large-format）",
            "表面光泽": gloss or "未定",
            "规格": fmt or "未定",
            "砖缝": "%s（%s）" % (grout or "未定", grout_mm(grout)),
            "铺贴方式": bond or "未定",
            "铺贴面": surface or "未定",
        }
    return positive, negative, meta


def main(argv=None):
    ap = argparse.ArgumentParser(description="大师风格提示词组装引擎")
    ap.add_argument("-s", "--space", default="客厅")
    ap.add_argument("-l", "--level", default="中度改造")
    ap.add_argument("-m", "--master", default="无特定风格")
    ap.add_argument("--light", default="傍晚暖光")
    ap.add_argument("--mode", default="txt2img", choices=["txt2img", "img2img"])
    ap.add_argument("--camera", default="auto", choices=list(CAMERAS))
    ap.add_argument("--tile", default=None, help="材质品类：%s" % "/".join(TILE_TYPES))
    ap.add_argument("--gloss", default=None, help="表面光泽：%s" % "/".join(GLOSSES))
    ap.add_argument("--format", dest="fmt", default=None, help="规格，如 750x1500")
    ap.add_argument("--grout", default=None, help="砖缝档位：%s" % "/".join(GROUTS))
    ap.add_argument("--bond", default=None, help="铺贴方式：%s" % "/".join(BONDS))
    ap.add_argument("--surface", default=None, help="铺贴面：%s" % "/".join(SURFACES))
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    ap.add_argument("--list", action="store_true", help="列出所有可选值")
    args = ap.parse_args(argv)

    if args.list:
        print("空间      :", " / ".join(SPACES))
        print("改动程度  :", " / ".join(LEVELS))
        print("大师风格  :", " / ".join(MASTERS))
        print("光线      :", " / ".join(LIGHTS))
        print("机位      :", " / ".join(CAMERAS))
        print("材质品类  :", " / ".join(TILE_TYPES))
        print("表面光泽  :", " / ".join(GLOSSES))
        print("砖缝档位  :", " / ".join(GROUTS))
        print("铺贴方式  :", " / ".join(BONDS))
        print("铺贴面    :", " / ".join(SURFACES))
        return 0

    try:
        positive, negative, meta = build(args.space, args.level, args.master,
                                         args.light, args.mode, args.camera,
                                         args.tile, args.gloss, args.fmt,
                                         args.grout, args.bond, args.surface)
    except ValueError as e:
        print("[错误] %s" % e, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"prompt": positive, "negative_prompt": negative, **meta},
                         ensure_ascii=False, indent=2))
    else:
        print("=" * 68)
        print("PROMPT")
        print("=" * 68)
        print(positive)
        print()
        print("-" * 68)
        print("NEGATIVE")
        print("-" * 68)
        print(negative)
        print()
        print("-" * 68)
        print("参数: %s" % " | ".join("%s=%s" % kv for kv in meta["参数"].items()))
        if "铺贴系统" in meta:
            print("铺贴: %s" % " | ".join("%s=%s" % kv for kv in meta["铺贴系统"].items()))
        print("图生图建议: input_fidelity=%s, denoise=%s, 参考图 %s"
              % (meta["图生图建议"]["input_fidelity"], meta["图生图建议"]["denoise"],
                 meta["图生图建议"]["参考图预处理"]))
        print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
