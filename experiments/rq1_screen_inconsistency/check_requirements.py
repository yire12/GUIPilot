#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RQ1 屏幕不一致性检测实验依赖检查脚本
检查运行 RQ1 实验所需的所有依赖和配置
"""
import os
import sys
from dotenv import load_dotenv

def check_conda_environment():
    """检查 Conda 环境"""
    print("=" * 60)
    print("1. 检查 Conda 环境")
    print("=" * 60)
    try:
        import guipilot  # noqa: F401
        print("✓ GUIPilot 包已安装")
    except ImportError:
        print("✗ GUIPilot 包未安装")
        return False
    return True

def check_dependencies():
    """检查 Python 依赖"""
    print("\n" + "=" * 60)
    print("2. 检查 Python 依赖")
    print("=" * 60)
    
    dependencies = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'supervision': 'supervision',
        'dotenv': 'python-dotenv',
    }
    
    all_ok = True
    for module_name, package_name in dependencies.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            print(f"✗ {package_name} 未安装")
            all_ok = False
    
    return all_ok

def check_dataset():
    """检查数据集"""
    print("\n" + "=" * 60)
    print("3. 检查数据集")
    print("=" * 60)
    
    load_dotenv()
    dataset_path = os.getenv("DATASET_PATH")
    
    if not dataset_path:
        print("✗ DATASET_PATH 环境变量未设置")
        print("  请设置: export DATASET_PATH=/path/to/dataset")
        return False
    
    print(f"数据集路径: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        print(f"✗ 数据集路径不存在: {dataset_path}")
        return False
    
    # 查找所有 .jpg 文件
    all_paths = []
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".jpg") and file.replace(".jpg", "").isdigit():
                full_path = os.path.join(root, file)
                all_paths.append(full_path)
    
    if len(all_paths) == 0:
        print(f"✗ 未找到测试图片文件（.jpg）")
        print(f"  期望的数据集结构:")
        print(f"  {dataset_path}/")
        print("    App1/")
        print("      1.jpg")
        print("      1.json")  # noqa: F541
        print("      2.jpg")  # noqa: F541
        print("      2.json")  # noqa: F541
        print("      ...")
        return False
    
    print(f"✓ 找到 {len(all_paths)} 个测试图片文件")
    
    # 检查是否有对应的 JSON 文件
    json_count = 0
    for image_path in all_paths[:10]:  # 只检查前10个
        json_path = image_path.replace(".jpg", ".json")
        if os.path.exists(json_path):
            json_count += 1
    
    if json_count == 0:
        print("⚠ 未找到对应的 JSON 标注文件")
        print("  实验可以使用自动 widget 检测，但需要 OCR 服务")
    else:
        print(f"✓ 找到 {json_count} 个 JSON 标注文件（在前10个图片中）")
    
    # 显示一些示例
    print("\n示例文件:")
    for image_path in all_paths[:3]:
        rel_path = os.path.relpath(image_path, dataset_path)
        print(f"  - {rel_path}")
    
    return True

def check_code_structure():
    """检查代码结构"""
    print("\n" + "=" * 60)
    print("4. 检查代码结构")
    print("=" * 60)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    required_files = [
        "main.py",
        "utils.py",
        "mutate/__init__.py",
        "mutate/deletion.py",
        "mutate/insertion.py",
        "mutate/substitution.py",
    ]
    
    all_ok = True
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} 不存在")
            all_ok = False
    
    return all_ok

def check_ocr_service():
    """检查 OCR 服务（可选）"""
    print("\n" + "=" * 60)
    print("5. 检查 OCR 服务（可选）")
    print("=" * 60)
    
    try:
        import requests
        try:
            requests.get("http://localhost:5000/detect", timeout=2)
            print("✓ OCR 服务正在运行 (localhost:5000)")
            return True
        except Exception:
            print("⚠ OCR 服务未运行 (localhost:5000)")
            print("  如果数据集包含 JSON 标注文件，则不需要 OCR 服务")
            print("  如果需要自动 widget 检测，请启动 OCR 服务")
            return False
    except ImportError:
        print("⚠ requests 模块未安装，无法检查 OCR 服务")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("RQ1 屏幕不一致性检测实验 - 依赖检查")
    print("=" * 60)
    
    results = {
        "Conda 环境": check_conda_environment(),
        "Python 依赖": check_dependencies(),
        "数据集": check_dataset(),
        "代码结构": check_code_structure(),
        "OCR 服务": check_ocr_service(),
    }
    
    print("\n" + "=" * 60)
    print("检查结果总结")
    print("=" * 60)
    
    all_ok = True
    for name, result in results.items():
        if name == "OCR 服务" and not result:
            status = "⚠"  # OCR 服务是可选的
        else:
            status = "✓" if result else "✗"
        print(f"{status} {name}")
        if not result and name != "OCR 服务":
            all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ 所有必需依赖已满足，可以运行 RQ1 实验")
        print("\n运行命令:")
        print("  cd /path/to/GUIPilot-main/experiments/rq1_screen_inconsistency")
        print("  export DATASET_PATH=/path/to/dataset")
        print("  python main.py")
    else:
        print("✗ 部分依赖未满足，请先解决上述问题")
        print("\n建议:")
        if not results["数据集"]:
            print("  1. 准备包含 .jpg 图片和 .json 标注的数据集")
            print("  2. 设置环境变量: export DATASET_PATH=/path/to/dataset")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())

