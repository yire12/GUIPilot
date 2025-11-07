# Git 代理配置指南

## 快速配置

### 方法 1: 使用配置脚本（推荐）

```bash
./configure_proxy.sh
```

脚本会引导你完成代理配置。

### 方法 2: 手动配置

#### 设置全局代理

```bash
# HTTP/HTTPS 代理
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# 或者使用 SOCKS5 代理
git config --global http.proxy socks5://127.0.0.1:1080
git config --global https.proxy socks5://127.0.0.1:1080
```

#### 仅对 GitHub 设置代理（推荐）

如果只想对 GitHub 使用代理，可以这样设置：

```bash
git config --global http.https://github.com.proxy http://proxy.example.com:8080
```

#### 取消代理设置

```bash
# 取消全局代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 取消 GitHub 代理
git config --global --unset http.https://github.com.proxy
```

## 常见代理类型

### 1. HTTP 代理

```bash
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080
```

### 2. HTTPS 代理

```bash
git config --global http.proxy https://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080
```

### 3. SOCKS5 代理

```bash
git config --global http.proxy socks5://127.0.0.1:1080
git config --global https.proxy socks5://127.0.0.1:1080
```

### 4. 带认证的代理

```bash
# 格式: http://username:password@proxy.example.com:8080
git config --global http.proxy http://user:pass@proxy.example.com:8080
git config --global https.proxy http://user:pass@proxy.example.com:8080
```

## 查看当前配置

```bash
# 查看所有 Git 配置
git config --global --list | grep proxy

# 查看特定配置
git config --global --get http.proxy
git config --global --get https.proxy
git config --global --get http.https://github.com.proxy
```

## 测试代理连接

```bash
# 测试 GitHub 连接
curl -I https://github.com

# 使用代理测试
curl -I --proxy http://proxy.example.com:8080 https://github.com
```

## 常见问题

### 1. 代理需要认证

如果代理需要用户名和密码：

```bash
git config --global http.proxy http://username:password@proxy.example.com:8080
```

**注意**: 密码会以明文形式存储在 Git 配置中。更安全的方式是使用环境变量：

```bash
export http_proxy=http://username:password@proxy.example.com:8080
export https_proxy=http://username:password@proxy.example.com:8080
```

### 2. 只对特定域名使用代理

```bash
# 只对 GitHub 使用代理
git config --global http.https://github.com.proxy http://proxy.example.com:8080

# 排除某些域名（不使用代理）
git config --global http.https://github.com.proxy ""
```

### 3. 使用系统代理设置

如果系统已经配置了代理环境变量，Git 可能不会自动使用。可以这样设置：

```bash
# 从环境变量读取代理
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080

# 或者让 Git 使用环境变量
git config --global http.proxy $http_proxy
git config --global https.proxy $https_proxy
```

### 4. 临时使用代理（不保存配置）

```bash
# 只对当前命令使用代理
http_proxy=http://proxy.example.com:8080 https_proxy=http://proxy.example.com:8080 git push origin main
```

## 验证配置

配置完成后，测试推送：

```bash
# 查看远程仓库
git remote -v

# 测试连接
git ls-remote origin

# 推送代码
git push origin main
```

## 代理服务器地址示例

根据你的网络环境，代理地址可能是：

- **公司代理**: `http://proxy.company.com:8080`
- **本地代理**: `http://127.0.0.1:8080` 或 `socks5://127.0.0.1:1080`
- **VPN 代理**: 通常由 VPN 软件提供，如 `http://127.0.0.1:7890`

## 注意事项

1. **安全性**: 如果代理需要认证，避免在配置文件中直接存储密码
2. **性能**: 使用代理可能会影响 Git 操作速度
3. **兼容性**: 确保代理服务器支持 HTTPS 连接
4. **测试**: 配置后务必测试连接是否正常

## 获取帮助

如果遇到问题：

1. 检查代理服务器是否正常运行
2. 验证代理地址和端口是否正确
3. 检查防火墙设置
4. 查看 Git 错误信息获取更多详情

```bash
# 查看详细错误信息
GIT_CURL_VERBOSE=1 GIT_TRACE=1 git push origin main
```
