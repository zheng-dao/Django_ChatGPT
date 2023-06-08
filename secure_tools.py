import base64, os
from Crypto import Random
from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder
from app.models import User, UserProfile
from datetime import date, datetime, timedelta;import time;import timedate
import random
import array
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import json

BLOCK_SIZE = 16

#https://stackoverflow.com/questions/14179784/python-encrypting-with-pycrypto-aes
def encrypt(payload, key):
    IV = get_salt(BLOCK_SIZE)
    aes = AES.new(key, AES.MODE_CBC, IV)
    if isinstance(payload, dict):
        payload = json.dumps(payload)
    return base64.b64encode(IV + aes.encrypt(pad(payload).encode("utf-8"))).decode('utf-8')

#https://stackoverflow.com/questions/30990129/encrypt-in-python-decrypt-in-javascript
def encrypt2(clear_text, key, iv):
    encoder = PKCS7Encoder()
    raw = encoder.encode(clear_text)
    cipher = AES.new( key, AES.MODE_CBC, iv )
    return base64.b64encode( iv + cipher.encrypt( raw.encode("utf-8")  ) )

def decrypt(payload, key):
    encrypted = base64.b64decode(payload)
    IV = encrypted[:BLOCK_SIZE]
    aes = AES.new(key, AES.MODE_CBC, IV)
    return unpad(aes.decrypt(encrypted[BLOCK_SIZE:])).decode('utf-8')

def decrypt2(encoded_text, key, iv, block_size=BLOCK_SIZE):
    encoder = PKCS7Encoder()
    decodetext =  base64.b64decode(encoded_text)
    aes = AES.new(key, AES.MODE_CBC, iv)
    cipher = aes.decrypt(decodetext)
    pad_text = encoder.decode(cipher[block_size:].decode('latin-1'))
    return pad_text

def unpad(data):
    return data[:-ord(data[-1:])]

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + chr(length)*length

def r_pad(payload, block_size=BLOCK_SIZE):
    length = block_size - (len(payload) % block_size)
    return payload + chr(length) * length

def get_salt(length=BLOCK_SIZE):
    return Random.new().read(BLOCK_SIZE)
    #return os.urandom(length)

def check_user_inactivity(days_inactive=365):
    dt = datetime.now() - timedelta(days_inactive)
    users = User.objects.filter(last_login__lt=dt)

def expire_passwords(days_active=90):
    dt = datetime.now() - timedelta(days_active)
    users = User.objects.filter(password_update_date__lt=dt).update(force_password_reset=True, force_password_reset_date=datetime.now())
    
def get_random_password(MAX_LEN=15):

    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                        'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', 
            '*', '(', ')', '<']
    
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
   
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    password = ""
    for x in temp_pass_list:
            password = password + x
            
    return password

class DigitLowerUpperValidator:
    password_requirements = _(
        "The password must contain at least one digit, symbol, lower case and "
        "upper case letter"
    )

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        # number in string
        if not any(c.isdigit() for c in password):
            raise ValidationError(self.password_requirements)
        # lower in string
        if not any(c.islower() for c in password):
            raise ValidationError(self.password_requirements)
        # upper in stirng
        if not any(c.isupper() for c in password):
            raise ValidationError(self.password_requirements)
        if not any(char in special_characters for char in password):
            raise ValidationError(self.password_requirements)

    def get_help_text(self):
        return _(
            "The password must contain at least one upper case, "
            "lower case letter and at least a digit")