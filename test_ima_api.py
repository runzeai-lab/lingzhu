#!/usr/bin/env python3
"""测试 IMA API 调用"""
import http.client, json

CLIENT_ID = "910fce0cc27f5685b8f06c9d88a9ae1e"
API_KEY = "BrqdfQbt50sKsme7VZX0xeTR4qwEYjS+vxUJP/2wiG5S57RGo7JB9uCh290CcXZuu6g88F4U8A=="

print("测试 IMA API 调用...")
print("=" * 60)

# 测试1: 搜索知识库
print("\n[测试1] 搜索知识库: query='经典V102'")
conn = http.client.HTTPSConnection("ima.qq.com", timeout=10)
headers = {
    "Content-Type": "application/json",
    "ima-openapi-clientid": CLIENT_ID,
    "ima-openapi-apikey": API_KEY
}
body = json.dumps({
    "query": "经典V102",
    "cursor": "",
    "limit": 10
})
conn.request("POST", "/openapi/wiki/v1/search_knowledge_base", body, headers)
response = conn.getresponse()
data = response.read().decode("utf-8")
conn.close()

print(f"状态码: {response.status}")
print(f"响应: {data[:200]}...")

result = json.loads(data)
if result.get("retcode", 0) == 0 or result.get("code", 0) == 0:
    print("✅ API 调用成功！")
    infos = result.get("data", {}).get("infos", [])
    print(f"找到 {len(infos)} 个知识库:")
    for kb in infos:
        print(f"  - {kb.get('name', '')} (ID: {kb.get('id', '')})")
else:
    print(f"❌ API 调用失败: {result.get('errmsg', result.get('msg', 'Unknown error'))}")

print("\n" + "=" * 60)
print("测试完成")
