def setAddress(address,country,city,province,street,postalCode):
    address.country = country
    address.city = city
    address.province = province
    address.street = street
    address.postalCode = postalCode

def setSchool(school,name,address,email,phoneNumber,adminAccessKey,teacherAccessKey):
    school.name = name
    school.address = address
    school.email = email
    school.phoneNumber = phoneNumber
    school.adminAccessKey = adminAccessKey
    school.teacherAccessKey = teacherAccessKey

def setSchedule(schedule,name,currentAdmin,start_date,end_date):
    schedule.school = currentAdmin.school
    schedule.name = name
    schedule.administrator = currentAdmin
    schedule.start_date = start_date
    schedule.end_date = end_date

def setSittingPlan(sittingPlan,schedule,schoolClass,student,deskNumber):
    sittingPlan.schedule=schedule
    sittingPlan.schoolClass=schoolClass
    sittingPlan.student=student
    sittingPlan.deskNumber=deskNumber