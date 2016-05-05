
```
  注意：本wiki和simplecd网站的源码已经差别很大，架设完毕的网站是无评论无图精简版
```
# SimpleCD使用方法 #

## 1.需求: ##
所有可以架设web.py的地方，例如：
  * 一个VPS(Virtual Dedicated Server)(参考[Xen和OpenVZ测试（附VPS推荐）](http://obmem.com/?p=296))
  * 一个支持web.py的国外共享主机(例如[dreamhost架设web.py攻略](http://wiki.dreamhost.com/index.php/Web.py))
  * 一个支持web.py的国内共享主机(例如[stdyun.com架设web.py攻略](http://wiki.woodpecker.org.cn/moin/stdyun))

推荐配置：
  * Xen VPS 需要至少768MB内存的Linux VPS
  * OpenVZ VPS 需要Burstable内存至少512MB内存的Linux VPS，基本内存可以小一点没问题。

内存太少的解决方法：
  * 修改nginx/spawn-fcgi.sh中"-F 2"改为"-F 1"，只使用一个守护进程
  * 重新写一个资源占用较低的框架来存取sqlite3。sqlite3直接存取占内存不大。
  * **不要\*试图用mysql来取代sqlite，mysql效率更低**

本教程基于操作系统Ubuntu 9.04
由于玩VPS的都非善类，相信其他操作系统的架设都能自己解决

## 2.修改软件源 ##
我们要用新软件，所以直接修改/etc/apt/sources.list
把其中的jaunty改为karmic，用9.10的软件源 :)

然后更新一下
```
apt-get update
```

接下来分别安装nginx，spawn-fcgi，和mercurial
```
apt-get install nginx
apt-get install spawn-fcgi
apt-get install mercurial
```

再接下来是easy\_install的安装，以及安装web.py和flup

_以下注意web.py只能用0.33版的，自己下载了编译吧_

```
apt-get install python-setuptools
~~easy_install web.py~~
easy_install flup
```

## 3. 简易架设攻略 ##
下载源码
```
cd /var/www
hg clone https://simplecd.googlecode.com/hg simplecd
cd simplecd
hg update dev-sqlite
```

注：分支建议采用dev-sqlite，这个和目前网站的代码最为相似

deployment分支继续不变，因为deployment分支代码简单看起来爽一点。


接下来做一些基本的配置
```
#创建数据库
./fetchvc.py createdb 

#nginx的配置文件(请根据视频进行相应修改)
cp nginx/nginx.conf /etc/nginx/
cp nginx/simplecd /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/simplecd /etc/nginx/sites-enabled/simplecd

#用spawn-fcgi开fcgi
nginx/spawn-fcgi.sh

#开启nginx服务
/etc/init.d/nginx start

```

好了，大功告成，访问vps的地址看看，应该已经架设完毕了

## 4.simplecd的使用 ##

### 一些数据库的更新方法： ###
上一步中的数据库还是空的，必须下载数据库，数据库更新方法如下
```
./fetchvc.py feed #按照feed更新数据库
./fetchvc.py update #更新主页的前20页数据
./fetchvc.py fetch q=海猫 #在verycd搜索所有关于海猫的内容并更新到数据库
./fetchvc.py fetch TopicID #直接更新topicid
./fetchvc.py fetchall #更新全部数据库，建议还是不要尝试为好
./fetchvc.py fetch 1000-1001 #更新verycd的archives页面第1000页到1001页的内容
```

### 下载全数据库(截止2009.12.18) ###
eMule链接：

ed2k://|file|verycd.sqlite3.db.lzma|233121378|0fd38cff1353e996576f9f3e9b8c65dd|

解压: lzma -d verycd.sqlite3.db.lzma

然后放入simplecd目录即可

### 设置自动更新 ###
想让simplecd自动和VeryCD保持同步？

试试看dev-sqlite branch的scdd.py:
```
hg update dev-sqlite
python scdd.py start
```
每隔15分钟看一下，如果成功的话应该已经有自动更新了

### 为什么simplecd.org的主页和deployment不一致？ ###
simplecd.org上有些特殊的设置，所以我没有让它与本源代码同步，而是同步到另一个目录，作出一些调整，然后复制到目标目录。

要尝试新界面和新功能你可以试试看dev-sqlite branch:
```
hg update dev-sqlite
```
**注意**：dev branch使用mysql数据库，这个版本因为性能问题我已经终止开发，原有代码保留，以备以后需要时用。

### 为什么翻页很慢？ ###
原始数据库貌似没有使用索引

使用以下方法添加索引(deployment分支只用前两个索引，其他分支需要全部)：
```
bash>sudo apt-get install sqlite3
bash>sqlite3 verycd.sqlite3.db
sqlite>create index idx1 on verycd (updtime);
sqlite>create index idx2 on verycd (updtime,title);
sqlite>create index idx4 on verycd (category1,updtime,title);
```