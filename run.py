import ipaddress
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

c = []
failed = []



def is_ip(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False

def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

API_TOKEN = "9675be53c248ae"



def make_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,  # waits 1s, 2s, 4s, 8s... between retries
        status_forcelist=[500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session

session = make_session()

def get_batch_ip_info(ips):
    url = f"https://api.ipinfo.io/batch/lite?token={API_TOKEN}"
    resp = requests.post(url, json=ips, timeout=15)
    resp.raise_for_status()
    return resp.json()


def find_by_ip(ip):
    for i in configs:
        if ip in i:
            return i

with open('configs.txt','r' , encoding='utf-8') as f:
    configs = [line.strip() for line in f if line.strip()]
    for i in configs:
        try :
            host = i.split('@')[1].split(':')[0]
            if is_ip(host) and host not in c:
                c.append(host)

        except :
            failed.append(c)


    print('f:',len(failed))
    all_results = {}
    for chunk in chunked(c, 1000):
        all_results.update(get_batch_ip_info(chunk))

    matching_ips = []

    target = "United States"

    print(target,'\n=========================================================================================================')

    for ip, info in all_results.items(): 
        if info and info.get("country") == target:
            matching_ips.append(ip)
            print(find_by_ip(ip))
