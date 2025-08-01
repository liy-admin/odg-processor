#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreOffice/OpenOffice API (Python-UNO Bridge) 操作ODG文件
ODG (OpenDocument Graphics) 文件操作示例
"""

import os
import sys
import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.connection import NoConnectException

class ODGProcessor:
    """ODG文件处理器类"""
    
    def __init__(self, libreoffice_path=None):
        """
        初始化ODG处理器
        
        Args:
            libreoffice_path: LibreOffice安装路径，如果为None则使用系统默认路径
        """
        self.libreoffice_path = libreoffice_path
        self.desktop = None
        self.document = None
        
    def connect_to_libreoffice(self):
        """连接到LibreOffice"""
        try:
            # 尝试连接到已运行的LibreOffice实例
            local_context = uno.getComponentContext()
            resolver = local_context.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", local_context)
            context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            self.desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
            print("已连接到运行中的LibreOffice实例")
            return True
        except Exception as e:
            print(f"无法连接到运行中的LibreOffice实例: {e}")
            return False
    
    def start_libreoffice_server(self):
        """启动LibreOffice服务器模式"""
        if self.libreoffice_path is None:
            # 尝试常见的LibreOffice安装路径
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                "/usr/bin/libreoffice",
                "/usr/bin/soffice",
                "/Applications/LibreOffice.app/Contents/MacOS/soffice"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.libreoffice_path = path
                    break
        
        if self.libreoffice_path and os.path.exists(self.libreoffice_path):
            import subprocess
            try:
                # 启动LibreOffice服务器模式
                cmd = [self.libreoffice_path, "--headless", "--accept=socket,host=localhost,port=2002;urp;"]
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("已启动LibreOffice服务器模式")
                import time
                time.sleep(3)  # 等待服务器启动
                return self.connect_to_libreoffice()
            except Exception as e:
                print(f"启动LibreOffice服务器失败: {e}")
                return False
        else:
            print("未找到LibreOffice安装路径，请手动指定")
            return False
    
    def create_new_odg(self, output_path):
        """
        创建新的ODG文件
        
        Args:
            output_path: 输出文件路径
        """
        try:
            if not self.desktop:
                if not self.start_libreoffice_server():
                    return False
            
            # 创建新的绘图文档
            url = uno.systemPathToFileUrl(os.path.abspath(output_path))
            properties = (
                PropertyValue("Hidden", 0, True, 0),
                PropertyValue("ReadOnly", 0, False, 0),
            )
            
            self.document = self.desktop.loadComponentFromURL(
                "private:factory/sdraw", "_blank", 0, properties)
            
            # 保存文档
            self.document.storeAsUrl(url, ())
            print(f"已创建新的ODG文件: {output_path}")
            return True
            
        except Exception as e:
            print(f"创建ODG文件失败: {e}")
            return False
    
    def open_odg(self, file_path):
        """
        打开现有的ODG文件
        
        Args:
            file_path: ODG文件路径
        """
        try:
            if not self.desktop:
                if not self.start_libreoffice_server():
                    return False
            
            url = uno.systemPathToFileUrl(os.path.abspath(file_path))
            properties = (
                PropertyValue("Hidden", 0, False, 0),
                PropertyValue("ReadOnly", 0, False, 0),
            )
            
            self.document = self.desktop.loadComponentFromURL(url, "_blank", 0, properties)
            print(f"已打开ODG文件: {file_path}")
            return True
            
        except Exception as e:
            print(f"打开ODG文件失败: {e}")
            return False
    
    def add_shape(self, shape_type="Rectangle", x=100, y=100, width=200, height=100):
        """
        添加形状到绘图页面
        
        Args:
            shape_type: 形状类型 (Rectangle, Ellipse, Line, Text, etc.)
            x, y: 位置坐标
            width, height: 尺寸
        """
        try:
            if not self.document:
                print("没有打开的文档")
                return False
            
            # 获取绘图页面
            pages = self.document.getDrawPages()
            page = pages.getByIndex(0)
            
            # 创建形状
            shape = self.document.createInstance(f"com.sun.star.drawing.{shape_type}Shape")
            
            # 设置形状属性
            shape.setPosition(uno.createUnoStruct("com.sun.star.awt.Point", x, y))
            shape.setSize(uno.createUnoStruct("com.sun.star.awt.Size", width, height))
            
            # 添加到页面
            page.add(shape)
            print(f"已添加 {shape_type} 形状")
            return True
            
        except Exception as e:
            print(f"添加形状失败: {e}")
            return False
    
    def add_text(self, text="示例文本", x=100, y=100, width=200, height=50):
        """
        添加文本到绘图页面
        
        Args:
            text: 文本内容
            x, y: 位置坐标
            width, height: 文本框尺寸
        """
        try:
            if not self.document:
                print("没有打开的文档")
                return False
            
            # 获取绘图页面
            pages = self.document.getDrawPages()
            page = pages.getByIndex(0)
            
            # 创建文本形状
            text_shape = self.document.createInstance("com.sun.star.drawing.TextShape")
            
            # 设置位置和尺寸
            text_shape.setPosition(uno.createUnoStruct("com.sun.star.awt.Point", x, y))
            text_shape.setSize(uno.createUnoStruct("com.sun.star.awt.Size", width, height))
            
            # 设置文本内容
            text_shape.setString(text)
            
            # 添加到页面
            page.add(text_shape)
            print(f"已添加文本: {text}")
            return True
            
        except Exception as e:
            print(f"添加文本失败: {e}")
            return False
    
    def save_document(self, output_path=None):
        """
        保存文档
        
        Args:
            output_path: 保存路径，如果为None则保存到原文件
        """
        try:
            if not self.document:
                print("没有打开的文档")
                return False
            
            if output_path:
                url = uno.systemPathToFileUrl(os.path.abspath(output_path))
                self.document.storeAsUrl(url, ())
                print(f"文档已保存到: {output_path}")
            else:
                self.document.store()
                print("文档已保存")
            
            return True
            
        except Exception as e:
            print(f"保存文档失败: {e}")
            return False
    
    def close_document(self):
        """关闭文档"""
        try:
            if self.document:
                self.document.close(True)
                self.document = None
                print("文档已关闭")
            return True
        except Exception as e:
            print(f"关闭文档失败: {e}")
            return False
    
    def export_to_pdf(self, output_path):
        """
        导出当前文档为PDF
        
        Args:
            output_path: PDF输出路径
            
        Returns:
            bool: 是否成功导出
        """
        try:
            if not self.document:
                print("没有打开的文档")
                return False
            
            # 确保输出目录存在
            output_dir = os.path.dirname(os.path.abspath(output_path))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            url = uno.systemPathToFileUrl(os.path.abspath(output_path))
            print(f"导出为PDF: {url}")
            
            # 方法1：使用标准的PDF导出过滤器 (最兼容的方法)
            try:
                filter_data = (
                    PropertyValue("FilterName", 0, "draw_pdf_Export", 0),
                    PropertyValue("Overwrite", 0, True, 0),
                    PropertyValue("Quality", 0, 90, 0),  # 添加质量设置
                )
                self.document.storeToURL(url, filter_data)
                
                # 验证文件是否真的被创建
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    print(f"已导出为PDF: {output_path} (大小: {os.path.getsize(output_path)} 字节)")
                    return True
                else:
                    print(f"PDF文件创建失败或为空: {output_path}")
                    
            except Exception as e1:
                print(f"方法1失败: {e1}")
                
                # 方法2：使用exportAsPDF方法
                try:
                    if hasattr(self.document, 'exportAsPDF'):
                        pdf_properties = (
                            PropertyValue("URL", 0, url, 0),
                            PropertyValue("FilterName", 0, "draw_pdf_Export", 0),  # 使用draw而不是writer
                            PropertyValue("Quality", 0, 90, 0),
                        )
                        self.document.exportAsPDF(pdf_properties)
                        
                        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                            print(f"已导出为PDF (方法2): {output_path} (大小: {os.path.getsize(output_path)} 字节)")
                            return True
                        else:
                            print(f"方法2: PDF文件创建失败或为空: {output_path}")
                            
                except Exception as e2:
                    print(f"方法2失败: {e2}")
                    
                    # 方法3：使用另一种过滤器名称
                    try:
                        export_filter = (
                            PropertyValue("FilterName", 0, "impress_pdf_Export", 0),  # 尝试使用impress过滤器
                            PropertyValue("Overwrite", 0, True, 0),
                            PropertyValue("Quality", 0, 90, 0),
                        )
                        self.document.storeToURL(url, export_filter)
                        
                        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                            print(f"已导出为PDF (方法3): {output_path} (大小: {os.path.getsize(output_path)} 字节)")
                            return True
                        else:
                            print(f"方法3: PDF文件创建失败或为空: {output_path}")
                            
                    except Exception as e3:
                        print(f"方法3失败: {e3}")
                        
                        # 方法4：最基本的导出方法
                        try:
                            basic_filter = (
                                PropertyValue("FilterName", 0, "PDF - Portable Document Format", 0),
                                PropertyValue("Overwrite", 0, True, 0),
                            )
                            self.document.storeToURL(url, basic_filter)
                            
                            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                                print(f"已导出为PDF (方法4): {output_path} (大小: {os.path.getsize(output_path)} 字节)")
                                return True
                            else:
                                print(f"方法4: PDF文件创建失败或为空: {output_path}")
                                
                        except Exception as e4:
                            print(f"方法4失败: {e4}")
                            print("所有PDF导出方法都失败了")
                            return False
            
        except Exception as e:
            print(f"导出PDF失败: {e}")
            print(f"错误类型: {type(e)}")
            import traceback
            traceback.print_exc()
            return False

    def get_odg_info(self, file_path):
        """
        获取ODG文件信息
        
        Args:
            file_path: ODG文件路径
            
        Returns:
            dict: 包含文件信息的字典
        """
        try:
            if not self.desktop:
                if not self.start_libreoffice_server():
                    return None
            
            url = uno.systemPathToFileUrl(os.path.abspath(file_path))
            properties = (
                PropertyValue("Hidden", 0, True, 0),  # 隐藏打开
                PropertyValue("ReadOnly", 0, True, 0),  # 只读模式
            )
            
            self.document = self.desktop.loadComponentFromURL(url, "_blank", 0, properties)
            
            # 获取文档信息
            info = {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'pages_count': 0,
                'pages_info': [],
                'document_properties': {}
            }
            
            # 获取页面信息
            pages = self.document.getDrawPages()
            info['pages_count'] = pages.getCount()
            
            # 遍历每个页面获取详细信息
            for i in range(pages.getCount()):
                page = pages.getByIndex(i)
                page_info = {
                    'page_number': i + 1,
                    'shapes_count': page.getCount(),
                    'shapes': []
                }
                
                # 获取页面中的所有形状
                for j in range(page.getCount()):
                    shape = page.getByIndex(j)
                    shape_info = {
                        'shape_index': j,
                        'shape_type': shape.getShapeType(),
                        'shape_name': '',
                        'position': {
                            'x': shape.getPosition().X,
                            'y': shape.getPosition().Y
                        },
                        'size': {
                            'width': shape.getSize().Width,
                            'height': shape.getSize().Height
                        }
                    }
                    
                    # 获取形状名称
                    try:
                        if hasattr(shape, 'Name'):
                            shape_info['shape_name'] = shape.Name
                        elif hasattr(shape, 'getString') and shape.getString():
                            # 对于文本形状，如果没有名称，可以用文本内容作为标识
                            shape_info['shape_name'] = f"Text: {shape.getString()[:20]}..."
                    except:
                        shape_info['shape_name'] = f"Shape_{j+1}"
                    
                    # 如果是文本形状，获取文本内容
                    try:
                        if hasattr(shape, 'getString'):
                            shape_info['text'] = shape.getString()
                        elif hasattr(shape, 'Text'):
                            shape_info['text'] = shape.Text.getString()
                    except:
                        pass
                    
                    page_info['shapes'].append(shape_info)
                
                info['pages_info'].append(page_info)
            
            # 获取文档属性
            try:
                doc_props = self.document.getDocumentProperties()
                info['document_properties'] = {
                    'title': doc_props.Title,
                    'subject': doc_props.Subject,
                    'author': doc_props.Author,
                    'creation_date': str(doc_props.CreationDate),
                    'modification_date': str(doc_props.ModificationDate)
                }
            except:
                pass
            
            # 关闭文档
            self.document.close(True)
            self.document = None
            
            return info
            
        except Exception as e:
            print(f"获取ODG文件信息失败: {e}")
            return None

    def modify_text_by_shape_names(self, file_path, shape_text_map, output_path=None, export_pdf=True):
        """
        根据形状名称批量修改文本内容
        
        Args:
            file_path: ODG文件路径
            shape_text_map: 字典，键为形状名称，值为新的文本内容
                          例如: {"name1": "新文本1", "name2": "新文本2"}
            output_path: 输出文件路径，如果为None则覆盖原文件
            export_pdf: 是否自动导出为PDF，默认为True
            
        Returns:
            dict: 修改结果，包含成功和失败的统计
        """
        try:
            if not self.desktop:
                if not self.start_libreoffice_server():
                    return {"success": False, "error": "无法启动LibreOffice服务器"}
            
            url = uno.systemPathToFileUrl(os.path.abspath(file_path))
            properties = (
                PropertyValue("Hidden", 0, True, 0),  # 隐藏打开
                PropertyValue("ReadOnly", 0, False, 0),  # 可编辑模式
            )
            
            self.document = self.desktop.loadComponentFromURL(url, "_blank", 0, properties)
            
            # 统计信息
            result = {
                "success": True,
                "total_targets": len(shape_text_map),
                "modified_count": 0,
                "found_shapes": [],
                "not_found_shapes": [],
                "error_shapes": []
            }
            
            # 记录已找到的形状，避免重复修改
            found_shapes = set()
            
            # 遍历所有页面
            pages = self.document.getDrawPages()
            for i in range(pages.getCount()):
                page = pages.getByIndex(i)
                
                # 遍历页面中的所有形状
                for j in range(page.getCount()):
                    shape = page.getByIndex(j)
                    
                    # 获取形状名称
                    shape_name = ""
                    try:
                        if hasattr(shape, 'Name'):
                            shape_name = shape.Name
                    except:
                        continue
                    
                    # 检查是否是目标形状
                    if shape_name in shape_text_map and shape_name not in found_shapes:
                        new_text = shape_text_map[shape_name]
                        try:
                            # 尝试修改文本内容
                            if hasattr(shape, 'setString'):
                                shape.setString(new_text)
                                result["modified_count"] += 1
                                result["found_shapes"].append(shape_name)
                                found_shapes.add(shape_name)
                                print(f"已修改形状 '{shape_name}' 的文本内容为: {new_text}")
                            elif hasattr(shape, 'Text'):
                                shape.Text.setString(new_text)
                                result["modified_count"] += 1
                                result["found_shapes"].append(shape_name)
                                found_shapes.add(shape_name)
                                print(f"已修改形状 '{shape_name}' 的文本内容为: {new_text}")
                            else:
                                result["error_shapes"].append({
                                    "name": shape_name,
                                    "error": "不是文本形状，无法修改文本内容"
                                })
                                print(f"形状 '{shape_name}' 不是文本形状，无法修改文本内容")
                        except Exception as e:
                            result["error_shapes"].append({
                                "name": shape_name,
                                "error": str(e)
                            })
                            print(f"修改形状 '{shape_name}' 文本失败: {e}")
            
            # 找出未找到的形状
            for target_name in shape_text_map:
                if target_name not in found_shapes:
                    result["not_found_shapes"].append(target_name)
            
            if result["modified_count"] > 0:
                # 保存文档
                try:
                    if output_path:
                        save_url = uno.systemPathToFileUrl(os.path.abspath(output_path))
                        self.document.storeAsUrl(save_url, ())
                        print(f"已保存修改后的ODG文件到: {output_path}")
                        
                        # 导出为PDF
                        if export_pdf:
                            pdf_path = output_path.replace('.odg', '.pdf')
                            print(f"尝试导出PDF到: {pdf_path}")
                            if self.export_to_pdf(pdf_path):
                                result["pdf_path"] = pdf_path
                                print(f"PDF导出成功: {pdf_path}")
                            else:
                                print(f"PDF导出失败: {pdf_path}")
                                result["pdf_export_error"] = "PDF导出失败"
                    else:
                        self.document.store()
                        print("已保存修改到原文件")
                    
                        # 导出为PDF（使用原文件名）
                        if export_pdf:
                            pdf_path = file_path.replace('.odg', '.pdf')
                            print(f"尝试导出PDF到: {pdf_path}")
                            if self.export_to_pdf(pdf_path):
                                result["pdf_path"] = pdf_path
                                print(f"PDF导出成功: {pdf_path}")
                            else:
                                print(f"PDF导出失败: {pdf_path}")
                                result["pdf_export_error"] = "PDF导出失败"
                    
                    print(f"总共修改了 {result['modified_count']} 个形状")
                    
                except Exception as save_error:
                    print(f"保存文档时发生错误: {save_error}")
                    result["save_error"] = str(save_error)
                    # 即使保存失败，也尝试导出PDF
                    if export_pdf:
                        pdf_path = (output_path or file_path).replace('.odg', '.pdf')
                        print(f"尝试直接导出PDF到: {pdf_path}")
                        if self.export_to_pdf(pdf_path):
                            result["pdf_path"] = pdf_path
                            print(f"PDF导出成功: {pdf_path}")
                        else:
                            print(f"PDF导出失败: {pdf_path}")
                            result["pdf_export_error"] = "PDF导出失败"
            else:
                print("没有修改任何形状，跳过保存和PDF导出")
            
            if result["not_found_shapes"]:
                print(f"未找到的形状: {', '.join(result['not_found_shapes'])}")
            
            # 关闭文档
            self.document.close(True)
            self.document = None
            
            return result
            
        except Exception as e:
            print(f"批量修改文本失败: {e.args}")
            return {"success": False, "error": str(e)}

def main():
    """主函数 - 演示ODG操作"""
    print("=== LibreOffice/OpenOffice API ODG文件信息读取 ===\n")
    
    # 调试信息
    print(f"当前工作目录: {os.getcwd()}")
    
    # 创建ODG处理器
    processor = ODGProcessor()
    
    # 获取ODG文件信息
    odg_file = 'payroll.odg'
    print(f"目标文件: {odg_file}")
    print(f"文件绝对路径: {os.path.abspath(odg_file)}")
    print(f"文件是否存在: {os.path.exists(odg_file)}")
    
    if os.path.exists(odg_file):
        print(f"正在读取ODG文件信息: {odg_file}")
        info = processor.get_odg_info(odg_file)
        
        if info:
            print("\n=== 文件信息 ===")
            print(f"文件名: {info['file_name']}")
            print(f"文件路径: {info['file_path']}")
            print(f"页面数量: {info['pages_count']}")
            
            # 显示文档属性
            if info['document_properties']:
                print("\n=== 文档属性 ===")
                for key, value in info['document_properties'].items():
                    if value:
                        print(f"{key}: {value}")
            # 示例：批量修改指定名称形状的文本内容
            print("\n=== 批量文本修改示例 ===")
            shape_text_map = {
                "name": "我的名字"
            }
            
            # 显示每个页面的信息
            for page_info in info['pages_info']:
                print(f"\n=== 页面 {page_info['page_number']} ===")
                print(f"形状数量: {page_info['shapes_count']}")
                
                for shape in page_info['shapes']:
                    if shape['shape_name'] not in shape_text_map:
                        continue
                    # print(f"\n  形状 {shape['shape_index'] + 1}:")
                    print(f"    名称: {shape['shape_name']}")
                    print(f"    类型: {shape['shape_type']}")
                    # print(f"    位置: ({shape['position']['x']}, {shape['position']['y']})")
                    # print(f"    尺寸: {shape['size']['width']} x {shape['size']['height']}")
                    if 'text' in shape and shape['text']:
                        print(f"    文本内容: {shape['text']}")
            
            print("尝试批量修改以下形状的文本:")
            for shape_name, new_text in shape_text_map.items():
                print(f"  - '{shape_name}' -> '{new_text}'")
            
            result = processor.modify_text_by_shape_names(
                file_path=odg_file,
                shape_text_map=shape_text_map,
                output_path=None  # 先尝试覆盖原文件，避免路径问题
            )
            
            if result["success"]:
                print(f"\n批量修改完成！")
                print(f"目标形状数量: {result['total_targets']}")
                print(f"成功修改: {result['modified_count']}")
                if result["found_shapes"]:
                    print(f"成功修改的形状: {', '.join(result['found_shapes'])}")
                if result["not_found_shapes"]:
                    print(f"未找到的形状: {', '.join(result['not_found_shapes'])}")
                if result["error_shapes"]:
                    print("修改失败的形状:")
                    for error_info in result["error_shapes"]:
                        print(f"  - {error_info['name']}: {error_info['error']}")
                if "pdf_path" in result:
                    print(f"已自动导出PDF文件: {result['pdf_path']}")
            else:
                print(f"批量修改失败: {result.get('error', '未知错误')}")
            
            # 返回信息字典供进一步处理
            return info
        else:
            print("无法读取文件信息")
            return None
    else:
        print(f"文件不存在: {odg_file}")
        return None

# 添加便捷函数，方便直接调用
def modify_odg_texts(file_path, shape_text_map, output_path=None, export_pdf=True):
    """
    便捷函数：批量修改ODG文件中多个形状的文本内容并导出PDF
    
    Args:
        file_path: ODG文件路径
        shape_text_map: 字典，键为形状名称，值为新文本内容
                       例如: {"name": "张三", "salary": "8000", "department": "技术部"}
        output_path: 输出文件路径（可选）
        export_pdf: 是否自动导出为PDF，默认为True
        
    Returns:
        dict: 修改结果统计，包含pdf_path字段（如果成功导出PDF）
    """
    processor = ODGProcessor()
    return processor.modify_text_by_shape_names(file_path, shape_text_map, output_path, export_pdf)

def modify_odg_text(file_path, shape_name, new_text, output_path=None, export_pdf=True):
    """
    便捷函数：修改ODG文件中单个形状的文本内容并导出PDF
    
    Args:
        file_path: ODG文件路径
        shape_name: 形状名称 
        new_text: 新文本内容
        output_path: 输出文件路径（可选）
        export_pdf: 是否自动导出为PDF，默认为True
        
    Returns:
        dict: 修改结果统计，包含pdf_path字段（如果成功导出PDF）
    """
    return modify_odg_texts(file_path, {shape_name: new_text}, output_path, export_pdf)

if __name__ == "__main__":
    main() 