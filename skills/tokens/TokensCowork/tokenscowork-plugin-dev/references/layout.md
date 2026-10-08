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

## 市场元数据模板

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

访问控制由私有 Registry 的 ACL 决定。不要声称 npm 的 access 字段就能保护包，也不要照抄示例的 access: public。
测试 JSON 能解析、两个语言字段均为非空字符串，**并断言英文不等于中文**：把中文复制进 en-US 能过"非空"断言，市场在英文 locale 下却和没填一样。同步扩展项目实际使用的清单 schema 或类型定义，翻译保持原意。

**改完不会立刻生效**：市场从**已发布的包**里读 `tokenscowork`，读不到才回退市场后台存的文案（通常只有中文）。所以补了字段的 package.json 不会改变已发布版本的显示，要等下一次发版；核对显示效果时按 locale 分别查目录接口，不要只看中文那次就当双语完成。

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

市场元数据（package.json 的 tokenscowork 字段）双语是**无条件要求**，与界面是否存在无关；它也不会自动翻译任何界面。

## 加载与打包契约

Cordis bundle 使用实际宿主支持的清单契约：

```yaml
- insert:
    - id: <unique-plugin-id>
      name: '<actual-npm-package-name>'
```

按需将 dsh.bundle.patch 指向该文件。main、types、exports 与真实构建产物一致。
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
