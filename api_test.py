import requests

IVLE_URL = "https://ivle.nus.edu.sg/api/Lapi.svc/"
API_KEY = "bAbUg4vhpnzADp7DO9GU0"
MAX_TOKEN = "ACD2D0125D4006AE356EEF14220F0DD529420AB5E3B6C054FCEE296E24B058E98EE8439F4AF920E28A27DA3EA97B0CDEBB179D276D99FE7C8CF33FE5C1181178D6EB87E936DA1A6901585C4A5520E05B6C7F0C9A72CD96E017E62981828FE923BCB7CC3F0F3CBDF25BCD9727DF95DEC6F1630D8C6C0D1879F27B8630447AE208C599CE1826991C8785F0E53FF8B5DD13FD22CEAF401A9DDB612A2C9305A8DDCA6A1C01CD1FB2F1ADA3E440995DD739CE4DC17C40004FE77835DB2367323795D218F09183698224774487B977E148272440FC176B3701B99F383C987FFB4EE697CB7DD13ECFCF8121954C053488C65191"
KAIDI_TOKEN = "36C5E5A0DAEEEFFDE451284055243FD1BAC5B957FD6EF2708290B454946D7B3246D675ECDA538638ECB96E25934984BF8BFEB8AFF005B0A98C959C3D1BA146334AC33453117EF1F69AB5177AEF1EABBB6BAB8D73088FE46CB1D642A8563290866093F1667B6ECB991F3FCCCD54B1E7C08147369D34B1F091D983763C6A0B70FA89B5BA60802F32F86A9485CD655AFFC86081C316699E41271F2634F3FCB0E9CA418450F1BD66C7D0259B8A59FD8F5E364CA9F2CC7C070C2D84B23FFA88BD23BF48B4A4A1271C5430AAE4FCA78C9E541A26B1459C22684CC0C44906A11C1E0BF0C4FEE0849CFE2D615FA39BBDB10F3900"
# TOKEN = "5DE4D4472526A2EA778FC8688F8B5444CB0CEB0731E3FA933AA63EF2162EBBE1DA1B2A0F49E0E799F3CE9E09878570424B249024EE147C2C97EAFA67A5411ADCFFA0B62AC2566FAFD52335CC942302BA9A0727FAAECC4B7AA92E9A8E0D883A2A6AB4BB377FCA95ED7B01B7B81753880D49019AB837991E0FD3AA008DEA0D345B01EBDC5CBA97A9CC45D1644584DF387547063391E184C8617F3C1FDE0751CF07432F220452DEC9299D645941B750C0ACF52BF95751E9578AAB641B4ADF759221FB51589847109DCAE833B07B69B2F7A9A4E385DF5C0B7D9D718922BE3AABA326A45E54749C9B53FDA41E32EEA384C032"

param = {
    "APIKey": API_KEY,
    "AuthToken": KAIDI_TOKEN,
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
    "AuthToken": MAX_TOKEN,
    "AcadYear": "2017/2018",
    "Semester": 1

}
service = "MyOrganizer_AcadSemesterInfo"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("Acad year info")
print(resp.json())
print()

# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": MAX_TOKEN,
# }
# service = "Profile_View"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Profile_View")
# print(resp.json())
# print()
# #
# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "StudentID": "a0111614"
# }
# service = "Modules_Taken"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Modules_Taken")
# print(resp.json())
# print()
#
# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "Duration": 0,
#     "IncludeAllInfo": False,
#     "CourseID": "cca020d4-f6f7-4a0c-b7bd-734b8a86a01e"
#
# }
# service = "Modules"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Modules info")
# print(resp.json())
# print()
#
# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "Duration": 0,
#     "IncludeAllInfo": False
#
# }
# service = "Modules_Staff"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Modules_Staff")
# print(resp.json())
# print()
#
# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "Duration": 0,
#     "IncludeAllInfo": False
#
# }
# service = "Modules_Student"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Modules_Student")
# print(resp.json())
# print()
#
# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "CourseID": "4620451d-5c40-445d-bb79-f4d0825ff237"
#
# }
# service = "Class_Roster"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Class Roster")
# print(resp.json())
# print()
#
# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "AcadYear": "2017/2018",
#     "Semester": 1,
#     "CourseID": "cca020d4-f6f7-4a0c-b7bd-734b8a86a01e"
#
# }
# service = "GroupsByUserAndModule"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("GroupsByUserAndModule")
# print(resp.text)
# print()
#
# # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
# }
# service = "GroupsByUser"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("GroupsByUser")
# print(resp.text)
# print()

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

# param = {
#     "APIKey": API_KEY,
#     "AuthToken": TOKEN,
#     "CourseID": "cca020d4-f6f7-4a0c-b7bd-734b8a86a01e"
#
# }
# service = "Timetable_Student_Module"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Timetable_Student_Module")
# print(resp.json())
# print()
#
# # =======================================================

param = {
    "APIKey": API_KEY,
    "AuthToken": MAX_TOKEN,
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

param = {
    "APIKey": API_KEY,
    "AuthToken": MAX_TOKEN,
    "AcadYear": "2017/2018",
    "Semester": 1
}
service = "MyOrganizer_AcadSemesterInfo"
url = IVLE_URL + service
resp = requests.get(url, params=param)
print("MyOrganizer_AcadSemesterInfo")
print(resp.json())
print()

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
#
# # # =======================================================
#
# param = {
#     "APIKey": API_KEY,
#     "AuthToken": KAIDI_TOKEN,
#     "CourseID": "a9eb1fbf-75b7-4bd4-b88f-e06541a62373",
#     "Duration": 0
# }
# service = "Module_Lecturers"
# url = IVLE_URL + service
# resp = requests.get(url, params=param)
# print("Module_Lecturers")
# print(resp.text)
# print()
