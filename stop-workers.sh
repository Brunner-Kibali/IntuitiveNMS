ps -ef | grep intuitiveNMS_worker | grep -v grep | awk '{print $2}' | xargs sudo kill
