from urllib.parse import urlencode
from urllib.request import Request, urlopen
from dotenv import load_dotenv
import os

load_dotenv()

private_key = os.getenv("PUSHSAFE")

def SendNotification(title, message):
  if private_key is None:
    raise ConnectionError("No private key")
  url = 'https://www.pushsafer.com/api'
  post_fields = {
    "t" : title,
    "m" : message,
    "v" : 3,
    "i" : 156,
    "d" : 'a', # All devices
    # "d" : 'gs4140', # Dev group
    "k" : private_key, 
  }

  request = Request(url, urlencode(post_fields).encode())
  json = urlopen(request).read().decode()
  return json

def SendFakeNotification(title, message):
  print(title)
  print(message)