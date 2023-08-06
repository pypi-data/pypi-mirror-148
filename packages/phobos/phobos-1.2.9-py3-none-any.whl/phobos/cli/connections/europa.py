import os
import json
import requests
import click
from appdirs import user_config_dir
from requests.models import Response
from tabulate import tabulate


__all__ = ["Europa"]

class Europa:
    def __init__(self, url, email, passwd):
        self.url = url 
        self.email = email 
        self.passwd = passwd
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.setup()

    def read_config(self):
        config_path = os.path.join(user_config_dir('phobos'), "config.json")
        fin = open(config_path, 'r')
        config_data = json.load(fin)
        fin.close()

        if not self.url:
            self.url = config_data['url']
        if not self.email:
            self.email = config_data['email']
        if not self.passwd:
            self.passwd = config_data['passwd']
        self.headers['Authorization'] = config_data['accessToken']

    def update_config(self):
        config_path = os.path.join(user_config_dir('phobos'), "config.json")
        fout = open(config_path, 'w')
        json.dump({'url': self.url, 
                    'email': self.email, 
                    'passwd': self.passwd, 
                    'accessToken': self.headers['Authorization']}, fout)
        fout.close()

    def is_token_valid(self):
        response = requests.post(f'{self.url}/europa/auth/v2/check-me', headers=self.headers)
        if response == 200:
            return True 
        return False

    def login(self):
        login_url = f'{self.url}/europa/auth/v2/login'
        data = {"email": self.email, "password": self.passwd}
        if 'Authorization' in self.headers:
            del self.headers['Authorization']

        response = requests.post(login_url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            resdata = response.json()
            self.headers["Authorization"] = f"Bearer {resdata['accessToken']}"
            self.update_config()
        else:
            print('failed to authenticate')
            print(f"authentication endpoint {self.url} returned with HTTP status code : {response.status_code}")
            print(f"please register at {f'{self.url}/europa/auth/v2/register'} if you havent")

    def setup(self):
        self.read_config()
        if not self.email or not self.passwd:
            click.echo("Please provide email and password")
        elif not self.is_token_valid():
            self.login()

    def get_labels(self, properties, labelmaps):
        labels = { key: [] for res in properties['responses'] for key in res }
        
        for res in properties['responses']:
            for key in res:
                labels[key].append(res[key][0])

        for key in labels:
            llist = []
            for i in range(len(labels[key])):
                llist.append(labelmaps[i][labels[key][i]])
            labels[key] = llist
        
        return labels

    def get_image_details(self, id):
        image_url = f'{self.url}/europa/api/v1/images/{id}'

        response = requests.get(image_url, headers=self.headers)

        if response.status_code == 200:
            image = response.json()['image']
            return image['tiles'], image['geometry'], image['status']
        else:
            print('image details cannot be retrieved')
            print('image meta endpoint {} returned with HTTP status code : {}'.format(image_url, response.status_code))
            return None, None, None
            
    def get_tasks(self):
        get_task_url = f'{self.url}/europa/api/v1/tasks'
        response = requests.get(get_task_url, headers=self.headers)

        if response.status_code == 200:
            tasks = response.json()['results']
            table = [[task['id'], task['name']] for task in tasks]

            print('\nList of Europa Tasks:\n')
            print(tabulate(table, headers=['ID', 'Name', 'Description'], tablefmt='pretty'))
            print()
        else:
            print('all Europa tasks cannot be retrieved')
            print('tasks endpoint {} returned with HTTP status code : {}\n'.format(get_task_url, response.status_code))

    def get_task_details(self, id):
        task_details_url = f'{self.url}/europa/api/v1/tasks/{id}'        

        response = requests.get(task_details_url, headers=self.headers)
        
        if response.status_code == 200:
            ignorelist = ['populateCounter', 'owner', 'createdAt', 'updatedAt', 'deteledAt', 'annotators']
            
            print('\nTask Details:\n')
            
            task = response.json()['task']
            for key in task.keys():
                if key == 'questions':
                    print(key+' : \n')
                    for qstn in task[key]:
                        print('name : {}'.format(qstn['name']))
                        print('description : {}'.format(qstn['description']))
                        print('response options : {}'.format(qstn['responseOptions']))
                        print()
                elif key not in ignorelist:
                    print('{} : {}'.format(key, task[key]))

            print()
        else:
            print('task details cannot be retrieved')
            print('task details endpoint {} returned with HTTP status code : {}\n'.format(task_details_url, response.status_code))

    def export_annotations(self, id):
        export_url = f'{self.url}/europa/api/v1/tasks/{id}/export'

        print(f'exporting annotations for task id : {id}')

        response = requests.post(export_url, headers=self.headers)

        if response.status_code != 200:
            print('cannot export annotations')
            print(f'export endpoint {export_url} returned with HTTP status code : {response.status_code}\n')
            return
        else:
            print('annotations export requested')
