import os
from supabase import create_client , Client
from dotenv import load_dotenv
from backend.app.database.supabase_client import SupabaseClient

class Authentication:
    @staticmethod
    def sign_up(email:str , password:str, full_name: str):
        res = SupabaseClient.client.auth.sign_up({
            "email": email,
            "password": password,
            "options" : {"data":{"full_name":full_name}}
        })
        print("USER METADATA",res.user.user_metadata)
        return res
    @staticmethod
    def log_in(email: str , password: str):
        try:
            auth_response = SupabaseClient.client.auth.sign_in_with_password(
                {
                    'email':email,
                    'password':password
                }
            )
            user_uuid = auth_response.user.id
            if auth_response.user is not None:
                return {"success": True, "user_uuid": user_uuid, "error": None}
            else:
                return {"success": False, "user_uuid": None, "error": "Invalid email or password structure."}
        except Exception as e:
            return {"success" : False, "user_uuid": None, "error":str(e)}
    @staticmethod
    def log_out():
        SupabaseClient.client.auth.sign_out()
        return