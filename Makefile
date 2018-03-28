
MYSQL_BASE=/remote/pv/server/mysql
HTTPSQS=/u/szhang/bin/httpsqs
mysqld = /depot/mysql-5.1.23/bin/mysqld_safe

PYTHONPATH = /u/jingqi/opt/python/lib/python2.7/site-packages

help:
	@ echo make osqa-mysqld
	@ echo make osqa-httpd

osqa-mysqld:
	$(mysqld) --defaults-file=/depot/mysql-5.1.23/share/mysql/my-huge.cnf \
	  --datadir=$(MYSQL_BASE)/external/data \
	  --pid-file=$(MYSQL_BASE)/external/mysql.pid \
          --log-error=$(MYSQL_BASE)/external/log/mysql.err \
	  --plugin_dir=$(MYSQL_BASE)/lib/plugin &

osqa-httpd:
	cd /u/phyan/workspace/xtage-dev && env LD_LIBRARY_PATH=/depot/python/lib:$$LD_LIBRARY_PATH PYTHONPATH=$(PYTHONPATH) \
	  /remote/pv/server/bin/apachectl -f /remote/us01home40/phyan/workspace/xtage-dev/conf/httpd.pvicc004.conf -k start
osqa-httpd-stop:
	cd /u/phyan/workspace/xtage-dev && env LD_LIBRARY_PATH=/depot/python/lib:$$LD_LIBRARY_PATH PYTHONPATH=$(PYTHONPATH) \
	  /remote/pv/server/bin/apachectl -f /remote/us01home40/phyan/workspace/xtage-dev/conf/httpd.pvicc004.conf -k stop
osqa-httpd-restart:
	cd /u/phyan/workspace/xtage-dev && env LD_LIBRARY_PATH=/depot/python/lib:$$LD_LIBRARY_PATH PYTHONPATH=$(PYTHONPATH) \
	  /remote/pv/server/bin/apachectl -f /remote/us01home40/phyan/workspace/xtage-dev/conf/httpd.pvicc004.conf -k restart

