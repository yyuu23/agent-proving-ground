# AgentProvingGround

> 工具调用型 Agent 运行、评测与安全执行平台

*Proving Ground*（试验场）指武器装备在受控场地中安全试射、检验性能、给出评分的场所 —— 本项目正是这样一个面向工具调用型 Agent 的受控试验场。

## 项目简介

基于 [AgentProvingGround](https://github.com/UKGovernmentBEIS/agent_proving_ground)（UK AI Security Institute 出品，MIT 许可）二次开发，对工具调用型 Agent 的**任务成功率、工具调用正确率、安全性、延迟与成本**进行可复现的批量评测。

核心理念：不做大而全的 Agent 平台，而是做一个**真正可以运行、可以评测、可以解释失败原因**的小型工程系统。

## 功能与路线图

### ✅ 已实现（第一阶段：评测基座）

- **自定义评测任务**：基于 Task 体系，支持内联样本与外部 JSON 数据集双模式，题库与代码分离
- **参数化任务过滤**：按类别（geography / science / common_sense 等）选择性运行样本
- **规则评分器**：确定性 includes 匹配评分，支持一题多正确答案
- **完整执行轨迹**：每次运行记录模型调用、工具调用、评分细节的 EvalLog（格式定义见 [`log_schema.json`](log_schema.json)）
- **并发批量评测**：支持并行运行多个样本并汇总统计

### 🚧 规划中

- **Tool Gateway**：工具白名单 → 参数 Schema 校验 → 权限检查 → 执行，拦截未授权调用
- **受限 Docker 沙盒**：`network=none`、非 root 用户、只读根分区、CPU/内存/进程/超时限制
- **五类任务套件**：单工具调用 / 多步工具调用 / 错误恢复 / 参数校验 / 安全执行（Prompt Injection 防御）
- **评测指标体系**：任务成功率、工具选择准确率、参数有效率、安全违规率、P50/P95 延迟、Token 用量与成本
- **LLM Judge**：确定性评分优先，语义判断引入模型评审并保留人工抽样校准

## 架构

```text
JSON / 内联 Task Suite
          │
          ▼
   Evaluation Runner（并发调度）
          │
          ▼
   Agent 执行 ──► Tool Gateway（规划）
                      │ 白名单 / Schema / 资源限制
                      ▼
                  受控工具 ──► Docker 沙盒（规划）
          │
          ▼
   Grader + Metrics（规则评分 ✅ / 指标汇总）
          │
          ▼
   EvalLog 轨迹 + 可视化报告（apg view）
```

## 快速开始

```bash
# 安装（Python 3.10+）
git clone https://github.com/yyuu23/agent-proving-ground.git
cd agent-proving-ground
pip install -e .

# 配置模型 API 密钥（按所用模型设置，例如）
export OPENAI_API_KEY=sk-...

# 运行评测任务
apg eval my_evals/basic_qa.py

# 按类别过滤运行
apg eval my_evals/basic_qa.py --task-args categories=geography

# 使用外部 JSON 题库版本
apg eval my_evals/basic_qa.py@qa_from_json

# 查看评测结果与执行轨迹
apg view
```

## 目录说明

```text
my_evals/            自定义评测任务
  basic_qa.py        知识问答评测（内联样本 + JSON 数据集两种定义方式）
  qa_dataset.json    外部题库（代码与数据分离示例）
log_schema.json      评测日志（执行轨迹）完整 JSON Schema
src/agent_proving_ground/      评测框架源码
```

## 致谢与许可

本项目的评测内核基于 UK AI Security Institute 以 MIT 许可开源的 LLM 评测框架二次开发，感谢其开源贡献。

- 遵循 [MIT 许可证](LICENSE)，并保留其版权声明
