cd ~/PycharmProjects/intuitiveNMS
python3 intuitiveNMS/workers/intuitiveNMS_worker.py -H ${1:-15} -W capture -Q 192.168.123.17 -S 5CD8095MMW -C rabbitmq &
python3 intuitiveNMS/workers/intuitiveNMS_worker.py -H ${1:-15} -W portscan -Q 192.168.123.17 -S 5CD8095MMW -C rabbitmq &
python3 intuitiveNMS/workers/intuitiveNMS_worker.py -H ${1:-15} -W traceroute -Q 192.168.123.17 -S 5CD8095MMW -C rabbitmq &