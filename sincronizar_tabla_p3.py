##para python3
import pymysql

def synctable(sync_col, sync_table, sync_table_2, all_cols, extra_where, limit):
    ret = False
    ##remoto, leo el ultimo dato id
    clientdb = pymysql.connect(host="3.91.208.3", user="user_devel_89", passwd="mAN8dv7m6TY", db="bd_melonaridosrancagua", port=3306)
    lcur = clientdb.cursor()
    lcur.execute("SELECT " + sync_col + " FROM " + sync_table_2 + " ORDER BY " + sync_col + " DESC LIMIT 1")
    clientlast = "0"
    for lrow in lcur:
        clientlast = str(lrow[0])
        break
    print(f"  el ultimod dato es {clientlast}")
    lcur.close()
    clientdb.close()
    print("CLOUD SQL (" + sync_table + ") CLIENT LAST " + sync_col + ": " + clientlast)
    buf = ""
    ##fuente de datos
    #vesatdb = pymysql.connect(host="10.8.0.38", user="remoteTC",passwd="xc%Tfg%", db="bd_melonaridosmovil")
    vesatdb = pymysql.connect(host="192.168.8.2", user="remoteTC", passwd="xc%Tfg%", db="bd_melonaridosmovil")

    rcur = vesatdb.cursor()
    rcur.execute("SELECT " + all_cols +
                 " FROM " + sync_table + " WHERE " + sync_col + " > '" + clientlast + "' " + extra_where +
                 " ORDER BY id ASC LIMIT " + str(limit))
    print(type(rcur))
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
    print(len(buf))
    rcur.close()
    vesatdb.close()
    if len(buf) > 0:
        ret = True
        clientdb = pymysql.connect(host="3.91.208.3", user="localvesatuser", passwd="070GITOOITU012tdotrwc024GTGFAE007wawftdotr700",
                                   db="bd_melonaridosrancagua", port=3306)
        lcur = clientdb.cursor()
        print("INSERT INTO " + sync_table_2 + " (" + all_cols + ") VALUES ")
        lcur.execute("INSERT INTO " + sync_table_2 + " (" + all_cols + ") VALUES " + buf)

        clientdb.commit()
        lcur.close()
        clientdb.close()
    return ret


while synctable("id", "pesometro", "pesometro","id,fecha,fechaInt,weight,rate,speed,load1,rssi,periodo", "", 500000):
    pass
