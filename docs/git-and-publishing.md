# Git 协作与 HTML 发布工作流

本项目的唯一 Git 工作目录：`~/Documents/project/embedded-product-course`。以课程负责人明确指定及实际存在的目录为准，不使用 `Documents/projects` 路径。

## 哪个地方是真正的教材？

- `chapters/*.md`、`governance/*.md`、`hardware/` 以及实验源码：**正式源文件**。所有新 Agent 必须基于仓库里的实际版本工作。
- `site/template.html`：HTML 阅读器外壳与交互示例的模板。可以编辑它的样式和行为，但不要直接在这里改教材正文。
- `scripts/build_site.py`：将 Markdown 正文写进 HTML 阅读器的可重复构建脚本。
- `index.html`：生成的阅读预览，便于离线打开。不要手工修正文；修改 Markdown 后重新运行脚本。
- ZIP 文件：交付快照，适合转交他人，不是持续更新仓库的方式。

## 仅在创建新仓库时初始化 Git（现有仓库不要重复执行）

```bash
cd embedded-product-course
git init
git add .
git commit -m "Initialize embedded product engineering course"
```

如果希望同步到自己的私有远端仓库，在 GitHub、GitLab 或其他 Git 服务创建一个空仓库后，再执行（地址换成你自己的）：

```bash
git branch -M main
git remote add origin YOUR_GIT_REMOTE_URL
git push -u origin main
```

> `YOUR_GIT_REMOTE_URL` 是占位符；仓库地址、SSH 密钥及权限需要你自己配置。不要把 API key、密码或设备私钥提交到仓库。

## 日常协作：只使用 main

仓库所有者于 2026-11-16 确认：只保留并使用 `main`，日常修改、构建和验证直接在 `main` 进行。Agent 不自动创建功能分支、额外工作树或 PR；只有仓库所有者明确要求时才例外。

开始任务时检查 Git 状态和提交关系。工作区干净且本地主分支可快进时，可以同步远端已有提交：

```bash
git status --short --branch
git switch main
git pull --ff-only
```

然后编辑被分配的 Markdown 或源码，重新构建并审查差异：

```bash
python3 scripts/build_site.py
git diff --check
git diff
```

检查完成后按任务需要保存本地提交；向 GitHub 推送内容必须另获仓库所有者明确同意。直接在 `main` 工作不代表草稿自动通过教学审查，也不改变 CCP、课程架构或正式发布门槛。

同一时间只安排一项会写入仓库的任务。多个 Agent 如需参与，可以分别阅读、提出建议，由当前编辑者整合；不要无协调地同时改写同一目录。发生本地与远端分歧时，先查看提交和差异，保留已有工作再处理。

## 本地重建 HTML

```bash
python3 -m pip install -r requirements-build.txt
python3 scripts/build_site.py
```

运行后直接打开 `index.html` 即可离线阅读。构建依赖 `requirements-build.txt` 中的 `mistune` 与 `beautifulsoup4`；打开生成的 HTML 不需要 Python 或网络。

目前 **1.1、1.2 Markdown** 均已接入自动生成流程，对应 `v0.3.0-preview`；分节导航与目录支持直接定位，无 JS 时按顺序显示全部正文。其他章节仍处于规划阶段。阅读预览和阅读器检查不代表章节通过人工审核，更不代表产品功能与硬件验收通过。

修改后检查 `git diff --check`，并按 `docs/validation/reader-v0.3.0-preview.md` 检查正文同步、锚点、桌面/移动布局、离线交互、无 JS 阅读和打印；需求测试计划须与已经执行的阅读器检查分开记录。未经仓库所有者同意，不直接 push 到 GitHub。

## rsync 放在哪里？

Git 保留历史和审查记录；rsync 适合把 HTML 阅读文件发送到你管理的服务器。比如：

```bash
rsync -av index.html YOUR_USER@YOUR_HOST:/path/to/course-site/
```

上面两个 `YOUR_...` 都是占位符。将来网站若拆成 HTML/CSS/JS 多文件，可以同步生成的 `dist/` 目录。不要使用 rsync 覆盖 Git 的 `.git` 目录，也不推荐让 rsync 作为多人同时编辑 Markdown 的主要协作方式。

谨慎使用 `rsync --delete`：它会删除远端目标目录中未出现在源目录的文件。第一次发布建议不使用它。

## 一次改动的实际路线

1. 读取 `README.md` 和治理规范，确定工作基线与当前章节状态。
2. 在 `main` 编辑被分配的 `chapters/*.md`，根据需要更新规范或实验源码，不自动创建分支。
3. 执行生成命令，检查文字、代码、表格、交互和无 JS 情况。
4. 审核 Git Diff，按任务需要保存本地提交；对重大课程方向变化先执行 CCP 流程。
5. 经仓库所有者明确同意后，再执行对应的远端 push 或 rsync 发布。
6. 不把 Git push 成功等同于“自动更新远端 HTML 网站”，除非另行配置并验证了发布流水线。


## 通过更新包导入治理修改

先运行 `git status`，保存正在进行的工作，再将 ZIP 内 `embedded-product-course/` 的文件**合并**到已有仓库，保留原 `.git/`。不要把更新包当成新的仓库历史；检查 `git diff`、未跟踪的新文件、HTML 构建结果，再由仓库所有者决定是否 commit/push。
