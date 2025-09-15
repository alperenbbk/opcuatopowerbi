import time
import pyodbc
from opcua import Client


opc_url = "opc.tcp://192.168.0.1:4840"  
client = Client(opc_url)
client.connect()
print("OPC UA conn succesfull")

node = client.get_node("ns=3;s=\"Start_Button\"")

connection_string = (
  "Driver= {ODBC Driver 18 for SQL Server};"
  "Server=tcp:provisioningforrbplc01.database.windows.net,1433;"
  "Database=plcssqlpowerbi;"
  "Uid=PLCtoCloud;"
  "Pwd=<Your_Specified_Password>;"
  "Encrypt=yes;"
  "TrustServerCertificate=no;"
  "Connection Timeout=30;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
print("Azure SQL conn succesfull")

while True:
    try:
     
        value = node.get_value()
        print("Start_Button =", value)

        
        cursor.execute(
            "INSERT INTO mytable (TagName, TagValue) VALUES (?, ?)",
            ("Start_Button", str(value))   
        )
        conn.commit()
        print("SQL'sended ", value)

        time.sleep(5)  
    except Exception as e:
        print("err:", e)
        break


cursor.close()
conn.close()

client.disconnect()
