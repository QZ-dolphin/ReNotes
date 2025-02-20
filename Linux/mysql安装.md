# mysql 在线安装(ubuntu版)
## 安装
```shell
# 查看可使用的安装包
sudo apt search mysql-server

# 安装最新版本
sudo apt install -y mysql-server
# 安装指定版本
sudo apt install -y mysql-server-8.0

# 如果不加-y 会在安装过程中，系统将提示你设置MySQL的root密码。
# 确保密码足够强，且记住它，因为你将在以后需要用到它。
# 所以还是不加吧
```
## 启动服务
安装完成后，MySQL服务会自动启动，未启动则使用以下命令启动MySQL服务
```shell
sudo systemctl start mysql
```
设置开机启动
```shell
sudo systemctl enable mysql
```
检查是否运行
```shell
sudo systemctl status mysql
```
## 修改密码、权限
查看原始密码
```shell
sudo cat /etc/mysql/debian.cnf
```
修改密码
```shell
# 登录 mysql
mysql -uroot -p
# 输入原始密码
# 设置密码 mysql8.0
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '新密码';
```
实现所有IP都能访问
```shell
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
```
找到并修改 `bind-address            = 0.0.0.0`
重启mysql
```shell
sudo systemctl restart mysql
```

## 远程连接报错
> 连接失败！null, message from server: “Host ‘xxxx‘ is not allowed to connect to this MySQL server“
> Error: Error 1698 (28000): Access denied for user 'root'@'172.17.0.2

解决方法：
连接数据库，这里以默认用户名密码为例
1. mysql -uroot -p密码
2. show databases;
3. use mysql;
4. select user,host from user;//可以看到user为root，host为localhost的话，说明mysql只允许本机连接，那么外网，本地软件客户端就无法连接了。
5. update user set host='%' where user='root';
6. GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
7. flush privileges;//刷新权限