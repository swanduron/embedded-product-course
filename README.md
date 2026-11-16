# 《现代嵌入式产品工程》

**当前状态**：课程架构保持 14 章、4 阶段；第 1.1、1.2 节均为连贯教材正文草稿，**待学习者审阅**；HTML 阅读器预览 `v0.3.0-preview`，两节均从 Markdown 生成。应用工程、硬件与产品验收尚未完成。

唯一工作仓库：`~/Documents/project/embedded-product-course`。远端：[swanduron/embedded-product-course](https://github.com/swanduron/embedded-product-course)，只保留并使用 `main`。教材叙事规范为 v1.3，Agent 运行规程已更新为 v1.3；这些修订号与 HTML 预览版本分别管理。

## 快速阅读

- 双击 [index.html](index.html) 打开离线 HTML 阅读预览，通过导航切换 1.1、1.2。
- 第 1.1 节权威正文：[chapters/ch01-lesson01.md](chapters/ch01-lesson01.md)。
- 第 1.2 节权威草稿：[chapters/ch01-lesson02.md](chapters/ch01-lesson02.md)，已重写并并入 HTML；包含 REQ-001～REQ-008 的需求推导、正常/边界测试计划和独立迁移练习。
- 第 1.2 节[编辑说明](docs/reviews/ch01-lesson02.md)与[阅读器验证记录](docs/validation/reader-v0.3.0-preview.md)。
- 原理图、固件工程与硬件测试尚未完成。

## 开发、构建和同步

```bash
cd ~/Documents/project/embedded-product-course
python3 -m pip install -r requirements-build.txt
python3 scripts/build_site.py
git diff --check
git diff
```

目前构建脚本自动把 **第 1.1、1.2 节** 写入 HTML 阅读预览，并保留原先可交互的 OLED 演示。**不要手工编辑 `index.html` 中的教材正文**；修改 Markdown 后重新构建。

**Git 工作约定**：本仓库只保留并使用 `main`，日常直接在 `main` 修改与验证；未经明确要求，不自动创建功能分支、工作树或 PR。未经仓库所有者同意，不推送内容到 GitHub。

同步、提交和发布步骤见 [Git 协作与 HTML 发布工作流](docs/git-and-publishing.md)。Git 保存正文与历史，rsync 可选用于部署 HTML；向 GitHub 推送仓库不会自动证明网站已更新，网站发布需另行配置与验证。

## 新 Agent 必读文件

1. `governance/agent-rules.md`（入口）与 `governance/vision.md`（愿景）。
2. **`governance/editorial-style.md`（教材叙事与反提纲化规范）**、`governance/learning-contract.md`（教学契约）。
3. `governance/curriculum.md`、`governance/decisions.md`（14 章结构与正式决策）。
4. `governance/agent-operations.md`、`governance/change-process.md`、`governance/release-policy.md`（协作与发布）。
5. 当前被分配的章节和必要的先修章节；当前案例与学习反馈材料。

## 我们在训练什么

从一个构想出发，能定义可检验的行为、推导系统架构与技术选择、理解底层原理、编写可维护软件、进行故障注入与验证，并最终把功能原型推进到可制造、可维护的产品。

教材主线案例：三页面 SSD1306 仪表、按键消抖与长按、统一故障管理、I²C 双屏/TCA9548A、FreeRTOS 任务通信、LVGL 与 ESP32/RP2040 跨平台。

## 证据状态

- 已确认：课程方向、14 章架构、教材风格与作者工作规则。
- 已编写、待审阅：1.1 扩展正文、1.2 连续教材重写稿及 REQ-001～REQ-008 教学需求与测试计划。
- 已生成预览：本仓库的 HTML（1.1、1.2 均同步自 Markdown），支持分节导航、无 JS 阅读和全文打印。
- 已检查：阅读器正文同步、目录锚点、离线导航与原 OLED 交互、320px/390px 布局、无 JavaScript 阅读和打印；这些检查不等于八条产品需求实现通过。
- 未验证：示例 C 代码构建、开发板、引脚配置、I²C 外设实测、实时性能、生产可靠性。

讨论中的新想法不得直接覆盖总纲，需要遵守 CCP 变更流程。不能将“发布 HTML 预览”描述成“全部教学与硬件验证通过”。

## 新会话启动提示

```text
请以 ~/Documents/project/embedded-product-course 为工作目录。先读取 README 和 governance 下的全部规范，并检查当前 Git 状态。以后以这个目录作为《现代嵌入式产品工程》的唯一工作仓库。
所有教材修改都必须遵守教学规范，以 Markdown 为正文来源，修改后重新生成 HTML、验证结果并检查 Git Diff。
只使用 main 分支，直接在 main 上修改和验证；未经我要求，不创建其他分支、工作树或 PR。
不要擅自修改已经确认的课程架构。未经我同意，不要直接 push 到 GitHub。
```
