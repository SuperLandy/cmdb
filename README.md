## IT资产管理系统
![图例](https://github.com/SuperLandy/cmdb/blob/master/example.png)

# 说明  
\$ 开头的行表示需要执行的命令  

## 环境
系统: CentOS 7  
目录: /opt  
数据库: mariadb  
web： nginx  

## 开始安装
$ systemctl start firewalld  
$ firewall-cmd --zone=public --add-port=80/tcp --permanent  
$ firewall-cmd --reload  # 重新载入规则  
$ setenforce 0  
$ sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config  

## 安装依赖包
$ yum -y install wget gcc epel-release git nginx  

# 安装 Mariadb
$ yum -y install mariadb mariadb-devel mariadb-server MariaDB-shared  
$ systemctl enable mariadb  
$ systemctl start mariadb  

# 创建数据库 Cmdb 并授权
$ DB_PASSWORD=`iamadmin`  # 设置数据库密码  
$ mysql -uroot -e "create database cmdb default charset 'utf8'; grant all on cmdb.* to \
'cmdb'@'127.0.0.1' identified by '$DB_PASSWORD'; flush privileges;"  

## 安装 Python3.6
$ yum -y install python36 python36-devel  

## 配置并载入 Python3 虚拟环境
$ cd /opt  
$ python3.6 -m venv py3  # py3为虚拟环境名称, 可自定义  
$ source /opt/py3/bin/activate  # 退出虚拟环境可以使用 deactivate 命令  

## 看到下面的提示符代表成功
$ (py3) [root@localhost py3]  

## 下载IT资产管理系统
$ cd /opt/  
$ git clone --depth=1 https://github.com/SuperLandy/cmdb.git  

## 安装 Python 库依赖
$ pip install --upgrade pip setuptools  
$ pip install -r /opt/cmdb/requirements.txt  

## 修改 cmdb 数据库配置文件
$ cd /opt/cmdb/cmdb/  
$ cp settings_example.py settings.py  
$ vi settings.py  
##### DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'cmdb',  
        'USER': 'cmdb',  
        'PASSWORD': 'cmdb',  
        'HOST': '127.0.0.1',  
        'PORT': '3306',  
    }  
 }  

## 配置nginx
$ vi /etc/nginx/conf.d/cmdb.conf
#### server {
        listen 80;
        server_name www.example.com;
        location ~/static {
                root  /opt/cmdb/;
        }
        location / {
                index index.html;
                proxy_pass http://127.0.0.1:8080;
        }
}

## 启动项目
$ chmod +x /opt/cmdb/start.sh  
$ /opt/cmdb/start.sh  
$ systemctl start nginx

## 创建超级管理员
$ cd /opt/cmdb/cmdb
$ source /opt/py3/bin/activate
$ python manage.py createsuperuser #根据提示输入账号密码

## 更新
$ cd /opt/cmdb/ && git pull
