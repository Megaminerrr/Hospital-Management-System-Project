class Schedule_Manager:
    def __init__(self,user_ID):
        self.user_ID = user_ID

    def getSchedule():
        #check user permission to view own schedule

        #fetch schedule data for user

    def getScheduleOf(user_ID):
        # check if user has permission to view relevant user's Schedule

        # fetch schedule data of user
        
    def setAppointment(Doctor, Patient, Room, Date, Time, Details):
        # check if user is the specified doctor or an admin
        
        # check if Room is available at specified Date and Time

        # Set Room as occupied
        
        # create new row for appointments, fill columns with given info

    def endAppointment(Appointment_ID, Treatment, Notes):
        # verify user is doctor of appointment or admin

        # verify Appointment exists

        # Create Medical Record with Appointment_ID, Treatment, and Notes

    def cancelAppointment(Appointment_ID):
        # verify user is patient of appointment, doctor of appointment or an admin

        # remove appointment from list

        # unreserve room for timeslot

        # notify Doctor and Patient of Appointment of cancelation

    def changeAppointment(Appointment_ID, Doctor, Patient, Room, Date, Time, Details):
        # verify is doctor of appointment or admin

        # modify/replace appointment with new details

        # notify doctor and patient of change

