# 系统类
## 修改PATH-永久有效
1. 针对当前用户
   ```shell
    sudo vim ~/.bashrc # 编辑.bashrc文件，添加下面一行内容
    export PATH=$PATH:/xxx/xxx # xxx/xxx为需要加入的环境变量地址，等号两边没空格
    
    source ~/.bashrc    # 使修改立即生效
    ```
2. 针对所有用户
方法一
sudo vim /etc/profile #编辑profile文件，添加下面一行内容
export PATH=$PATH:/xxx/xxx # xxx/xxx为需要加入的环境变量地址，等号两边没空格

reboot    # 重启系统生效

方法二
sudo vim /etc/environment #编辑environment文件，添加下面一行内容
在PATH最后添加需要加入的环境变量地址xxx/xxx

reboot    # 重启系统生效
## apt 配置清华源
24.04LTS 后，apt源的位置从/etc/apt/sources.list替换到了/etc/apt/sources.list.d/ubuntu.sources中。
备份 cp ubuntu.sources ubuntu.sources.bak
修改ubuntu.sources中内容为
Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu/
#如果使用其他镜像站，上面这行可以改成其他镜像站的网址
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://security.ubuntu.com/ubuntu
#如果安全更新需要使用镜像站，上面这行也改成 URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu/
Suites: noble-security
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
之后运行
sudo apt update
sudo apt upgrade
## 命令安装
apt --fix-broken install
su 密码 user@****** 

安装.deb
sudo dpkg -i 文件名
## 用户组 group
### 查看已有用户组
cat /etc/group
添加<user>到<group>中，再reboot
sudo usermod -aG <group> <user>
### 查看用户所属用户组
groups [user]
不填 user 则默认为当前用户
## 终端
- 居中显示：gsettings set org.gnome.mutter center-new-windows true
- 打开终端快捷键：ctrl+alt+t
## Ping得通，但端口无法访问
关闭防火墙
systemctl stop firewalld // 停止
 systemctl disable firewalld // 禁用
## 软件安装 Deb
sudo dpkg -i
# 文件类
## 压缩&解压 tar
tar -tvf archive.tar
- -t: 列出归档文件中的内容
- -v: 显示详细输出，列出归档文件中的所有文件和目录
- -f: 指定要列出内容的归档文件的名称
tar -zxvf example.tar.gz
- -z: 表示要使用 gzip 解压归档文件。
## unzip
unzip file.zip
解压到当前目录
unzip file.zip -d path
解压到指定目录
unzip -P password file.zip # 输入解压密码
unzip -o file.zip # 覆盖任何已有文件
更多详细内容
# 网络类
curl 
-X
参数指定 HTTP 请求的方法。
curl -X POST https://www.example.com
-o
参数将服务器的回应保存成文件，等同于wget命令
curl -o filename https://www.example.com
-O
参数将服务器回应保存成文件，并将 URL 的最后部分当作文件名
curl -O https://www.example.com/file
-d
发送 POST 请求时附带的数据
curl -d "key1=value1&key2=value2" -X POST http://example.com/api