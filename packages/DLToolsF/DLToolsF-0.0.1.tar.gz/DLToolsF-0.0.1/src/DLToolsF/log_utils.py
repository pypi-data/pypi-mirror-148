import requests
import os

def SET_URL(url):
    """
    设置转发服务器地址, 一次设置, 永久生效
    """
    with open(os.path.join(os.path.dirname(__file__), "url_temp"), "w", encoding="utf-8") as fp:
        fp.write(url)

def print_remote(user_id, server_name, message):
    try:
        with open(os.path.join(os.path.dirname(__file__), "url_temp"), "r", encoding="utf-8") as fp:
            url = fp.read()
    except:
        print("无法读取有效url, 请重新设置(SET_URL)")
    try:
        re = requests.get(url + f"?userId={user_id}&serverName={server_name}&message={message}")
        if re.status_code != 200:
            print("远程消息递送失败!")
    except Exception as e:
            print(f"远程消息递送失败! {str(e)}")