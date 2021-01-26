ip=$(hostname -I)
echo starting sdwan-sim with host IP address: ${ip}
cd ~/PycharmProjects/intuitiveNMS
python3 intuitiveNMS/sim/sim_main.py -intuitiveNMS=${ip}
