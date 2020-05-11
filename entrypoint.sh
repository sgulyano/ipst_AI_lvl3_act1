#!/bin/bash

# For a command line such as:
# "/home/jovyan/entrypoint.sh jupyter notebook --ip 0.0.0.0 --port 59537 --NotebookApp.custom_display_url=http://127.0.0.1:59537"
# strip out most args, just pass on the port

port="8888"

base_url=$JUPYTERHUB_SERVICE_PREFIX

voila /home/ipst/test_voila.ipynb --port=${port} --no-browser --Voila.base_url=${base_url}