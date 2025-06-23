#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODG处理桥接脚本 - 用于Node.js调用
"""

import sys
import json
import os
import traceback

# 导入我们的ODG处理器
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from odg_operations import ODGProcessor

def get_odg_info(file_path):
    """获取ODG文件信息"""
    try:
        processor = ODGProcessor()
        info = processor.get_odg_info(file_path)
        return {"success": True, "data": info}
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}

def modify_texts(file_path, shape_text_map, output_path=None, export_pdf=True):
    """批量修改文本"""
    try:
        processor = ODGProcessor()
        
        # 解析参数
        if isinstance(shape_text_map, str):
            shape_text_map = json.loads(shape_text_map)
        
        if isinstance(export_pdf, str):
            export_pdf = export_pdf.lower() == 'true'
        
        output_path = output_path if output_path and output_path.strip() else None
        
        result = processor.modify_text_by_shape_names(
            file_path=file_path,
            shape_text_map=shape_text_map,
            output_path=output_path,
            export_pdf=export_pdf
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}

def create_odg(output_path):
    """创建新的ODG文件"""
    try:
        processor = ODGProcessor()
        success = processor.create_new_odg(output_path)
        return {"success": success, "message": f"ODG文件已创建: {output_path}" if success else "创建失败"}
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}

def export_pdf(file_path, output_path):
    """导出为PDF"""
    try:
        processor = ODGProcessor()
        if processor.open_odg(file_path):
            success = processor.export_to_pdf(output_path)
            processor.close_document()
            return {"success": success, "message": f"PDF已导出: {output_path}" if success else "导出失败"}
        else:
            return {"success": False, "error": "无法打开ODG文件"}
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}

def main():
    """主函数 - 处理命令行参数"""
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "缺少命令参数"}))
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        if command == "get_info":
            if len(args) < 1:
                result = {"success": False, "error": "缺少文件路径参数"}
            else:
                result = get_odg_info(args[0])
                
        elif command == "modify_texts":
            if len(args) < 2:
                result = {"success": False, "error": "参数不足"}
            else:
                file_path = args[0]
                shape_text_map = args[1]
                output_path = args[2] if len(args) > 2 else None
                export_pdf = args[3] if len(args) > 3 else True
                result = modify_texts(file_path, shape_text_map, output_path, export_pdf)
                
        elif command == "create_odg":
            if len(args) < 1:
                result = {"success": False, "error": "缺少输出路径参数"}
            else:
                result = create_odg(args[0])
                
        elif command == "export_pdf":
            if len(args) < 2:
                result = {"success": False, "error": "参数不足"}
            else:
                result = export_pdf(args[0], args[1])
                
        else:
            result = {"success": False, "error": f"未知命令: {command}"}
            
    except Exception as e:
        result = {"success": False, "error": str(e), "traceback": traceback.format_exc()}
    
    # 输出JSON结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 