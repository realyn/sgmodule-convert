class URLConfig:
    URLS = {
        'weibo': 'https://kelee.one/Tool/Loon/Plugin/Weibo_remove_ads.plugin',
        'weibo_js': 'https://kelee.one/Resource/Script/Weibo/Weibo_remove_ads.js',
        'himalaya': 'https://kelee.one/Tool/Loon/Plugin/Himalaya_remove_ads.plugin'
    }

import requests
from pathlib import Path
import os
from datetime import datetime

def fetch_script(script_name):
    # 改为使用 loon-plugin 目录
    output_dir = Path("loon-plugin")
    output_dir.mkdir(exist_ok=True)
    
    if script_name not in URLConfig.URLS:
        print(f"未找到脚本: {script_name}")
        print(f"可用的脚本: {list(URLConfig.URLS.keys())}")
        return False
        
    url = URLConfig.URLS[script_name]
    headers = {
        'user-agent': 'Loon/805 CFNetwork/1335.0.3.4 Darwin/21.6.0',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh-Hans;q=0.9',
        'accept-encoding': 'gzip, deflate, br'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        output_file = output_dir / Path(url).name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"文件已保存到: {output_file}")
        
        # 更新时间记录
        update_time_file = output_dir / "update_time.txt"
        with open(update_time_file, "a", encoding='utf-8') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Updated {script_name}\n")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"下载失败 {script_name}: {e}")
        return False

def fetch_all_scripts():
    success_count = 0
    total_count = len(URLConfig.URLS)
    
    for script_name in URLConfig.URLS:
        if fetch_script(script_name):
            success_count += 1
            
    print(f"\n下载完成: 成功 {success_count}/{total_count}")

if __name__ == '__main__':
    fetch_all_scripts()
