# QA Skills

赵子轩的测试与评审 Skills 作品集，收录 7 份 Skill：需求评审、需求分析、结构化测试设计、用例评审、测试报告、通用测试设计和简历风险审查。

这些 Skills 来自个人编写与 AI 辅助迭代实践。本仓聚焦工作规则、输入输出和人工确认边界，提供使用说明、格式定义及虚构示例。Butterfly 的 Agent 编排尚未完成，未作为本仓交付内容。

## Skills 一览

| Skill | 适用场景 | 主要输入 | 主要输出 |
| --- | --- | --- | --- |
| [requirement-review](skills/requirement-review/SKILL.md) | 需求准入评审 | 需求、设计与业务约束 | 歧义、遗漏、冲突与准入结论 JSON |
| [requirement-analysis](skills/requirement-analysis/SKILL.md) | 需求分析 | 当前需求及评审结论 | 流程、状态、规则和待确认项 JSON |
| [structured-testcase-design](skills/structured-testcase-design/SKILL.md) | 结构化测试点与用例设计 | 需求分析与原始资料 | 带需求关联的测试点、用例 JSON |
| [testcase-evaluation](skills/testcase-evaluation/SKILL.md) | 独立审查测试点和用例 | 需求分析、测试设计 | 覆盖与可执行性问题、评审结论 JSON |
| [test-report](skills/test-report/SKILL.md) | 汇总实际测试结果 | 已确认用例、人工执行记录与证据 | 结构化统计及 Markdown 报告 |
| [testcase-design](skills/testcase-design/SKILL.md) | 直接从需求设计人工测试用例 | 需求、设计图或 PRD | 用例表格，支持待确认项与需求来源 |
| [resume-fraud-review](skills/resume-fraud-review/SKILL.md) | 辅助审查测试岗位简历主张 | 简历、岗位与可核验材料 | 风险信号、合理解释及验证问题 |

两份测试设计 Skill 各有用途：通用版面向直接使用的测试表格；结构化版面向需求、测试点、用例之间的稳定关联。结构化版发布时改用独立名称，避免安装重名。

## 使用方式

可以让支持本地文件读取的 AI 助手读取指定 `SKILL.md`，再提供相应输入。例如：

```text
请按 skills/requirement-review/SKILL.md 评审 examples/address-change/requirement-draft.md。
逐条标出问题依据和行号，不补充资料未提供的业务规则。
```

```text
请按 skills/testcase-design/SKILL.md，为 examples/general-testcase-design/input.md
设计功能测试用例，使用 Markdown 表格；规则不明确时先列待确认项。
```

在 Codex 中，可将需要的单个 Skill 文件夹连同其 `references/` 复制到 `~/.codex/skills/` 后，在新会话中按名称调用，例如 `$requirement-review`。若已有同名目录，先比较版本，勿直接覆盖原有内容。Claude Code 可按其本地 Skills 机制使用这些文件夹。

结构化的 5 项 Skills 每项都附带完整输出 JSON Schema，以及实际需要的输入 Schema。安装单个目录即可保留格式说明；工具运行权限和人工确认仍由使用环境及当前用户指令决定。

## 示例与校验

- [收货地址示例](examples/address-change/README.md)：需求评审、需求分析、测试设计、评审与修订、人工执行记录和报告。
- [通用用例设计](examples/general-testcase-design/input.md)：需求与表格输出。
- [简历风险审查](examples/resume-review/input.md)：虚构简历片段与审查报告。

所有示例均为人工编写的演示材料，不包含真实候选人、公司内部需求或用户数据，也不是已运行模型的测评结果。

本地检查：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_portfolio.py
```

检查范围包括 7 个 Skill 的名称与前置信息、文档链接、JSON Schema、示例数据类型、关联 ID、版本和报告计数；这些检查不衡量真实模型的生成质量，也不承诺在所有模型上得到相同结果。

## 实践重点

- 将需求事实、推导、假设和待确认问题分开记录。
- 为需求、测试点、用例与执行证据建立可追溯关联。
- 用例生成与用例评审分工，修改产生新版本。
- 业务裁决和正式确认由人完成，测试报告依据实际执行记录。
- 简历风险属于待验证判断，结合证据和合理解释，由招聘人员作最终决定。

本次发布整理说明见 [发布记录](docs/release-notes.md)。
