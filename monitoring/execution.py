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

def logger(results):
    with open('monitoring.log', 'a') as f:
        f.write(f"{results}\n")

def ping_website(url, timeout=4):
    domain = sanitize_url(url)
    logger(f'Pinging {domain}')
    results = {
        'url': url,
        'latency': -1,
        'status_code': 404,
        'error': None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        latency = ping(domain, timeout=timeout)
        status_code = check_website_status(url)
        if latency is not None:
            results['latency'] = latency
        else:
            results['error'] = 'Could not ping the website'
        if status_code:
            print(f'The status code for {url} is {status_code}')
            results['status_code'] = status_code
        for key, value in results.items():
            logger(f'{key}: {value}')
        return results
    except Exception as e:
        print(f'Error: {e}')
        return results