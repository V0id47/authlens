# AuthLens

**离线分析身份验证日志，提供可检查、可追溯的证据。**

[English](README.md) · [Español](README.es.md) · [Русский](README.ru.md)

Python 3.11+ · MIT · v0.1.0 · 无运行时第三方依赖。当前为本地候选版本；参见[验证结果与待完成事项](docs/release-readiness.md)。

## 为什么需要这个项目

调查一份身份验证日志，不应必须上传敏感数据或部署 SIEM。AuthLens 展示相关事件、来源和被丢弃的数据。检测到的迹象需要进一步调查，不能证明账户已失陷。

## 功能

支持 SSH 日志语法和严格的 JSONL 模式；统一为 UTC；使用包含边界的时间窗口，检测重复失败、多个账户的失败及失败后的成功登录。提供排除项、去重、SHA-256、行号引用、输入质量诊断、结构化运行日志，以及四种语言的 text/JSON/CSV/Markdown/HTML 报告。不会连接网络、尝试登录或封禁账户。

## 演示

示例数据为合成数据，使用文档专用 IP 地址，无需外部服务器：

```console
authlens analyze examples/ssh-demo.log --input-format ssh --lang zh-CN
authlens analyze examples/events.jsonl --format html --output demo-zh.html --lang zh-CN
```

预期得到 AL-001（alice 的五次失败）、AL-003（随后成功登录）和 AL-002（五个不同账户失败）。参见[预期结果](examples/expected-findings.json)。

## 架构

有界文件读取与哈希 → 解析器 → UTC 事件 → 排除与去重 → 双端队列及计数器维护时间窗口 → 带证据的迹象 → 本地化导出。核心引擎独立于 CLI 和报告格式。参见[架构](docs/architecture.md)与[技术决策](docs/adr/0001-language.md)。

## 安装

使用 Python 3.11–3.14。在项目目录中，Linux/macOS：

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
```

Windows PowerShell：

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install .
.venv\Scripts\authlens.exe --help
```

未激活环境时，将 `authlens` 替换为 `.venv\Scripts\authlens.exe`。安装可能下载构建工具；运行完全离线。尚未宣称发布到 PyPI。本地验证环境为 Windows/Python 3.12；其他平台的公开 CI 仍需运行。

## 快速开始

```console
authlens analyze examples/events.jsonl --lang zh-CN
authlens analyze examples/events.jsonl --format json --output report.json
```

输出必须使用新文件名。报告包含用户名和 IP，请保存在私有目录。

## 用法

```console
authlens analyze --help
authlens analyze examples/events.jsonl --window-seconds 60 --burst-threshold 5
authlens analyze examples/events.jsonl --exclude-cidr 198.51.100.0/24 --exclude-user healthcheck
authlens analyze examples/events.jsonl --strict --fail-on MEDIUM --format json --log-file run.log
authlens analyze auth.log --input-format ssh --year 2026 --timezone=-03:00
```

退出码：0 完整分析；1 达到 `--fail-on` 阈值；2 参数或配置错误；3 I/O 或资源限制；4 输入不完整、格式错误或无可分析事件；130 取消。输入不完整的状态优先于检测结果。stdout 只输出报告，stderr 输出诊断。`--quiet` 保留报告和错误；`--verbose` 添加完成统计。文本输出本身不带颜色。

## 输出

JSON `schema_version=1.0` 包含版本、UTC 生成时间、来源哈希、计数、诊断和实际配置。每个结果分别列出观察、推断、假设、建议和正常原因，并包含严重级别、定性置信度、参数、参考资料及最多 20 条事件证据。机器键名、ID 和枚举不翻译。每条规则的每个分组仅报告首次达到阈值的事件窗口。无结果的 CSV 只有表头；此时需要 JSON 才能保留输入质量信息。参见[模式](docs/report-schema.json)。

## 配置

使用 `--config examples/config.toml`。优先级：CLI > 明确指定的 TOML > 默认值。未知键名、错误类型或越界数值会被拒绝。默认窗口 300 秒，阈值 5，文件上限 16 MiB，每行 16 KiB，排除和去重前最多 50,000 条有效记录。参见[配置参考](docs/configuration.md)。

## 语言

支持 `--lang en`、`es`、`ru`、`zh-CN`，也可在 TOML 中设置 `language = "zh-CN"`。未指定时读取系统区域设置，并回退到英语。语言目录随软件包安装，测试会检查键名和格式参数一致性。欢迎母语使用者审校；不宣称翻译经过认证。

## 安全

报告不保留原始日志行或 SSH 后缀；运行日志不记录身份、路径或输入内容。HTML/Markdown 内容经过转义，CSV 公式前缀被中和。不会覆盖已有文件。POSIX 文件模式为 0600；Windows 使用目录继承的 ACL。参见[安全政策](SECURITY.md)和[威胁模型](THREAT_MODEL.md)。

## 范围与授权

仅处理自有或明确获准处理的日志。范围是本地文件及排除项，而非网络目标。请使用固定导出文件和自己控制的目录。哈希标识已处理字节，不能证明日志真实性或证据保管链。

## 限制

仅支持文档描述的 SSH 语法与 JSONL 模式，不支持任意 syslog、EVTX、原生 VPN 或 Web 日志。传统时间戳必须提供年份及固定偏移；时间倒退会被拒绝，不推测跨年或夏令时。没有 GeoIP、信誉查询、攻击归因、机器学习或缓慢/分布式攻击检测。低精度时间戳下，完全重复的记录也可能是真实事件；可使用 `--keep-duplicates` 保留。资源限制可降低风险，但不能保证固定 RAM 占用。

## 误报

用户重试、自动化程序的过期凭据、共享 NAT、QA 测试及 SSO 故障可能产生类似模式。失败后的成功登录也可能是正常恢复。没有尝试密码的信息，无法确认 password spraying。MEDIUM/HIGH 是调查优先级，并非 CVSS。参见[规则逻辑](docs/detection-logic.md)。

## 开发

```console
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python -m ruff check src tests scripts evaluation
python -m ruff format --check src tests scripts evaluation
```

参见[贡献指南](CONTRIBUTING.md)。新规则必须有具体需求、证据定义、反例和测试。详细技术文档使用英语。

## 测试

```console
python -m pytest --cov=authlens --cov-report=term-missing
python -m bandit -r src -q
python -m pip_audit -r requirements-dev.txt
python -m build
python scripts/benchmark.py
```

测试涵盖窗口边界、Unicode、恶意输入、语言目录、导出及真实 CLI。覆盖率包含子进程。不具备所需权限的测试会明确标记为跳过。依赖漏洞检查需要联网。

## 路线图

先完成公开 CI、发布和代表性数据验证，再评估多事件窗口、新适配器及假名化报告。这些扩展目前尚未实现。参见[开发阶段](docs/development-phases.md)与[作品集说明](docs/portfolio.md)。

## 许可证

[MIT](LICENSE)。
