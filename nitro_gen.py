import string
import random
import requests
from colorama import *
import json
import stem
from stem import Signal
from stem.control import Controller
import time

logo = """
    )                       *                                     
 ( /(         )           (  `                       )            
 )\()) (   ( /( (         )\))(                   ( /(   (   (    
((_)\  )\  )\()))(    (  ((_)()\   (    (     (   )\()) ))\  )(   
 _((_)((_)(_))/(()\   )\ (_()((_)  )\   )\ )  )\ (_))/ /((_)(()\  
| \| | (_)| |_  ((_) ((_)|  \/  | ((_) _(_/( ((_)| |_ (_))   ((_) 
| .` | | ||  _|| '_|/ _ \| |\/| |/ _ \| ' \))(_-<|  _|/ -_) | '_| 
|_|\_| |_| \__||_|  \___/|_|  |_|\___/|_||_| /__/ \__|\___| |_|
"""

proxies = {

    'http':  'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'

    }

headers = {}

num = 1

with open('user-agents.txt', 'r') as file:

    lines = file.readlines()

    for line in lines:

        headers[f'useragent{num}'] = line.replace("\n", "")

        num = num + 1


def changeIP(session):

    with Controller.from_port(port = 9051) as controller:

        controller.authenticate("Net1234")

        controller.signal(Signal.NEWNYM)

        print(Fore.MAGENTA + "IP switched" + Fore.WHITE)

        r = session.get('http://httpbin.org/ip', proxies=proxies, stream=False)

        ip = r.text

        print("ip: " + ip.replace("{", "").replace("}", "").replace("\"origin\":", "").replace(" ", "").replace("\n", ""))


print(Fore.RED + logo + Fore.WHITE)

while True:

    session = requests.session()

    code = "".join(random.choice(string.ascii_letters + string.digits) for i in range(19))

    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}"#?with_application=false&with_subscription_plan=true

    result = session.get(url, proxies=proxies, headers = headers, stream=False)#, timeout=(5, 5))
        
    if "Unknown Gift Code" in result.text:

        print("[" + Fore.RED + "-" + Fore.WHITE + "] invalid code! {" + code + "}")

    elif "The resource is being rate limited." in result.text:

        print(Fore.WHITE + "[" + Fore.YELLOW + "!" + Fore.WHITE + "] Got rate limit! changing the ip..")

        changeIP(session)

    else:

        print(Fore.GREEN + "[+]" + Fore.WHITE + f"found a valid code!\nCode: {url}")

        print(result.text)

        break