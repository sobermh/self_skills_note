# 目录与模板

## 目录约定

以下是组织参考，不是强制脚手架；保留项目既有测试路径。**目录位置可选，但「有测试」本身不可选**，见 SKILL.md 的「实现与验证」。

```text
plugin/
  README.md                 中文主说明
  LICENSE                   根目录许可证
  AGENTS.md                 仓库专属约束
  CLAUDE.md                 可选，仅简短指向 AGENTS.md
  package.json
  <既有锁文件与必要构建配置>
  cordis.patch.yml          宿主 bundle 加载器需要时添加
  src/                      运行时及插件自有界面源码
  test/
    test_cases.csv          功能用例定义与断言映射
    run-test-cases.mjs       断言、夹具和统一执行入口
  scripts/                  可复用的构建、测试、发布辅助脚本
  docs/
    README.en-US.md          英文说明
    configuration.md        需要独立配置参考时添加
    architecture.md         需要解释宿主边界时添加
    publishing.md           有发布流程时添加
    CHANGELOG.md
    CONTRIBUTING.md
    THIRD_PARTY_NOTICES.md   需要第三方归属声明时添加
  .github/
    workflows/checks.yml      分支与 PR 的检查
    workflows/publish-npm.yml  v* 标签发布，自带同一份检查矩阵
```

不要生成空文档、重复规则或运行态目录。lib/、node_modules/、覆盖率和本地评估输出保持忽略。
默认不生成 SECURITY.md；仅在用户明确要求或项目已有维护规范要求时添加。
无法确认可删除的本地产物移到明确标识的仓库外备份，不放进 npm 包。
删除脚本或合并文档前检查引用，移动后同步修改 Markdown 链接、Agent 规则和 package.files 匹配规则。

## 展示元数据（插件市场与 dsh 插件页）

同一个插件会在两处显示，读的是**两套不同字段**，缺哪一套，哪一处就退化：

| 显示位置 | 读取 | 缺失时 |
|---|---|---|
| TokensCowork 插件市场（Discover 卡片） | `package.json` 的 `tokenscowork.displayName` / `summary`，缺的语言再读 `locale/<lang>.json` 的 `meta` | 回退市场后台登记文案（通常只有中文） |
| dsh 侧栏「插件」页（已安装卡片、详情、组件行） | 只读 `locale/<lang>.json` 的 `meta.title` / `meta.description` 和清单 `icon`，**不认 `tokenscowork`** | 标题退成完整包名，描述退成 `package.json.description`（不随界面语言切换），图标用默认插画 |

两处都要双语，所以**两套都写，文案保持一致**。市场只从私有 Registry 的包里读 `locale/`，公开 npm 条目只认 `tokenscowork`。

### 市场字段

替换为真实名称与准确简介，保留既有 name、description、repository、license 和依赖字段。

```json
{
  "tokenscowork": {
    "displayName": {
      "zh-CN": "中文插件名称",
      "en-US": "English Plugin Name"
    },
    "summary": {
      "zh-CN": "准确说明插件用途，不夸大能力。",
      "en-US": "An accurate description of the plugin's purpose."
    }
  },
  "publishConfig": {
    "registry": "https://npm.tokensapi.ai/"
  }
}
```

### dsh locale 文件与图标

按 dsh 约定在包根放 `locale/en.json`（发现入口，必须有）和 `locale/zh.json`：

```json
{ "meta": { "title": "English Plugin Name", "description": "An accurate description of the plugin's purpose." } }
```

`package.json` 合并以下条目（保留既有运行时 exports 与 files）。dsh 和市场都只在声明了 `./locale/*.json` 导出时才去读这些文件，只放文件不加导出等于没写：

```json
{
  "exports": {
    "./package.json": "./package.json",
    "./locale/*.json": "./locale/*.json"
  },
  "files": ["locale/*.json", "icon.svg"],
  "icon": "./icon.svg"
}
```

- `meta` 字段可选，填写时必须是非空字符串；JSON 损坏会在 dsh 插件页显示诊断。
- `icon` 相对清单所在目录，支持不超过 256 KiB 的 SVG、PNG、JPEG、WebP，必须自包含；绝对路径、URL、目录外路径都会被拒绝。不需要单独导出图片，但要放进 `files`。
- 宿主仓库提供 `pnpm run verify-package-meta` 时用它核对字段、导出和 files 覆盖。

### 共同要求

访问控制由私有 Registry 的 ACL 决定。不要声称 npm 的 access 字段就能保护包，也不要照抄示例的 access: public。
测试两套字段：JSON 能解析、各语言字段均为非空字符串，**并断言英文不等于中文**——把中文复制进 en-US 能过"非空"断言，在英文界面下却和没填一样；同时断言 `tokenscowork` 与 `locale/*.json` 同语言文案一致，`./locale/*.json` 导出存在，`npm pack --dry-run` 的文件列表包含 `locale/en.json`（以及声明了的图标）。同步扩展项目实际使用的清单 schema 或类型定义，翻译保持原意。

**改完不会立刻生效**：两处都读**已发布的包**，补了字段的仓库不会改变已发布版本的显示，要等下一次发版并重新安装。核对时分别看市场目录接口的中英文结果，以及 dsh 插件页切换界面语言后的标题和描述，不要只看中文那次就当双语完成。

## 界面文案国际化（仅当插件自带 UI 时适用）

**先确认界面是否存在，再谈双语。** 定义了 schemastery 配置 schema 不等于存在配置界面：

- 宿主没有通用的 schema 表单渲染器。查证方式：在宿主源码树中搜索 schema 库名（如 `schemastery`），无命中即无通用渲染。
- 有界面的插件自带 `src/client/` 下的组件，由插件自己渲染。
- 没有 `src/client/` 时，配置 schema 只被配置文件消费，字段说明写给读配置的人，用注释或文档即可，**不要求双语，也不要为此加 `.description()`**。

误判代价是凭空造出一批无人可见的翻译。核对宿主与插件两侧后再下结论，不要从"schema 理论上可被渲染"推出"存在双语界面缺口"。

插件确实自带 UI 时才适用以下要求：

- 面向用户的显示名、字段标签、说明、分组标题、选项标签、占位提示和校验提示均提供 zh-CN 与 en-US，中文保持原意，英文自然准确。
- 沿用宿主实际支持的国际化 API 及其语言选择和回退机制；不臆造双语字段，不把"中文 / English"拼在同一个标签里。宿主不支持时明确记录限制，不声称已完成双语显示。
- 配置键、枚举值、工具名及其他程序标识保持稳定，只翻译展示文案，不改变默认值、校验规则、持久化格式或运行行为。
- 测试两种语言的必需文案均为非空、翻译键完整，schema 仍可加载，语言解析及回退符合宿主契约；在真实界面切换中文和英文核对显示。未执行界面验证时明确标注。

### 中英文混杂防护

- 检查插件自有文案的实际输出，不只检查翻译表：覆盖错误提示、空状态、加载/重试提示和动态拼接文案。en-US 下不得残留未翻译的中文产品提示；zh-CN 下也应本地化非技术英文提示。用户输入、服务端业务内容、品牌名、代码/API 标识和明确标注的原始诊断信息不机械翻译，不用“禁止所有中文/英文”的全局扫描误伤这些内容。
- 上游固定中文错误消息可能绕过翻译表。优先按稳定错误码或错误类型映射本地化提示；无法可靠分类时使用本地化的通用失败提示，不靠替换中文字符串推测错误类型。需要保留的原始诊断信息与面向用户的提示分开，不把原始消息当作已完成国际化的文案。
- 在插件现有用例清单与执行器中增加适用的回归检查：分别断言中文和英文输出、语言回退，以及代表性动态提示/上游错误路径。字段非空、两种译文不同或字符扫描只能辅助检查，不能证明翻译正确或界面无混杂；实际语言切换验收仍按上文要求执行并报告未验证项。

展示元数据（`tokenscowork` 字段与 `locale/*.json` 的 `meta`）双语是**无条件要求**，与插件是否自带界面无关；它们也不会自动翻译任何界面。

## 加载与打包契约

Cordis bundle 使用实际宿主支持的清单契约：

```yaml
- insert:
    - id: <unique-plugin-id>
      name: '<actual-npm-package-name>'
```

按需将 dsh.bundle.patch 指向该文件。main、types、exports 与真实构建产物一致。
声明 `dsh.engine` 时，范围必须包含产品当前固定的 dsh 版本；随产品升级 dsh 后同步复核，例如 `<0.2.0` 会把 0.2.x 宿主排除在外。
发布编译代码和引用的运行时资源，避免要求用户在 install/postinstall 时现场编译。
若架构要求共享宿主服务身份，宿主提供的依赖放在 peerDependencies，支持版本范围需有契约验证依据。

## 中文 README 提纲

仅保留与插件相关的章节：

1. 用途、边界和英文版链接。
2. 支持的市场或 Registry 安装方式、宿主版本要求。
3. 最小配置与真实使用流程。
4. 已知限制、权限和错误恢复行为。
5. 开发测试命令及详细文档链接。

不要在 README 与专门参考文档中重复完整配置和发布流程。法律声明不是可丢弃的杂项。
