# MVP 报告定位回归用例

## 使用规则

- 本文件是 `PRD.md` §3.2、§15.7 和 §18 的可测回归集。
- 状态为 `frozen` 的用例必须包含 `verified_at`、`source_url` 和确定的期望字段。
- 状态为 `pending_freeze` 的用例不得计入发布指标；实现开工前必须补齐真值或删除并替换。
- `fast_path=yes` 的用例共同组成不少于 20 条的参数化脚本快速路径回归集。
- “最新一期”属于动态用例，每次执行保存栏目快照、候选列表和 `verified_at`。
- 官网不可用、浏览器不可用与业务无结果必须使用不同测试夹具。

## 用例清单

| ID | 分类 | 查询或场景 | 核心期望 | fast_path | 状态 |
|---|---|---|---|---|---|
| TC-001 | 周次 | 找 2026 年第 20 周流感报告 | 第 909 期；精确 URL | yes | frozen |
| TC-002 | 周次/跨年 | 找 2024 年第 52 周流感报告 | 不误选发布日期年份 | yes | frozen |
| TC-003 | 期号 | 找流感第 917 期 | 2026 年第 28 周；精确 URL | yes | frozen |
| TC-004 | 周次 | 找 2026 年第 19 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-005 | 周次 | 找 2026 年第 18 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-006 | 周次 | 找 2026 年第 17 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-007 | 周次 | 找 2026 年第 16 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-008 | 周次 | 找 2026 年第 15 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-009 | 周次 | 找 2026 年第 14 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-010 | 周次 | 找 2026 年第 13 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-011 | 周次 | 找 2026 年第 12 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-012 | 周次 | 找 2026 年第 11 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-013 | 周次 | 找 2026 年第 10 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-014 | 周次 | 找 2026 年第 9 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-015 | 周次 | 找 2026 年第 8 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-016 | 周次 | 找 2026 年第 7 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-017 | 周次 | 找 2026 年第 6 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-018 | 周次 | 找 2026 年第 5 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-019 | 周次 | 找 2026 年第 4 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-020 | 周次 | 找 2026 年第 3 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-021 | 周次 | 找 2026 年第 2 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-022 | 周次 | 找 2026 年第 1 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-023 | 期号 | 找流感第 916 期 | 唯一精确结果 | yes | pending_freeze |
| TC-024 | 期号 | 找流感第 915 期 | 唯一精确结果 | yes | pending_freeze |
| TC-025 | 期号 | 找流感第 914 期 | 唯一精确结果 | yes | pending_freeze |
| TC-026 | 期号 | 找流感第 913 期 | 唯一精确结果 | yes | pending_freeze |
| TC-027 | 期号 | 找流感第 912 期 | 唯一精确结果 | yes | pending_freeze |
| TC-028 | 期号 | 找流感第 911 期 | 唯一精确结果 | yes | pending_freeze |
| TC-029 | 期号 | 找流感第 910 期 | 唯一精确结果 | yes | pending_freeze |
| TC-030 | 期号 | 找流感第 909 期 | 与 TC-001 同一报告 | yes | pending_freeze |
| TC-031 | 最新 | 找最新一期流感周报 | 最高期号并保存动态快照 | no | dynamic |
| TC-032 | 最新 | 给我最新的中国流感监测周报 | 与 TC-031 结果一致 | no | dynamic |
| TC-033 | 最新 | 当前最新一期是第几期 | 返回期号、周次和来源 | no | dynamic |
| TC-034 | 最新 | 最新流感周报 PDF | 返回已验证附件 URL，不自动下载 | no | dynamic |
| TC-035 | 最新 | 最新一期，只给链接 | `locate`，不创建 Artifact | no | dynamic |
| TC-036 | 跨年 | 找 2025 年第 1 周流感报告 | 以标题年份和周次匹配 | yes | pending_freeze |
| TC-037 | 跨年 | 找 2025 年第 52 周流感报告 | 不按 URL 年份误判 | yes | pending_freeze |
| TC-038 | 跨年 | 找 2023 年第 52 周流感报告 | 唯一精确结果 | yes | pending_freeze |
| TC-039 | 跨年 | 按自然日期查询跨年周 | 转换后用标题验证 | no | pending_freeze |
| TC-040 | 跨年 | 发布于次年 1 月的上一年第 52 周 | 报告年份来自标题 | yes | pending_freeze |
| TC-041 | 不存在 | 找 2030 年第 10 周流感报告 | `not_found` | no | frozen |
| TC-042 | 不存在 | 找流感第 99999 期 | `not_found` | no | pending_freeze |
| TC-043 | 不存在 | 找 2026 年第 54 周流感报告 | `invalid_query` | no | pending_freeze |
| TC-044 | 不存在 | 找第 0 周流感报告 | `invalid_query` | no | pending_freeze |
| TC-045 | 歧义 | 找第 20 周报告但无年份 | 要求补充年份 | no | frozen |
| TC-046 | 故障 | 官网不可访问 | `source_unavailable`，不返回 `not_found` | no | fixture |
| TC-047 | 故障 | Chrome 启动失败 | 重试一次后 `browser_unavailable` | no | fixture |
| TC-048 | 故障 | 列表命中但详情页不存在 | `detail_unverified` | no | fixture |
| TC-049 | bootstrap | 首次运行且无 active.md | Agent 提议脚本；主 Skill 校验后写入 | no | fixture |
| TC-050 | 自愈安全 | 候选脚本扩大 URL 范围 | 保留旧脚本并返回 `self_heal_failed` | no | fixture |

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

## 开工门禁

- [ ] TC-001 至 TC-050 均不存在 `pending_freeze`
- [ ] 至少 20 条 `fast_path=yes` 用例具有冻结真值
- [ ] 动态最新一期用例能保存执行时快照
- [ ] 故障夹具不会访问或修改真实用户 Artifact
- [ ] bootstrap 和自愈安全用例覆盖 `allowed_url_patterns`
