import pandas as pd
from suds.client import Client
import os
from dotenv import load_dotenv
import json

load_dotenv()

SOAPUI_LYTX_USERNAME = os.getenv('SOAPUI_LYTX_USERNAME')
SOAPUI_LYTX_PASSWORD = os.getenv('SOAPUI_LYTX_PASSWORD')


def LYTX_Login_SOAPUI():
        LYTX_Login_URL = "https://services-sd05.drivecam.com/HSServicesAPI/AuthenticationService/V1/AuthenticationService.svc?WSDL"
        LYTX_Login_Client = Client(LYTX_Login_URL)
        login_request = LYTX_Login_Client.factory.create('ns2:LoginRequest')
        login_request.Username = SOAPUI_LYTX_USERNAME
        login_request.Password = SOAPUI_LYTX_PASSWORD
        login_response = LYTX_Login_Client.service.Login(login_request)
        return(login_response)

def LYTX_GetIndividualVehicle_SOUPUI(vehicleId, login_response):
        LYTX_GetIndividualVehicle_URL = "https://services-sd05.drivecam.com/HSServicesAPI/VehicleService/V1/VehicleService.svc?WSDL"
        LYTX_GetIndividualVehicle_Client = Client(LYTX_GetIndividualVehicle_URL)
        GetIndividualVehicle_request = LYTX_GetIndividualVehicle_Client.factory.create('ns2:GetVehicleRequest')
        GetIndividualVehicle_request.SessionId = login_response.SessionId
        GetIndividualVehicle_request.GroupId = login_response.HomeGroupId
        GetIndividualVehicle_request.VehicleId = vehicleId
        GetIndividualVehicle_response = LYTX_GetIndividualVehicle_Client.service.GetVehicle(GetIndividualVehicle_request)
        return(GetIndividualVehicle_response)

def LYTX_GetUsers_SOUPUI(login_response):
    LYTX_GetUsers_URL = "https://services-sd05.drivecam.com/HSServicesAPI/UserService/V1/UserService.svc?WSDL"
    LYTX_GetUsers_Client = Client(LYTX_GetUsers_URL)
    GetUsers_request = LYTX_GetUsers_Client.factory.create('ns2:GetUsersRequest')
    GetUsers_request.SessionId = login_response.SessionId
    # GetUsers_request.GroupId = login_response.HomeGroupId
    GetUsers_request.GroupId = "5100ffff-60b6-e5cd-0e05-60a3e15b0000" # DIO Group Id
    GetUsers_request.IncludeSubGroups = 1
    GetUsers_response = LYTX_GetUsers_Client.service.GetUsers(GetUsers_request)

    # convert response to json
    user_response = GetUsers_response.Users.UserSummary
    user_dicts = [
        {k: getattr(user, k, None) for k in ['FirstName', 'LastName', 'UserId']}
        for user in user_response
    ]
    return(user_dicts)

def LYTX_GetUsers_fromGroup_SOUPUI(login_response, groupId):
    LYTX_GetUsers_URL = "https://services-sd05.drivecam.com/HSServicesAPI/UserService/V1/UserService.svc?WSDL"
    LYTX_GetUsers_Client = Client(LYTX_GetUsers_URL)
    GetUsers_request = LYTX_GetUsers_Client.factory.create('ns2:GetUsersRequest')
    GetUsers_request.SessionId = login_response.SessionId
    GetUsers_request.GroupId = groupId
    GetUsers_request.IncludeSubGroups = 0
    GetUsers_response = LYTX_GetUsers_Client.service.GetUsers(GetUsers_request)
    return(GetUsers_response)


login_response = LYTX_Login_SOAPUI()
user_response = LYTX_GetUsers_SOUPUI(login_response)

with open('temp_json_files/lytx_users.json', 'w') as f:
    json.dump(user_response, f, indent=4)

skip=1


# def pulling_avaliable_LYTX_drivers(procurement_instance, mobile=False):
#     login_response = LYTX_Login_SOAPUI()

#     if not mobile:
#         deviceName = procurement_instance.vehicleId
#     else:
#         deviceName = procurement_instance
    
#     LytxApi_Vehicles_data = refreshLytxVehicles_database.objects.all()
#     LytxApi_Vehicles_df = pd.DataFrame.from_records(LytxApi_Vehicles_data.values())

#     temp_lytxVehicle_instance = LytxApi_Vehicles_df[LytxApi_Vehicles_df.lytxName == deviceName]
    
#     temp_lytxVehicle_instance = temp_lytxVehicle_instance.reset_index(drop=True)

#     temp_lytxVehicleId = temp_lytxVehicle_instance.loc[0, 'lytxVehicleId']
#     temp_lytxVehcileGroupId = temp_lytxVehicle_instance.loc[0, 'lytxGroupId']
    
#     # GetIndividualVehicle_response = LYTX_GetIndividualVehicle_SOUPUI(temp_lytxVehicleId, login_response)
#     def LYTX_GetUsers_fromGroup_SOUPUI(login_response, groupId):
#         LYTX_GetUsers_URL = "https://services-sd05.drivecam.com/HSServicesAPI/UserService/V1/UserService.svc?WSDL"
#         LYTX_GetUsers_Client = Client(LYTX_GetUsers_URL)
#         GetUsers_request = LYTX_GetUsers_Client.factory.create('ns2:GetUsersRequest')
#         GetUsers_request.SessionId = login_response.SessionId
#         GetUsers_request.GroupId = groupId
#         GetUsers_request.IncludeSubGroups = 0
#         GetUsers_response = LYTX_GetUsers_Client.service.GetUsers(GetUsers_request)
#         return(GetUsers_response)

#     GetUsers_response = LYTX_GetUsers_fromGroup_SOUPUI(login_response, temp_lytxVehcileGroupId)
    
#     users_list = GetUsers_response.Users.UserSummary
#     users_dicts = [{k: v for k, v in vars(user).items() if not k.startswith('__')} for user in users_list]
#     users_df = pd.DataFrame(users_dicts)
#     users_df = users_df.sort_values('FirstName', ascending=True).reset_index(drop=True)
#     users_df['FullName'] = users_df['FirstName'].str.strip() + ' ' + users_df['LastName'].str.strip()
#     users_df = users_df[['FirstName', 'LastName', 'FullName', 'UserId', 'UserName', 'UserStatus']]

#     users_inGroup = list(users_df['FullName'])
#     users_inGroup.insert(0, 'Unassigned Driver')

#     return(users_inGroup)

