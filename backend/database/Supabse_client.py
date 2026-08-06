import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
class SupabaseClient:
    URL: str = os.getenv('SUPABASE_URL')
    KEY: str = os.getenv('SUPABASE_KEY')
    SERVICE_ROLE_KEY: str = os.getenv('SERVICE_ROLE_KEY')
    client: Client = create_client(URL , SERVICE_ROLE_KEY)