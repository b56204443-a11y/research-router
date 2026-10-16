# Research-Router-Paper-Skills

[English](README_EN.md) · [模块目录](docs/MODULES.md) · [来源与许可证](docs/LICENSING.md)

为 Codex 按需选择科研技能：论文写作、文献检索、统计分析、科研绘图和科学计算。
只加载一个路由技能，在需要时codex自动检索并读取对应模块，避免启动时把全部技能加入上下文。

当前发布包含 **245 个模块**。这是整理自多个开源项目的技能库，保留上游作者、提交版本、许可证和第三方声明。
感谢所有上游贡献者；模块不是本项目从零编写的。路由与安装工具使用 MIT，模块各自保留原许可证。

## 安装

需要 Codex 和 Python **3.10 或更高版本**。路由器及安装工具只用 Python 标准库。

```bash
git clone https://github.com/b56204443-a11y/research-router.git
cd research-router
python3 scripts/install.py
```

Windows 通常可把 `python3` 换成 `py -3`。也可以点击仓库的 **Code → Download ZIP**，解压后在该目录运行安装命令。

安装后新开一个 Codex 聊天，输入：

```text
使用 $research-router，帮我规划这篇论文的统计分析。
使用 $research-router，检索并核实这个课题的参考文献。
使用 $research-router，把这组实验数据画成适合论文的图。
```

如果想先预览安装位置：

```bash
python3 scripts/install.py --dry-run
```

默认安装到 `CODEX_HOME`（未设置时为 `~/.codex`）。自定义位置：

```bash
python3 scripts/install.py --codex-home /path/to/codex-home
```

只有 `skills/research-router` 进入技能发现目录；模块保存在
`skill-libraries/research-router/modules`。不要把所有模块复制到 `skills/`。

## 更新与卸载

```bash
git pull --ff-only
python3 scripts/install.py --replace
```

`--replace` 会先备份同名路由器和模块库，再替换。备份位置会显示在输出中。
其他技能不会被替换。自定义安装位置时，更新和卸载也要传相同的 `--codex-home`。

```bash
python3 scripts/uninstall.py
```

卸载会把本安装器管理的路由器和模块库移到 `research-router-backups/`，可手动恢复。
旧版手工安装没有管理标记时，本卸载器会拒绝操作。

## 检索与检查

在仓库目录里可以直接检索，无须先安装：

```bash
python3 skills/research-router/scripts/find_modules.py --query "统计分析" --limit 5
python3 skills/research-router/scripts/find_modules.py --query "scanpy" --json
python3 skills/research-router/scripts/find_modules.py --list --category literature
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

检索结果给出模块 `SKILL.md` 的实际绝对路径。`--library-root` 或 `RESEARCH_ROUTER_LIBRARY`
可以覆盖模块目录。中文常用任务词有检索映射；检索是本地关键词排序，不是在线语义搜索。

## 使用范围

- 路由和安装不需要 API Key。具体文献平台、数据库、云服务可能需要网络、机构权限或用户自己的 Key。
- 科学软件依赖按所选模块安装；本仓库不包含完整 Python 环境、模型权重或论文数据库。
- 没有把各模块的原生 `allowed-tools` 字段变成新工具；能否使用浏览器、联网、PDF/PPT 工具取决于运行环境。
- 已测试目录、检索、安装和卸载。245 个模块的外部服务与科学算法没有逐一执行验证。
- 技能不构成额外的发表、上传、购买或发送消息授权；按用户实际请求操作。

首版暂时排除 11 个模块：4 个明确限制分发的文档模块，以及 7 个许可证未知、专有、非商业或上游明确指出授权未解决的模块。
这表示暂未确认适合纳入此开源发布，不意味着所涉及的软件或数据本身一律禁止使用。
完整名单见 [excluded-modules.json](skill-libraries/research-router/excluded-modules.json)。

## 贡献

欢迎 Star、提交 Issue 或 Pull Request。新增模块请提供明确的来源、固定提交版本与可分发许可证；
同步更新目录、来源记录和文件哈希，再运行校验与测试。不要提交 API Key、个人绝对路径、论文全文或无授权素材。
参见 [CONTRIBUTING.md](CONTRIBUTING.md)。
