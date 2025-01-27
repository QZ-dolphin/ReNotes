# Git 教程简单版
## 目标
远程 pull github中的该笔记至本地库，并实现同步。

## 步骤
### 下载软件
https://git=scm.com/downloads/win
需要用梯子下载 Standalone Installer版本
### 创建 ssh key
在⽤户主目录下，看看有没有.ssh⺫录，如果有，再看看这个⺫录下 有没有id_rsa和id_rsa.pub这两个⽂件，如果已经有了，可直接跳到下⼀步。如果没有，打开Shell（Windows下打开Git Bash），创建SSH Key：

```bash
ssh-keygen -t rsa -C "troyartum@outlook.com"
```
然后⼀路回⻋，使⽤默认值即可。

### 添加 ssh key

> 点击头像->点击`setting`

![setting](pics/3.png)

> 点击 `SSH and GPG keys`

![sshkeys](pics/4.png)

> 点击`New SSH key`

![new](pics/5.png)

> 填上任意Title，在Key⽂本框⾥粘贴id_rsa.pub⽂件的内容

![add](pics/6.png)

### 初始化文件夹
打开要存放文件的文件夹，打开Git Bash，输入
```Bash
git config --global user.name "qingzhen_laptop"
git config --global user.email "troyartum@outlook.com"

git init
```

### 复制笔记ssh地址
> 点击`code`

![code](pics/1.png)

> 复制`ssh`

![ssh](pics/2.png)

### 克隆笔记仓库
在要存放文件的文件夹，打开Git Bash，输入
```Bash
git clone git@github.com:QZ-dolphin/ReNotes.git
```
### 切换电脑时
先pull github中最新的文件，再编辑本地，再push。
```Bash
git pull

git push origin
```