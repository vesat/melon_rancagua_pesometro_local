import serial, time

import paho.mqtt.client as mqtt
broker = "45.236.129.79"
port = 1883
client = mqtt.Client("movil_ranc", port)
lector = serial.Serial('/dev/ttyUSB0', 19200)
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

            client.connect(broker)
            client.publish("/melon/movil/Total1", cambio[inicio + 2:fin - 2])

        # print(type(cambio))
        print("+" * 100)
    time.sleep(1)

lector.close()