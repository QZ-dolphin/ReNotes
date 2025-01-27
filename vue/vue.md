# Vue 学习总结
## 创建项目--基础
```bash
npm --version # 查看版本
npm create@latest # 创建项目
npm get registry # 查看镜像源
npm set registry http://registry.npmmirror.com # 设置镜像源

npm install 包名 # 会自动将下载的包信息注册到package.json文件中
```
当已有package.json时，输入
```bash
npm install
```
即可安装所有所需的包