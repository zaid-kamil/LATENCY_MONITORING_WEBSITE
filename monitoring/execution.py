import time
import requests
from datetime import datetime
from ping3 import ping
import re

def sanitize_url(url):
    # get only domain name  
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)
    url = re.sub(r'/$', '', url)
    return url

def check_website_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except Exception as e:
        print(f'Error: {e}')
        return None

def ping_website(url, timeout=4):
    domain = sanitize_url(url)
    results = {
        'url': url,
        'ping_time': None,
        'status_code': None,
        'error': None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        ping_time = ping(domain, timeout=timeout)
        status_code = check_website_status(url)
        if ping_time is not None:
            results['ping_time'] = ping_time
        else:
            results['error'] = 'Could not ping the website'
        if status_code:
            print(f'The status code for {url} is {status_code}')
            results['status_code'] = status_code
        return results
    except Exception as e:
        print(f'Error: {e}')
        return results