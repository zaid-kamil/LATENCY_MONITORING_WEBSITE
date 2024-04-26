import time
import requests
from datetime import datetime
from ping3 import ping
import requests

from ping3 import ping

def check_website_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except Exception as e:
        print(f'Error: {e}')
        return None

def ping_website(url, timeout=4):
    results = {
        'url': url,
        'ping_time': None,
        'status_code': None,
        'error': None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        ping_time = ping(url, timeout=timeout)
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

    

