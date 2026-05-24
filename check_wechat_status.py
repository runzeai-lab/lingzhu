import json
import requests
import time

# 读取配置
with open('E:/WorkBuddy/Claw/wechat_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

app_id = config['wechat_official_account']['app_id']
app_secret = config['wechat_official_account']['app_secret']

# 获取 access_token
def get_access_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        resp = requests.get(url, timeout=30)
        data = resp.json()
        if 'access_token' in data:
            print(f"✅ 获取 access_token 成功")
            print(f"   Token: {data['access_token'][:20]}...")
            print(f"   有效期: {data['expires_in']} 秒")
            return data['access_token']
        else:
            print(f"❌ 获取 access_token 失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

# 查询草稿箱
def get_drafts(token):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}"
    payload = {
        "offset": 0,
        "count": 20,
        "no_content": 1  # 不返回 content，只返回元数据
    }
    try:
        body_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        resp = requests.post(url, data=body_bytes, headers=headers, timeout=30)
        data = resp.json()
        print(f"\n查询草稿箱结果:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return data
    except Exception as e:
        print(f"❌ 查询草稿箱失败: {e}")
        return None

# 主流程
print("=== 微信公众号发布状态检查 ===\n")

token = get_access_token(app_id, app_secret)
if token:
    get_drafts(token)
else:
    print("\n❌ 无法获取 access_token，请检查配置")
