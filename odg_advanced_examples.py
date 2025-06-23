#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreOffice/OpenOffice API 高级ODG操作示例
展示更多ODG文件操作功能
"""

import os
import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.awt import Point, Size
from com.sun.star.drawing import LineStyle
from com.sun.star.drawing import FillStyle
from com.sun.star.drawing import TextAdjust
from com.sun.star.drawing import TextVerticalAdjust
from com.sun.star.drawing import TextHorizontalAdjust

class AdvancedODGProcessor:
    """高级ODG处理器类"""
    
    def __init__(self, libreoffice_path=None):
        self.libreoffice_path = libreoffice_path
        self.desktop = None
        self.document = None
        
    def connect_to_libreoffice(self):
        """连接到LibreOffice"""
        try:
            local_context = uno.getComponentContext()
            resolver = local_context.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", local_context)
            context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            self.desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
            print("已连接到LibreOffice")
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    def start_libreoffice_server(self):
        """启动LibreOffice服务器"""
        if self.libreoffice_path is None:
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                "/usr/bin/libreoffice",
                "/usr/bin/soffice"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.libreoffice_path = path
                    break
        
        if self.libreoffice_path and os.path.exists(self.libreoffice_path):
            import subprocess
            try:
                cmd = [self.libreoffice_path, "--headless", "--accept=socket,host=localhost,port=2002;urp;"]
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("已启动LibreOffice服务器")
                import time
                time.sleep(3)
                return self.connect_to_libreoffice()
            except Exception as e:
                print(f"启动失败: {e}")
                return False
        else:
            print("未找到LibreOffice")
            return False
    
    def create_new_odg(self, output_path):
        """创建新的ODG文件"""
        try:
            if not self.desktop:
                if not self.start_libreoffice_server():
                    return False
            
            url = uno.systemPathToFileUrl(os.path.abspath(output_path))
            properties = (
                PropertyValue("Hidden", 0, True, 0),
                PropertyValue("ReadOnly", 0, False, 0),
            )
            
            self.document = self.desktop.loadComponentFromURL(
                "private:factory/sdraw", "_blank", 0, properties)
            
            self.document.storeAsUrl(url, ())
            print(f"已创建ODG文件: {output_path}")
            return True
            
        except Exception as e:
            print(f"创建失败: {e}")
            return False
    
    def get_current_page(self):
        """获取当前页面"""
        if not self.document:
            return None
        pages = self.document.getDrawPages()
        return pages.getByIndex(0)
    
    def add_rectangle_with_style(self, x=100, y=100, width=150, height=100, 
                                fill_color=0xFFFF00, line_color=0x0000FF, line_width=2):
        """添加带样式的矩形"""
        try:
            page = self.get_current_page()
            if not page:
                return False
            
            shape = self.document.createInstance("com.sun.star.drawing.RectangleShape")
            
            # 设置位置和尺寸
            shape.setPosition(Point(x, y))
            shape.setSize(Size(width, height))
            
            # 设置填充样式
            shape.setFillStyle(FillStyle.SOLID)
            shape.setFillColor(fill_color)
            
            # 设置线条样式
            shape.setLineStyle(LineStyle.SOLID)
            shape.setLineColor(line_color)
            shape.setLineWidth(line_width)
            
            page.add(shape)
            print(f"已添加样式矩形: ({x}, {y})")
            return True
            
        except Exception as e:
            print(f"添加矩形失败: {e}")
            return False
    
    def add_ellipse_with_gradient(self, x=300, y=100, width=150, height=100):
        """添加带渐变的椭圆"""
        try:
            page = self.get_current_page()
            if not page:
                return False
            
            shape = self.document.createInstance("com.sun.star.drawing.EllipseShape")
            
            # 设置位置和尺寸
            shape.setPosition(Point(x, y))
            shape.setSize(Size(width, height))
            
            # 设置渐变填充
            shape.setFillStyle(FillStyle.GRADIENT)
            
            # 创建渐变
            gradient = self.document.createInstance("com.sun.star.drawing.GradientTable").getByName("Blue")
            shape.setFillGradient(gradient)
            
            page.add(shape)
            print(f"已添加渐变椭圆: ({x}, {y})")
            return True
            
        except Exception as e:
            print(f"添加椭圆失败: {e}")
            return False
    
    def add_line(self, x1=100, y1=300, x2=400, y2=300, line_color=0xFF0000, line_width=3):
        """添加线条"""
        try:
            page = self.get_current_page()
            if not page:
                return False
            
            shape = self.document.createInstance("com.sun.star.drawing.LineShape")
            
            # 设置线条起点和终点
            shape.setStartPosition(Point(x1, y1))
            shape.setEndPosition(Point(x2, y2))
            
            # 设置线条样式
            shape.setLineStyle(LineStyle.SOLID)
            shape.setLineColor(line_color)
            shape.setLineWidth(line_width)
            
            page.add(shape)
            print(f"已添加线条: ({x1},{y1}) -> ({x2},{y2})")
            return True
            
        except Exception as e:
            print(f"添加线条失败: {e}")
            return False
    
    def add_text_with_formatting(self, text="格式化文本", x=100, y=400, width=300, height=50,
                                font_size=16, font_color=0x000000, bold=False):
        """添加带格式的文本"""
        try:
            page = self.get_current_page()
            if not page:
                return False
            
            text_shape = self.document.createInstance("com.sun.star.drawing.TextShape")
            
            # 设置位置和尺寸
            text_shape.setPosition(Point(x, y))
            text_shape.setSize(Size(width, height))
            
            # 设置文本内容
            text_shape.setString(text)
            
            # 设置文本对齐
            text_shape.setTextAdjust(TextAdjust.BLOCK)
            text_shape.setTextVerticalAdjust(TextVerticalAdjust.CENTER)
            text_shape.setTextHorizontalAdjust(TextHorizontalAdjust.CENTER)
            
            # 设置字体属性
            text_shape.CharHeight = font_size
            text_shape.CharColor = font_color
            text_shape.CharWeight = 150 if bold else 100  # 粗体
            
            page.add(text_shape)
            print(f"已添加格式化文本: {text}")
            return True
            
        except Exception as e:
            print(f"添加文本失败: {e}")
            return False
    
    def add_arrow(self, x1=100, y1=500, x2=400, y2=500, arrow_style="Arrow"):
        """添加箭头"""
        try:
            page = self.get_current_page()
            if not page:
                return False
            
            shape = self.document.createInstance("com.sun.star.drawing.LineShape")
            
            # 设置起点和终点
            shape.setStartPosition(Point(x1, y1))
            shape.setEndPosition(Point(x2, y2))
            
            # 设置箭头样式
            shape.setLineStartName(arrow_style)
            shape.setLineEndName(arrow_style)
            
            # 设置线条样式
            shape.setLineStyle(LineStyle.SOLID)
            shape.setLineColor(0x000000)
            shape.setLineWidth(2)
            
            page.add(shape)
            print(f"已添加箭头: ({x1},{y1}) -> ({x2},{y2})")
            return True
            
        except Exception as e:
            print(f"添加箭头失败: {e}")
            return False
    
    def add_connector(self, x1=100, y1=600, x2=400, y2=600, connector_type="Straight"):
        """添加连接线"""
        try:
            page = self.get_current_page()
            if not page:
                return False
            
            shape = self.document.createInstance("com.sun.star.drawing.ConnectorShape")
            
            # 设置连接线类型
            shape.setEdgeKind(connector_type)
            
            # 设置起点和终点
            shape.setStartPosition(Point(x1, y1))
            shape.setEndPosition(Point(x2, y2))
            
            # 设置样式
            shape.setLineStyle(LineStyle.SOLID)
            shape.setLineColor(0x008000)
            shape.setLineWidth(2)
            
            page.add(shape)
            print(f"已添加连接线: ({x1},{y1}) -> ({x2},{y2})")
            return True
            
        except Exception as e:
            print(f"添加连接线失败: {e}")
            return False
    
    def add_group(self, shapes_info):
        """添加形状组"""
        try:
            page = self.get_current_page()
            if not page:
                return False
            
            shapes = []
            
            # 创建多个形状
            for info in shapes_info:
                shape = self.document.createInstance(f"com.sun.star.drawing.{info['type']}Shape")
                shape.setPosition(Point(info['x'], info['y']))
                shape.setSize(Size(info['width'], info['height']))
                
                if 'fill_color' in info:
                    shape.setFillStyle(FillStyle.SOLID)
                    shape.setFillColor(info['fill_color'])
                
                if 'line_color' in info:
                    shape.setLineStyle(LineStyle.SOLID)
                    shape.setLineColor(info['line_color'])
                    shape.setLineWidth(info.get('line_width', 1))
                
                page.add(shape)
                shapes.append(shape)
            
            # 创建组
            if len(shapes) > 1:
                group = self.document.createInstance("com.sun.star.drawing.GroupShape")
                for shape in shapes:
                    group.add(shape)
                page.add(group)
                print(f"已创建形状组，包含 {len(shapes)} 个形状")
            
            return True
            
        except Exception as e:
            print(f"创建形状组失败: {e}")
            return False
    
    def save_document(self, output_path=None):
        """保存文档"""
        try:
            if not self.document:
                return False
            
            if output_path:
                url = uno.systemPathToFileUrl(os.path.abspath(output_path))
                self.document.storeAsUrl(url, ())
                print(f"文档已保存: {output_path}")
            else:
                self.document.store()
                print("文档已保存")
            
            return True
            
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def export_to_pdf(self, output_path):
        """导出为PDF"""
        try:
            if not self.document:
                return False
            
            url = uno.systemPathToFileUrl(os.path.abspath(output_path))
            filter_data = (PropertyValue("FilterName", 0, "draw_pdf_Export", 0),)
            self.document.storeToUrl(url, filter_data)
            print(f"已导出PDF: {output_path}")
            return True
            
        except Exception as e:
            print(f"导出PDF失败: {e}")
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
            print(f"关闭失败: {e}")
            return False

def demo_advanced_features():
    """演示高级功能"""
    print("=== LibreOffice/OpenOffice API 高级ODG操作演示 ===\n")
    
    processor = AdvancedODGProcessor()
    
    # 创建新的ODG文件
    print("1. 创建高级ODG文档...")
    if processor.create_new_odg("advanced_example.odg"):
        
        # 添加带样式的矩形
        processor.add_rectangle_with_style(50, 50, 150, 100, 0xFFFF00, 0x0000FF, 3)
        
        # 添加渐变椭圆
        processor.add_ellipse_with_gradient(250, 50, 150, 100)
        
        # 添加线条
        processor.add_line(50, 200, 400, 200, 0xFF0000, 4)
        
        # 添加格式化文本
        processor.add_text_with_formatting("这是粗体文本", 50, 250, 300, 40, 18, 0x000000, True)
        processor.add_text_with_formatting("这是普通文本", 50, 300, 300, 40, 14, 0x666666, False)
        
        # 添加箭头
        processor.add_arrow(50, 350, 400, 350, "Arrow")
        
        # 添加连接线
        processor.add_connector(50, 400, 400, 400, "Straight")
        
        # 添加形状组
        shapes_info = [
            {"type": "Rectangle", "x": 50, "y": 450, "width": 80, "height": 60, "fill_color": 0xFF0000},
            {"type": "Ellipse", "x": 150, "y": 450, "width": 80, "height": 60, "fill_color": 0x00FF00},
            {"type": "Rectangle", "x": 250, "y": 450, "width": 80, "height": 60, "fill_color": 0x0000FF}
        ]
        processor.add_group(shapes_info)
        
        # 保存文档
        processor.save_document()
        
        # 导出为PDF
        processor.export_to_pdf("advanced_example.pdf")
        
        # 关闭文档
        processor.close_document()
    
    print("\n=== 高级演示完成 ===")
    print("生成的文件:")
    print("- advanced_example.odg (高级ODG文档)")
    print("- advanced_example.pdf (PDF导出文件)")

if __name__ == "__main__":
    demo_advanced_features() 