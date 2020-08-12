#!/bin/bash

cd /usr/local/bin/melon_rancagua

while true
do
        /usr/local/bin/melon_rancagua/venv/bin/python serial_mqtt_pesometro.py
        sleep 5
done
