# 快速推送指南 - 使用 Personal Access Token

## 📋 步骤概览

1. 创建 GitHub Personal Access Token
2. 配置 Git 凭证存储（已完成 ✅）
3. 推送代码

## 🔑 步骤 1: 创建 Personal Access Token

### 方法 1: 通过网页创建（推荐）

1. **访问 GitHub Token 页面**
   ```
   https://github.com/settings/tokens
   ```

2. **点击 "Generate new token"**
   - 选择 "Generate new token (classic)"

3. **填写 Token 信息**
   - **Note**: 填写描述，例如 "GUIPilot Push Token"
   - **Expiration**: 选择过期时间
     - 90 days（90天）
     - 或者 No expiration（不过期，但不太安全）
   - **Select scopes**: 至少勾选以下权限
     - ✅ **repo** (完整仓库访问权限)
       - repo:status
       - repo_deployment
       - public_repo
       - repo:invite
       - security_events

4. **生成 Token**
   - 点击页面底部的 "Generate token" 按钮
   - **重要**: 立即复制 token（格式类似：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
   - Token 只会显示一次，如果关闭页面就看不到了！

### 方法 2: 通过命令行创建（需要 GitHub CLI）

```bash
# 如果已安装 GitHub CLI
gh auth login
gh auth token
```

## 🚀 步骤 2: 推送代码

### 方法 1: 直接在命令中使用 Token（一次性）

```bash
# 替换 YOUR_TOKEN 为你的 token
git push https://YOUR_TOKEN@github.com/yire12/GUIPilot.git main
```

### 方法 2: 交互式输入（推荐，更安全）

```bash
git push origin main
```

然后按提示输入：
- **Username**: `yire12`
- **Password**: 粘贴你的 token（不是 GitHub 密码）

凭证会被自动保存，下次推送不需要再输入。

## 📝 完整示例

```bash
# 1. 进入项目目录
cd /data5/weihan/GUIPilot-main

# 2. 检查状态
git status

# 3. 推送代码
git push origin main

# 4. 输入凭证
# Username for 'https://github.com': yire12
# Password for 'https://yire12@github.com': ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## ✅ 验证推送成功

推送成功后，你会看到类似输出：

```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Delta compression using up to X threads
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), X.XX MiB | X.XX MiB/s, done.
Total X (delta X), reused X (delta X), pack-reused 0
To https://github.com/yire12/GUIPilot.git
 * [new branch]      main -> main
```

## 🔍 检查推送结果

1. **在 GitHub 网页查看**
   - 访问: https://github.com/yire12/GUIPilot
   - 确认代码已推送

2. **使用命令检查**
   ```bash
   git ls-remote origin
   ```

## ⚠️ 常见问题

### 问题 1: "Authentication failed"

**原因**: Token 无效或权限不足

**解决**:
- 检查 token 是否正确复制（注意不要有多余空格）
- 确认 token 有 `repo` 权限
- 确认 token 未过期

### 问题 2: "remote: Invalid username or password"

**原因**: 输入错误

**解决**:
- Username 应该是: `yire12`
- Password 应该是: 你的 token（以 `ghp_` 开头）

### 问题 3: "Permission denied"

**原因**: Token 权限不足

**解决**:
- 重新生成 token，确保勾选 `repo` 权限

### 问题 4: 凭证已保存但推送失败

**解决**:
```bash
# 清除保存的凭证
git credential reject https://github.com

# 重新推送
git push origin main
```

## 🔐 安全提示

1. **不要将 token 提交到代码仓库**
   - Token 应该保存在 `.gitignore` 中
   - 不要在任何公开的地方分享 token

2. **使用最小权限原则**
   - 只授予必要的权限（repo）

3. **定期轮换 token**
   - 定期更新 token
   - 删除不再使用的 token

4. **使用 SSH 密钥（长期推荐）**
   - Token 更适合临时使用
   - 长期使用建议配置 SSH 密钥

## 📚 相关文档

- GitHub Token 文档: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
- Git 凭证存储: https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage

## 🎯 当前状态

- ✅ Git 凭证存储已配置
- ✅ 远程仓库已配置: `https://github.com/yire12/GUIPilot.git`
- ✅ 本地代码已提交
- ⏳ 等待创建 Personal Access Token 并推送

## 下一步

1. 访问 https://github.com/settings/tokens 创建 token
2. 运行 `git push origin main`
3. 输入用户名和 token
4. 完成！

