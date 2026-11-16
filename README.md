# 《现代嵌入式产品工程》

**当前状态**：课程架构为 14 章；Governance 教材写作规范已更新；第 1.1 节已扩展为连贯教材正文 **待学习者审阅**；HTML 阅读器预览 `v0.2.0-preview`。第 1.2 节仍然是 Markdown 草稿，尚未并入 HTML。项目不是已经完成、实机验证的教程。

## 快速阅读

- 双击 `index.html` 打开离线 HTML 阅读预览。
- 第 1.1 节权威正文：`chapters/ch01-lesson01.md`。
- 第 1.2 节草稿：`chapters/ch01-lesson02.md`。
- 原理图、固件工程与硬件测试尚未完成。

## 开发、构建和同步

```bash
python3 -m pip install -r requirements-build.txt
python3 scripts/build_site.py
```

目前构建脚本自动把 **第 1.1 节** 写入 HTML 原型，并保留原先可交互的 OLED 演示。**不要手工编辑 `index.html` 中的教材正文**；修改 Markdown 后重新构建。

Git 与 rsync 的建议用法参见：**`docs/git-and-publishing.md`**。Git 管理正文与历史，rsync 可选用于部署 HTML；普通聊天无法自动同步到你的本地仓库。

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
- 已编写、待审阅：1.1 扩展正文、1.2 需求草稿。
- 已生成预览：本仓库的 HTML（1.1 同步自 Markdown）。
- 未验证：示例 C 代码构建、开发板、引脚配置、I²C 外设实测、实时性能、生产可靠性。

讨论中的新想法不得直接覆盖总纲，需要遵守 CCP 变更流程。不能将“发布 HTML 预览”描述成“全部教学与硬件验证通过”。
