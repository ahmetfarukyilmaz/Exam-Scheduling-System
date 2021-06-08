
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