#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RQ2 实验依赖检查脚本
检查运行 RQ2 实验所需的所有依赖和配置
"""
import os
import sys
import glob
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
        'uiautomator2': 'uiautomator2',
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'supervision': 'supervision',
        'PIL': 'Pillow',
        'pydantic': 'pydantic',
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

def check_android_device():
    """检查 Android 设备连接"""
    print("\n" + "=" * 60)
    print("3. 检查 Android 设备连接")
    print("=" * 60)
    
    try:
        import uiautomator2 as u2
        
        # 尝试连接默认设备
        default_device = "192.168.240.112:5555"
        print(f"尝试连接设备: {default_device}")
        
        try:
            device = u2.connect(default_device)
            info = device.info
            print(f"✓ 设备已连接: {info.get('productName', 'Unknown')}")
            print(f"  设备信息: {info}")
            return True
        except Exception as e:
            print(f"✗ 无法连接到默认设备 {default_device}")
            print(f"  错误: {e}")
            
            # 尝试列出可用设备
            print("\n尝试查找可用设备...")
            try:
                import subprocess
                result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
                print("ADB 设备列表:")
                print(result.stdout)
            except Exception:
                print("无法运行 adb devices 命令")
            
            return False
    except ImportError:
        print("✗ uiautomator2 未安装")
        return False

def check_dataset():
    """检查数据集"""
    print("\n" + "=" * 60)
    print("4. 检查数据集")
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
    
    # 查找 process_* 目录
    process_paths = glob.glob(os.path.join(dataset_path, "*", "process_*"))
    
    if len(process_paths) == 0:
        print(f"✗ 未找到 process_* 目录")
        print(f"  期望的数据集结构:")
        print(f"  {dataset_path}/")
        print(f"    App1/")
        print("      process_1/")  # noqa: F541
        print("        record.json")  # noqa: F541
        print("        1.jpg")  # noqa: F541
        print("        1.xml")  # noqa: F541
        print("        ...")  # noqa: F541
        return False
    
    print(f"✓ 找到 {len(process_paths)} 个 process 目录")
    
    # 检查每个 process 目录是否有 record.json
    valid_processes = 0
    for process_path in process_paths[:5]:  # 只检查前5个
        record_path = os.path.join(process_path, "record.json")
        if os.path.exists(record_path):
            valid_processes += 1
            print(f"  ✓ {os.path.basename(process_path)}: 有 record.json")
        else:
            print(f"  ✗ {os.path.basename(process_path)}: 缺少 record.json")
    
    if valid_processes == 0:
        print("✗ 没有找到有效的 process 目录（包含 record.json）")
        return False
    
    return True

def check_openai_key():
    """检查 OpenAI API Key"""
    print("\n" + "=" * 60)
    print("5. 检查 OpenAI API Key")
    print("=" * 60)
    
    load_dotenv()
    openai_key = os.getenv("OPENAI_KEY")
    
    if not openai_key:
        print("✗ OPENAI_KEY 环境变量未设置")
        print("  请设置: export OPENAI_KEY=your_api_key")
        return False
    
    if len(openai_key) < 20:
        print("✗ OPENAI_KEY 看起来无效（太短）")
        return False
    
    print(f"✓ OPENAI_KEY 已设置 (长度: {len(openai_key)})")
    return True

def check_manual_interaction():
    """检查手动交互要求"""
    print("\n" + "=" * 60)
    print("6. 手动交互要求")
    print("=" * 60)
    print("⚠ RQ2 实验需要手动交互:")
    print("  - 需要手动对齐手机屏幕")
    print("  - 需要手动执行某些操作")
    print("  - 需要手动验证结果")
    print("  实验脚本包含多个 input() 调用，需要人工参与")
    return True

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("RQ2 流程不一致性检测实验 - 依赖检查")
    print("=" * 60)
    
    results = {
        "Conda 环境": check_conda_environment(),
        "Python 依赖": check_dependencies(),
        "Android 设备": check_android_device(),
        "数据集": check_dataset(),
        "OpenAI API Key": check_openai_key(),
        "手动交互": check_manual_interaction(),
    }
    
    print("\n" + "=" * 60)
    print("检查结果总结")
    print("=" * 60)
    
    all_ok = True
    for name, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {name}")
        if not result:
            all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ 所有依赖已满足，可以运行 RQ2 实验")
        print("\n运行命令:")
        print("  cd /path/to/GUIPilot-main/experiments/rq2_flow_inconsistency")
        print("  export DATASET_PATH=/path/to/dataset")
        print("  export OPENAI_KEY=your_api_key")
        print("  python main.py")
    else:
        print("✗ 部分依赖未满足，请先解决上述问题")
        print("\n建议:")
        if not results["Android 设备"]:
            print("  1. 连接 Android 设备或启动模拟器")
            print("  2. 启用 USB 调试或配置 ADB 连接")
            print("  3. 运行: adb devices 确认设备连接")
        if not results["数据集"]:
            print("  1. 准备包含 process_* 目录的数据集")
            print("  2. 每个 process 目录需要包含 record.json 文件")
        if not results["OpenAI API Key"]:
            print("  1. 获取 OpenAI API Key")
            print("  2. 设置环境变量: export OPENAI_KEY=your_key")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())

