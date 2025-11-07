#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RQ4 案例研究实验依赖检查脚本
检查运行 RQ4 实验所需的所有依赖和配置
"""
import json
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
        "cv2": "opencv-python",
        "numpy": "numpy",
        "supervision": "supervision",
        "PIL": "Pillow",
        "jsbeautifier": "jsbeautifier",
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


def check_openai_key():
    """检查 OpenAI API Key"""
    print("\n" + "=" * 60)
    print("3. 检查 OpenAI API Key")
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

    # 查找包含 mockup 目录的 process 目录
    process_paths = []
    for root, dirs, files in os.walk(dataset_path):
        if "mockup" in dirs:
            full_path = os.path.abspath(root)
            process_paths.append(full_path)

    if len(process_paths) == 0:
        print(f"✗ 未找到包含 mockup 目录的 process 目录")
        print(f"  期望的数据集结构:")
        print(f"  {dataset_path}/")
        print("    Process1/")
        print("      mockup/")
        print("        1.png")
        print("        2.png")  # noqa: F541
        print("        ...")  # noqa: F541
        print("      implementation/")  # noqa: F541
        print("        process.json")  # noqa: F541
        print("        1.jpg")
        print("        2.jpg")
        print("        ...")
        return False

    print(f"✓ 找到 {len(process_paths)} 个 process 目录")

    # 检查每个 process 目录的结构
    valid_processes = 0
    for process_path in process_paths[:5]:  # 只检查前5个
        mockup_path = os.path.join(process_path, "mockup")
        implementation_path = os.path.join(process_path, "implementation")
        json_path = os.path.join(implementation_path, "process.json")

        has_mockup = os.path.exists(mockup_path) and os.path.isdir(mockup_path)
        has_implementation = os.path.exists(implementation_path) and os.path.isdir(implementation_path)
        has_json = os.path.exists(json_path)

        if has_mockup and has_implementation and has_json:
            valid_processes += 1
            print(f"  ✓ {os.path.basename(process_path)}: 结构完整")

            # 检查 process.json 格式
            try:
                with open(json_path, "r") as f:
                    process_data = json.load(f)
                if isinstance(process_data, list) and len(process_data) > 0:
                    print(f"    - process.json 格式正确 ({len(process_data)} 个步骤)")
                else:
                    print(f"    ⚠ process.json 格式可能不正确")
            except Exception as e:
                print(f"    ✗ process.json 解析失败: {e}")  # noqa: F541
        else:
            missing = []
            if not has_mockup:
                missing.append("mockup/")
            if not has_implementation:
                missing.append("implementation/")
            if not has_json:
                missing.append("implementation/process.json")
            print(f"  ✗ {os.path.basename(process_path)}: 缺少 {', '.join(missing)}")

    if valid_processes == 0:
        print("✗ 没有找到有效的 process 目录")
        return False

    return True


def check_code_structure():
    """检查代码结构"""
    print("\n" + "=" * 60)
    print("5. 检查代码结构")
    print("=" * 60)

    base_path = os.path.dirname(os.path.abspath(__file__))
    required_files = [
        "main.py",
        "utils.py",
        "action_completion.user.prompt",
        "actions/translator.py",
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


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("RQ4 案例研究实验 - 依赖检查")
    print("=" * 60)

    results = {
        "Conda 环境": check_conda_environment(),
        "Python 依赖": check_dependencies(),
        "OpenAI API Key": check_openai_key(),
        "数据集": check_dataset(),
        "代码结构": check_code_structure(),
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
        print("✓ 所有依赖已满足，可以运行 RQ4 实验")
        print("\n运行命令:")
        print("  cd /path/to/GUIPilot-main/experiments/rq4_case_study")
        print("  export DATASET_PATH=/path/to/dataset")
        print("  export OPENAI_KEY=your_api_key")
        print("  python main.py")
    else:
        print("✗ 部分依赖未满足，请先解决上述问题")
        print("\n建议:")
        if not results["数据集"]:
            print("  1. 准备包含 mockup 和 implementation 目录的数据集")
            print("  2. 每个 process 目录需要包含:")
            print("     - mockup/ 目录（包含 .png 文件）")
            print("     - implementation/ 目录（包含 process.json 和 .jpg 文件）")
        if not results["OpenAI API Key"]:
            print("  1. 获取 OpenAI API Key")
            print("  2. 设置环境变量: export OPENAI_KEY=your_key")
    print("=" * 60)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
