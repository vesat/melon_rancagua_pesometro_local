#!/bin/bash
cd /home/pi/sinc_datos_pesometros/melon_rancagua_pesometro_local
while true
do
	python /home/pi/sinc_datos_pesometros/melon_rancagua_pesometro_local/venv/bin/python sincronizar_tabla_p3.py
	sleep 5
done
