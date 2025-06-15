import subprocess
import logging
from typing import Tuple

def make_adb_call(phone_number: str) -> Tuple[bool, str]:
    """
    Make a phone call via ADB
    Returns (success_status, error_message)
    """
    try:
        # Validate phone number format
        if not phone_number.isdigit() or len(phone_number) < 10:
            return False, "Invalid phone number format"
        
        # ADB command to initiate call
        command = f'adb shell am start -n com.google.android.dialer/com.android.dialer.DialtactsActivity -d tel:{phone_number}'
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15  # Timeout in seconds
        )
        
        if result.returncode == 0:
            return True, "Call initiated successfully"
        else:
            error_msg = f"ADB Error: {result.stderr.strip()}"
            logging.error(error_msg)
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        error_msg = "ADB command timed out (device not responding)"
        logging.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logging.error(error_msg)
        return False, error_msg