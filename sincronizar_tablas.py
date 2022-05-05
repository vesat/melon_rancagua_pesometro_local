##para python2
import MySQLdb

def synctable(sync_col, sync_table, sync_table_2, all_cols, extra_where, limit):
    ret = False
    ##remoto, leo el ultimo dato id
    clientdb = MySQLdb.connect(host="45.236.129.79", user="RemDevelop", passwd="xc%Tfg%", db="topcolor", port=3306)
    lcur = clientdb.cursor()
    lcur.execute("SELECT " + sync_col + " FROM " + sync_table_2 + " ORDER BY " + sync_col + " DESC LIMIT 1")
    clientlast = "0"
    for lrow in lcur:
        clientlast = str(lrow[0])
        break
    lcur.close()
    clientdb.close()
    print("CLOUD SQL (" + sync_table + ") CLIENT LAST " + sync_col + ": " + clientlast)
    buf = ""
    vesatdb = MySQLdb.connect(host="127.0.0.1", user="localvesatuser",
                              passwd="070GITOOITU012tdotrwc024GTGFAE007wawftdotr700", db="topcolor")
    rcur = vesatdb.cursor()
    rcur.execute("SELECT " + all_cols +
                 " FROM " + sync_table + " WHERE " + sync_col + " > '" + clientlast + "' " + extra_where +
                 " ORDER BY id ASC LIMIT " + str(limit))
    for rrow in rcur:
        if len(buf) > 0:
            buf += ","
        buf += "(";
        xmax = len(all_cols.split(','))
        xcur = 0
        while xcur < xmax:
            if xcur > 0:
                buf += ","
            if rrow[xcur] is None:
                buf += "NULL"
            else:
                buf += "'" + str(rrow[xcur]) + "'"
            xcur = xcur + 1
        buf += ")";
    rcur.close()
    vesatdb.close()
    if len(buf) > 0:
        ret = True
        clientdb = MySQLdb.connect(host="45.236.129.79", user="RemDevelop", passwd="xc%Tfg%", db="topcolor", port=3306)
        lcur = clientdb.cursor()
        lcur.execute("INSERT INTO " + sync_table_2 + " (" + all_cols + ") VALUES " + buf)
        clientdb.commit()
        lcur.close()
        clientdb.close()
    return ret


while synctable("id", "linea_7_modbus_tcp", "linea_7_modbus_tcp",
                "id,fecha,r40001,r40003,r40005,r40007,r40009,r40011,r40013,r40015,r40017,r40019" +
                ",r40021,r40023,r40025,r40027,r40029,apagado", "", 500):
    pass

while synctable("id", "linea_7_detenciones", "linea_7_detenciones",
                "id,inicio,inicio_date,inicio_time,fin,fin_date,fin_time,motivo,comentario", "", 500):
    pass

while synctable("id", "linea_7_producto", "linea_7_producto",
                "id,tiempo,masa_linea,tiempo_real,flujo_medio,kcm1_masa_linea,kcm1_linea,kcm1_flujo_medio,kcm2_masa_linea," +
                "kcm2_linea,kcm2_flujo_medio,kcm3_masa_linea,kcm3_linea,kcm3_flujo_medio,nro_datos,set_KV,set_kcm1,set_kcm2,set_kcm3",
                "", 500):
    pass