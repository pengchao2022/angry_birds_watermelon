#!/usr/bin/env python3
"""
诊断导入问题
"""

import os
import sys

def check_math_imports():
    """检查所有 Python 文件是否导入了 math 模块"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(project_root, 'src')
    
    python_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print("检查所有 Python 文件的 math 导入...")
    issues_found = False
    
    for file_path in python_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否使用了 math 但没有导入
        uses_math = any(math_func in content for math_func in [
            'math.sqrt', 'math.pi', 'math.cos', 'math.sin', 
            'math.radians', 'math.degrees', 'math.atan2'
        ])
        
        has_math_import = 'import math' in content
        
        filename = os.path.basename(file_path)
        if uses_math and not has_math_import:
            print(f"❌ {filename}: 使用了 math 但没有导入")
            issues_found = True
        elif uses_math and has_math_import:
            print(f"✅ {filename}: 正确导入了 math")
        else:
            print(f"➖ {filename}: 未使用 math")
    
    return issues_found

if __name__ == "__main__":
    if check_math_imports():
        print("\n❌ 发现导入问题！")
        sys.exit(1)
    else:
        print("\n✅ 所有文件导入正常")
        sys.exit(0)