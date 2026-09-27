# tool-issue-form-architect

> **GitHub 强类型 YAML Issue 表单、PR 模板与 CODEOWNERS 协作治理架构师**  
> Universal CLI Facade (UCFS v1.0) 标准实现 | 100% 离线自省 | 高信噪比社区治理契约生成

> [!NOTE]
> **第一性原理架构收敛声明 (Evolution Notice)**:  
> 本工具所包含的 Issue 结构化表单、PR 协作模板与 CODEOWNERS 治理规范，已正式通过第一性原理仲裁并收敛归入高内聚特种技能 [skill-github-ops](file:///D:/github/skill-github-ops)（三级渐进式披露架构）。  
> 存量代码已冻结并归档保留。在现代 AI 协同中，推荐直接调用 `skill-github-ops` 享受更轻量、零 Token 浪费的最佳实践。


---

## 🌟 核心价值与实用性痛点解答

在开源协同或多人团队研发中，低质量的 Issue 和 PR 会严重消耗维护者精力：
1. **空白与非结构化 Issue 泛滥**：用户随意提交“无法运行”、“报错了”等仅有一句话的 Issue，缺少操作系统、软件版本、复现步骤与关键错误日志。
2. **重复询问降低研发效率**：维护者必须反复回复“请提供复现步骤和环境信息”，导致工单解决周期成倍延长。
3. **缺少 PR 质量门禁与责任人路由**：PR 缺乏测试用例自查清单，且未配置 `CODEOWNERS`，核心模块变更无法自动通知对应技术专家。

`tool-issue-form-architect` 一键建立工业级协同门禁：
- **强类型 Issue Forms (`.github/ISSUE_TEMPLATE/*.yml`)**：提供带必填项校验（`required: true`）、下拉选项（操作系统/架构）、Shell 语法高亮日志框的结构化表单。
- **空白 Issue 强制抑制 (`config.yml`)**：关闭无格式自由发帖，将通用咨询与安全漏洞引流至 Discussions 与私密安全披露通道。
- **PR 质量检查契约 (`pull_request_template.md`)**：强制要求附带单测通过证明、破坏性变更声明与文档更新。
- **代码所有权路由 (`CODEOWNERS`)**：按目录将关键路径精确绑定至指定维护者。

---

## ⚡ 极速开始 (Quick Start in 3 Seconds)

```bash
# 1. 环境校验
python main.py setup

# 2. 对当前项目架构全套协作治理模板 (.github/ 目录)
python main.py run

# 3. 运行离线单元测试
python main.py test

# 4. 核心健康自检
python main.py health

# 5. 清理缓存
python main.py clean
```

### 高级功能：定制所有者与静态审计
```bash
# 为指定项目脚手架治理模板，并绑定责任团队
python main.py scaffold --target D:\github\my-project --owner @core-maintainers

# 巡检现有工程的表单规范与 CODEOWNERS 配置
python main.py lint --target D:\github\my-project
```

---

## 🛡️ 架构与不变式

- **独立职责**：专注于 GitHub 社区协同表单与治理文件架构，不干预业务运行态。
- **离线确定性**：模板生成基于固化的 GitHub Forms Schema，100% 离线免网。

---

## 🚫 Non-Goals (明确非目标)

1. **不自动回复或关闭 Issue**：本工具不包含云端 Bot 自动回复/打标签逻辑（应由 GitHub Actions 触发器完成）。
2. **不审查 PR 代码实质**：本工具提供治理规范与模板，不对用户提交的代码行逻辑进行人工语义裁决。
3. **不越权修改源码**：仅在 `.github/` 目录下生成标准规范文件，绝不触碰业务代码。
