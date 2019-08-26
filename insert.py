from database import Database
database = Database("alert_db.db")

for i in range(100):
    database.insert(15, "C:\\Users\\Nurts\\Pictures\\test_bit.jpg")