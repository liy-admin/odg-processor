#!/bin/bash

# ODG Processor 发布脚本

echo "🚀 开始发布 ODG Processor..."

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ 错误: 有未提交的更改，请先提交所有更改"
    exit 1
fi

# 运行测试
echo "🧪 运行测试..."
npm test
if [ $? -ne 0 ]; then
    echo "❌ 测试失败，取消发布"
    exit 1
fi

# 检查包内容
echo "📦 检查包内容..."
npm pack --dry-run

# 询问版本类型
echo "📋 选择版本更新类型:"
echo "1) patch (1.0.0 -> 1.0.1) - Bug修复"
echo "2) minor (1.0.0 -> 1.1.0) - 新功能"
echo "3) major (1.0.0 -> 2.0.0) - 破坏性更改"
echo "4) 手动输入版本号"
read -p "请选择 (1-4): " version_choice

case $version_choice in
    1)
        echo "🔧 更新patch版本..."
        npm version patch
        ;;
    2)
        echo "✨ 更新minor版本..."
        npm version minor
        ;;
    3)
        echo "💥 更新major版本..."
        npm version major
        ;;
    4)
        read -p "请输入版本号 (例如: 1.2.3): " manual_version
        npm version $manual_version
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

# 推送到GitHub
echo "📤 推送到GitHub..."
git push origin main --tags

# 发布到npm
echo "📦 发布到npm..."
npm publish

if [ $? -eq 0 ]; then
    echo "🎉 发布成功!"
    echo "📋 发布信息:"
    echo "   - 包名: $(npm pkg get name | tr -d '\"')"
    echo "   - 版本: $(npm pkg get version | tr -d '\"')"
    echo "   - 仓库: $(npm pkg get repository.url | tr -d '\"')"
    echo ""
    echo "🔗 链接:"
    echo "   - npm: https://www.npmjs.com/package/$(npm pkg get name | tr -d '\"')"
    echo "   - GitHub: $(npm pkg get repository.url | tr -d '\"')"
else
    echo "❌ 发布失败"
    exit 1
fi 