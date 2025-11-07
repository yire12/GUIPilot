# GitHub 推送指南

## 问题

使用 HTTPS 方式推送代码到 GitHub 需要身份验证。GitHub 不再支持密码认证，需要使用 **Personal Access Token (PAT)**。

## 解决方案

### 方案 1: 使用 Personal Access Token (推荐)

#### 步骤 1: 创建 Personal Access Token

1. 登录 GitHub
2. 点击右上角头像 → **Settings**
3. 左侧菜单选择 **Developer settings**
4. 选择 **Personal access tokens** → **Tokens (classic)**
5. 点击 **Generate new token** → **Generate new token (classic)**
6. 填写信息：
   - **Note**: 例如 "GUIPilot Push Token"
   - **Expiration**: 选择过期时间（或 No expiration）
   - **Scopes**: 至少勾选 `repo` (完整仓库访问权限)
7. 点击 **Generate token**
8. **重要**: 复制生成的 token（只显示一次！）

#### 步骤 2: 使用 Token 推送

```bash
# 方法 1: 在 URL 中包含 token
git remote set-url origin https://<TOKEN>@github.com/yire12/GUIPilot.git
git push origin main

# 方法 2: 推送时输入（用户名：你的GitHub用户名，密码：token）
git push origin main
# Username: yire12
# Password: <你的token>
```

#### 步骤 3: 配置凭证存储（避免每次都输入）

```bash
# 使用 Git 凭证助手存储凭证
git config --global credential.helper store

# 或者使用缓存（15分钟内不需要重新输入）
git config --global credential.helper cache

# 或者使用缓存并设置超时时间（例如1小时）
git config --global credential.helper 'cache --timeout=3600'
```

### 方案 2: 使用 SSH 密钥（更安全，推荐长期使用）

#### 步骤 1: 检查是否已有 SSH 密钥

```bash
ls -la ~/.ssh
```

如果看到 `id_rsa` 或 `id_ed25519` 等文件，说明已有密钥。

#### 步骤 2: 生成新的 SSH 密钥（如果没有）

```bash
# 使用你的 GitHub 邮箱
ssh-keygen -t ed25519 -C "your_email@example.com"

# 或使用 RSA（如果系统不支持 ed25519）
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

按提示操作：
- 保存位置：直接回车使用默认位置
- 密码：可以设置密码或直接回车（不设置）

#### 步骤 3: 将公钥添加到 GitHub

```bash
# 显示公钥内容
cat ~/.ssh/id_ed25519.pub
# 或
cat ~/.ssh/id_rsa.pub
```

复制输出的内容，然后：

1. 登录 GitHub
2. 点击右上角头像 → **Settings**
3. 左侧菜单选择 **SSH and GPG keys**
4. 点击 **New SSH key**
5. **Title**: 填写描述（例如 "My Laptop"）
6. **Key**: 粘贴刚才复制的公钥内容
7. 点击 **Add SSH key**

#### 步骤 4: 测试 SSH 连接

```bash
ssh -T git@github.com
```

如果看到 "Hi yire12! You've successfully authenticated..." 说明配置成功。

#### 步骤 5: 更改远程 URL 为 SSH

```bash
git remote set-url origin git@github.com:yire12/GUIPilot.git
git push origin main
```

### 方案 3: 使用 GitHub CLI

```bash
# 安装 GitHub CLI（如果未安装）
# Ubuntu/Debian:
# sudo apt install gh

# 登录
gh auth login

# 选择 GitHub.com
# 选择 HTTPS 或 SSH
# 完成认证

# 推送
git push origin main
```

## 快速配置脚本

我创建了一个配置脚本，你可以运行：

```bash
./configure_proxy.sh
```

## 当前推荐方案

根据你的情况，我推荐：

1. **短期解决**: 使用 Personal Access Token + 凭证存储
2. **长期解决**: 配置 SSH 密钥（更安全，更方便）

## 验证配置

配置完成后，测试推送：

```bash
# 查看远程仓库配置
git remote -v

# 测试连接
git ls-remote origin

# 推送代码
git push origin main
```

## 常见问题

### 1. Token 在哪里使用？

- **Username**: 你的 GitHub 用户名（例如：yire12）
- **Password**: 使用 Personal Access Token（不是你的 GitHub 密码）

### 2. Token 过期了怎么办？

重新生成新的 token，然后更新凭证：
```bash
git credential reject https://github.com
git push origin main  # 重新输入新的 token
```

### 3. 如何查看已保存的凭证？

```bash
# 查看存储的凭证
cat ~/.git-credentials
```

### 4. 如何删除保存的凭证？

```bash
git credential reject https://github.com
```

### 5. SSH 连接测试失败？

检查 SSH 代理：
```bash
# 启动 SSH 代理
eval "$(ssh-agent -s)"

# 添加密钥
ssh-add ~/.ssh/id_ed25519
# 或
ssh-add ~/.ssh/id_rsa
```

## 安全建议

1. **Token 安全**:
   - 不要将 token 提交到代码仓库
   - 使用最小权限原则（只授予必要的权限）
   - 定期轮换 token

2. **SSH 密钥安全**:
   - 为 SSH 密钥设置密码
   - 不要在多个设备间共享私钥
   - 定期检查和更新授权的密钥

3. **凭证存储**:
   - 使用 `cache` 而不是 `store`（更安全）
   - 定期清理存储的凭证

## 需要帮助？

如果遇到问题，可以：
1. 查看 GitHub 官方文档：https://docs.github.com/en/authentication
2. 检查 Git 配置：`git config --list`
3. 查看详细错误信息：`GIT_CURL_VERBOSE=1 git push origin main`

