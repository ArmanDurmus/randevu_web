from turkeysms import TurkeySmsClient
import asyncio
from backend.settings import settings

client = TurkeySmsClient(api_key=settings.turkeysms_api_key)

def _send_sms_sync(phone_number: str, message: str):
    return client.send_sms(
        title=settings.turkeysms_sender,
        mobile=phone_number,
        text=message,
        lang=1
    )

async def send_sms_call(phone_number: str, message: str):
    await asyncio.to_thread(
        _send_sms_sync,
        phone_number,
        message
    )