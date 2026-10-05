import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shailesh1",
    database="ScholarshipFinancialAidDB"
)

print("Connected to MySQL successfully!")

connection.close()
print("Connection closed.")