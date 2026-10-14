# 自定义风格提取案例

除内置大师外，任何参考图都可以走同一套「风格 DNA 提取 → 提示词块 → 出图验证 → 迭代」流程。
以下是第一个实测案例，提取流程与结论沉淀下来作为模板。

---

## 案例 01：卡莎杜拉「意式质感」（CASADUNL）

**参考图特征**（2026-09-22 实测提取）：
暖白无缝烤漆柜体 + 浅橡木岛台 + 浅灰褐水泥质感大板地面 + 黑框百叶窗 + 雕塑感吊灯群 + 黑色皮革悬臂椅。

### 风格 DNA

| 维度 | 特征 |
|---|---|
| 空间气质 | 意式极简、克制的暖、明亮通透 |
| 材质 | 暖象牙白哑光烤漆无缝柜体、浅橡木、浅灰褐水泥纹大板、哑光黑金属/电器、铬合金 |
| 色彩 | 象牙白 60% · 浅灰褐 25% · 浅橡木 10% · 哑光黑 5% |
| 光线 | 百叶窗过滤的柔和自然光、明亮 airy、软阴影 |
| 软装 | 深棕皮革悬臂椅（铬管脚）、雕塑感有机吊灯群、暖光灯带 |

### PROMPT BLOCK（终版，两轮迭代后）

```
Italian quiet luxury minimalism, monolithic warm ivory matte lacquer cabinetry, minimal flush-panel
fronts with fine shadow-gap reveal lines, pale oak wood island and recessed niche accents,
very pale warm-grey cement-look large-format tile floor with fine subtle mottling and soft satin sheen,
matte black window frames with venetian blinds, matte black built-in appliances,
sculptural organic pendant cluster, dark brown leather cantilever chairs with chrome tubular frames,
warm under-cabinet LED strip, refined restrained elegance, bright airy atmosphere
```

**负向词**：`ornate carving, saturated color, rustic clutter, glossy plastic, heavy drapery`

**口诀**：暖白无缝 + 橡木暖点 + 水泥大板 + 黑色利落

### 迭代记录（2026-09-22 实测）

| 轮次 | 偏差 | 修正 |
|---|---|---|
| 第 1 轮 | 地面偏深偏花（mottling 过重）；柜体拼接感强、不够整块 | 地面改 `very pale warm-grey + fine subtle mottling + soft satin sheen`；柜体改 `monolithic + fine shadow-gap reveal lines` |
| 第 2 轮 | 与参考图高度一致，验收 | — |

**教训**：`cement-look` 单独写会被 AI 加重纹理——必须叠加 `fine / subtle / pale` 三个限定词才压得住；
柜体「无缝」要用 `monolithic + shadow-gap` 表达，光写 `seamless` 会被忽略。

### 提取方法论（可复用流程）

1. **先定主材 4 件套**：墙面/柜体主材 + 地面主材 + 对比材质 + 金属件。参考图里占比最大的先写。
2. **色彩写配比不写名字**：`ivory 60% · greige 25% · oak 10% · black 5%`，比例比色名更能锁调性。
3. **光源必须写「经过什么」**：不是 `natural light`，而是 `daylight filtered through venetian blinds`——过滤介质决定光质。
4. **家具写「形制 + 材质 + 脚」**：`dark brown leather cantilever chairs with chrome tubular frames`，三要素齐了 AI 才不会自由发挥。
5. **出图验证 → 找偏差 → 改块**：第一次出图重点比对（a）地面质感强度（b）色彩配比（c）光质，哪个偏改哪个，不要整块重写。
