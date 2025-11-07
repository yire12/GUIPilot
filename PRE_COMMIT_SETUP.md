# Pre-commit Hooks 安装完成

## 安装状态

✅ **Pre-commit 已成功安装并配置**

- Pre-commit 版本: 4.3.0
- Hooks 已安装到: `.git/hooks/pre-commit`
- 配置文件: `.pre-commit-config.yaml`

## 已配置的 Hooks

### 1. 基础检查 (pre-commit-hooks)
- ✅ `trailing-whitespace`: 检查并移除行尾空白
- ✅ `end-of-file-fixer`: 确保文件以换行符结尾
- ✅ `check-yaml`: 验证 YAML 文件格式
- ✅ `check-json`: 验证 JSON 文件格式
- ✅ `check-toml`: 验证 TOML 文件格式
- ✅ `check-added-large-files`: 检查大文件
- ✅ `check-merge-conflict`: 检查合并冲突标记
- ✅ `debug-statements`: 检查调试语句
- ✅ `mixed-line-ending`: 检查混合行尾

### 2. 代码格式化
- ✅ `black`: Python 代码格式化（已更新到 v25.9.0）
- ✅ `isort`: 导入排序（已更新到 v7.0.0）

### 3. 代码质量检查
- ✅ `flake8`: 代码风格检查（已更新到 v7.3.0）
- ⚠️ `mypy`: 类型检查（已配置，但有一些类型错误需要修复）

## 使用方法

### 自动运行（推荐）

Pre-commit hooks 会在每次 `git commit` 时自动运行：

```bash
git add .
git commit -m "Your commit message"
# Hooks 会自动运行并检查代码
```

### 手动运行

运行所有 hooks：
```bash
pre-commit run --all-files
```

运行特定 hook：
```bash
pre-commit run black --all-files
pre-commit run flake8 --all-files
```

### 跳过 hooks（不推荐）

如果确实需要跳过 hooks（紧急情况）：
```bash
git commit --no-verify -m "Emergency commit"
```

## 当前状态

### 通过的检查 ✅
- 基础文件检查（trailing-whitespace, end-of-file-fixer 等）
- YAML/JSON/TOML 格式检查
- Black 代码格式化
- isort 导入排序

### 需要修复的问题 ⚠️

运行 `pre-commit run --all-files` 时发现了一些 flake8 错误：

1. **未使用的导入** (F401)
   - `experiments/rq1_screen_inconsistency/check_requirements.py`: 未使用的 `glob` 和 `guipilot` 导入
   - `experiments/rq1_screen_inconsistency/main.py`: 未使用的 `glob` 导入

2. **F-string 占位符问题** (F541)
   - 一些 f-string 缺少占位符，应该使用普通字符串

3. **未使用的变量** (F841)
   - 一些异常变量被赋值但未使用

4. **Bare except** (E722)
   - 应该使用具体的异常类型

### 修复建议

可以运行以下命令自动修复部分问题：

```bash
# 自动格式化代码
make format

# 或者手动运行
black guipilot/ experiments/
isort guipilot/ experiments/
```

对于其他问题，需要手动修复。

## 更新 Hooks

定期更新 hooks 到最新版本：

```bash
pre-commit autoupdate
```

## 禁用特定 Hook

如果某个 hook 在特定情况下不需要，可以在提交时跳过：

```bash
SKIP=flake8 git commit -m "Skip flake8 for this commit"
```

或者在配置文件中临时注释掉。

## 验证安装

验证 hooks 是否正确安装：

```bash
# 检查 hooks 是否安装
ls -la .git/hooks/pre-commit

# 测试 hooks
pre-commit run --all-files
```

## 下一步

1. **修复代码质量问题**:
   ```bash
   # 查看所有问题
   pre-commit run --all-files

   # 自动修复格式问题
   make format
   ```

2. **提交配置**:
   ```bash
   git add .pre-commit-config.yaml
   git commit -m "Add pre-commit configuration"
   ```

3. **团队协作**:
   - 确保团队成员也安装 pre-commit
   - 在项目 README 中添加安装说明

## 故障排除

### 问题: Hooks 运行太慢

**解决方案**: 可以跳过某些耗时的检查（如 mypy）：
```bash
SKIP=mypy git commit -m "Skip type checking"
```

### 问题: Hook 失败但代码是正确的

**解决方案**:
1. 检查 hook 配置是否正确
2. 查看具体错误信息
3. 如果确认是误报，可以调整配置或跳过该 hook

### 问题: 某些文件被意外修改

**解决方案**:
- Pre-commit 会自动修复某些问题（如行尾空白）
- 检查修改是否符合预期
- 如果不符合，可以调整 hook 配置

## 参考

- [Pre-commit 文档](https://pre-commit.com/)
- [Black 文档](https://black.readthedocs.io/)
- [isort 文档](https://pycqa.github.io/isort/)
- [Flake8 文档](https://flake8.pycqa.org/)

---

**安装日期**: 2025-11-06
**状态**: ✅ 已安装并配置完成
