# 开发计划（Development Plan）

> 依据：`docs/prd.md` v1.7
> 覆盖范围：阶段 0（前置）→ 阶段 1（MVP）→ 阶段 1.5（多来源）→ 阶段 2（下载与提取）→ 阶段 3（视觉与高级分析）
> 任务编号规则：`<阶段>-T<两位序号>`；每个任务标注关联 PRD 条目、产出物、依赖与验收映射。

---

## 0. 概述

### 0.1 目标

按 PRD §16 分阶段交付一个可定位（阶段 1）、多来源（阶段 1.5）、可下载与确定性提取（阶段 2）、可视觉处理（阶段 3）的中国疾控健康监测报告 Codex Skill。

### 0.2 范围边界（依据 PRD §4 非目标）

本计划不包含：医学建议、第三方来源、绕过访问控制、独立长期数据库、自动预测、未授权下载/提取/视觉处理、自动跨期比较。

### 0.3 阶段总览

| 阶段 | 主题 | 默认动作 | 来源 | 主要交付 |
|---|---|---|---|---|
| 0 | 前置准备 | — | — | 仓库迁移、脚手架、用例冻结、样本基线 |
| 1 | MVP 定位 | `locate` | `influenza_weekly` | 唯一精确匹配 + 附件 URL + 参数化脚本 |
| 1.5 | 多来源定位 | `locate` | 全部 4 来源 | 类型消歧、周/月匹配、HTTP→浏览器回退 |
| 2 | 下载与提取 | `download`/`extract` | 全部 | 下载校验、HTML/PDF 提取、PDF 提取 Skill |
| 3 | 视觉与高级 | `vision` | 全部 | OCR/图表、摘要、批量、跨报告比较 |

### 0.4 处理级别与授权（FR-36）

```
vision ⊃ extract ⊃ download ⊃ locate
```

默认 `locate`。上级授权包含下级；未授权不得升级。

---

## 1. 阶段 0：前置准备

> 开工门禁：完成 P0 全部任务后才能进入阶段 1 编码。

### P0-T01 仓库迁移

- **关联**：PRD §1、§21
- **描述**：将仓库目录从 `find-china-flu-weekly-report` 迁移为 `find-china-cdc-health-report`；同步 remote、脚本、文档路径。
- **产出**：新目录名；更新后的 remote；无残留旧名引用。
- **验证**：`grep -ri "find-china-flu-weekly-report" .` 仅出现在迁移说明中。

### P0-T02 Skill 脚手架

- **关联**：PRD §15、§15.1、§21
- **描述**：创建目录结构骨架（空文件或占位）。
- **产出**：

```
find-china-cdc-health-report/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── browser-memory/
├── artifacts/
└── .gitignore
```

- **验证**：目录结构与 PRD §15 一致；`.gitignore` 忽略运行时 `artifacts/`。

### P0-T03 agents/openai.yaml

- **关联**：PRD §15.1
- **描述**：定义 `display_name`、`short_description`、`default_prompt`（按 PRD 原文）。
- **验证**：字段值与 PRD 一致；不设置未授权品牌资产。

### P0-T04 冻结测试用例真值

- **关联**：PRD §18、`references/test-cases.md` 开工门禁
- **描述**：当前 TC-004 至 TC-040 多数为 `pending_freeze`。逐条访问官网冻结 `verified_at`、`source_url`、期望字段、SHA-256（引用文件时）。
- **产出**：`references/test-cases.md` 全部 `frozen` 或 `dynamic`/`fixture`，无 `pending_freeze`；`fast_path=yes` 冻结用例 ≥ 20 条。
- **验证**：开工门禁清单全部勾选。

### P0-T05 样本基线入库

- **关联**：PRD §27
- **描述**：将 `P020260715815376876315.pdf`（SHA-256 `9a6f23...c79356`）字节检入 `references/samples/`，或存入版本化 Release 并在仓库保存不可变 URL + 哈希。
- **验证**：`sha256sum` 与 PRD §27 一致；不从用户 Downloads 取文件。

### P0-T06 环境就绪检查

- **关联**：PRD §20
- **描述**：确认 agent-browser、Chrome for Testing、对 chinacdc.cn 的网络访问；MVP 不依赖 Python/PDF 工具。
- **验证**：agent-browser 可启动命名会话并访问栏目首页。

---

## 2. 阶段 1：MVP（流感周报定位）

> 退出标准：AC-01 ~ AC-13 全部通过；TC-001 ~ TC-050 回归通过；MVP 仅 `locate`，不下载/不提取/不视觉/不创建 Artifact。

### 2.1 工作流（ Sprint 划分 ）

#### Sprint A：Skill 指令与来源注册

**MVP-T01 SKILL.md 核心指令**

- **关联**：PRD §15.1、§9（FR-01 ~ FR-12）、§21
- **描述**：编写 250–350 行（硬上限 500）的核心指令：数据源与导航边界、报告类型识别、输入标准化、agent-browser 工作流、分页/匹配/验证规则、输出协议、错误恢复、状态机加载规则、参数化脚本快速路径与回退、分级授权。
- **要点**：不复制完整 agent-browser 文档；按需加载 references。
- **验证**：行数 ≤ 500；skill-creator 快速校验通过。

**MVP-T02 references/source-registry.md**

- **关联**：FR-26
- **描述**：登记 `influenza_weekly` 来源：`id`、`name`、`index_url`、`period_type=week`、`content_mode=html_with_pdf`、`title_pattern`（流感标题正则）、`pagination_mode`、`transport_preference=http_first`、`supports_issue_number=true`、`allowed_url_patterns`、`adapter_version`。
- **产出**：流感标题正则范本 `^(?<year>\d{4})年第(?<week>\d{1,2})周第(?<issue>\d{1,4})期中国流感监测周报`。

**MVP-T03 references/source-schema.md**

- **关联**：FR-03、FR-04、FR-26、§15.2
- **描述**：栏目 URL、列表/详情页字段、分页模式、附件类型、标题示例与字段解释。

**MVP-T04 references/matching-rules.md**

- **关联**：§11、FR-06、FR-07
- **描述**：日期/周次/期号匹配优先级、跨年案例、歧义处理、相邻候选规则。

**MVP-T05 references/workflow.md**

- **关联**：PRD §10、§15.9
- **描述**：完整状态机（Mermaid）、阶段输入输出、失败恢复、清理策略。

**MVP-T06 references/browser-scripts.md**

- **关联**：FR-32、FR-33、FR-34、§15.13
- **描述**：参数定义（`report_type/year/week/issue_number/latest`）、语义步骤、稳定锚点、分页方式、成功断言、失败恢复输入；MVP 不定义复杂 Playbook 状态机。

**MVP-T07 references/report-schema.md / output-schema.md**

- **关联**：FR-30、§12、§15.4、§15.12
- **描述**：通用报告对象（含 `reporting_period`/`data_periods`）；最终输出字段（status 枚举见 §12.3）。

#### Sprint B：核心定位工作流

**MVP-T08 运行时指南加载（FR-01）**

- **描述**：首次执行 agent-browser 前调用 `skills get core`；加载失败时报告工具环境异常。

**MVP-T09 会话隔离（FR-02、FR-16）**

- **描述**：每次查询使用独立命名会话；不复用 `default`；不复用用户 Profile；不读/输出 Cookie 或令牌；任务结束关闭会话，清理失败仅记警告。

**MVP-T10 来源选择与栏目访问（FR-03）**

- **描述**：`http_first`：先 HTTP 请求栏目首页，2xx + 非空 + 内容类型合理 + 标题验证通过才算成功；否则回退 agent-browser。
- **要点**：MVP 必须验证浏览器回退路径存在。

**MVP-T11 列表记录提取（FR-04）**

- **描述**：对每条周报提取并标准化 12 个字段（`report_type` ... `source_page_url`）。
- **要点**：只处理符合标题正则的有效链接；相对→绝对 URL；清理重复空白；按 `detail_url ?? document_url` 生成 canonical URL 去重；解析失败保留原始标题并警告。

**MVP-T12 分页发现（FR-05）**

- **描述**：从首页识别"下一页/尾页/页码"；推导最大范围；防循环；找到唯一精确匹配立即停止；默认最多 8 个列表页（§14.2），超出返回 `search_budget_exceeded`。

**MVP-T13 按年份+周次匹配（FR-06）**

- **描述**：同时精确匹配 `period_year`、`period_week`、`report_type`；不用发布日期年份替代报告年份；多类型候选返回 `ambiguous`。

**MVP-T14 按期号匹配（FR-07）**

- **描述**：仅 `supports_issue_number=true` 来源生效；一结果成功、多结果 `ambiguous`、无结果 `not_found`（不返回近似）。

**MVP-T15 查询最新一期（FR-10）**

- **描述**：限定报告类型；有期号选最高；排序异常谓词检查；异常时打开冲突候选验证，仍无法唯一确定返回 `ambiguous`。

**MVP-T16 详情页/直接文档验证（FR-11）**

- **描述**：根据 `content_mode=html_with_pdf` 打开 HTML 并验证：URL 一致/官方重定向、标题语义一致、来源范围、无明显错误；验证失败记 `detail_unverified`。

**MVP-T17 文档和附件发现（FR-12）**

- **描述**：提取 PDF/Word/Excel 及语义附件链接；每条含 `name/url/type/language`；语言识别四级规则，无法确定用 `unknown`。

**MVP-T18 内容载体路由（FR-30）**

- **描述**：MVP 实现 `html_with_pdf`：`detail_url` + `document_url` 均必填；验证 HTML 后记录 PDF 附件。

#### Sprint C：参数化脚本与自愈

**MVP-T19 参数化脚本机制（FR-32、FR-35）**

- **描述**：维护 `browser-memory/influenza_weekly/{active.md, previous.md}`；脚本只含稳定操作知识（栏目入口、参数、标题模式、分页、附件特征、成功断言）。
- **禁止**：`@eN`、坐标、Cookie、认证头、Profile、完整推理、整页 HTML。

**MVP-T20 快速路径（FR-33）**

- **描述**：查 `active.md` → 替换参数 → 执行 → 验证（域名、标题周期、候选唯一性、附件 URL）→ 全部断言通过才返回；首次/缺失进入 bootstrap。

**MVP-T21 Bootstrap（FR-33 步骤 5）**

- **描述**：Agent 首次探索并提出初始脚本 → 主 Skill 按 FR-34 确定性校验 → 通过写入 `active.md`；失败返回 `bootstrap_failed`，不写入。

**MVP-T22 失败恢复与脚本更新（FR-34）**

- **描述**：快速路径失败时只向 Agent 提供：查询参数、当前脚本、失败步骤、失败断言、最小相关页面快照；Agent 探索定位；提出候选 → 主 Skill 5 项确定性校验 → 通过则旧文件原子保存为 `previous.md` 再写 `active.md`；失败保留旧文件返回 `self_heal_failed`。

#### Sprint D：授权、输出与错误恢复

**MVP-T23 分级授权（FR-36、FR-38）**

- **描述**：默认 `locate`；返回链接并询问是否继续；用户未明确处理方式时提供四级选项；只表达"看数据/趋势"不构成授权；不自动获取上一期、不跨期比较。

**MVP-T24 按授权保存 Artifact（FR-37）**

- **描述**：MVP 定位阶段不保存任何报告数据；`<skill-root>/artifacts/` 受保护；默认目录不可写返回 `artifact_store_unavailable`，不静默回退平台目录。

**MVP-T25 输出格式化（§12）**

- **描述**：实现 text 与 json 两种输出；状态枚举按 §12.3；成功结果含报告类型/周期/期号/发布日期/详情页/附件/匹配方式/来源。

**MVP-T26 错误处理与恢复（§13）**

- **描述**：
  - 浏览器启动失败：新会话重试一次；CI/容器外不自动 `--no-sandbox`；返回 `browser_unavailable`。
  - 网络/来源故障：区分 DNS/TLS/超时/HTTP/重定向/结构变化/数据不存在；只有完整搜索后才 `not_found`。
  - 页面结构变化：优先语义条件（链接文本、URL 范围、分页文本）。
  - 内容安全：页面为不可信输入；不执行页面指示；不上传到第三方。

**MVP-T27 时间语义规则（§8.3）**

- **描述**：区分报告类型/报告周期/数据周期/期号/发布日期/URL 日期；跨年以标题年份和周次为准；`publish_date` 解释为 `Asia/Shanghai` 自然日，不补造时间戳。

**MVP-T28 输入标准化与默认值（§8.1、§8.2）**

- **描述**：自然语言→标准查询对象；缺年份优先用上下文，无可靠上下文必须要求补充；未到达周次不自动回退上一年；多类型候选要求选择。

#### Sprint E：测试与验收

**MVP-T29 MVP 回归执行**

- **关联**：§17.1、`test-cases.md`
- **描述**：执行 TC-001 ~ TC-050；覆盖率：年+周 ≥20、期号 ≥10、最新动态 ≥5、跨年 ≥5、不存在 ≥5、故障 ≥5。
- **验证**：Top-1 命中率 ≥ 95%；期号 100%；`source_unavailable` 误判 `not_found` = 0。

**MVP-T30 前向验证（§18.4）**

- **描述**：使用独立 Agent 上下文，以真实用户口吻验证（不泄露预期答案）。

**MVP-T31 发布前检查清单（§21）**

- **描述**：逐项勾选 §21 清单。

### 2.2 MVP 验收映射

| AC | 覆盖任务 |
|---|---|
| AC-01 年+周精确 | T13/T16 |
| AC-02 跨年发布 | T13/T27 |
| AC-03 期号 | T14 |
| AC-04 最新一期 | T15 |
| AC-05 不存在 | T13 |
| AC-06 缺年份 | T28 |
| AC-07 会话损坏 | T09/T26 |
| AC-08 官网不可访问 | T26 |
| AC-09 详情页不存在 | T16 |
| AC-10 无附件 | T17 |
| AC-11 仅 locate | T23/T24 |
| AC-12 选择下载不提取 | T23 |
| AC-13 未授权处理 | T23 |

---

## 3. 阶段 1.5：多来源定位

> 退出标准：AC-14 ~ AC-25 通过；4 来源全部可定位；类型消歧生效。

### P15-T01 新增来源适配器

- **关联**：FR-26、§6.1
- **描述**：在 `source-registry.md` 登记 `respiratory_weekly`（周度 HTML）、`covid_monthly`（月度 HTML）、`global_infectious_risk_monthly`（栏目直链 PDF）。
- **要点**：各自 `title_pattern`、`content_mode`（`html`/`pdf`）、`pagination_mode`、`transport_preference`、`allowed_url_patterns`、`adapter_version`。

### P15-T02 月度报告匹配（FR-28）

- **描述**：按标题年份+月份精确匹配；发布日期可跨月，不用发布月替代报告月。

### P15-T03 报告周期与数据周期（FR-29）

- **描述**：结果分别保存 `reporting_period` 和 `data_periods[]`；月报含多周时不改名为周报。

### P15-T04 内容载体路由扩展（FR-30）

- **描述**：实现 `html`（`detail_url` 必填，`document_url=null`）和 `pdf`（`detail_url=null`，`document_url` 必填）模式。

### P15-T05 报告类型识别与消歧（FR-27）

- **描述**：识别 4 类型关键词；只给周次/月份但多候选时列出候选要求选择，不静默匹配。

### P15-T06 HTTP→浏览器回退（FR-03）

- **描述**：HTTP 非 2xx/超时/空/内容类型不匹配时切换 agent-browser（如全球风险评估 PDF）。

### P15-T07 每来源参数化脚本（FR-32 ~ FR-35）

- **描述**：4 来源各维护 `active.md`/`previous.md`；月度来源脚本增加 `month` 参数；快速路径失败只提供失败步骤+最小快照。

### P15-T08 阶段 1.5 回归与验收

- **关联**：§17.2
- **验证**：AC-14 ~ AC-25；尤其 AC-22/23/24/25 参数化脚本复用与自愈。

---

## 4. 阶段 2：下载与确定性提取

> 退出标准：AC-26 ~ AC-38 通过；`download`/`extract` 授权链路完整；PDF 提取 Skill 协作可用。

### Sprint F：下载与 Artifact

**P2-T01 按发布日期匹配（FR-08）**

- **描述**："发布于"用官网发布日期精确匹配；同日多候选返回所有并要求选择。

**P2-T02 按自然日期所在周/月匹配（FR-09）**

- **描述**：日期→候选周/月→官网标题二次验证；口径不一致返回前后相邻候选；不直接构造详情页 URL。

**P2-T03 下载报告（FR-13）**

- **描述**：明确授权后执行；HTTP 优先，失败切浏览器；命名 `{report_type}_{year}_W{week}_{issue}_{sha256_8}.{ext}`（月报用 `M{month}`）；ASCII 字符；下载后验证大小>0、类型合理；不覆盖同名；相同 SHA-256 复用；冲突追加序号。

**P2-T04 Artifact 存储（FR-37、§15.14）**

- **描述**：`artifacts/<report-id>/{source.pdf, extracted.json, evidence.json}`；report-id 确定性格式；只授权后才创建目录。

**P2-T05 HTML 内容提取（FR-14）**

- **描述**：agent-browser 读取主要内容、DOM 表格、图题、图片链接；先 DOM，无法获得才创建视觉任务。

### Sprint G：PDF 提取 Skill 与确定性提取

**P2-T06 cdc-report-pdf-extractor Skill 脚手架（FR-25）**

- **描述**：独立 Skill；主 Skill 只声明触发条件、授权边界、结果协议；不嵌入主 Skill。

**P2-T07 PDF 能力诊断（FR-17）**

- **描述**：获 `extract` 后执行；逐页检测文本层/字符数、图片/矢量线条、候选表格/图表、扫描/封面/封底、原生抽取质量；不默认整份送入模型或 OCR。

**P2-T08 原生文字提取（FR-18）**

- **描述**：存在文本层则用 `pdfinfo`/`pdftotext`/`pypdf`/`pdfplumber`；输出保留 `page/text/blocks/reading_order/bbox/extraction_method`。

**P2-T09 原生表格提取与校验（FR-19）**

- **描述**：字符+矢量边框表格程序化还原；保留原始字符串与解析值；数量/比例/单位拆分；行列合计与百分比校验；异常警告；不满足阈值才创建图片表格视觉任务。

**P2-T10 视觉缺口识别（FR-20）**

- **描述**：原生不足时生成 `unresolved` 记录（含 `id/type/page/image/bbox/reason/requires_vision/relevance_tags/estimated_cost/expected_output`）；不等于授权执行；向用户说明缺口与成本后询问 `vision`。

**P2-T11 证据结果协议（§24）**

- **描述**：轻量 evidence JSON；每条保留页码/位置/原始文本/数值/单位/方法/校验；图表估算含 `approximate=true`+置信度+误差。

**P2-T12 阶段 2 回归与验收**

- **关联**：§17.3
- **验证**：AC-26 ~ AC-38；尤其 AC-31/32/36/37 授权边界与 AC-33/34 原生优先。

---

## 5. 阶段 3：视觉与高级分析

> 退出标准：AC-39 ~ AC-49 通过；`vision` 链路完整；预算与重试受控。

### P3-T01 按需 Agent 视觉处理（FR-21）

- **描述**：五条件全满足才执行（已授权 vision、与问题相关、原生无法回答、非装饰、未超预算）；OCR 保持阅读顺序不补写；图片表格保行列；图表识别标题/类型/轴/图例/标注值；无标签曲线给近似值+置信度。

### P3-T02 视觉结果校验与合并（FR-22）

- **描述**：Agent 结果不覆盖原生；冲突字段并存标记来源；表格合计校验；图表估算标 `approximate=true`；记录 `method/confidence/warnings`；稳定 Schema 版本。

### P3-T03 有限重试（FR-23）与预算（FR-24、§26.2）

- **描述**：首试局部裁剪正常细节；重试提高分辨率/扩大裁剪并附失败原因；上限以 §26.2 为唯一规范（economy 0/0，balanced 3/2，complete 全部/2，complete>3 需确认）；超限返回部分结果+警告。

### P3-T04 摘要生成（FR-15）

- **描述**：总结请求视为 `extract` 授权但不含 `vision`；区分原文事实/归纳/缺失；不据标题虚构。

### P3-T05 批量与日期范围查询

- **关联**：§6.2 P2 意图
- **描述**：一次查多周/日期范围；按周次排序无重复；不受单条预算约束。

### P3-T06 结构化指标与口径保护（FR-31）

- **描述**：指标含 `metric_id/topic/pathogen/population/region/data_period/value/unit/denominator/methodology/source_report_type/source_location/extraction_method/confidence`；跨报告比较前检查口径，不一致解释或拒绝。

### P3-T07 跨报告指标比较（受控）

- **描述**：仅用户明确要求时进入独立后续流程；通过口径校验后才比较。

### P3-T08 阶段 3 回归与验收

- **关联**：§17.4
- **验证**：AC-39 ~ AC-49；尤其 AC-44/45/46/47/48/49 视觉、预算、口径。

---

## 6. 里程碑与依赖

```mermaid
flowchart LR
    P0[阶段 0 前置] --> P1[阶段 1 MVP]
    P1 --> P15[阶段 1.5 多来源]
    P15 --> P2[阶段 2 下载与提取]
    P2 --> P3[阶段 3 视觉与高级]
```

| 里程碑 | 前置依赖 | 关键交付 |
|---|---|---|
| M0 开工门禁 | — | 用例冻结 + 样本入库 + 环境就绪 |
| M1 MVP 发布 | M0 | AC-01~13 通过；仅 locate；流感单来源 |
| M2 多来源发布 | M1 | AC-14~25 通过；4 来源 |
| M3 下载与提取发布 | M2 | AC-26~38 通过；PDF 提取 Skill |
| M4 视觉与高级发布 | M3 | AC-39~49 通过；vision 链路 |

### 6.1 关键依赖链

- 自愈/快速路径（FR-32~35）是 MVP 核心风险点，必须在 Sprint C 充分验证。
- 阶段 2 PDF 提取依赖环境 PDF 工具（Poppler/pypdf/pdfplumber）；缺失时按需最小安装并告知用户。
- 阶段 3 视觉依赖支持图片输入的 Agent 运行环境。

---

## 7. 风险跟踪（摘自 PRD §19）

| 风险 | 阶段 | 缓解任务 |
|---|---|---|
| 官网结构变化 | 全期 | T11/T26 语义匹配；T22 自愈 |
| 跨年语义误判 | MVP+ | T27 时间语义；T13 标题年份为准 |
| 浏览器会话损坏 | MVP+ | T09 独立会话；T26 安全重试 |
| 网络故障误判 not_found | MVP+ | T26 故障分类 |
| 脚本保存脆弱选择器 | MVP+ | T19 禁止 `@eN`/坐标；T22 安全校验 |
| 临时异常污染脚本 | MVP+ | T22 `previous.md` 回退 |
| 页面诱导扩大来源范围 | MVP+ | T26 内容不可信；T22 URL 权限校验 |
| 整份 PDF 逐页视觉 | 阶段 2/3 | T07 程序化分流；T03 最小裁剪 |
| 视觉无限重试 | 阶段 3 | T03 §26.2 上限 |

---

## 8. 发布门禁汇总

### 8.1 每阶段通用

- [ ] 对应 AC 全部通过
- [ ] §21 适用项勾选
- [ ] 前向验证（独立上下文）通过
- [ ] 不含 Cookie/令牌/Profile

### 8.2 MVP 额外

- [ ] 仅 `influenza_weekly`；其余适配器不阻塞
- [ ] 仅 `locate`；无自动下载/提取/视觉
- [ ] `active.md` 不含 `@eN`/坐标/认证
- [ ] `source_unavailable` ≠ `not_found` 为 0
- [ ] 期号命中率 100%；Top-1 ≥ 95%
- [ ] `fast_path` 用例 ≥ 20，脚本成功率 ≥ 90%

### 8.3 阶段 2 额外

- [ ] `download` 不触发 PDF 提取
- [ ] 原生可用时不创建视觉任务
- [ ] 证据/输出带 `schema_version`

### 8.4 阶段 3 额外

- [ ] 视觉预算/重试仅以 §26.2 为准
- [ ] 图表估算标 `approximate=true`
- [ ] 跨报告比较需明确要求 + 口径校验

---

## 9. references 文档交付清单

| 文件 | 首次交付阶段 | 关联任务 |
|---|---|---|
| `source-registry.md` | 0/1 | P0-T02、MVP-T02、P15-T01 |
| `source-schema.md` | 1 | MVP-T03 |
| `matching-rules.md` | 1 | MVP-T04 |
| `workflow.md` | 1 | MVP-T05 |
| `browser-scripts.md` | 1 | MVP-T06 |
| `report-schema.md` | 1 | MVP-T07 |
| `output-schema.md` | 1 | MVP-T07 |
| `test-cases.md` | 0 | P0-T04 |
| `metric-schema.md` | 2/3 | P3-T06 |
| `pdf-extraction-rules.md` | 2 | P2-T06~T09 |
| `vision-task-rules.md` | 3 | P3-T01~T03 |
| `artifact-schema.md` | 2 | P2-T04 |
| `samples/` | 0 | P0-T05 |
