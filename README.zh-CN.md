# Stage Grid Poster

[English](README.md) · [简体中文](README.zh-CN.md)

一个由给定素材集生成的可复用公共 style-skill。

## 使用

用主题、文字、图片或载体请求调用该 skill。它会应用学到的视觉语法，产出原创结果，而不是重建某个参考来源。

### 示例

- `用 stage-grid-poster 做一张关于夜市的原创海报。`
- `用 stage-grid-poster 处理这张给定图片，同时保留主体。`
- `用 stage-grid-poster 做一张方形封面，标题严格保留 “SIDE B”。`

## 公共行为

- 严格保留用户给定的文字与事实内容。
- 未指定的选择使用稳定默认值。
- 给定参考仅作为视觉证据，不作为模板。
- 有工具时返回成品，无工具时返回制作规格。

## 包含内容

- `SKILL.md`：公共入口
- `design-system/`：可执行 token 与有界选择
- `evals/`：公共行为契约
- `examples/`：原创演示
- `REFERENCES.md`：来源与署名
- `scripts/validate_public.py`：独立子包校验器

## 版本

子包在 `release.json` 与 `CHANGELOG.md` 中独立使用语义化版本。为公开发布创建 Git 标签，例如 `v1.0.0`。子包版本与父级私有 run ID、公共契约/schema 版本相互独立。该子包无需父级项目即可维护和校验。

## 许可证与范围

本子包对包所有者有权许可的原创代码、指令、schema 和演示使用 Apache License 2.0。对受 Apache-2.0 覆盖的材料，允许商业使用而无需单独付费或授权，但须遵守 `LICENSE` 中的 Apache-2.0 声明与免责条款。

Apache License 2.0 **不会**重新授权给定的源素材、第三方图片、字体、logo、商标、用户提供文本、模型输出或其他资产。这些材料仍受 `REFERENCES.md` 与 `ASSET-LICENSE.md` 中记录的条款约束。署名不等于授权。未经核实权利，请勿发布或商用任何资产。
