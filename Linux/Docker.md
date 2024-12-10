# Docker 安装
## 在线安装
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
# -y 的作用是：
# 自动确认所有安装提示。
# 确保安装过程不需要用户手动输入 "y"。
# 适用于自动化脚本和批量安装软件。
```
## 验证安装
```bash
docker --version
```
## 权限设置
将用户账户添加到 docker 用户组中
- 创建 docker 用户组（如果该组不存在）：
```sudo groupadd docker```
- 将当前用户添加到 docker 用户组：
```sudo usermod -aG docker $USER```
- 重新加载用户组： 为了使组更改生效，你需要重新登录或重新加载用户组。你可以通过以下命令重新加载组：
```newgrp docker```
或者重新登录你的终端会话。
- 验证更改： 你可以通过运行以下命令来验证你的用户是否已成功添加到 docker 用户组：
```groups```
你应该会看到 docker 组在输出中。