# ODG操作测试套件

这个目录包含了用于测试ODG（OpenDocument Graphics）文件操作功能的测试脚本。

## 测试文件

- `test_odg_operations.py` - Python版本的测试套件
- `test_odg_operations.js` - Node.js版本的测试套件

## 运行测试

### Python测试

```bash
# 运行Python测试
python tests/test_odg_operations.py

# 或者从项目根目录运行
cd /path/to/nodejs_test
python tests/test_odg_operations.py
```

### Node.js测试

```bash
# 运行Node.js测试
node tests/test_odg_operations.js

# 或者从项目根目录运行
cd /path/to/nodejs_test
node tests/test_odg_operations.js
```

## 测试内容

### 环境测试
- UNO模块导入检查
- LibreOffice安装路径检测
- LibreOffice服务连接测试

### 基本功能测试
- ODG文件信息读取
- 文档创建和基本操作

### 高级功能测试
- 文本内容修改
- PDF导出功能
- 完整工作流（修改+导出）

## 测试输出

测试完成后会生成：
- 控制台输出显示测试结果
- `tests/test_report.json` - 详细的JSON格式测试报告

## 前置条件

1. **LibreOffice安装**
   - 确保系统已安装LibreOffice
   - Windows: 通常安装在 `C:\Program Files\LibreOffice\`
   - Linux: 通常可通过包管理器安装
   - macOS: 通常安装在 `/Applications/LibreOffice.app/`

2. **Python环境**
   - Python 3.x
   - UNO模块（通常随LibreOffice安装）

3. **Node.js环境**（用于Node.js测试）
   - Node.js 12.x 或更高版本

## 故障排除

### 常见问题

1. **UNO模块导入失败**
   ```
   ImportError: No module named 'uno'
   ```
   解决方案：
   - 确保LibreOffice已正确安装
   - 在某些系统上，可能需要将LibreOffice的Python路径添加到环境变量

2. **LibreOffice连接失败**
   ```
   LibreOffice连接失败
   ```
   解决方案：
   - 启动LibreOffice服务器模式：
     ```bash
     # Windows
     "C:\Program Files\LibreOffice\program\soffice.exe" --headless --accept=socket,host=localhost,port=2002;urp;
     
     # Linux/macOS
     libreoffice --headless --accept=socket,host=localhost,port=2002;urp;
     ```

3. **PDF导出失败**
   - 检查输出目录权限
   - 确保LibreOffice版本支持PDF导出
   - 检查磁盘空间

4. **找不到测试ODG文件**
   - 测试会自动创建临时ODG文件
   - 如果有现有的ODG文件（如payroll.odg），测试会优先使用

## 测试文件清理

测试过程中会在 `tests/` 目录下创建临时文件：
- `*.odg` - 测试用的ODG文件
- `*.pdf` - 导出的PDF文件
- `test_report.json` - 测试报告

这些文件已被添加到 `.gitignore` 中，不会被提交到版本控制。

## 开发者说明

如果需要添加新的测试用例：

1. 在对应的测试类中添加新的测试方法
2. 方法名以 `test_` 开头
3. 使用 `self.log_test()` 记录测试结果
4. 在 `run_all_tests()` 方法中添加新测试到测试列表

## 自动化CI/CD

这些测试脚本可以集成到CI/CD管道中：

```yaml
# 示例GitHub Actions配置
- name: Install LibreOffice
  run: sudo apt-get install libreoffice

- name: Run Python tests
  run: python tests/test_odg_operations.py

- name: Run Node.js tests  
  run: node tests/test_odg_operations.js
``` 