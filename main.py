import requests


def main():
    ACCESS_TOKENS = []
    print(r'''
        
     __  __  __     ______                ___               __                  __      __  __                             _    
    /\ \/\ \/\ \   /\__  _\              /\_ \             /\ \                /\ \  __/\ \/\ \                          /'_`\  
    \ \ \ \ \ \ \/'\/_/\ \/   ___     ___\//\ \     ____   \ \ \____  __  __   \ \ \/\ \ \ \ \ \___     ___     ___ ___ /\_\/\`\
     \ \ \ \ \ \ , <  \ \ \  / __`\  / __`\\ \ \   /',__\   \ \ '__`\/\ \/\ \   \ \ \ \ \ \ \ \  _ `\  / __`\ /' __` __`\/_//'/'
      \ \ \_/ \ \ \\`\ \ \ \/\ \L\ \/\ \L\ \\_\ \_/\__, `\   \ \ \L\ \ \ \_\ \   \ \ \_/ \_\ \ \ \ \ \/\ \L\ \/\ \/\ \/\ \ /\_\ 
       \ `\___/\ \_\ \_\\ \_\ \____/\ \____//\____\/\____/    \ \_,__/\/`____ \   \ `\___x___/\ \_\ \_\ \____/\ \_\ \_\ \_\\/\_\
        `\/__/  \/_/\/_/ \/_/\/___/  \/___/ \/____/\/___/      \/___/  `/___/> \   '\/__//__/  \/_/\/_/\/___/  \/_/\/_/\/_/ \/_/
                                                                          /\___/                                                
                                                                          \/__/   
    
    ''')
    print('''\tПрежде всего, вам необходимо выполнить настройку.
        Каким сопособом вы хотите добавить токены?
            1. Ручным
            2. Считать с tokens.txt
            ''')
    todo_token = str(input('Введите цифру: '))
    if todo_token == '1':
        co = int(input('Сколько токенов вы хотите добавть?: '))
        for i in range(0, co):
            ACCESS_TOKEN = str(input('Access_token ' + str(i+1) + ' : ' ))
            ACCESS_TOKENS.append(ACCESS_TOKEN)
    if todo_token == '2':
        file = open('tokens.txt')
        for line in file:
            ACCESS_TOKENS.append(line.rstrip())
    print('''
    Полученные токены: 
    ''' + str(ACCESS_TOKENS))
    MY_ID = str(input('\n\tID вашей страницы: '))
    while True:
        print('''\n
        1.Удалить всех друзей
        2.Изменить статусы у страниц
        3.Узнать в каких сообществах ДАННЫЕ страница является администратором.
        4.Узнать в каких сообществах ЛЮБАЯ страница является администратором( РАБОТАЕТ КРИВО! ).
        5.Сделать посты на страницах(ссылки запрещены APIVk).
        6.Cделать репост записи СООБЩЕСТВА на страницу(для ссылок). 
        ''')
        todo = str(input('Введите цифру: '))

        if todo == '1':
            delete_all_friends(ACCESS_TOKENS, MY_ID)
        elif todo == '2':
            set_status(ACCESS_TOKENS)
        elif todo == '3':
            get_adm_groups_cur(ACCESS_TOKENS)
        elif todo == '4':
            get_adm_groups(ACCESS_TOKENS)
        elif todo == '5':
            make_post_on_wall(ACCESS_TOKENS)
        elif todo == '6':
            make_repost_on_wall(ACCESS_TOKENS)

def make_repost_on_wall(ACCESS_TOKENS):
    object = str(input('Идентификатор поста который нужно репостнуть(Пример: wall66748_3675): '))
    text = str(input('Текст к записи(Оставьте пустым, если нужно.): '))
    for ACCESS_TOKEN in ACCESS_TOKENS:
        try:
            r = requests.get(
                'https://api.vk.com/method/wall.repost?object=' + object + '&message=' + text + '&access_token=' + ACCESS_TOKEN + '&v=5.103')
            if r.json()['response']['success'] == 1:
                print('Запись создана!')
            else:
                print('Запись НЕ создана!')
        except:
            print('Ошибка!')


def make_post_on_wall(ACCESS_TOKENS):
    body = str(input('Введите текст поста: '))
    try:
        for ACCESS_TOKEN in ACCESS_TOKENS:
            r = requests.get(
                'https://api.vk.com/method/wall.post?message=' + body + '&access_token=' + ACCESS_TOKEN + '&v=5.103')
            print(r.json())
    except:
        print('Ошибка')

def get_adm_groups(ACCESS_TOKENS):
    ACCESS_TOKEN = ACCESS_TOKENS[0]
    ID = str(input('Введите ID страницы которую нужно пробить: '))
    try:
        r = requests.get(
            'https://api.vk.com/method/groups.get?user_id=' + ID + '&extended=1&fields=is_admin&access_token=' + ACCESS_TOKEN + '&v=5.103')
        r = r.json()
        adm_lvl = requests.get(
            'https://api.vk.com/method/groups.get?user_id=' + ID + '&extended=1&fields=admin_level&access_token=' + ACCESS_TOKEN + '&v=5.103')
        count = requests.get(
            'https://api.vk.com/method/groups.get?user_id=' + ID + '&extended=1&fields=members_count&access_token=' + ACCESS_TOKEN + '&v=5.103')
        count = count.json()
        print(r)
        print('''
           Пользователь админ в группах:
           ''')
        for i in range(1, r['response']['count']):
            if str(r['response']['items'][i]['is_admin']) == '1':
                if str(adm_lvl.json()['response']['items'][i]['admin_level']) == '3':
                    adm = 'Cоздатель'
                elif str(adm_lvl.json()['response']['items'][i]['admin_level']) == '2':
                    adm = 'Редактор'
                else:
                    adm = 'Модератор'
                print(str(r['response']['items'][i]['id']) + ', ' + str(r['response']['items'][i]['name'])
                      + ', Уровень Admin: ' + adm +
                      ', Количество подписчиков: ' + str(count['response']['items'][i]['members_count']))
    except:
        print('Произошла ошибка!')

def get_adm_groups_cur(ACCESS_TOKENS):
    for ACCESS_TOKEN in ACCESS_TOKENS:
        try:
            r = requests.get('https://api.vk.com/method/groups.get?&extended=1&fields=is_admin&access_token=' + ACCESS_TOKEN + '&v=5.103')
            r = r.json()
            adm_lvl = requests.get('https://api.vk.com/method/groups.get?&extended=1&fields=admin_level&access_token=' + ACCESS_TOKEN + '&v=5.103')
            count = requests.get('https://api.vk.com/method/groups.get?&extended=1&fields=members_count&access_token=' + ACCESS_TOKEN + '&v=5.103')
            count = count.json()
            print('''
            Пользователь админ в группах:
            ''')
            for i in range(1, r['response']['count']):
                if str(r['response']['items'][i]['is_admin']) == '1':
                    if str(adm_lvl.json()['response']['items'][i]['admin_level']) == '3':
                        adm = 'Cоздатель'
                    elif str(adm_lvl.json()['response']['items'][i]['admin_level']) == '2':
                        adm = 'Редактор'
                    else:
                        adm = 'Модератор'
                    print(str(r['response']['items'][i]['id']) + ', ' + str(r['response']['items'][i]['name'])
                          + ', Уровень Admin: ' + adm +
                          ', Количество подписчиков: ' + str(count['response']['items'][i]['members_count']))
        except:
            print('Произошла ошибка')


#def send_message(ACCESS_TOKEN):
#    message = str(input('Какое сообщение отправть?: '))
#    ID = str(input('ID получателя сообщения: '))
#    random_id = random.getrandbits(64)
#    r = requests.get('https://api.vk.com/method/messages.send?user_id=' + ID + '&random_id=' + str(random_id) + 'message=' + message + '&access_token=' + ACCESS_TOKEN + '&v=5.103')
#    r = r.json()
#    print(r)

def delete_all_friends(ACCESS_TOKENS, MY_ID):
    ACCESS_TOKEN = ACCESS_TOKENS[0]
    try:
        r = requests.get('https://api.vk.com/method/friends.get?user_id=' + MY_ID + '&access_token=' + ACCESS_TOKEN + '&v=5.103')
        r = r.json()
        frends = ((r['response']['items']))
        for ID in frends:
            try:
                r = requests.get('https://api.vk.com/method/friends.delete?user_id=' + str(ID) + '&access_token=' + ACCESS_TOKEN + '&v=5.103')
                r = r.json()
                if str(r['response']['success']) == '1':
                    print('\tУспешно удален друг ' + ID)
            except:
                print('\tНе вышло удалить друга ' + ID + ' !')
    except:
        print('\tПроизошла ошибка!')


def set_status(ACCESS_TOKENS):
    status = str(input('Введите нужный статус: '))
    try:
        for ACCESS_TOKEN in ACCESS_TOKENS:
            r = requests.get('https://api.vk.com/method/status.set?text=' + str(status) + '&access_token=' + ACCESS_TOKEN + '&v=5.103')
            r = r.json()
            if str(r['response']) == '1':
                print('Статус изменен!')
    except:
        print(r)
        print('Ошибка!')


if __name__ == '__main__':
    main()