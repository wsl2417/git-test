import pymysql

try:
    pymysql.connect(
    host='192.168.0.21',
    user='dev_casamiel',
    password='Vv7XaBvQagWIo7NB',
    database='dev_casamiel_db',
    port=1433
)
except pymysql.err.OperationalError as e:
    print("Error: %s" % e)
    # pymysql.err.OperationalError