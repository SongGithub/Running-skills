# Garmin Analysis Skill 🏃📊

结构化 Garmin 训练数据分析模块。7 种训练类型的 AI 复盘。

[English](#) | [中文](#)

## 概述

基于 Garmin 1Hz 时间序列数据的训练分析。按训练类型分流，生成结构化复盘报告。

### 支持的训练类型

| Type | Focus |
|------|-------|
| **Long Run** | Aerobic stability, Pa:HR decoupling |
| **Tempo / Threshold** | Smoothness, cardiac drift |
| **Intervals** | Per-rep consistency, HR recovery |
| **Hill Repeats** | GAP × grade, cadence step-down |
| **Trail** | Terrain adaptation |
| **Race** | Distance-aware analysis |
| **Aerobic Base** | HR ceiling discipline |

## 核心指标

- **Pa:HR Decoupling** — 心率-配速脱节率
- **Form Breakdown** — 力学衰减四件套
- **Cardiac Drift** — HR-time 漂移斜率
- **GAP** — 坡度校正配速

## 鸣谢

本模块的方法论提炼自 [tracing-run](https://github.com/yuchong-li/tracing-run) (作者 [yuchong-li](https://github.com/yuchong-li))。
