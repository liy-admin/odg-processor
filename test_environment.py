#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreOffice/OpenOffice API 环境测试脚本
用于验证UNO模块和LibreOffice连接是否正常
"""

import os
import sys

def test_uno_import():
    """测试UNO模块导入"""
    print("1. 测试UNO模块导入...")
    try:
        import uno
        print("   ✅ UNO模块导入成功")
        return True
    except ImportError as e:
        print(f"   ❌ UNO模块导入失败: {e}")
        print("   请安装UNO模块或从LibreOffice安装目录复制uno.py")
        return False

def test_libreoffice_path():
    """测试LibreOffice安装路径"""
    print("2. 测试LibreOffice安装路径...")
    
    possible_paths = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/usr/bin/libreoffice",
        "/usr/bin/soffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"   ✅ 找到LibreOffice: {path}")
            return path
    
    print("   ❌ 未找到LibreOffice安装路径")
    print("   请确保LibreOffice已正确安装")
    return None

def test_libreoffice_connection():
    """测试LibreOffice连接"""
    print("3. 测试LibreOffice连接...")
    
    try:
        import uno
        local_context = uno.getComponentContext()
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context)
        context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
        print("   ✅ LibreOffice连接成功")
        return True
    except Exception as e:
        print(f"   ❌ LibreOffice连接失败: {e}")
        print("   请确保LibreOffice服务器模式已启动:")
        print("   Windows: \"C:\\Program Files\\LibreOffice\\program\\soffice.exe\" --headless --accept=socket,host=localhost,port=2002;urp;")
        print("   Linux/macOS: libreoffice --headless --accept=socket,host=localhost,port=2002;urp;")
        return False

def test_basic_operations():
    """测试基本操作"""
    print("4. 测试基本操作...")
    
    try:
        import uno
        from com.sun.star.beans import PropertyValue
        
        # 连接到LibreOffice
        local_context = uno.getComponentContext()
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context)
        context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
        
        # 创建测试文档
        url = uno.systemPathToFileUrl(os.path.abspath("test.odg"))
        properties = (
            PropertyValue("Hidden", 0, True, 0),
            PropertyValue("ReadOnly", 0, False, 0),
        )
        
        document = desktop.loadComponentFromURL(
            "private:factory/sdraw", "_blank", 0, properties)
        
        # 保存文档
        document.storeAsUrl(url, ())
        
        # 关闭文档
        document.close(True)
        
        # 删除测试文件
        if os.path.exists("test.odg"):
            os.remove("test.odg")
        
        print("   ✅ 基本操作测试成功")
        return True
        
    except Exception as e:
        print(f"   ❌ 基本操作测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== LibreOffice/OpenOffice API 环境测试 ===\n")
    
    tests = [
        test_uno_import,
        test_libreoffice_path,
        test_libreoffice_connection,
        test_basic_operations
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # 总结
    print("=== 测试结果总结 ===")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ 所有测试通过 ({passed}/{total})")
        print("环境配置正确，可以运行ODG操作脚本")
    else:
        print(f"❌ 部分测试失败 ({passed}/{total})")
        print("请根据上述错误信息修复环境配置")
    
    print("\n=== 下一步操作 ===")
    if passed == total:
        print("1. 运行基础示例: python odg_operations.py")
        print("2. 运行高级示例: python odg_advanced_examples.py")
    else:
        print("1. 安装LibreOffice")
        print("2. 安装Python UNO模块")
        print("3. 启动LibreOffice服务器模式")
        print("4. 重新运行此测试脚本")

if __name__ == "__main__":
    main() 