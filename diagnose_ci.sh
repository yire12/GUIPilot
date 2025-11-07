#!/bin/bash
echo "=== CI 诊断脚本 ==="
echo ""

echo "1. 检查 Python 版本..."
python3 --version

echo ""
echo "2. 检查关键文件..."
test -f setup.py && echo "✅ setup.py 存在" || echo "❌ setup.py 不存在"
test -f pyproject.toml && echo "✅ pyproject.toml 存在" || echo "❌ pyproject.toml 不存在"
test -f README.md && echo "✅ README.md 存在" || echo "❌ README.md 不存在"

echo ""
echo "3. 测试构建..."
python3 -m pip install build wheel --quiet
python3 -m build --wheel 2>&1 | tail -5

echo ""
echo "4. 测试安装..."
pip install dist/*.whl --quiet 2>&1 | tail -3
python3 -c "import guipilot; print('✅ guipilot 导入成功')" 2>&1

echo ""
echo "5. 测试语法检查..."
python3 -c "
import ast
import os
for root, dirs, files in os.walk('guipilot'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r') as f:
                    ast.parse(f.read())
            except SyntaxError as e:
                print(f'❌ {path}: {e}')
                exit(1)
print('✅ 所有 Python 文件语法正确')
"

echo ""
echo "诊断完成"
