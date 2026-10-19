# 首次发布整理说明

日期：2026-10-19。

本次按 7 份 Skill 整理作品：Butterfly 的 5 份测试流程定义、独立通用版 testcase-design，以及 resume-fraud-review。保留原有核心职责和业务规则，发布副本中做以下调整：

- 将 Butterfly 的 testcase-design 命名为 structured-testcase-design，保持两个测试设计版本可同时安装。
- 根据原结构化模型导出必要的 JSON Schema，每个结构化 Skill 目录包含自身所需的格式定义。
- 补充独立调用、格式选择和输入位置说明，不依赖未完成的 Agent 编排。
- 修正 requirement-review 原示例中“存在高等级未解决问题却标记 pass”的自相矛盾，改为 fail。
- 将通用版中的特定业务代币名称替换为通用积分示例。
- 新增人工编写的收货地址、通用用例设计和虚构简历示例，以及静态校验脚本。

原始文件保持不变。本仓未包含原项目的运行时产物、真实需求、凭证、候选人资料、未完成的 Agent 实现或其验收声明。当前发布未附许可证。
