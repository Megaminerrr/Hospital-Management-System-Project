import sqlite3

# 1 - can view own
# 2 - can view/edit own   - works as request for pAppointment
# 3 - can view patient's
# 4 - can view/edit patient's - works as reserve room for pRoom
# 5 - can view any
# 6 - can view/edit any
conn = sqlite3.connect("permissions_database.db") # need to replace this with the actual database name
cursor.execute("""CREATE TABLE IF NOT EXISTS Permissions (
PermissionsID VARCHAR(3) NOT NULL PRIMARY KEY,
pProfile INTEGER NOT NULL,
pSchedule INTEGER NOT NULL,
pAppointment INTEGER NOT NULL,
pTreatment INTEGER NOT NULL,
pBilling INTEGER NOT NULL,
pRoom INTEGER NOT NULL
)""")


class User_Permissions:
    def __init__(self,User_ID,Permissions_Type,):
        self.User_ID = User_ID
        self.Permissions_Type = Permissions_Type

    def CheckPerm(Perm_Type):
        cursor.execute("""SELECT ? FROM Permissions WHERE PermissionsID = """, (Perm_Type, self.User_ID))
        result = cursor.fetchone()
        return result[0] if result else 0

