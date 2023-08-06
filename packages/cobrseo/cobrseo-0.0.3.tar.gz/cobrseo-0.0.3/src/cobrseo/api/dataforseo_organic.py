from http.client import HTTPSConnection
import json
import os
import hashlib
import time
from typing import List
import logging

SAVE_FILE = 'post_id_save.txt'


# ===================================
#     Adding logger to the module
# ===================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s : %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

file_handler = logging.FileHandler('dataforseo_log.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# ===================================


class RestClient:
    domain = 'api.dataforseo.com'

    def __init__(self, credential):
        self.credential = credential

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        
        try:
            headers = {
                'Authorization' : f'Basic {self.credential}',
                'Content-Type': 'application/json'
            }
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            
            return json.loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = json.dumps(data)
        return self.request(path, 'POST', data_str)
    
    
def make_post_request(client, post_data):
    post_ids = []
    
    post_response = client.post('/v3/serp/google/organic/task_post', post_data)
    if post_response['status_code'] == 20000:
            
        post_ids = [t['id'] for t in post_response['tasks'] if t['status_message']=='Task Created.']
        # post_status = [t['status_message'] for t in post_response['tasks']]
        logger.debug(f'POST. id size = {len(post_ids)}')
        
        with open(SAVE_FILE, 'w') as f:
            for p in post_ids:
                f.write(f'{p}\n')
        
    else:
        logger.error(f"POST error. Code: {post_response['status_code']} Message: {post_response['status_message']}")
        time.sleep(5)
            
    return post_ids


def make_ready_request(client, post_ids):
    post_ids_size = len(post_ids)
    
    if post_ids_size <= 10:
        timeout = post_ids_size * 5
    elif post_ids_size <= 20:
        timeout = post_ids_size * 4
    elif post_ids_size <= 40:
        timeout = post_ids_size * 3
    else:
        timeout = post_ids_size * 2
        
    ready_ids = []
    while True:
        time.sleep(timeout)
        
        ready_response = client.get('/v3/serp/google/organic/tasks_ready')
        
        if ready_response['status_code'] == 20000:
            if not ready_response['tasks'][0]['result']:
                logger.warning('Retrying READY request')
                continue

            ready_ids = [t['id'] for t in ready_response['tasks'][0]['result'] if t['id'] in post_ids]
            logger.debug(f'READY. id size = {len(ready_ids)}')
            if len(ready_ids) == len(post_ids):
                break
            
        else:
            logger.error(f"READY error. Code: {ready_response['status_code']} Message: {ready_response['status_message']}")
            time.sleep(5)
    
    return ready_ids


def make_get_request(client, ready_ids, destination_path, keywords_paths_mapped):
    for i in ready_ids:
        
        while True:
            get_response = client.get(f'/v3/serp/google/organic/task_get/advanced/{i}')
            if get_response['status_code'] == 20000:
                keyword = get_response['tasks'][0]['data']['keyword']
                logger.info(f'GET. keyword = {keyword}')
                json_name = f"{hashlib.md5(keyword.encode('utf-8')).hexdigest()}.json"
                json_path = os.path.join(destination_path, json_name)
                
                keywords_paths_mapped.append({'keyword': keyword, 'path': json_path})

                with open(json_path, 'w') as f:
                    json.dump(get_response['tasks'][0]['result'], f)

                break
            else:
                logger.error(f"GET error. Code: {get_response['status_code']} Message: {get_response['status_message']}")
                time.sleep(5)
    
    open(SAVE_FILE, 'w').close()


def check_kw_in_dir(keyword, directory, keywords_paths_mapped):
    json_name = f"{hashlib.md5(keyword.encode('utf-8')).hexdigest()}.json"
    
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if json_name in files:
        keywords_paths_mapped.append({'keyword': keyword, 'path': os.path.join(directory, json_name)})
        return True

    return False


def save_dataforseo_organic_serps(keywords: List[str], 
                   destination_path: str, 
                   rewrite_serp: bool,
                   token: str, 
                   post_size: int=80, 
                   lang: str='en', 
                   loc: int=2840, 
                   depth: int=10) -> List[dict]:
    
    keywords_copy = keywords.copy()
    client = RestClient(token)
    post_data = dict()
    stop = False
    keywords_paths_mapped = list()
    
    if os.path.isfile(SAVE_FILE):
        with open(SAVE_FILE) as f:
            post_ids_save = f.read().splitlines()
        
        logger.debug(f'SAVED POST. id size = {len(post_ids_save)}')
        make_get_request(client, post_ids_save, destination_path, keywords_paths_mapped)
        
    while True:
        
        while True:
            try:
                k = keywords_copy.pop(0)
            except IndexError:
                stop = True
                break

            if not rewrite_serp and check_kw_in_dir(k, destination_path, keywords_paths_mapped):
                logger.debug(f'ALREADY EXISTS. [{k}].')
                continue

            post_data[len(post_data)] = dict(
                language_code = lang,
                location_code = loc,
                keyword = k,
                depth = depth
            )
            if len(post_data) == post_size:
                break

        if len(post_data) > 0:
            post_ids = make_post_request(client, post_data)
            ready_ids = make_ready_request(client, post_ids)
            make_get_request(client, ready_ids, destination_path, keywords_paths_mapped)

        post_data.clear()
        if stop:
            break

    return keywords_paths_mapped
