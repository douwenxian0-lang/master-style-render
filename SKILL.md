---
name: master-style-render
version: 1.0.0
description: 复刻「灵雀AI 大师风格」的完整方法——内置 8 位室内设计大师 + 10 位建筑设计大师的风格提示词库，通过「空间 × 改动程度 × 大师风格 × 光线」四参数自动组装生图提示词，走文生图/图生图出效果图。适用于旧改升级、效果风格迁移、建筑外观风格迁移。
trigger:
  - 大师风格
  - 大师风格效果图
  - 梁志天风格
  - CCD 风格
  - 如恩风格
  - 吴滨风格
  - 摩登东方
  - 旧改升级
  - 老房翻新效果图
  - 效果风格迁移
  - 风格迁移到我的空间
  - 建筑大师风格
  - master style render
---

# master-style-render（大师风格效果图）

把「某个大师的设计语言」变成可参数化调用的生图指令——**不是让 AI 自由发挥，而是锁死风格 DNA 后出图**。

本 Skill 逆向自灵雀AI的「大师风格」产品（8 位室内大师 + 10 位建筑大师），
把它的三层结构完整复刻并做了增强：**风格库 → 参数组装 → 图生图引擎**。

## 三层结构（复刻自原产品）

| 层 | 原产品 | 本 Skill |
|---|---|---|
| 风格库 | 8 位室内 + 10 位建筑，各一份风格描述 | `references/interior-masters.md` / `architecture-masters.md`，每位含完整风格 DNA + 英文提示词块 + 负向词；自定义风格提取流程见 `references/custom-style-extraction.md`（含实测案例） |
| 参数组装 | 4 个下拉框拼 prompt | `references/assembler.md` + `scripts/build_prompt.py`，可 CLI 直接出 prompt |
| 生图引擎 | 上传图 + 出图 | ImageGen / Nano Banana Pro / ComfyUI，改动程度决定保留结构强度 |
| **铺贴系统**（本 Skill 新增） | 无 | `references/tile-fidelity-and-grout.md`：材质高保真（L1/L2/L3 三级）+ 砖缝可控（档位表 + 尺度锚原理），CLI 参数 `--tile --gloss --format --grout --bond --surface` |

## 铺贴系统模块（材质保真 + 砖缝可控）

**核心洞见：砖缝是 AI 的尺子。** AI 判断纹理尺度的唯一依据就是画面里的砖缝与砖规格。
写 `large-format tile floor` → AI 猜尺度 → 纹理假；写 `1200x600 slabs, tight 1mm joints` →
纹理尺度、缝宽、砖块比例同时对齐。**规格 + 缝宽是尺度锚，不是装饰细节。**

解决两个交付问题：

1. **材质还原度**——三个杀手逐个堵：① 材质错位（瓷砖画成真石头）→ 必须加
   `man-made porcelain tile surface, printed ceramic glazing, not natural stone slab`；
   ② 尺度错乱 → 写规格；③ 图案重复 → `varied veining across each tile, no repeating pattern`。
   还原度三级：L1 纯提示词 60–70% / L2 图生图 + 产品图 ~80% / **L3 真实产品纹理贴图 100%**（终局方案）。
2. **砖缝可控**——五档位：密缝 0.5–1mm / 细缝 1.5–2mm / 常规 3mm / 宽缝 6–8mm / 美缝。
   **用毫米值，不用形容词**（`thin joints` 会被忽略，`1.5mm joints` 不会）。
   让缝不像贴纸的两句必加：`grout recessed 0.5mm below the tile surface` +
   `subtle shadow line along each joint`。组装器已自动带上。

完整参数表与写法见 `references/tile-fidelity-and-grout.md`。

## 三个入口（与原产品对齐）

### 入口一：旧改升级（最常用）
上传**现状照片** → 四参数 → 出效果图。

```
空间：客厅 / 主卧 / 次卧 / 书房 / 厨房 / 餐厅 / 玄关 / 卫生间 / 阳台 / 大堂 / 客房
改动程度：软装更换 / 轻度翻新 / 中度改造 / 重新装修
大师风格：CCD / 如恩 / 杨邦胜 / 吴滨 / 孙建亚 / 戴昆 / 葛亚曦 / 梁志天 / 无特定风格
光线：清早晨曦 / 正午阳光 / 傍晚暖光 / 夜晚灯光
```

**改动程度是本方法最关键的一个参数**——它直接决定图生图时保留多少原结构，
原文没讲透，但这是唯一能防止「AI 把房子画变形」的开关（详见 assembler.md）。

### 入口二：效果风格迁移
已有**效果图** + **意向参考图** → 双图输入，把参考的风格迁到当前空间。
- 首选 **Nano Banana Pro**（多图输入，结构保真最好）
- 或 ImageGen 图生图：`image=现有效果图`，prompt 里用参考图描述风格 DNA

### 入口三：建筑外观风格迁移
建筑线稿/原建筑照片 + 建筑大师风格。
- 现代公建 → 扎哈·哈迪德 / 安藤忠雄
- 文旅住宅 → 马岩松 / 王澍
- 文化建筑 → 贝聿铭 / 何镜堂

## 执行流程

### Step 1 拿齐四参数
用户没给全就问，别猜。**最少要「空间 + 大师风格」**，其余可给默认值（改动程度默认「中度改造」，光线默认「傍晚暖光」）。

### Step 2 组装 prompt
```bash
# 基础四参数
python scripts/build_prompt.py --space 客厅 --level 重新装修 --master 梁志天 --light 傍晚暖光

# 带铺贴系统（推荐：规格+缝宽是尺度锚）
python scripts/build_prompt.py -s 客厅 -l 重新装修 -m 孙建亚 --light 清早晨曦 \
  --tile 水泥灰 --gloss 柔光 --format 750x1500 --grout 密缝 --bond 大板通铺 --surface 地面
```
或手工按 `references/assembler.md` 的模板拼。结构固定：

```
[画质] + [改动指令] + [空间描述] + [大师风格DNA] + [铺贴系统] + [光线] + [机位] + [渲染质感] + [负向]
```

### Step 3 出图
- **文生图**：直接投组装好的英文 prompt
- **图生图（旧改）**：压缩参考图到长边 1024px / JPEG q85 / ≤500KB 后作为 image 输入
  （ImageGen 有请求体大小限制，原图 >1MB 会报 `maxBodyLength`）
- **风格迁移**：优先 Nano Banana Pro，双图输入

### Step 4 交付
- 命名：`空间_大师_光线.png`（如 `客厅_梁志天_傍晚暖光.png`）
- 回传：所用 prompt + 参数对照 + 大师风格要点说明（为什么这么出）

## 关键原则

1. **风格 DNA 优先于形容词**。不要写「高端大气」——写材质、色彩、光线、家具语言。
   每位大师的 DNA 已固化在 references 里，照抄不要自己发挥。
2. **方向描述用上/下/左/右**，不用东南西北。
3. **大师风格 ≠ 抄图**。学的是设计语言（材质配比、光线逻辑、秩序关系），不是复制某个项目。
4. **一次一变量**。想比风格就让用户换大师重跑，不要在一个 prompt 里混两位大师。

## 配套 Skill
- `render-prompt-expert`：瓷砖材质 PBR 参数映射 + 图生图压缩规则（本 Skill 复用其压缩流程）
- `render-prompt-expert/references/param-bank.md`：5 类瓷砖材质参数表

## 信用点提示
ImageGen 出图约 5–10 信用点/张，图生图同价。批量前先算总量告知用户。
