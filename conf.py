#dbinfo
dbuser='webpy'
dbpw='webpy'
dbname='simplecd'
#sqlite2mysql
#  ----------------------------------------------------
#  sqlite3 verycd.sqlite3.db .dump .exit > verycd.dump
#  ----------------------------------------------------
#  sed -i 's/INSERT INTO "verycd"/INSERT INTO `verycd`/g;/COMMIT/d;/BEGIN TRANSACTION/d;/CREATE INDEX/d' verycd.dump
#  #because different treat on \, may need further adjustment @@
#  ----------------------------------------------------
#  mysql -u root -p
#  mysql> create schema simplecd;
#  mysql> FLUSH PRIVILEGES;
#  mysql> use simplecd;
#  mysql> grant all privileges on simplecd to 'webpy'@'localhost' identified by 'webpy' with grant option;
#  mysql> grant all privileges on simplecd.* to 'webpy'@'localhost' identified by 'webpy' with grant option;
#  mysql> exit;
#  ---------------------------------------------------
#  mysql -u webpy -p simplecd < verycd.dump
#  ---------------------------------------------------
#  mysql -u webpy -p simplecd
#  mysql> create table verycd2c(verycdid integer primary key,content text);
#  mysql> create table verycd2( verycdid integer primary key,title text,status text,brief text,pubtime text,updtime text,category1 text,category2 text,ed2k text);
#  mysql> replace into verycd2 select verycdid,title,status,brief,pubtime,updtime,category1,category2,ed2k from verycd;
#  mysql> replace into verycd2c select verycdid,content from verycd;
#  #done
