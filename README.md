# ODG Processor

一个用于处理ODG（OpenDocument Graphics）文件的Node.js包，支持读取文件信息、修改文本内容并导出为PDF。

## 特性

- 🔍 **读取ODG文件信息** - 获取页面、形状、文本等详细信息
- ✏️ **批量修改文本** - 一次性修改多个形状的文本内容
- 📄 **自动导出PDF** - 修改后自动生成PDF文件
- 🚀 **异步操作** - 基于Promise的现代异步API
- 🔧 **灵活配置** - 支持自定义LibreOffice路径

## 安装

```bash
npm install odg-processor
```

## 前置要求

- Node.js >= 12.0.0
- LibreOffice 或 OpenOffice 已安装
- Python 3.x（通常随LibreOffice一起安装）

## 快速开始

### 基本使用

```javascript
const { getODGInfo, modifyODGTexts } = require('odg-processor');

// 获取ODG文件信息
async function getFileInfo() {
    const info = await getODGInfo('document.odg');
    if (info.success) {
        console.log('文件名:', info.data.file_name);
        console.log('页面数:', info.data.pages_count);
        
        // 显示所有形状
        info.data.pages_info.forEach(page => {
            page.shapes.forEach(shape => {
                console.log(`形状: ${shape.shape_name}, 文本: ${shape.text}`);
            });
        });
    }
}

// 批量修改文本
async function modifyTexts() {
    const result = await modifyODGTexts('template.odg', {
        'name': '张三',
        'salary': '8000元',
        'department': '技术部',
        'date': '2024-01-01'
    }, {
        outputPath: 'output.odg',
        exportPDF: true
    });
    
    if (result.success) {
        console.log(`成功修改 ${result.data.modified_count} 个形状`);
        console.log('PDF路径:', result.data.pdf_path);
    }
}
```

### 使用类实例

```javascript
const { ODGProcessor } = require('odg-processor');

const processor = new ODGProcessor({
    libreOfficePath: '/path/to/libreoffice/python'  // 可选：自定义路径
});

// 获取文件信息
const info = await processor.getODGInfo('document.odg');

// 修改单个文本
const result = await processor.modifyText('document.odg', 'name', '新名字');

// 批量修改
const batchResult = await processor.modifyTexts('document.odg', {
    'field1': 'value1',
    'field2': 'value2'
});
```

## API 文档

### 便捷函数

#### `getODGInfo(filePath, options)`

获取ODG文件的详细信息。

**参数:**
- `filePath` (string) - ODG文件路径
- `options` (object, 可选) - 配置选项
  - `libreOfficePath` (string) - LibreOffice Python路径

**返回:**
```javascript
{
    success: true,
    data: {
        file_name: 'document.odg',
        file_path: '/path/to/document.odg',
        pages_count: 1,
        pages_info: [{
            page_number: 1,
            shapes_count: 3,
            shapes: [{
                shape_name: 'name',
                shape_type: 'com.sun.star.drawing.TextShape',
                text: '原始文本',
                position: { x: 100, y: 200 },
                size: { width: 150, height: 50 }
            }]
        }],
        document_properties: {
            title: '文档标题',
            author: '作者'
        }
    }
}
```

#### `modifyODGTexts(filePath, shapeTextMap, options)`

批量修改ODG文件中的文本内容。

**参数:**
- `filePath` (string) - ODG文件路径
- `shapeTextMap` (object) - 形状名称到新文本的映射
- `options` (object, 可选) - 配置选项
  - `outputPath` (string) - 输出文件路径
  - `exportPDF` (boolean) - 是否导出PDF，默认true
  - `libreOfficePath` (string) - LibreOffice Python路径

**返回:**
```javascript
{
    success: true,
    data: {
        total_targets: 3,
        modified_count: 2,
        found_shapes: ['name', 'salary'],
        not_found_shapes: ['missing_shape'],
        error_shapes: [],
        pdf_path: '/path/to/output.pdf'
    }
}
```

#### `modifyODGText(filePath, shapeName, newText, options)`

修改单个形状的文本内容。

**参数:**
- `filePath` (string) - ODG文件路径  
- `shapeName` (string) - 形状名称
- `newText` (string) - 新文本内容
- `options` (object, 可选) - 同上

### ODGProcessor 类

#### 构造函数

```javascript
const processor = new ODGProcessor(options)
```

**选项:**
- `libreOfficePath` (string) - LibreOffice Python路径
- `pythonPath` (string) - Python路径（通常不需要设置）

#### 方法

- `getODGInfo(filePath)` - 获取文件信息
- `modifyTexts(filePath, shapeTextMap, outputPath, exportPDF)` - 批量修改文本
- `modifyText(filePath, shapeName, newText, outputPath, exportPDF)` - 修改单个文本
- `createODG(outputPath)` - 创建新的ODG文件
- `exportToPDF(filePath, outputPath)` - 导出为PDF

## 配置

### LibreOffice 路径

包会自动检测常见的LibreOffice安装路径：

- **Windows:** `C:\Program Files\LibreOffice\program\python.exe`
- **macOS:** `/Applications/LibreOffice.app/Contents/MacOS/python`
- **Linux:** `/usr/lib/libreoffice/program/python3`

如果自动检测失败，可以手动指定：

```javascript
const processor = new ODGProcessor({
    libreOfficePath: '/your/custom/path/to/libreoffice/python'
});
```

## 错误处理

所有方法都返回包含 `success` 字段的对象：

```javascript
const result = await modifyODGTexts('file.odg', {'name': 'value'});

if (result.success) {
    // 操作成功
    console.log('数据:', result.data);
} else {
    // 操作失败
    console.error('错误:', result.error);
    if (result.traceback) {
        console.error('详细错误:', result.traceback);
    }
}
```

## 示例

### 批量处理工资单

```javascript
const { modifyODGTexts } = require('odg-processor');

async function processPayroll(employeeData) {
    for (const employee of employeeData) {
        const result = await modifyODGTexts('payroll_template.odg', {
            'employee_name': employee.name,
            'employee_id': employee.id,
            'salary': employee.salary,
            'department': employee.department,
            'date': new Date().toISOString().split('T')[0]
        }, {
            outputPath: `payroll_${employee.id}.odg`,
            exportPDF: true
        });
        
        if (result.success) {
            console.log(`${employee.name} 的工资单已生成`);
        } else {
            console.error(`生成 ${employee.name} 工资单失败:`, result.error);
        }
    }
}

// 使用示例
processPayroll([
    { name: '张三', id: '001', salary: '8000', department: '技术部' },
    { name: '李四', id: '002', salary: '7500', department: '销售部' }
]);
```

## 许可证

MIT

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### 1.0.0
- 初始版本
- 支持ODG文件信息读取
- 支持批量文本修改
- 支持PDF导出 