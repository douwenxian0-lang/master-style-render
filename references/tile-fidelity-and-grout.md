# 铺贴系统模块：材质高保真 + 砖缝可控

解决两个真实交付问题：**① 生成图里的瓷砖纹理不够还原（AI 画的是"石头"，不是"我们那款砖"）② 砖缝大小不受控**。

---

## 核心洞见：砖缝是 AI 的尺子

这是整个模块的理论支点。AI 判断纹理尺度的唯一依据，就是画面里的**砖缝与砖规格**：

- 只写 `large-format tile floor` → AI 自己猜尺度，纹理尺度随机 → 假
- 写了 `1200x600 slabs, tight 1mm joints` → AI 有了参照物 → 纹理尺度、缝宽、砖块比例同时对齐 → 真

所以**砖缝不是装饰细节，是尺度锚**。写规格 + 缝宽，等于给 AI 递了一把尺子，
材质还原度和缝宽可控性这两个问题会同时改善。这一点务必优先写。

---

## 一、材质高保真

### 1. 材质 DNA 五要素（照着写，不要漏）

| 要素 | 取值范围 | 示例 |
|---|---|---|
| 品类 | porcelain slab / ceramic wall tile / 木纹砖 / 仿古砖 / 微水泥砖 / 水磨石砖 | `large-format porcelain slab` |
| 表面处理与光泽 | polished / soft satin / matte / skin-feel soft-touch / 3D relief texture | `soft satin sheen, low gloss` |
| 纹理母题 | travertine / Carrara / Calacatta / 砂岩 / 玉石 / 水泥灰 / 木纹 / 水磨石 | `travertine-like veining` |
| 纹理尺度与走向 | large-scale / fine grain / directional flow / book-matched | `fine subtle mottling, no dominant veins` |
| 边缘与倒角 | rectified straight edge / micro-bevel / slight chamfer | `rectified straight edge, sharp arris` |

### 2. 第一道防线：声明这是工业瓷砖

AI 的默认倾向是把"大理石纹"画成真石材、把"木纹砖"画成真木头。必须显式声明：

```
man-made porcelain tile surface, printed ceramic glazing, uniform industrial finish, not natural stone slab
```

**这是材质还原度的第一道也是最有效的一道防线。**

### 3. 真实度四杀手与对策

| 杀手 | 现象 | 对策（直接写进 prompt） |
|---|---|---|
| 材质错位 | 瓷砖被画成真石头/真木头，有天然瑕疵 | `man-made porcelain, printed surface, no natural stone imperfections` |
| 尺度错乱 | 写明 750x1500，纹理却像 300x300 小砖 | 把规格 + 缝宽写进 prompt（尺度锚） |
| 图案重复 | 大面机械重复同一片纹理 → 一眼假 | `varied veining across each tile, no repeating pattern, continuous vein flow across joints` |
| 光泽失真 | 哑光砖画出镜面反射，亮光砖画出塑料感 | 光泽写到具体行为：`broad diffuse reflection, no mirror-like gloss` / `sharp specular reflections, wet-look polish` |

### 4. 高还原性三级方案（按还原度排序）

| 级别 | 做法 | 还原度 | 适用 |
|---|---|---|---|
| **L1 纯提示词** | 材质 DNA + 尺度锚 | 60–70% | 快速比方案、定风格方向 |
| **L2 图生图 + 产品图** | ImageGen `image1=空间现状`（或 Nano Banana Pro 多图：空间图 + 产品图），prompt 声明"材质取自参考图" | ~80% | 谈单主图、方案汇报 |
| **L3 真实纹理贴图** | AI 只负责构图 / 光影 / 软装，**地面墙面用真实产品高清图做透视贴图**（PS 变形 + 材质叠加，或 Blender 贴 PBR） | 100% | 对客户说"这就是你家铺这款砖"的唯一正解 |

**L3 是行业终局**：AI 永远画不出我们那款砖的印刷纹，但可以算出它的光影。
真实纹理贴图 + AI 光影的方案，既保真又好看，而且是同行做不到的交付物。
本模块的 prompt 侧优化主要服务于 L1/L2；L3 走图像合成流程（PS/Blender），prompt 侧只需保证
画面留出干净的铺贴面（见下方"给 L3 留路"写法）。

**给 L3 留路的写法**：prompt 里加 `clean uninterrupted floor and wall planes, minimal furniture occlusion of the floor,
no rugs or carpets covering the tiled floor` —— 保证地面大面积可见，后面好贴图。

---

## 二、砖缝可控

### 1. 缝宽档位表

| 档位 | 缝宽 | Prompt 片段 |
|---|---|---|
| 密缝 | 0.5–1mm | `tight-joint installation, joints under 1mm, almost invisible hairline lines, tiles read as one continuous seamless surface` |
| 细缝 | 1.5–2mm | `narrow 1.5mm grout joints, color-matched fine grout, crisp straight joint lines` |
| 常规 | 3mm | `3mm wide cement grout joints, light grey grout, perfectly even joint width` |
| 宽缝 | 6–8mm | `8mm wide deep grout joints, contrasting dark grout, strong grid rhythm` |
| 美缝 | 任意 | `epoxy grout, matching or contrasting color, glossy smooth joint surface, flush with tile` |

**用毫米值，不要用形容词。** `thin joints` 会被 AI 忽略，`1.5mm joints` 不会。
（缝宽太小无法用像素精确表现时，毫米值仍能约束 AI 的相对比例判断。）

### 2. 让砖缝"不像贴纸"的两个细节

真实砖缝的真实感来自**微高差与缝内阴影**，必须显式写：

```
grout recessed 0.5mm below the tile surface, subtle shadow line along each joint,
microscopic level differences between adjacent tiles
```

不加这句，AI 画出来的缝是一张平面网格线，像贴图；加了才有立体感。

### 3. 铺贴方式（bond pattern）

| 方式 | Prompt |
|---|---|
| 对缝 / 方格 | `stack bond, grid layout, joints perfectly aligned` |
| 工字 / 错缝 | `offset bond, half-tile staggered joints` |
| 斜铺 | `45-degree diagonal layout` |
| 人字 | `herringbone pattern` |
| 鱼骨 | `chevron pattern` |
| 大板通铺 | `continuous large-format slab layout, layout spans the floor with minimal joints` |

### 4. 规格决定空间气质（不是附属参数）

同一材质下，规格 + 缝宽直接改变空间观感，选型时要一起定：

| 组合 | 观感 | 场景 |
|---|---|---|
| 750x1500 密缝 | 整体、高级、无缝感 | 客厅、大平层通铺 |
| 900x1800 通铺 | 极简、岩板感 | 高端住宅、酒店公区 |
| 600x1200 细缝 | 克制、干净 | 常规居家主力 |
| 600x600 3mm 缝 | 规整、日常 | 厨卫、经济型 |
| 300x600 墙砖 2mm | 厨卫常规 | 卫生间墙面 |
| 200x200 宽缝 | 复古、手作感 | 阳台、复古风格 |

### 5. 负向词（必加）

```
uneven joint width, wavy joint lines, mismatched grid, random tile sizes, floating misaligned tiles,
inconsistent spacing, bent joint lines around corners
```

---

## 三、完整铺贴段落模板

组装时把这一段插在 `[大师风格DNA]` 之后：

```
tile installation system: {规格} porcelain tiles laid in {铺贴方式}, {缝宽档位描述},
{tile 材质 DNA 五要素}, man-made porcelain tile surface, printed ceramic glazing, uniform industrial finish, not natural stone slab,
varied veining across each tile, no repeating pattern,
grout recessed 0.5mm below the tile surface, subtle shadow line along each joint,
microscopic level differences between adjacent tiles,
clean uninterrupted floor and wall planes, no rugs covering the tiled floor
--no uneven joint width, wavy joint lines, mismatched grid, random tile sizes, floating misaligned tiles
```

---

## 四、实测记录

**2026-09-22 毛坯房 A/B 实测**（同一毛坯现状图，同机位，同水泥灰柔光材质，ImageGen img2img input_fidelity=medium）：

| 组 | 规格 / 缝宽 / 铺贴 | 结果 |
|---|---|---|
| A | 750x1500 / 密缝 <1mm / 大板通铺 | 大板观感、缝极细带阴影、纹理连贯跨缝，空间整体高级 ✅ |
| B | 600x600 / 常规 3mm / 对缝方格 | 方格规整、缝宽明显、砖块比例小，空间日常规整 ✅ |

**结论**：① 缝宽档位与规格**可受控**——毫米值 + 对缝/通铺写法有效；
② 同材质下「规格 + 缝宽」切换直接改变空间气质，验证「砖缝是尺子」；
③ 材质保真句（man-made porcelain + varied veining + grout recessed）出图纹理无「真石头感」、无图案重复。

**附赠验证**：上一轮栏杆被 AI 改成玻璃，本轮在 prompt 里点名
`dark metal vertical baluster railing` 后被正确保留——**结构细节要点名材质才锁得住**。
