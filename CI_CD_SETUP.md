# GUIPilot 持续集成/持续部署 (CI/CD) 设置指南

## 概述

本文档说明如何为 GUIPilot 项目设置持续集成和持续部署流程。

## CI/CD 组件

### 1. GitHub Actions 工作流

项目包含以下 GitHub Actions 工作流：

#### `ci.yml` - 主 CI 流程
- **代码检查 (Lint)**: 使用 flake8, black, isort, pylint
- **单元测试 (Test)**: 支持 Python 3.10, 3.11, 3.12
- **构建验证 (Build)**: 验证包可以正确构建和安装
- **依赖检查 (Dependency Check)**: 检查依赖漏洞
- **集成测试 (Integration Test)**: 验证核心模块导入
- **文档检查 (Documentation)**: 验证 README 文件存在

#### `experiments.yml` - 实验验证
- **RQ1 验证**: 验证屏幕不一致性检测实验
- **RQ2 验证**: 验证流程不一致性检测实验（需要 Android 设备）
- **RQ4 验证**: 验证案例研究实验（需要 OpenAI API）

#### `release.yml` - 发布流程
- 当创建版本标签时自动构建和发布包
- 生成 GitHub Release

### 2. Pre-commit Hooks

使用 pre-commit 在提交前自动检查代码：

```bash
# 安装 pre-commit
pip install pre-commit

# 安装 hooks
pre-commit install

# 手动运行所有 hooks
pre-commit run --all-files
```

### 3. Makefile 命令

提供便捷的命令来运行常见任务：

```bash
make install          # 安装包
make test            # 运行测试
make lint            # 运行代码检查
make format          # 格式化代码
make check           # 运行所有检查
make build           # 构建包
make clean           # 清理构建文件
make check-rq1       # 检查 RQ1 实验依赖
make check-rq2       # 检查 RQ2 实验依赖
make check-rq4       # 检查 RQ4 实验依赖
```

## 设置步骤

### 1. 初始化 Git 仓库（如果还没有）

```bash
cd /data5/weihan/GUIPilot-main
git init
git add .
git commit -m "Initial commit with CI/CD setup"
```

### 2. 设置 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库，然后：
git remote add origin https://github.com/your-username/GUIPilot-main.git
git branch -M main
git push -u origin main
```

### 3. 配置 GitHub Actions Secrets（如需要）

如果实验需要敏感信息（如 OpenAI API Key），在 GitHub 仓库设置中添加 Secrets：

1. 进入仓库 Settings → Secrets and variables → Actions
2. 添加以下 secrets（如需要）：
   - `OPENAI_KEY`: OpenAI API Key（用于 RQ4）
   - `DATASET_PATH`: 数据集路径（可选）

### 4. 安装 Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 5. 创建测试目录结构

```bash
mkdir -p tests
touch tests/__init__.py
touch tests/test_entities.py
touch tests/test_matcher.py
touch tests/test_checker.py
```

## 工作流说明

### 触发条件

- **Push 到主分支**: 自动运行所有检查
- **Pull Request**: 运行检查但不部署
- **创建标签**: 触发发布流程
- **手动触发**: 可以通过 GitHub Actions 界面手动触发

### 工作流状态

- ✅ **通过**: 所有检查通过
- ❌ **失败**: 至少一个检查失败
- ⚠️ **跳过**: 某些可选检查被跳过（如 RQ2/RQ4 需要外部依赖）

## 代码质量工具

### Black - 代码格式化

```bash
# 检查格式
black --check guipilot/ experiments/

# 自动格式化
black guipilot/ experiments/
```

### isort - 导入排序

```bash
# 检查导入顺序
isort --check-only guipilot/ experiments/

# 自动排序
isort guipilot/ experiments/
```

### flake8 - 代码风格检查

```bash
flake8 guipilot/ experiments/ --max-line-length=127
```

### pylint - 代码质量分析

```bash
pylint guipilot/
```

### mypy - 类型检查

```bash
mypy guipilot/ --ignore-missing-imports
```

## 测试策略

### 单元测试

创建 `tests/` 目录并添加测试文件：

```python
# tests/test_entities.py
import pytest
from guipilot.entities import Screen, Widget, WidgetType, Bbox

def test_widget_creation():
    bbox = Bbox(0, 0, 100, 100)
    widget = Widget(type=WidgetType.Button, bbox=bbox)
    assert widget.type == WidgetType.Button
    assert widget.bbox == bbox
```

### 集成测试

验证核心模块可以正确导入和基本功能：

```python
# tests/test_integration.py
def test_core_imports():
    from guipilot.entities import Screen
    from guipilot.matcher import GUIPilotV2
    from guipilot.checker import GVT
    assert True
```

### 实验验证

每个实验都有 `check_requirements.py` 脚本来验证依赖：

```bash
cd experiments/rq1_screen_inconsistency
python check_requirements.py
```

## 持续部署

### 版本发布

1. 更新版本号（在 `setup.py` 和 `pyproject.toml` 中）
2. 创建 Git 标签：
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```
3. GitHub Actions 会自动：
   - 构建包
   - 检查包质量
   - 创建 GitHub Release
   - 上传构建产物

### 包发布到 PyPI（可选）

如果需要发布到 PyPI，添加以下步骤到 `release.yml`：

```yaml
- name: Publish to PyPI
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    twine upload dist/*
```

## 监控和通知

### GitHub Actions 状态徽章

在 README.md 中添加状态徽章：

```markdown
![CI](https://github.com/your-username/GUIPilot-main/workflows/CI/badge.svg)
![Experiments](https://github.com/your-username/GUIPilot-main/workflows/Experiments%20Validation/badge.svg)
```

### 通知设置

在 GitHub 仓库设置中配置通知：
- Settings → Notifications → Actions
- 选择何时接收通知（失败、成功、所有）

## 最佳实践

### 1. 提交前检查

始终在提交前运行检查：

```bash
make check
```

### 2. 小步提交

频繁提交小的、经过测试的更改，而不是大的批量提交。

### 3. 分支策略

- `main/master`: 稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `fix/*`: 修复分支

### 4. Pull Request 检查清单

在创建 PR 前检查：
- [ ] 代码通过所有 lint 检查
- [ ] 所有测试通过
- [ ] 代码已格式化
- [ ] 更新了相关文档
- [ ] 添加了必要的测试

### 5. 版本管理

遵循语义化版本控制（Semantic Versioning）：
- `MAJOR.MINOR.PATCH` (例如: 1.0.0)
- MAJOR: 不兼容的 API 更改
- MINOR: 向后兼容的功能添加
- PATCH: 向后兼容的 bug 修复

## 故障排除

### CI 失败常见原因

1. **代码格式问题**: 运行 `make format` 修复
2. **导入错误**: 检查 `__init__.py` 文件
3. **测试失败**: 检查测试代码和依赖
4. **依赖问题**: 更新 `environment.yml` 或 `requirements.txt`

### 本地复现 CI 问题

```bash
# 使用 Docker 复现 CI 环境
docker run -it --rm -v $(pwd):/workspace python:3.12 bash
cd /workspace
pip install -e .
make check
```

## 扩展 CI/CD

### 添加新的检查

1. 在 `.github/workflows/ci.yml` 中添加新 job
2. 在 `Makefile` 中添加对应命令
3. 在 `.pre-commit-config.yaml` 中添加 hook（如适用）

### 添加新的测试

1. 在 `tests/` 目录创建测试文件
2. 使用 pytest 编写测试
3. 确保测试可以通过 `make test` 运行

### 集成代码覆盖率

已配置 pytest-cov，查看覆盖率报告：

```bash
pytest --cov=guipilot --cov-report=html
open htmlcov/index.html
```

## 参考资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Pre-commit 文档](https://pre-commit.com/)
- [Pytest 文档](https://docs.pytest.org/)
- [Black 文档](https://black.readthedocs.io/)

## 维护

定期更新：
- GitHub Actions 版本
- Python 依赖版本
- 代码质量工具版本
- CI/CD 配置

---

**最后更新**: 2025-11-06
