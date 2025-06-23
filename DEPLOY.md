# 部署说明

## 1. 初始化Git仓库并推送到GitHub

### 步骤1: 初始化Git仓库
```bash
git init
git add .
git commit -m "Initial commit: ODG Processor Node.js package"
```

### 步骤2: 在GitHub上创建仓库
1. 访问 https://github.com/new
2. 仓库名称: `odg-processor`
3. 描述: `A Node.js package for processing ODG (OpenDocument Graphics) files`
4. 选择 Public（如果要发布到npm）
5. 不要初始化README（我们已经有了）
6. 点击 "Create repository"

### 步骤3: 连接本地仓库到GitHub
```bash
git remote add origin https://github.com/yourusername/odg-processor.git
git branch -M main
git push -u origin main
```

## 2. 发布到npm

### 步骤1: 登录npm
```bash
npm login
```

### 步骤2: 检查包信息
```bash
npm run test  # 运行测试
npm pack --dry-run  # 预览要发布的文件
```

### 步骤3: 发布包
```bash
# 首次发布
npm publish

# 后续版本更新
npm version patch  # 或 minor, major
npm publish
```

## 3. 版本管理

### 语义化版本控制
- `patch`: 1.0.0 -> 1.0.1 (bug修复)
- `minor`: 1.0.0 -> 1.1.0 (新功能，向后兼容)
- `major`: 1.0.0 -> 2.0.0 (破坏性更改)

### 更新版本命令
```bash
npm version patch -m "Fix: 修复文本修改问题"
npm version minor -m "Feature: 添加新的导出格式"
npm version major -m "Breaking: 重构API接口"
```

## 4. 持续集成（可选）

可以添加GitHub Actions来自动化测试和发布流程。

### .github/workflows/publish.yml
```yaml
name: Publish to npm

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '16'
          registry-url: 'https://registry.npmjs.org'
      - run: npm install
      - run: npm test
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## 5. 文档维护

### README.md
- 保持示例代码最新
- 添加更多使用场景
- 更新API文档

### CHANGELOG.md
记录每个版本的更改：
```markdown
# Changelog

## [1.0.1] - 2024-01-XX
### Fixed
- 修复文本修改返回格式问题

## [1.0.0] - 2024-01-XX
### Added
- 初始版本发布
- ODG文件信息读取功能
- 文本批量修改功能
- PDF自动导出功能
```

## 6. 注意事项

1. **更新package.json中的用户名**：将 `yourusername` 替换为你的GitHub用户名
2. **检查依赖**：确保所有依赖都正确安装
3. **测试**：发布前务必运行测试确保功能正常
4. **文档**：保持README.md和示例代码同步更新
5. **许可证**：确认MIT许可证符合你的需求

## 7. 推广

发布后可以：
- 在相关技术社区分享
- 写博客介绍使用方法
- 提交到awesome列表
- 在Stack Overflow回答相关问题时推荐 