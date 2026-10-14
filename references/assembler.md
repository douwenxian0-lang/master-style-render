# 参数组装规则（空间 × 改动程度 × 大师风格 × 光线）

## 组装模板

```
{QUALITY}, {TASK_DIRECTIVE}, {SPACE_DESC}, style: {MASTER_BLOCK}, {CAMERA}, {RENDER}, --no {NEGATIVE}
```

| 槽位 | 来源 | 说明 |
|---|---|---|
| QUALITY | 固定 | 画质锚点，永远放最前 |
| TASK_DIRECTIVE | 改动程度 | **图生图成败关键**，见下表 |
| SPACE_DESC | 空间 | 空间类型 + 该空间的功能元素 |
| MASTER_BLOCK | 大师风格 | 从 references 原样插入 |
| CAMERA | 空间默认值 | 机位与构图 |
| RENDER | 固定 | 渲染质感收尾 |
| NEGATIVE | 固定 + 大师负向 | 排除项 |

`QUALITY`：
```
photorealistic interior architectural photography, 8k ultra sharp detail, physically accurate global illumination, V-Ray render quality
```
`RENDER`：
```
professional architectural visualization, natural material response, subtle film grain, straight uncropped verticals
```
`NEGATIVE`（固定部分）：
```
distorted perspective, tilted verticals, warped walls, duplicated furniture, text, watermark, logo, oversaturated, plastic look, cartoon, low-poly, fisheye
```

---

## 参数一：空间 → SPACE_DESC

| 空间 | SPACE_DESC |
|---|---|
| 客厅 | `spacious modern living room with sofa group, coffee table, TV or feature wall, floor-to-ceiling window` |
| 主卧 | `master bedroom with king bed, bedside tables, wardrobe wall, large window with sheer curtain` |
| 次卧 | `secondary bedroom with single or queen bed, desk, compact wardrobe` |
| 书房 | `home study with desk, bookshelf wall, reading chair, task lighting` |
| 厨房 | `modern kitchen with island counter, full-height cabinetry, backsplash, integrated appliances` |
| 餐厅 | `dining room with dining table for six, pendant light above, sideboard, decorative wall` |
| 玄关 | `entrance foyer with shoe cabinet, feature wall, mirror, lighting accent` |
| 卫生间 | `bathroom with double vanity, mirror, walk-in shower, freestanding tub, large-format tile wall` |
| 阳台 | `balcony or terrace with lounge seating, planter greenery, glass railing, view beyond` |
| 大堂（酒店） | `hotel lobby with reception desk area, double-height volume, feature art wall, lounge seating` |
| 客房（酒店） | `hotel guest room with bed, work desk, seating chair, minibar console, layered lighting` |

**默认机位（CAMERA）**：`one-point perspective, camera at eye level 1.5m, 24mm wide angle, balanced symmetrical composition, straight verticals`

按需替换：
- 强调地面铺贴 → `low camera angle 0.8m emphasizing the floor plane`
- 强调天花与灯 → `slightly upward angle showing ceiling and lighting layers`
- 空间全貌 → `elevated 30° corner view showing full room layout`
- 局部特写 → `close-up detail shot of the feature wall and material junction`

---

## 参数二：改动程度 → TASK_DIRECTIVE（最重要）

这个参数控制**图生图时保留多少原结构**。原文没讲透，但它是唯一能防「AI 把房子画变形」的开关。

| 选项 | TASK_DIRECTIVE | input_fidelity | 适用 |
|---|---|---|---|
| 软装更换 | `preserve existing architecture, wall layout, window positions, floor and ceiling exactly; replace only furniture, soft furnishings, textiles, lighting fixtures and decor` | high (0.85+) | 硬装不动，只换家具陈设 |
| 轻度翻新 | `keep structural layout and window openings unchanged; refresh wall and floor finishes, replace furniture, fixtures and lighting` | high (0.75–0.85) | 换面层材料 |
| 中度改造 | `retain overall structural grid and window positions; redesign partitions, wall and floor finishes, ceiling design, furniture and lighting` | medium (0.55–0.7) | 常规改造 |
| 重新装修 | `redesign the entire interior; keep only the room's outer shell, window positions and general proportions` | medium-low (0.4–0.55) | 全面重做 |

**注**：`input_fidelity` 为参考值，ImageGen 图生图接口以 `input_fidelity="high"` 为准；
若模型支持数值权重（ComfyUI / 某些 API），按上表区间调 denoise。

**纯文生图时**：TASK_DIRECTIVE 退化为 `design a complete {space} from scratch,`。

### 实测记录（2026-09-22，毛坯房图生图）

毛坯房现状（左侧阳台门洞 + 城市景观）+ 意式质感块 + 「重新装修」指令，一轮出图验收：
门洞位置、栏杆、外部景观、机位全部保住，室内完整重做。
关键写法：**外壳保留必须点名景观**——`the balcony opening on the left with its railing,
the city skyline and green trees visible outside`，只写 `window positions` AI 会自作主张改观景面。
毛坯房可直接投图（489KB 内无需压缩），另加 `no construction debris` 压掉杂物残留。

---

## 参数三：大师风格 → MASTER_BLOCK

从 `references/interior-masters.md` 或 `architecture-masters.md` 整块插入。
选项：CCD / 如恩 / 杨邦胜 / 吴滨 / 孙建亚 / 戴昆 / 葛亚曦 / 梁志天 / 无特定风格。

「无特定风格」→ `clean contemporary interior design, neutral material palette, timeless proportions`

---

## 参数四：光线 → LIGHT

| 选项 | 英文片段 |
|---|---|
| 清早晨曦 | `early morning light, soft cool-white daylight, long gentle shadows, slightly blue-grey atmospheric cast, fresh and airy` |
| 正午阳光 | `bright midday sunlight, hard-edged contrast shadows, clear warm-neutral light, high dynamic range` |
| 傍晚暖光 | `golden hour warm light 2700K, soft amber glow across surfaces, long warm shadows, cozy romantic mood` |
| 夜晚灯光 | `night scene, layered artificial lighting, warm pools of light, dark surrounding, dramatic contrast, glowing fixtures and concealed strips` |

夜光场景额外追加：`interior exclusively lit by its own fixtures, no daylight entering`

---

## 完整示例

**输入**：客厅 / 重新装修 / 梁志天 / 傍晚暖光

```
photorealistic interior architectural photography, 8k ultra sharp detail, physically accurate global illumination, V-Ray render quality,
redesign the entire interior; keep only the room's outer shell, window positions and general proportions,
spacious modern living room with sofa group, coffee table, TV or feature wall, floor-to-ceiling window,
style: modern minimalist luxury by Steve Leung, form follows function, clean precise lines and refined proportions, contrast of polished and matte surfaces: high-gloss wood veneer, marble, mirror panels, satin metal, leather, ivory and light grey palette with champagne and dark wood accents, bright even illumination with targeted accent spots and a linear or crystal pendant above the table, sophisticated hotel-residence elegance, immaculate detailing,
one-point perspective, camera at eye level 1.5m, 24mm wide angle, balanced symmetrical composition, straight verticals,
golden hour warm light 2700K, soft amber glow across surfaces, long warm shadows, cozy romantic mood,
professional architectural visualization, natural material response, subtle film grain, straight uncropped verticals
--no distorted perspective, tilted verticals, warped walls, duplicated furniture, text, watermark, logo, oversaturated, plastic look, cartoon, low-poly, fisheye, rustic texture, excessive ornament, dim moody lighting, industrial exposed concrete
```

---

## 风格迁移模式（入口二）

双图输入，不做改动程度参数，改用**分离语法**：

```
[风格提取] Transfer ONLY the design language — material palette, color scheme, lighting logic, furniture style, spatial order — from the reference image.
[结构锁定] Keep the geometry, layout, camera angle and proportions of the original image completely unchanged.
[禁止] Do not copy any specific object, artwork or layout element from the reference.
[目标] + {大师 DNA 或纯风格描述} + {LIGHT 可保留原图} + {RENDER}
```

**首选工具**：Nano Banana Pro（多图输入保结构最强）。
**ImageGen 图生图**：只支持单图，需先用一段文字概括参考图风格再作为 prompt 传入。
