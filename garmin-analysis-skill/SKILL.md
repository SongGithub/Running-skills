---
name: garmin-analysis
description: |-
  基于 Garmin 1Hz 训练数据的 AI 运动分析模块。支持七种训练类型的结构化复盘
  (长距离/节奏跑/间歇/爬坡/越野/比赛/有氧)，提供 Pa:HR decoupling、力学衰减检测、
  rep 一致性分析等深度指标。中英双语。
license: MIT
metadata:
  version: 1.0.0
  category: health
  based_on:
    name: tracing-run
    author: yuchong-li
    repo: https://github.com/yuchong-li/tracing-run
---

# Garmin Analysis Skill

> 基于 Garmin 1Hz 时序数据的结构化训练分析模块

## 概述

本模块从 Garmin Connect 获取活动的完整 1Hz 时间序列数据（心率、配速、步频、触地时间 GCT、垂直振幅 VR、步距、功率、GPS 等），按训练类型分流至对应的分析管道，生成结构化复盘报告并支持深度追问钻取。

### 数据来源

- **Garmin Connect** — 通过 Garmin API 或 CSV 导入获取活动数据
- **1Hz 时间序列** — 心率、配速、步频、GCT、VR、步距、功率、海拔
- **Laps** — 自动/手动分段数据及用户备注
- **天气** — 温度、湿度（可选）

### 训练类型分类

| 类型 | 标识 | 核心关注 |
|------|------|---------|
| 长距离 | `long_run` | 有氧底子稳定性、Pa:HR decoupling |
| 节奏跑/阈值跑 | `tempo` | 主集平滑度(smoothness)、cardiac drift |
| 间歇训练 | `intervals` | per-rep 一致性、HRR 恢复、起跑 crispness |
| 爬坡训练 | `hill` | GAP × grade、末段步频 step-down |
| 越野跑 | `trail` | 地形适配、quad-braking 检测 |
| 比赛 | `race` | distance-aware 分析、pacing 策略 |
| 有氧基础/恢复 | `aerobic` | HR 守界、有氧效率 |
| 通用 | `generic` | 基础数据分析 |

---

## 核心分析指标

### 1. Pa:HR Decoupling（心率-配速脱节率）

全程/分段的心率与配速脱节程度，衡量有氧效率的核心指标：

```
Pa:HR = (EF_后半 - EF_前半) / EF_前半 × 100%

EF (Efficiency Factor) = 距离 / 平均心率

阈值: <5% 良好 | 5-8% 边界 | >8% 超出
```

漂移斜率 + R²：
- R² 高(>0.5) = 线性心脏漂移主导 → 可作 cardiac drift 解读
- R² 低(<0.3) = HR 波动受配速切换驱动 → 不是真 drift

### 2. 力学衰减检测 (Form Breakdown)

监测四件套同时变差——伤病前兆信号：

| 信号模式 | 解读 |
|---------|------|
| 步频↓ + 步距↑ + GCT↑ + VR↑ | **坏形变红旗** — 疲劳导致力学崩溃 |
| 步频↓ + 步距↑ + 配速维持 | **拉长步距硬撑** — 预失败信号 |
| GCT 单边上升 >10ms | 可能是着地方式改变 |
| Hill 特有: 末段步频 step-down >3spm | **弹性流失** — 改为硬蹬地 |

### 3. 心脏漂移 (Cardiac Drift)

同配速下心率随时间上升的斜率：

```
HR-time drift slope (bpm/min) — 漂移速度
R² — 漂移线性度
```

### 4. Rep 分析 (间歇/爬坡)

- **Per-rep 一致性**: rep N vs rep 1 的配速/HR delta
- **起跑 crispness**: 进入稳态 ±5% 所需时间 (>20s = 起跑差)
- **HRR 60s drop**: 间歇期心率恢复幅度（前 30s 占比 = 副交感激活速度）
- **Cross-rep 衰减**: 末 rep 比首 rep 慢 ≥5s/km 或 HR 高 ≥5bpm

### 5. Grade-Adjusted Pace (GAP)

爬坡/越野场景下，把 raw pace 按坡度校正为平地等效配速：

```
GAP = raw_pace × correction_factor(grade)
```

**规则**: 永远不在无 grade 上下文时孤立解读 raw pace。

---

## 结构对比元规则

三种合法对比框架，分析时必须先选定、不混用：

| 框架 | 自变量 | 控制变量 | 能回答的问题 |
|------|--------|---------|------------|
| 疲劳坏形变筛查 | 时间(前段/后段) | 配速尽量相同 | 累计疲劳是否导致力学崩溃 |
| 同强度块内疲劳 | 同一推段的前半 vs 后半 | 配速近似相同 | 同强度下力学是否走样 |
| 末段端对端粗筛 | 首 km vs 末 km / 首 lap vs 末 lap | 不控制配速 | 二元: 末段是否出现坏形变红旗 |

---

## 输出规范

### 语言

- **跑步永远用配速不用 m/s**: 3.70 m/s → 4:30/km
- **数字精度**: 配速精确到秒(4:35/km)、HR/步频/功率取整数、步距精确到 cm(1.18m)、GCT 取整 ms
- **禁止 meta-talk**: 不出现"污染/不能对比/框架/无效/无法归因"等词汇——直接给结论
- **每个数字配 1 句语境解读**: contextualized, 不是通用 glossary

### 格式

初始报告结构：

```
🎯 这次训练的本质 — 1句话定性
📊 数据故事 — markdown 表格（3列：指标 | 数据 | 教练解读）
🔍 根因/关键 enabler — 解释 why（按需）
💡 下次具体执行 — blockquote 高亮，含具体 bpm/配速/时长
🔬 关键指标卡 — 每个指标 title 行 + 1-3 句解读
```

### 钻取工具（追问时使用）

- `get_window_stats(start, end, key_type)` — 任意窗口聚合（HR/配速/力学均值+百分位+漂移斜率）
- `get_raw_window_by_time(start_sec, end_sec)` — 1Hz 原始时序
- `get_raw_window_by_distance(start_m, end_m)` — 同上但按距离

---

## 提示词模板

本模块附带 7 种训练类型的分析提示词模板，位于 `prompts/{en,zh-cn}/` 目录：

```
prompts/
├── en/
│   ├── review_report_long_run.md
│   ├── review_report_tempo.md
│   ├── review_report_intervals.md
│   ├── review_report_hill.md
│   ├── review_report_trail.md
│   ├── review_report_race.md
│   ├── review_report_aerobic_base.md
│   ├── review_report_aerobic_recovery.md
│   └── coach_system.md
└── zh-cn/
    └── (同上, 中文版)
```

---

## 鸣谢

本模块的分析方法论和提示词架构源自 **tracing-run** 项目：

- **项目**: [tracing-run](https://github.com/yuchong-li/tracing-run)
- **作者**: [yuchong-li](https://github.com/yuchong-li)
- **描述**: AI-native, mobile-first training analysis tool for serious runners.

## 许可

MIT License
