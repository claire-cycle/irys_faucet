import requests
import json
import time
import sys
from urllib.parse import urlparse

# === 读取配置 ===
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ 配置文件 config.json 不存在！")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ 配置文件格式错误！")
        sys.exit(1)

# === 读取地址和代理 ===
def load_addresses_and_proxies(config):
    try:
        with open(config['address_file'], 'r', encoding='utf-8') as f:
            addresses = [line.strip() for line in f.readlines() if line.strip()]
        
        with open(config['proxy_file'], 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        
        if len(addresses) != len(proxies):
            print("❌ 地址数量和代理数量不一致！")
            sys.exit(1)
        
        return addresses, proxies
    except FileNotFoundError as e:
        print(f"❌ 文件不存在：{e.filename}")
        sys.exit(1)

# === 创建 CAPTCHA 任务 ===
def create_captcha_task(wallet, proxy, config):
    proxy_dict = {
        'http': proxy,
        'https': proxy
    }
    
    payload = {
        'clientKey': config['api_key'],
        'task': {
            'type': 'TurnstileTaskProxyless',
            'websiteURL': config['website_url'],
            'websiteKey': config['site_key']
        },
        "softID": "51545"
    }
    
    try:
        response = requests.post(
            'https://api.yescaptcha.com/createTask',
            json=payload,
            proxies=proxy_dict,
            timeout=30
        )
        response.raise_for_status()
        task_res = response.json()
        
        if 'taskId' not in task_res:
            print(f"❌ 创建 CAPTCHA 失败 - {wallet}")
            print(f"返回内容：{task_res}")
            return None
        
        return task_res['taskId']
    except requests.exceptions.RequestException as e:
        print(f"❌ 创建 CAPTCHA 请求失败 - {wallet}: {e}")
        return None

# === 轮询 CAPTCHA 结果 ===
def get_captcha_result(task_id, wallet, config):
    payload = {
        'clientKey': config['api_key'],
        'taskId': task_id
    }
    
    while True:
        time.sleep(config['captcha_wait_time'])
        
        try:
            response = requests.post(
                'https://api.yescaptcha.com/getTaskResult',
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            res = response.json()
            
            if res.get('status') == 'ready':
                return res['solution']['token']
            else:
                print(f"⏳ 等待 CAPTCHA：{wallet}")
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取 CAPTCHA 结果失败 - {wallet}: {e}")
            time.sleep(config['captcha_wait_time'])

# === 请求 Faucet ===
def request_faucet(wallet, token, proxy, config):
    proxy_dict = {
        'http': proxy,
        'https': proxy
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Origin': config['website_url'],
        'Referer': config['website_url'],
        'User-Agent': config['user_agent']
    }
    
    payload = {
        'captchaToken': token,
        'walletAddress': wallet
    }
    
    try:
        response = requests.post(
            'https://irys.xyz/api/faucet',
            json=payload,
            headers=headers,
            proxies=proxy_dict,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e

# === 主流程 ===
def main():
    config = load_config()
    addresses, proxies = load_addresses_and_proxies(config)
    
    print(f"📋 共加载 {len(addresses)} 个地址和代理")
    print("🚀 开始批量领取...\n")
    
    for i, (wallet, proxy) in enumerate(zip(addresses, proxies), 1):
        print(f"🚀 [{i}/{len(addresses)}] 开始领取：{wallet}（代理：{proxy}）")
        
        try:
            # 创建 CAPTCHA 任务
            task_id = create_captcha_task(wallet, proxy, config)
            if not task_id:
                continue
            
            # 获取 CAPTCHA 结果
            captcha_token = get_captcha_result(task_id, wallet, config)
            if not captcha_token:
                continue
            
            # 请求 Faucet
            result = request_faucet(wallet, captcha_token, proxy, config)
            print(f"✅ 成功领取 {wallet}：{result.get('message', '未知响应')}")
            
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data
                except:
                    error_msg = e.response.text
            print(f"❌ {wallet} 出错：{error_msg}")
        except Exception as e:
            print(f"❌ {wallet} 出错：{str(e)}")
        
        print("-----------------------------")
    
    print("🎉 所有任务完成！")

if __name__ == "__main__":
    main()