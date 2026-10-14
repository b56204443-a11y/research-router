# 来源、许可证和发布边界

本仓库的路由器与安装工具采用根目录 [MIT License](../LICENSE)。
模块保留上游与各组件的许可证，不能用根目录 MIT 覆盖所有内容。

所有源提交来自原技能目录的来源记录。模块可能包含本地整理；它们不是声称与上游提交逐字相同的镜像。
[provenance.json](../skill-libraries/research-router/provenance.json) 的 SHA-256 对应实际发布文件。
每个模块的 `ORIGIN.md` 说明本次打包修改。
直接来自 Apache-2.0 上游的模块也已逐文件比较，修改记录见
[APACHE_MODIFICATIONS.md](../skill-libraries/research-router/licenses/APACHE_MODIFICATIONS.md)。

| 来源 | 保存的许可证及说明 |
|---|---|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 根目录 MIT；模块内原许可证、标签另行保留 |
| [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills) | MIT 与 Apache-2.0 组件；保留 LICENSE、LICENSE-APACHE、NOTICE、ATTRIBUTION |
| [YuanyuanMa03/academic-research-skills](https://github.com/YuanyuanMa03/academic-research-skills) | 根目录 MIT |
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Apache-2.0 |
| [cLin-c/paper-skill](https://github.com/cLin-c/paper-skill) | MIT |

完整文本保存在 [licenses/](../skill-libraries/research-router/licenses/)。原模块的 LICENSE 和 THIRD_PARTY_NOTICES 也保留。
上游 Boom5426 的 ATTRIBUTION 描述更早的二次来源；对应说明仍然随包分发。

`SKILL.md` 的 `license` 有时指被介绍的软件、模型或服务，有时指技能本身。因此未知、专有与非商业标注没有被自动改写成 MIT。
首版暂时排除这些尚未明确适合发布的模块，名单和具体原因见 [excluded-modules.json](../skill-libraries/research-router/excluded-modules.json)。
未来获得明确说明或许可后，可逐项恢复。被排除模块的原始文件不随包分发。

依赖的软件、数据库、云 API、模型权重和下载论文不随包分发，其许可和访问条件独立。
科学软件模块保留 BSD、GPL、CC 等原始标注；根目录上游许可不改变所调用软件与数据的条款。

这是对本次发布材料的来源整理，不是对所有外部服务的许可证审查。
