import requests

IVLE_URL = "https://ivle.nus.edu.sg/api/Lapi.svc/"
API_KEY = "bAbUg4vhpnzADp7DO9GU0"
TOKEN = "CA4D4789F4EB325345562439992BCB0946F0CE922B574795C9BE19C1F0CAEC56A51847029F85A91D834C3CA6C99B1C7FFD3DF01E79811E4451E4561C0DFCE592F1F9DB4F11B0AF9880400942798A3BC6606F533C654990F0CE6DF4A6E0628706C1619B43E595A9BFA103710D46FF8377B87565A5EB51A1BFD47060D7603686F417DAE78615C5301DA600DDE3BAD058A7C6DFEA0764164CA5C7702C2EF66BFF08426965F03C3A2B1B7F143F3AF6004ABD4AD03DAB8B40ED9710B05A37917B3B521069C8858E32E2011F8698BBFBB99D3C32D88504F29AFEDB848A37AD4869FEF41BABC03CA0751CC929EF9634622948B6"
# TOKEN = "5DE4D4472526A2EA778FC8688F8B5444CB0CEB0731E3FA933AA63EF2162EBBE1DA1B2A0F49E0E799F3CE9E09878570424B249024EE147C2C97EAFA67A5411ADCFFA0B62AC2566FAFD52335CC942302BA9A0727FAAECC4B7AA92E9A8E0D883A2A6AB4BB377FCA95ED7B01B7B81753880D49019AB837991E0FD3AA008DEA0D345B01EBDC5CBA97A9CC45D1644584DF387547063391E184C8617F3C1FDE0751CF07432F220452DEC9299D645941B750C0ACF52BF95751E9578AAB641B4ADF759221FB51589847109DCAE833B07B69B2F7A9A4E385DF5C0B7D9D718922BE3AABA326A45E54749C9B53FDA41E32EEA384C032"

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "AcadYear": "2017/2018",
    "Semester": 1

}
service = "Timetable_Student"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Timetable")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "AcadYear": "2017/2018",
    "Semester": 1

}
service = "MyOrganizer_AcadSemesterInfo"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Acad year info")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
}
service = "Profile_View"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Profile_View")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "StudentID": "a0111614"
}
service = "Modules_Taken"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Modules_Taken")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "Duration": 0,
    "IncludeAllInfo": False,
    "CourseID": "cca020d4-f6f7-4a0c-b7bd-734b8a86a01e"

}
service = "Modules"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Modules info")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "Duration": 0,
    "IncludeAllInfo": False

}
service = "Modules_Staff"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Modules_Staff")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "Duration": 0,
    "IncludeAllInfo": False

}
service = "Modules_Student"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Modules_Student")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "CourseID": "4620451d-5c40-445d-bb79-f4d0825ff237"

}
service = "Class_Roster"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Class Roster")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "AcadYear": "2017/2018",
    "Semester": 1,
    "CourseID": "cca020d4-f6f7-4a0c-b7bd-734b8a86a01e"

}
service = "GroupsByUserAndModule"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("GroupsByUserAndModule")
print(resp.text)
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    # "AuthToken": TOKEN,
}
service = "GroupsByUser"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("GroupsByUser")
print(resp.text)
print()

# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "CourseID": "cca020d4-f6f7-4a0c-b7bd-734b8a86a01e",
#     "flag": "A"
#
# }
# service = "Module_ClassGroups"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Module_ClassGroups")
# print(resp.json())
# print()
#
# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "AcadYear": "2017/2018",
#     "Semester": 1
#
# }
# service = "Module_ClassGroupUsers"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Module_ClassGroupUsers")
# print(resp.json())
# print()
#
# # =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "CourseID": "cca020d4-f6f7-4a0c-b7bd-734b8a86a01e"

}
service = "Timetable_Student_Module"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Timetable_Student_Module")
print(resp.json())
print()

# =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": TOKEN,
    "CourseID": "cca020d4-f6f7-4a0c-b7bd-734b8a86a01e",
    "ModuleCode": "ST2132",
    "GroupName": "SL1",
    "AcadYear": "2017/2018",
    "Semester": 1,
    "GroupType": "LECTURE"
}
service = "Module_OfficialGroupUsers"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Module_OfficialGroupUsers")
print(resp.text)
print()

# =======================================================

# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "AcadYear": "2017/2018",
#     "Semester": 1
#
# }
# service = "MyOrganizer_AcadSemesterInfo"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Acad year info")
# print(resp.json())
# print()

# =======================================================

# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "AcadYear": "2017/2018",
#     "Semester": 1
# }
# service = "MyOrganizer_AcadSemesterInfo"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("MyOrganizer_AcadSemesterInfo")
# print(resp.json())
# print()

# # =======================================================
#
# param = {
#     "APIKey": API_KEY
# }
# service = "CodeTable_WeekTypes"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("CodeTable_WeekTypes")
# print(resp.json())
# print()
