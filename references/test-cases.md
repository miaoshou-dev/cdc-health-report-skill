# MVP 报告定位回归用例

## 使用规则

- 本文件是 `PRD.md` §3.2、§15.7 和 §18 的可测回归集。
- 状态为 `frozen` 的用例必须包含 `verified_at`、`source_url` 和确定的期望字段。
- 状态为 `pending_freeze` 的用例不得计入发布指标；实现开工前必须补齐真值或删除并替换。
- `regression=yes` 的用例共同组成定位与匹配回归集。
- “最新一期”属于动态用例，每次执行在任务内校验栏目候选和 `verified_at`，不持久化浏览器状态。
- 官网不可用、浏览器不可用与业务无结果必须使用不同测试夹具。

## 用例清单

| ID | 分类 | 查询或场景 | 核心期望 | regression | 状态 |
|---|---|---|---|---|---|
| TC-001 | 周次 | 找 2026 年第 20 周流感报告 | 第 909 期；精确 URL | yes | frozen |
| TC-002 | 周次/跨年 | 找 2024 年第 52 周流感报告 | 不误选发布日期年份 | yes | frozen |
| TC-003 | 期号 | 找流感第 917 期 | 2026 年第 28 周；精确 URL | yes | frozen |
| TC-004 | 周次 | 找 2026 年第 19 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-005 | 周次 | 找 2026 年第 18 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-006 | 周次 | 找 2026 年第 17 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-007 | 周次 | 找 2026 年第 16 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-008 | 周次 | 找 2026 年第 15 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-009 | 周次 | 找 2026 年第 14 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-010 | 周次 | 找 2026 年第 13 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-011 | 周次 | 找 2026 年第 12 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-012 | 周次 | 找 2026 年第 11 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-013 | 周次 | 找 2026 年第 10 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-014 | 周次 | 找 2026 年第 9 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-015 | 周次 | 找 2026 年第 8 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-016 | 周次 | 找 2026 年第 7 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-017 | 周次 | 找 2026 年第 6 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-018 | 周次 | 找 2026 年第 5 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-019 | 周次 | 找 2026 年第 4 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-020 | 周次 | 找 2026 年第 3 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-021 | 周次 | 找 2026 年第 2 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-022 | 周次 | 找 2026 年第 1 周流感报告 | 唯一精确结果 | yes | frozen |
| TC-023 | 期号 | 找流感第 916 期 | 唯一精确结果 | yes | frozen |
| TC-024 | 期号 | 找流感第 915 期 | 唯一精确结果 | yes | frozen |
| TC-025 | 期号 | 找流感第 914 期 | 唯一精确结果 | yes | frozen |
| TC-026 | 期号 | 找流感第 913 期 | 唯一精确结果 | yes | frozen |
| TC-027 | 期号 | 找流感第 912 期 | 唯一精确结果 | yes | frozen |
| TC-028 | 期号 | 找流感第 911 期 | 唯一精确结果 | yes | frozen |
| TC-029 | 期号 | 找流感第 910 期 | 唯一精确结果 | yes | frozen |
| TC-030 | 期号 | 找流感第 909 期 | 与 TC-001 同一报告 | yes | frozen |
| TC-031 | 最新 | 找最新一期流感周报 | 最高期号并保存动态快照 | no | dynamic |
| TC-032 | 最新 | 给我最新的中国流感监测周报 | 与 TC-031 结果一致 | no | dynamic |
| TC-033 | 最新 | 当前最新一期是第几期 | 返回期号、周次和来源 | no | dynamic |
| TC-034 | 最新 | 最新流感周报 PDF | 返回已验证附件 URL，不自动下载 | no | dynamic |
| TC-035 | 最新 | 最新一期，只给链接 | `locate`，不创建 Artifact | no | dynamic |
| TC-036 | 跨年 | 找 2025 年第 1 周流感报告 | 以标题年份和周次匹配 | yes | frozen |
| TC-037 | 跨年 | 找 2025 年第 52 周流感报告 | 不按 URL 年份误判 | yes | frozen |
| TC-038 | 跨年 | 找 2023 年第 52 周流感报告 | 旧栏目快照中唯一精确结果 | yes | fixture |
| TC-039 | 跨年 | 按自然日期查询跨年周 | 转换后用标题验证 | no | fixture |
| TC-040 | 跨年 | 发布于次年 1 月的上一年第 52 周 | 报告年份来自标题 | yes | frozen |
| TC-041 | 不存在 | 找 2030 年第 10 周流感报告 | `not_found` | no | frozen |
| TC-042 | 不存在 | 找流感第 99999 期 | `not_found` | no | fixture |
| TC-043 | 不存在 | 找 2026 年第 54 周流感报告 | `invalid_query` | no | fixture |
| TC-044 | 不存在 | 找第 0 周流感报告 | `invalid_query` | no | fixture |
| TC-045 | 歧义 | 找第 20 周报告但无年份 | 要求补充年份 | no | frozen |
| TC-046 | 故障 | 官网不可访问 | `source_unavailable`，不返回 `not_found` | no | fixture |
| TC-047 | 故障 | Chrome 启动失败 | 重试一次后 `browser_unavailable` | no | fixture |
| TC-048 | 故障 | 列表命中但详情页不存在 | `detail_unverified` | no | fixture |
| TC-049 | 无状态浏览 | 首次运行且无任何浏览器状态 | 直接从 adapter 入口完成定位，不写执行轨迹 | no | fixture |
| TC-050 | 边界安全 | 页面结构变化并出现站外候选 | 拒绝扩大 adapter URL 边界并返回验证失败 | no | fixture |

## 已冻结真值

### TC-001

```text
verified_at: 2026-07-22
source_url: https://www.chinacdc.cn/jksj/jksj04_14249/202605/t20260520_1835963.html
period_year: 2026
period_week: 20
issue_number: 909
```

### TC-002

```text
verified_at: 2026-07-22
source_url: https://www.chinacdc.cn/jksj/jksj04_14249/202501/t20250102_303653.html
period_year: 2024
period_week: 52
```

### TC-003

```text
verified_at: 2026-07-22
source_url: https://www.chinacdc.cn/jksj/jksj04_14249/202607/t20260715_1838199.html
period_year: 2026
period_week: 28
issue_number: 917
sample_pdf_sha256: 9a6f23cef5ae56ff570feec73cd3b1eaedf14927a6943a2eb232d6924dc79356
```

### TC-004 至 TC-022（2026 年周次矩阵）

`verified_at: 2026-07-22`。以下均为 `period_year=2026`；表中 URL 是官网列表实际链接。

| TC | 周 | 期号 | source_url |
|---|---:|---:|---|
| TC-004 | 19 | 908 | https://www.chinacdc.cn/jksj/jksj04_14249/202605/t20260514_1835783.html |
| TC-005 | 18 | 907 | https://www.chinacdc.cn/jksj/jksj04_14249/202605/t20260508_1835622.html |
| TC-006 | 17 | 906 | https://www.chinacdc.cn/jksj/jksj04_14249/202604/t20260430_1835474.html |
| TC-007 | 16 | 905 | https://www.chinacdc.cn/jksj/jksj04_14249/202604/t20260423_1835288.html |
| TC-008 | 15 | 904 | https://www.chinacdc.cn/jksj/jksj04_14249/202604/t20260416_1835095.html |
| TC-009 | 14 | 903 | https://www.chinacdc.cn/jksj/jksj04_14249/202604/t20260410_1834910.html |
| TC-010 | 13 | 902 | https://www.chinacdc.cn/jksj/jksj04_14249/202604/t20260403_316138.html |
| TC-011 | 12 | 901 | https://www.chinacdc.cn/jksj/jksj04_14249/202603/t20260326_315961.html |
| TC-012 | 11 | 900 | https://www.chinacdc.cn/jksj/jksj04_14249/202603/t20260319_315645.html |
| TC-013 | 10 | 899 | https://www.chinacdc.cn/jksj/jksj04_14249/202603/t20260312_315422.html |
| TC-014 | 9 | 898 | https://www.chinacdc.cn/jksj/jksj04_14249/202603/t20260305_315294.html |
| TC-015 | 8 | 897 | https://www.chinacdc.cn/jksj/jksj04_14249/202602/t20260226_315208.html |
| TC-016 | 7 | 896 | https://www.chinacdc.cn/jksj/jksj04_14249/202602/t20260223_315154.html |
| TC-017 | 6 | 895 | https://www.chinacdc.cn/jksj/jksj04_14249/202602/t20260211_315041.html |
| TC-018 | 5 | 894 | https://www.chinacdc.cn/jksj/jksj04_14249/202602/t20260204_314937.html |
| TC-019 | 4 | 893 | https://www.chinacdc.cn/jksj/jksj04_14249/202601/t20260128_314825.html |
| TC-020 | 3 | 892 | https://www.chinacdc.cn/jksj/jksj04_14249/202601/t20260121_314754.html |
| TC-021 | 2 | 891 | https://www.chinacdc.cn/jksj/jksj04_14249/202601/t20260114_314616.html |
| TC-022 | 1 | 890 | https://www.chinacdc.cn/jksj/jksj04_14249/202601/t20260108_314536.html |

### TC-023 至 TC-030（期号矩阵）

`verified_at: 2026-07-22`。

| TC | 期号 | 年/周 | source_url |
|---|---:|---|---|
| TC-023 | 916 | 2026/27 | https://www.chinacdc.cn/jksj/jksj04_14249/202607/t20260709_1838009.html |
| TC-024 | 915 | 2026/26 | https://www.chinacdc.cn/jksj/jksj04_14249/202607/t20260702_1837752.html |
| TC-025 | 914 | 2026/25 | https://www.chinacdc.cn/jksj/jksj04_14249/202606/t20260625_1837459.html |
| TC-026 | 913 | 2026/24 | https://www.chinacdc.cn/jksj/jksj04_14249/202606/t20260617_1836880.html |
| TC-027 | 912 | 2026/23 | https://www.chinacdc.cn/jksj/jksj04_14249/202606/t20260611_1836732.html |
| TC-028 | 911 | 2026/22 | https://www.chinacdc.cn/jksj/jksj04_14249/202606/t20260603_1836483.html |
| TC-029 | 910 | 2026/21 | https://www.chinacdc.cn/jksj/jksj04_14249/202605/t20260528_1836120.html |
| TC-030 | 909 | 2026/20 | https://www.chinacdc.cn/jksj/jksj04_14249/202605/t20260520_1835963.html |

### TC-036、TC-037、TC-040（跨年真值）

```text
verified_at: 2026-07-22
TC-036 source_url: https://www.chinacdc.cn/jksj/jksj04_14249/202501/t20250109_303781.html
TC-036 period_year/week/issue: 2025/1/838
TC-037 source_url: https://www.chinacdc.cn/jksj/jksj04_14249/202512/t20251231_314388.html
TC-037 period_year/week/issue: 2025/52/889
TC-040 source_url: https://www.chinacdc.cn/jksj/jksj04_14249/202501/t20250102_303653.html
TC-040 period_year/week/issue: 2024/52/837
```

### 动态与夹具规则

- TC-031 至 TC-035 每次保存 `verified_at`、栏目 URL、第一页有效候选及所选最高期号；不得提交运行时 Artifact。
- TC-038 使用版本化旧栏目快照，避免当前栏目不再覆盖 2023 年时误测网络。
- TC-039 固定 ISO 跨年输入与前后官方候选。
- TC-042 使用完整分页的版本化目录夹具；TC-043/044 在网络调用前失败。
- TC-046 至 TC-050 使用隔离临时目录且不持久化浏览器状态。

## 开工门禁

- [x] TC-001 至 TC-050 均不存在 `pending_freeze`
- [x] 至少 20 条 `regression=yes` 用例具有冻结真值
- [x] 动态最新一期用例定义任务内校验字段
- [x] 故障夹具使用隔离临时 Artifact 根目录
- [x] 无状态浏览和边界安全用例覆盖 `allowed_url_patterns`
