# Git 协作与 HTML 发布工作流

这份文档假定你将整个 `embedded-product-course/` 目录放在自己的电脑或有权限的服务器上。

## 哪个地方是真正的教材？

- `chapters/*.md`、`governance/*.md`、`hardware/` 以及实验源码：**正式源文件**。所有新 Agent 必须基于仓库里的实际版本工作。
- `site/template.html`：HTML 阅读器外壳与交互示例的模板。可以编辑它的样式和行为，但不要直接在这里改教材正文。
- `scripts/build_site.py`：将 Markdown 正文写进 HTML 阅读器的可重复构建脚本。
- `index.html`：生成的阅读预览，便于离线打开。不要手工修正文；修改 Markdown 后重新运行脚本。
- ZIP 文件：交付快照，适合转交他人，不是持续更新仓库的方式。

## 首次使用 Git

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

## 多 Agent 以后怎么协作

主分支 `main` 保留已确认的教材基线；写作 Agent 只在功能分支完成任务，例如 `chapter/ch01-expand-1-1`。审查后再合并。不要让几个 Agent 同时无协调地直接写 `main`。

```bash
git switch -c chapter/ch01-expand-1-1
# 编辑 Markdown 和相关测试
python3 scripts/build_site.py
git diff --check
git add chapters/ site/ index.html governance/ scripts/
git commit -m "Expand chapter 1.1 into textbook narrative"
# 经审查后再通过 PR 或人工合并到 main
```

多个 Agent 应各自使用独立的工作树或分支。发生冲突时必须先查看差异并解决，不能用覆盖整个文件的方式跳过审查。**普通聊天没有自动访问你本地 Git 仓库的能力**；Agent 要在能访问代码仓库的环境中执行这套流程。

## 本地重建 HTML

```bash
python3 -m pip install -r requirements-build.txt
python3 scripts/build_site.py
```

运行后直接打开 `index.html` 即可离线阅读。构建依赖 `mistune`；打开生成的 HTML 不需要 Python 或网络。

目前只把 **1.1 Markdown** 接入了自动生成流程；其他章节仍处于草稿/规划阶段，不能因为存在 Markdown 文件就宣称它们已发布。

## rsync 放在哪里？

Git 保留历史和审查记录；rsync 适合把 HTML 阅读文件发送到你管理的服务器。比如：

```bash
rsync -av index.html YOUR_USER@YOUR_HOST:/path/to/course-site/
```

上面两个 `YOUR_...` 都是占位符。将来网站若拆成 HTML/CSS/JS 多文件，可以同步生成的 `dist/` 目录。不要使用 rsync 覆盖 Git 的 `.git` 目录，也不推荐让 rsync 作为多人同时编辑 Markdown 的主要协作方式。

谨慎使用 `rsync --delete`：它会删除远端目标目录中未出现在源目录的文件。第一次发布建议不使用它。

## 一次改动的实际路线

1. 读取 `README.md` 和治理规范，确定工作基线与当前章节状态。
2. 新 Agent 在独立分支编辑 `chapters/*.md`，根据需要更新规范或实验源码。
3. 执行生成命令，检查文字、代码、表格、交互和无 JS 情况。
4. 审核并合并 Git 变更；对重大课程方向变化先执行 CCP 流程。
5. 用 rsync 把 HTML 阅读器发布到服务器，或把仓库 push 到远端以供其他 Agent 拉取。
6. 不把 Git push 成功等同于“自动更新远端 HTML 网站”，除非另行配置并验证了发布流水线。
