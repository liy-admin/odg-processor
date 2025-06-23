# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-15

### Added
- 🎉 初始版本发布
- 📖 ODG文件信息读取功能
  - 获取页面数量和详细信息
  - 提取所有形状的属性（名称、类型、位置、大小）
  - 读取文本内容和格式信息
- ✏️ 文本内容修改功能
  - 单个形状文本修改
  - 批量形状文本修改
  - 基于形状名称的精确定位
- 📄 PDF自动导出功能
  - 修改后自动生成PDF文件
  - 多种导出方法的容错处理
  - 自定义输出路径支持
- 🔧 完善的错误处理
  - 详细的错误信息和调试日志
  - 操作状态反馈
  - 异常情况的优雅处理
- 📚 完整的文档和示例
  - 详细的README文档
  - 使用示例和API说明
  - 部署和发布指南

### Technical Details
- 基于LibreOffice Python-UNO Bridge
- 通过子进程调用Python脚本
- 异步Promise API
- 跨平台支持（Windows, macOS, Linux）
- Node.js >= 12.0.0 兼容

### Dependencies
- Node.js built-in modules only
- LibreOffice/OpenOffice required for ODG processing
- Python 3.x (usually comes with LibreOffice) 