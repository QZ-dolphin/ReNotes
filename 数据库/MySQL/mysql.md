## 安装mysql
- mac版
社区版`.dmg`安装包[下载链接](https://dev.mysql.com/downloads/mysql/)
安装导航时，需设置密码大于8位数，root用户

## 自动启用
启用

```bash
sudo /usr/local/mysql/support-files/mysql.server start
```
退出
```bash
sudo /usr/local/mysql/support-files/mysql.server stop
```

## 登陆
```bash
mysql -u root -p
```
## 连接设置
```sql
USE mysql;
UPDATE user SET host = '%' WHERE user = 'root';
SELECT host, user FROM user;
```

无论是homebrew等方式，在Mac下都是不会生成my.cnf文件，因为已经使用了最优默认值，如果需要也可以自行新建或配置/etc/my.cnf
## 安装dbeaver
- [社区版下载](https://dbeaver.io/download/)
- 