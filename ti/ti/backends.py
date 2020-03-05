import requests
from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from tickets.models import User


def sync_user(user_data, password=None):
    leader_data = user_data['leader']
    
    user, created = User.objects.get_or_create(username=user_data['username'])
    user.email = user_data['email']
    user.full_name = user_data['full_name']
    user.mobile = user_data['mobile']
    user.department = user_data['department']
    user.job = user_data['job']
    user.is_active = user_data['is_active']
    
    if leader_data:
        leader, created = User.objects.get_or_create(username=leader_data['username'])
        leader.email = user_data['email']
        leader.full_name = user_data['full_name']
        leader.mobile = user_data['mobile']
        leader.department = user_data['department']
        leader.job = user_data['job']
        leader.is_active = user_data['is_active']
        leader.save()
        user.leader = leader
    
    if password:
        user.set_password(password)
        
    user.save()
    return user


def sync_all_users():
    url = settings.TIADMIN_HOST + '/kong/users/'
    print(url)
    r = requests.get(url).json()
    print(r)
    for user_data in r['results']:
        print('=====================')
        print(user_data)
        sync_user(user_data)
    print('sync_all_users finish')


class TiadminUserBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        url = settings.TIADMIN_HOST + '/kong/user_login/'
        data = {
            'username': username,
            'password': password,
        }
        r = requests.post(url, data=data).json()
        if not r.get('token'):
            return
        
        user_data = r['user']
        user = sync_user(user_data, password)
        
        if self.user_can_authenticate(user):
            return user

