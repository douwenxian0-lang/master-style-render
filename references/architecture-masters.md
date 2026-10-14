# 建筑设计大师风格库（10 位）

用于「建筑外观风格迁移」——上传建筑线稿/现状照片，锁风格 DNA 后出效果图。

**选型指引（对齐原产品）**
- 现代公建 → 扎哈·哈迪德 / 安藤忠雄
- 文旅住宅 → 马岩松 / 王澍
- 文化建筑 → 贝聿铭 / 何镜堂
- 高技办公 → 诺曼·福斯特 / 让·努维尔
- 在地实验 → 刘家琨 / 张永和

---

## 国际大师

### 1. 贝聿铭 I.M. Pei
几何纯粹主义，光影雕刻空间，东西方交融的庭院序列。
```
I.M. Pei language: pure Euclidean geometry, monumental yet serene volumes, sculpted light and shadow,
smooth precast concrete, warm limestone, steel-and-glass pyramid skylight, water court reflections,
stepped terrace series, restrained monumentality, East-meets-West courtyard sequence, timeless clarity
```
负向：`organic blob form, chaotic massing, neon facade`

### 2. 让·努维尔 Jean Nouvel
玻璃幕墙的影像化，光与色彩的滤网，立面即媒介。
```
Jean Nouvel language: dematerialized glass facade as a filter of light and image, diaphanous layering,
mechanized aperture screens, perforated metal, patterned mashrabiya-like skin, planted vertical garden,
vivid projected color and shifting transparency, dense urban context dialogue, cinematic facade
```
负向：`solid blank wall, plain brick, traditional pitched roof`

### 3. 诺曼·福斯特 Norman Foster
高技派，钢结构外露，可持续与精密构造。
```
Norman Foster language: high-tech expression, exposed structural steel, seamless glass curtain wall,
long-span lightweight roof, precise engineered detailing, diagrid structure, generous atrium,
environmental sustainability integrated, immaculate industrial refinement, corporate clarity
```
负向：`rustic, handcrafted irregularity, heavy masonry, ornament`

### 4. 扎哈·哈迪德 Zaha Hadid
参数化流体，无直角，动感未来。
```
Zaha Hadid language: parametric fluid geometry, no right angles, continuous flowing surfaces,
sweeping cantilevers, seamless white GRC panels and glass, dynamic deformation, aerodynamic massing,
futuristic iconic form, sharp shadow lines across curved skin, seamless interior-exterior continuity
```
负向：`orthogonal box, traditional detail, decorative molding, flat facade`

### 5. 安藤忠雄 Tadao Ando
清水混凝土，几何体块，光的精神性。
```
Tadao Ando language: fair-faced exposed concrete with visible tie-holes, pure geometric volumes,
framed sky opening and cross-shaped light slot, dramatic natural light incision,
shadow as material, minimalist austerity, water and wind in courtyard, spiritual silence, disciplined void
```
负向：`ornate, colorful, curved organic form, applied decoration, bright glossy finish`

---

## 中国大师

### 6. 王澍 Wang Shu
在地性、回收旧砖瓦砌筑、山水画意。
```
Wang Shu language: regional materiality, recycled grey brick and roof tile masonry with irregular bonding,
craft-based construction texture, mountain-and-water painting composition, sloping tiled roof as landscape,
timber and rammed earth, weathered patina, poetic ruin aesthetic, contemporary literati sensibility
```
负向：`pristine glossy facade, international style glass box, sleek metal panel`

### 7. 刘家琨 Liu Jiakun
低技策略，材料真实，粗粝中的诗性。
```
Liu Jiakun language: low-tech strategy, honest local materials, exposed recycled brick and concrete,
rough textured surfaces, pragmatic structure revealed, informal community space and rooftop walkway,
spontaneous and culturally embedded, unpolished yet poetic, humane scale
```
负向：`luxury finish, geometric sculpture, polished stone, neo-classical order`

### 8. 马岩松 Ma Yansong / MAD
山水城市，有机曲线，未来东方。
```
MAD Architects language: shan-shui city concept, organic curved silhouette mimicking mountains and clouds,
smooth white or metallic skin, continuous balcony contours, blurred boundary between building and nature,
poetic futuristic form, soft flowing massing, greenery integrated into facade
```
负向：`rigid grid facade, heavy classical base, dark brick, orthogonal block`

### 9. 何镜堂 He Jingtang
文化建筑，院落与轴线，现代岭南。
```
He Jingtang language: cultural institutional architecture, ceremonial axis and enclosed courtyard sequence,
monumental but composed massing, reinterpreted traditional roof silhouette, stone base and grille screen,
regional Lingnan response to climate, dignified public order, restrained modern Chinese expression
```
负向：`chaotic form, parametric blob, informal scattering, glass-only skin`

### 10. 张永和 Yung Ho Chang / 非常建筑
概念性，极简，结构理性，清冷的日常性。
```
Yung Ho Chang language: conceptual minimalism, structural rationalism, ordinary materials used with precision,
thin frames and flat planes, muted monochrome palette, austerity and clarity,
anti-spectacle modest architecture, quiet intellectual rigor, spatial prototype study
```
负向：`decorative, showy icon, rich material, curved gesture, colorful facade`

---

## 建筑外观组装要点

建筑与室内不同，**三个额外变量必须显式写入 prompt**：

1. **结构保留强度**（对应室内的「改动程度」）
   - 线稿输入 → `follow the line drawing exactly, preserve all massing and opening positions`
   - 现状照片 + 只换表皮 → `preserve overall massing and structure, replace only cladding material and facade language`
   - 概念推演 → 允许重构体量
2. **场地环境**：`urban street context / waterfront / mountain slope / suburban plot`
3. **画质定位**：`architectural visualization, professional CGI render, physically accurate daylight, 8k`
   避免出现 `photograph of existing building` 这类会拉低质感的措辞。

## 快速对照表

| 大师 | 一句话 | 形态 | 材质主调 |
|---|---|---|---|
| 贝聿铭 | 几何光影 | 纯粹几何体块 | 混凝土＋石材＋玻璃 |
| 让·努维尔 | 立面即媒介 | 透明层叠 | 玻璃＋金属滤网 |
| 诺曼·福斯特 | 高技精密 | 大跨轻构 | 钢＋玻璃 |
| 扎哈 | 参数化流体 | 无直角曲线 | 白色 GRC＋玻璃 |
| 安藤忠雄 | 光的精神性 | 几何＋切口 | 清水混凝土 |
| 王澍 | 在地砌筑 | 山水坡屋顶 | 旧砖瓦＋夯土 |
| 刘家琨 | 低技诗性 | 日常结构 | 回收砖＋素混凝土 |
| 马岩松 | 山水城市 | 有机流线 | 白／金属曲面 |
| 何镜堂 | 文化庄重 | 轴线院落 | 石材＋花格 |
| 张永和 | 结构理性 | 薄板极简 | 素色日常材料 |
