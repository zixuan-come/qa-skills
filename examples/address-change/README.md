# 收货地址示例

本目录是人工编写的虚构示例，不是真实产品需求、真实模型生成结果或真实性能/功能测试证据。

1. requirement-review：输入 requirement-draft.md，参考输出 review.json。问题定位按文件物理行号计算，空行也计数。
2. requirement-analysis：输入补齐规则后的 requirement-confirmed.md 与 review-confirmed.json。后者演示人工确认问题已解决后给出的第二版评审结论；旧 review.json 只作为历史追溯。参考输出 analysis.json。
3. structured-testcase-design：输入 analysis.json 和已确认需求，参考 design-v1.json。
4. testcase-evaluation：输入 analysis.json 与 design-v1.json，参考 evaluation.json。design-v2-partial.json 展示部分修订，不表示所有问题已经解决。
5. test-report：单独使用 design-approved-demo.json、execution-demo.json 与 evidence/；参考 report-demo.json 和 report-demo.md。

报告部分模拟的是“人明确批准4条限定范围用例并接受未覆盖风险”的输入场景。它不表示前面部分修订已经自动通过评审；如需正式执行完整地址模块，应补齐风险场景并重新评审。元数据里的 approved 是虚构的演示输入，不是 AI 自动批准。

每项 Skill 可独立运行，不会自动调用其他 Skill 或跳过人工确认。要求 AI 生成输出时，请指定相应输出 Schema；示例文件仅用于理解格式。
