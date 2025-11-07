#!/bin/bash
# Git 代理配置脚本

echo "=========================================="
echo "Git 代理配置工具"
echo "=========================================="
echo ""

# 检查当前代理设置
echo "当前 Git 代理设置："
echo "HTTP 代理: $(git config --global --get http.proxy || echo '未设置')"
echo "HTTPS 代理: $(git config --global --get https.proxy || echo '未设置')"
echo ""

# 显示选项
echo "请选择操作："
echo "1. 设置 HTTP/HTTPS 代理"
echo "2. 仅对 GitHub 设置代理"
echo "3. 取消代理设置"
echo "4. 查看当前代理设置"
echo "5. 测试代理连接"
echo ""

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo ""
        echo "设置全局 HTTP/HTTPS 代理"
        read -p "请输入代理地址 (例如: http://proxy.example.com:8080): " proxy_url
        if [ -n "$proxy_url" ]; then
            git config --global http.proxy "$proxy_url"
            git config --global https.proxy "$proxy_url"
            echo "✅ 代理已设置: $proxy_url"
        else
            echo "❌ 代理地址不能为空"
        fi
        ;;
    2)
        echo ""
        echo "仅对 GitHub 设置代理"
        read -p "请输入代理地址 (例如: http://proxy.example.com:8080): " proxy_url
        if [ -n "$proxy_url" ]; then
            git config --global http.https://github.com.proxy "$proxy_url"
            echo "✅ GitHub 代理已设置: $proxy_url"
        else
            echo "❌ 代理地址不能为空"
        fi
        ;;
    3)
        echo ""
        echo "取消代理设置"
        git config --global --unset http.proxy
        git config --global --unset https.proxy
        git config --global --unset http.https://github.com.proxy
        echo "✅ 代理设置已清除"
        ;;
    4)
        echo ""
        echo "当前代理设置："
        echo "HTTP 代理: $(git config --global --get http.proxy || echo '未设置')"
        echo "HTTPS 代理: $(git config --global --get https.proxy || echo '未设置')"
        echo "GitHub 代理: $(git config --global --get http.https://github.com.proxy || echo '未设置')"
        ;;
    5)
        echo ""
        echo "测试代理连接..."
        proxy=$(git config --global --get http.https://github.com.proxy || git config --global --get https.proxy || echo "")
        if [ -n "$proxy" ]; then
            echo "使用代理: $proxy"
            echo "测试连接到 GitHub..."
            curl -I --proxy "$proxy" https://github.com 2>&1 | head -5
        else
            echo "未设置代理，直接测试连接..."
            curl -I https://github.com 2>&1 | head -5
        fi
        ;;
    *)
        echo "❌ 无效的选项"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
