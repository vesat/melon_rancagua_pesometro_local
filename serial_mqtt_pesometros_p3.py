import serial, time
import pymysql

import paho.mqtt.client as mqtt
#broker = "45.236.129.79"
broker="192.168.8.5"
port = 1883
client = mqtt.Client("movil_ranc", port)
lector = serial.Serial('/dev/ttyUSB0', 19200)

servidor='192.168.8.2'
usuario_serv='remoteTC'
contrasena_serv='xc%Tfg%'

db = pymysql.connect(host=servidor,user=usuario_serv,passwd=contrasena_serv,db="bd_melonaridosmovil",charset = "utf8" )
cur = db.cursor()

while True:
    cadena = lector.readline()
    # print(cadena.decode())
    if (cadena.decode() != ''):
        print(cadena.decode())  # cadena.decode()  es unicode
        cambio = cadena.decode()
        if cambio.find("Flujo") != -1:
            print("el el netooooooooooooooooo")

            inicio = cambio.find(" ")
            fin = cambio.find("t")

            print(cambio.find(" "))  # entrega la posicion donde esta :, es un entero
            print(len(cambio))
            # print(cambio[2:6]) #Tot Neto     :        0       , devuelve el t Ne
            print(cambio[inicio:fin])  # Tot Neto     :        0       , devuelve el t Ne
            print(type(cambio.find(":")))

            db2 = pymysql.connect(host=servidor, user=usuario_serv, passwd=contrasena_serv, db="bd_melonaridosmovil",charset="utf8")
            cur2 = db2.cursor()
            consulta = "INSERT INTO `pesometro` (`fecha`,`weight`) VALUES (now(), '" + str(cambio[inicio:fin]) + "')"
            print(consulta)
            cur2.execute(consulta)
            db2.commit()
            db2.close()


            client.connect(broker)
            client.publish("/melon/movil/Flujo", cambio[inicio:fin])
            client.disconnect()

        if cambio.find("Total 1") != -1:
            print("es el total 1")

            inicio = cambio.find(" ")
            fin = cambio.find("n")

            print(cambio.find(" "))  # entrega la posicion donde esta :, es un entero
            print(len(cambio))
            # print(cambio[2:6]) #Tot Neto     :        0       , devuelve el t Ne
            print(cambio[inicio + 2:fin - 2])  # Tot Neto     :        0       , devuelve el t Ne
            print(type(cambio.find(":")))
            db = pymysql.connect(host=servidor, user=usuario_serv, passwd=contrasena_serv, db="bd_melonaridosmovil",charset="utf8")
            cur = db.cursor()
            consulta = "INSERT INTO `pesometro` (`fecha`,`load1`) VALUES (now(), '"+str(cambio[inicio + 2:fin - 2])+"')"
            print(consulta)
            cur.execute(consulta)
            db.commit()
            db.close()

            client.connect(broker)
            client.publish("/melon/movil/Total1", cambio[inicio + 2:fin - 2])

        # print(type(cambio))
        print("+" * 100)
    time.sleep(1)

lector.close()
