import requests
from database import check_id_user


TOKEN_VK = ''
url = 'https://api.vk.com/method/'

list_skipped = []

def user_search(age=None, gender=0, city=None, status=None):
    search_users_url = url + 'users.search'
    search_users_params = {
        'access_token': TOKEN_VK,
        'v': '5.126',
        'age_from': age,
        'age_to': age,
        'status': status,
        'sex': gender,
        'count': 1000,
        'hometown': city,
        'has_photo': 1,
        'fields': 'screen_name'
    }
    response = requests.get(search_users_url, params=search_users_params)
    result = response.json()
    if 'response' in result:
        global list_users
        list_users = result['response']['items']
        return list_users

def photos_get(user_id):
    photos_get_url = url + 'photos.get'
    photos_get_params = {
        'access_token': TOKEN_VK,
        'v': '5.126',
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': '1',
        'photo_sizes': '0',
    }
    response = requests.get(photos_get_url, params=photos_get_params)
    user_foto_dict = response.json()
    return user_foto_dict

def photo_selection(user_foto_dict):
    list_foto = []
    for photo in user_foto_dict['response']['items']:
        dict_foto = {}
        dict_foto['id'] = 'photo' + str(photo['owner_id']) + '_' + str(photo['id'])
        dict_foto['popular'] = photo['likes']['count'] + photo['comments']['count']
        list_foto.append(dict_foto)
    sort_list = sorted(list_foto, key=lambda x: x['popular'], reverse=True)[:3]
    return sort_list

def user_profile(list_users):
    check_photo = {}
    check_database = 0
    while 'response' not in check_photo or check_database != True:
        if len(list_users) != 0:
            user = list_users.pop(0)
            check_database = check_id_user(user['id'])
            check_photo = photos_get(user['id'])
        else:
            break
    user_profile_dict = {}
    user_profile_dict['name'] = user['first_name']
    user_profile_dict['last_name'] = user['last_name']
    user_profile_dict['id'] = user['id']
    user_profile_dict['url'] = 'https://vk.com/id' + str(user['id'])
    user_profile_dict['photo'] = photo_selection(check_photo)
    return user_profile_dict

def download_list_skipped(user):
    list_skipped.append(user)

def get_user():
    if len(list_users) != 0:
        return user_profile(list_users)
    elif len(list_skipped) != 0:
        return list_skipped.pop(0)
    elif len(list_users) == 0 and len(list_skipped) == 0:
        return None






