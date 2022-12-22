#!/bin/bash

# Expects the following project strcuture:
# /opt/stargazer/StargazerSetup/stargazer/start_stargazer.sh
# /opt/stargazer/StargazerSetup/stargazer/init/*.py
# /opt/stargazer/logs/*.log
# /opt/stargazer/repos/AlpacaServer/
# /opt/stargazer/repos/StargazerServer-AlpacaClient/

echo -e "Creating soft link to /dev/serial0"
ln -sf /dev/ttyS0 /dev/serial0

if [[ -z "${SKIP_SWARM_PICO_SETUP}" ]]; then
  echo -e "Setting swarm message rates, obtaining latitude, sending to pico, and waiting for pico setup.\nCheck /opt/stargazer/logs/swarm_init.log"
  # start python in background, pipe output into log
  echo -e "\n\n***STARTING INIT PROCESS at: $(date)***\n" | tee -a /opt/stargazer/logs/swarm_pico_init.log >> /opt/stargazer/logs/master_log.log
  python -u /opt/stargazer/StargazerSetup/stargazer/init/swarm_pico_init.py | tee -a /opt/stargazer/logs/swarm_pico_init.log >> /opt/stargazer/logs/master_log.log &
  wait $!
else
  echo -e "Skipping swarm and pico setup. \nCheck /opt/stargazer/logs/swarm_init.log"
fi

echo -e "Swarm and pico setup complete. Starting django server.\nCheck /opt/stargazer/logs/django_server.log"
echo -e "\n\n***STARTING DJANGO PROCESS at: $(date)***\n" | tee -a /opt/stargazer/logs/django_server.log >> /opt/stargazer/logs/master_log.log

# start django server in background, pipe output into log
python -u /opt/stargazer/repos/AlpacaServer/manage.py runserver | tee -a /opt/stargazer/logs/django_server.log >> /opt/stargazer/logs/master_log.log &
# TODO change from sleeping
sleep 2
echo -e "Django started successfully. Starting StargazerServer-AlpacaClient.\nCheck /opt/stargazer/logs/stargazer_server-alpaca_client.log"
echo -e "\n\n***STARTING STARGAZERSERVER-ALPACACLIENT PROCESS at: $(date)***\n" | tee -a /opt/stargazer/logs/stargazer_server.log >> /opt/stargazer/logs/master_log.log
python -u /opt/stargazer/repos/StargazerServer-AlpacaClient/main.py | tee -a /opt/stargazer/logs/stargazer_server.log >> /opt/stargazer/logs/master_log.log &

tail -f /opt/stargazer/logs/stargazer_server.log
