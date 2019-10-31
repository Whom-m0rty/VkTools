import requests


def main():
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
    print('\tПрежде всего, вам необходимо выполнить настройку.')
    ACCESS_TOKEN = str(input('\tAccess_token: '))
    MY_ID = str(input('\tID вашей страницы: '))
    while True:
        print('''\n
        1.Удалить всех друзей
        2.Изменить статус
        ''')
        todo = str(input('Введите цифру: '))

        if todo == '1':
            delete_all_friends(ACCESS_TOKEN, MY_ID)
        elif todo == '2':
            set_status(ACCESS_TOKEN)

def delete_all_friends(ACCESS_TOKEN, MY_ID):
    try:
        r = requests.get('https://api.vk.com/method/friends.get?user_id=' + MY_ID + '&access_token=' + ACCESS_TOKEN + '&v=5.103')
        r = r.json()
        frends = ((r['response']['items']))
        print(frends)
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


def set_status(ACCESS_TOKEN):
    status = str(input('Введите нужный статус: '))
    r = requests.get('https://api.vk.com/method/status.set?text=' + str(status) + '&access_token=' + ACCESS_TOKEN + '&v=5.103')
    r = r.json()
    if str(r['response']) == '1':
        print('\n\tСтатус изменен!')


if __name__ == '__main__':
    main()