import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
from datetime import datetime
import time
from pystyle import Center, Colorate, Colors
import webbrowser


webbrowser.open("https://t.me/+00Uzen6uu10zYTZk", new=2)
COLOR_CODE = {'RESET': '\x1b[0m', 'UNDERLINE': '\x1b[04m', 'GREEN': '\x1b[32m', 'RED': '\x1b[93m', 'RED': '\x1b[31m', 'WHITE': '\x1b[36m', 'BOLD': '\x1b[01m', 'PINK': '\x1b[95m', 'URL_L': '\x1b[36m', 'LI_G': '\x1b[92m', 'F_CL': '\x1b[0m', 'DARK': '\x1b[90m', 'WHITE': '\x1b[97m'}

def cls():
    input(f"\n{COLOR_CODE['RED']}{COLOR_CODE['BOLD']}[◆] {COLOR_CODE['WHITE']}Нажмите ENTER чтобы продолжить.")
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
  
    banner = """



         ▄█    █▄     ▄████████ ████████▄  ████████▄   ▄██████▄     ▄████████    ▄█   ▄█▄
        ███    ███   ███    ███ ███   ▀███ ███   ▀███ ███    ███   ███    ███   ███ ▄███▀
        ███    ███   ███    █▀  ███    ███ ███    ███ ███    ███   ███    ███   ███▐██▀  
        ███    ███  ▄███▄▄▄     ███    ███ ███    ███ ███    ███  ▄███▄▄▄▄██▀  ▄█████▀   
        ███    ███ ▀▀███▀▀▀     ███    ███ ███    ███ ███    ███ ▀▀███▀▀▀▀▀   ▀▀█████▄   
        ███    ███   ███    █▄  ███    ███ ███    ███ ███    ███ ▀███████████   ███▐██▄  
        ███    ███   ███    ███ ███   ▄███ ███   ▄███ ███    ███   ███    ███   ███ ▀███▄
         ▀██████▀    ██████████ ████████▀  ████████▀   ▀██████▀    ███    ███   ███   ▀█▀
                                                                   ███    ███   ▀     

                                owner: @pypkg

                [1] SQL Search - поиск уязвимых к SQL Injection сайтов                          
                
                [2] Dork Search - поиск уязвимых сайтов через дорки
                

                


    """

    print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))


def sql_search():
    import threading
    import random
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
    import urllib3
    from queue import Queue
    urllib3.disable_warnings()
    SEARCH_ENGINES = {'google': 'https://www.google.com/search?q={}', 'bing': 'https://www.bing.com/search?q={}', 'yahoo': 'https://search.yahoo.com/search?p={}', 'duckduckgo': 'https://duckduckgo.com/html?q={}'}
    BLOCKED_DOMAINS = {'youtube.com', 'google.com', 'facebook.com', 'microsoft.com', 'github.com', 'amazon.com', 'stackoverflow.com', 'linkedin.com', 'twitter.com', 'instagram.com'}
    dorks = ['inurl:.php?id=', 'inurl:.asp?id=', 'inurl:product.php?id=', 'inurl:category.php?id=', 'inurl:news.php?id=', 'inurl:index.php?id=', 'inurl:item.php?id=', 'inurl:view.php?id=', 'inurl:article.php?id=', 'inurl:show.php?id=', 'inurl:gallery.php?id=', 'inurl:event.php?id=', 'inurl:download.php?id=', 'inurl:main.php?id=', 'inurl:review.php?id=', 'inurl:process.php?id=', 'inurl:plugin.php?id=', 'inurl:readme.php?id=', 'inurl:profile.php?id=', 'inurl:about.php?id=', 'inurl:file.php?id=', 'inurl:user.php?id=', 'inurl:page.php?pid=', 'inurl:forum.php?topic=', 'inurl:thread.php?tid=', 'inurl:message.php?id=', 'inurl:cart.php?id=']
    sql_errors = ['mysql_fetch_array()', 'You have an error in your SQL syntax', 'Warning: mysql_', 'mysqli_fetch_array', 'Error Executing Database Query']
    ua = UserAgent()
    lock = threading.Lock()
    scanned_urls = set()
    vulnerable_sites = set()
    stop_event = threading.Event()

    def get_random_headers():
        return {'User-Agent': ua.random, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'DNT': '1', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1'}

    def normalize_url(url):
        return url.split('?')[0]

    def search_urls(dork):
        urls = set()
        for engine in SEARCH_ENGINES.keys():
            try:
                response = requests.get(SEARCH_ENGINES[engine].format(dork), headers=get_random_headers(), verify=False, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a'):
                        url = link.get('href', '')
                        if any((d in url for d in ['.php?', '.asp?'])):
                            if not any((bd in url for bd in BLOCKED_DOMAINS)):
                                normalized_url = normalize_url(url)
                                if normalized_url not in scanned_urls:
                                    urls.add(url)
                                    scanned_urls.add(normalized_url)
            except:
                continue
        return urls

    def check_sqli(url):
        try:
            response = requests.get(url + "'", headers=get_random_headers(), verify=False, timeout=3)
            content = response.text.lower()
            return any((error.lower() in content for error in sql_errors))
        except:
            return False

    def worker(max_count):
        while not stop_event.is_set() and len(vulnerable_sites) < max_count:
            dork = random.choice(dorks)
            try:
                urls = search_urls(dork)
                for url in urls:
                    if stop_event.is_set() or len(vulnerable_sites) >= max_count:
                        return
                    if check_sqli(url):
                        with lock:
                            if url not in vulnerable_sites:
                                vulnerable_sites.add(url)
                                print(f"\n{COLOR_CODE['GREEN']}[+] Уязвимый сайт: {url}{COLOR_CODE['RESET']}")
            except:
                continue
    print(f"\n{COLOR_CODE['PINK']}{COLOR_CODE['BOLD']}[◆] {COLOR_CODE['WHITE']}Запуск SQL-сканера...")
    print(f"{COLOR_CODE['WHITE']}Используются {len(dorks)} dorks для поиска уязвимых сайтов\n")
    try:
        max_count = int(input(f"{COLOR_CODE['PINK']}[◆] {COLOR_CODE['WHITE']}Сколько уязвимостей найти (макс. 100)? → {COLOR_CODE['WHITE']}"))
        max_count = min(max(1, max_count), 100)
    except ValueError:
        max_count = 10
        print(f"{COLOR_CODE['PINK']}Используется значение по умолчанию: 10")
    thread_count = 20
    threads = []
    try:
        for _ in range(thread_count):
            t = threading.Thread(target=worker, args=(max_count,))
            t.daemon = True
            t.start()
            threads.append(t)
        while any((t.is_alive() for t in threads)) and len(vulnerable_sites) < max_count:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{COLOR_CODE['PINK']}Остановка сканирования...")
    finally:
        stop_event.set()
        for t in threads:
            t.join()
    print(f"\n{COLOR_CODE['GREEN']}Сканирование завершено!")
    print(f"{COLOR_CODE['WHITE']}Найдено уязвимых сайтов: {len(vulnerable_sites)}/{max_count}")
    if vulnerable_sites:
        print(f"\n{COLOR_CODE['GREEN']}Найденные уязвимые сайты:")
        for i, site in enumerate(vulnerable_sites, 1):
            print(f"{COLOR_CODE['WHITE']}{i}. {site}")
    else:
        print(f"{COLOR_CODE['PINK']}Уязвимых сайтов не найдено.")
    cls()



def dorking_search():
    import requests
    from bs4 import BeautifulSoup
    import urllib.parse
    import time
    dorks = ['inurl:login {query}', 'intitle:"index of" {query}', 'intext:"contact" {query}', 'filetype:pdf {query}', 'site:edu {query}', 'site:gov {query}', 'inurl:register {query}', 'inurl:profile {query}', 'inurl:forum {query}', 'ext:txt {query}']
    search_engines = {'Google': 'https://www.google.com/search?q={}', 'Bing': 'https://www.bing.com/search?q={}', 'DuckDuckGo': 'https://duckduckgo.com/html/?q={}'}
    query = input(f"\n{COLOR_CODE['PINK']}[◆] {COLOR_CODE['WHITE']}Введите тему для поиска → {COLOR_CODE['WHITE']}").strip()
    if not query:
        print(f"{COLOR_CODE['PINK']}Пустой запрос!{COLOR_CODE['RESET']}")
        cls()
        return
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for dork_template in dorks:
        dork = dork_template.format(query=query)
        print(f"\n{COLOR_CODE['PINK']}▶ Поиск с дорком: {COLOR_CODE['WHITE']}{dork}{COLOR_CODE['RESET']}")
        for engine_name, base_url in search_engines.items():
            url = base_url.format(urllib.parse.quote_plus(dork))
            print(f"{COLOR_CODE['PINK']}🔍› {engine_name}: {COLOR_CODE['WHITE']}{url}{COLOR_CODE['RESET']}")
            try:
                resp = requests.get(url, headers=headers, timeout=7)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'html.parser')
                links = []
                if engine_name == 'Google':
                    for g in soup.select('div.yuRUbf > a'):
                        href = g.get('href')
                        if href:
                            links.append(href)
                elif engine_name == 'Bing':
                    for li in soup.select('li.b_algo a'):
                        href = li.get('href')
                        if href:
                            links.append(href)
                elif engine_name == 'DuckDuckGo':
                    for a in soup.select('a.result__a'):
                        href = a.get('href')
                        if href:
                            links.append(href)
                if links:
                    for i, link in enumerate(links[:7], 1):
                        print(f"{COLOR_CODE['LI_G']}  {i}. {link}{COLOR_CODE['RESET']}")
                else:
                    print(f"{COLOR_CODE['PINK']}  Нет результатов.{COLOR_CODE['RESET']}")
            except Exception as e:
                print(f"{COLOR_CODE['PINK']}Ошибка при поиске на {engine_name}: {str(e)}{COLOR_CODE['RESET']}")
            time.sleep(2)
    cls()


def main():
    while True:
        banner()
        choice = input(f"\n{COLOR_CODE['PINK']}{COLOR_CODE['BOLD']}[◆] {COLOR_CODE['WHITE']}Введите опцию → {COLOR_CODE['WHITE']}")

        if choice == '1':
            sql_search()

        elif choice == '2':
            dorking_search()

        elif choice == '3':
            print(f"{COLOR_CODE['PINK']}Выход...{COLOR_CODE['RESET']}")
            break
        else:
            print(f"{COLOR_CODE['PINK']}Неверная опция.")
            cls()
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    main()