#!/bin/bash
set -e


# TO DO
export PYTHONPATH=$PYTHONPATH:/home/$user/src

# Start Supervisor
sudo -E supervisord -n -c /etc/supervisord.conf
