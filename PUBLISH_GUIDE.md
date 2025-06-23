# ODG Processor 发布指南

## 📋 发布前检查清单

### ✅ 必要条件
- [ ] Node.js >= 12.0.0 已安装
- [ ] Git 已安装并配置
- [ ] npm 账号已创建并登录
- [ ] GitHub 账号已创建
- [ ] 代码已通过测试

### ✅ 文件检查
- [ ] `package.json` - 包信息正确
- [ ] `README.md` - 文档完整
- [ ] `CHANGELOG.md` - 版本记录
- [ ] `index.js` - 主文件
- [ ] `python/` - Python脚本目录
- [ ] `.gitignore` - Git忽略文件
- [ ] `.npmignore` - npm发布忽略文件

## 🚀 发布步骤

### 第一步：准备GitHub仓库

1. **在GitHub创建新仓库**
   ```
   仓库名: odg-processor
   描述: A Node.js package for processing ODG (OpenDocument Graphics) files
   类型: Public
   不要初始化README（我们已经有了）
   ```

2. **更新package.json中的用户名**
   ```bash
   # 将 yourusername 替换为你的GitHub用户名
   sed -i 's/yourusername/你的GitHub用户名/g' package.json
   ```

### 第二步：初始化Git仓库

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "feat: Initial release of ODG Processor v1.0.0

- Add ODG file information reading
- Add text modification functionality  
- Add PDF export capability
- Add comprehensive error handling
- Add documentation and examples"

# 连接到GitHub仓库（替换yourusername）
git remote add origin https://github.com/yourusername/odg-processor.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 第三步：测试包

```bash
# 运行测试
npm test

# 检查包内容（预览将要发布的文件）
npm pack --dry-run

# 本地测试安装
npm pack
npm install odg-processor-1.0.0.tgz
```

### 第四步：发布到npm

```bash
# 登录npm（如果还没登录）
npm login

# 发布包
npm publish

# 如果包名已被占用，可以使用scoped包名
# npm publish --access public
```

## 🔄 版本更新流程

### 更新版本
```bash
# Bug修复 (1.0.0 -> 1.0.1)
npm version patch -m "fix: 修复文本修改问题"

# 新功能 (1.0.0 -> 1.1.0)  
npm version minor -m "feat: 添加新的导出格式"

# 破坏性更改 (1.0.0 -> 2.0.0)
npm version major -m "feat!: 重构API接口"
```

### 发布更新
```bash
# 推送标签到GitHub
git push origin main --tags

# 发布到npm
npm publish
```

## 📦 包信息

### 当前配置
- **包名**: `odg-processor`
- **版本**: `1.0.0`
- **主文件**: `index.js`
- **许可证**: `MIT`
- **Node.js要求**: `>=12.0.0`

### 包含的文件
- `index.js` - 主模块
- `python/` - Python桥接脚本
- `README.md` - 文档
- `CHANGELOG.md` - 变更日志

### 排除的文件
- 测试文件 (`test.js`, `example.js`)
- 示例ODG文件
- Python虚拟环境
- IDE配置文件
- Git文件

## 🔗 发布后的链接

发布成功后，你的包将在以下位置可用：

- **npm**: https://www.npmjs.com/package/odg-processor
- **GitHub**: https://github.com/yourusername/odg-processor
- **安装命令**: `npm install odg-processor`

## 🐛 常见问题

### 1. 包名已被占用
```bash
# 使用scoped包名
npm init --scope=@yourusername
# 然后发布
npm publish --access public
```

### 2. 权限错误
```bash
# 检查npm登录状态
npm whoami

# 重新登录
npm logout
npm login
```

### 3. Git推送失败
```bash
# 检查远程仓库地址
git remote -v

# 重新设置远程仓库
git remote set-url origin https://github.com/yourusername/odg-processor.git
```

### 4. 测试失败
```bash
# 检查LibreOffice是否安装
# Windows: C:\Program Files\LibreOffice\program\python.exe
# macOS: /Applications/LibreOffice.app/Contents/MacOS/python
# Linux: /usr/lib/libreoffice/program/python3

# 检查Python脚本
python python/odg_bridge.py get_info payroll.odg
```

## 📈 发布后推广

1. **更新README徽章**
   ```markdown
   ![npm version](https://img.shields.io/npm/v/odg-processor)
   ![npm downloads](https://img.shields.io/npm/dm/odg-processor)
   ![GitHub stars](https://img.shields.io/github/stars/yourusername/odg-processor)
   ```

2. **社区分享**
   - 在相关论坛和社区分享
   - 写技术博客介绍使用方法
   - 在Stack Overflow回答相关问题

3. **持续维护**
   - 及时响应issues和PR
   - 定期更新依赖
   - 改进文档和示例

## 🎉 完成！

恭喜！你已经成功将ODG Processor发布为npm包。现在任何人都可以通过 `npm install odg-processor` 来使用你的包了！ 