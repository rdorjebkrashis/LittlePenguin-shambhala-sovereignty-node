import json
import hashlib
from nacl.signing import SigningKey
import base64

# --- 逻辑锚点 ---
HANDSHAKE_PATH = ".shambhala/handshake.json"
PRIVATE_KEY_PATH = "path/to/your/private.key" # 绝对不要上传此文件

def canonicalize_json(data):
    # 实现 RFC8785 简易规范化：排序键名，去除空格
    return json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')

def sign_protocol():
    with open(HANDSHAKE_PATH, 'r') as f:
        data = json.load(f)
    
    # 移除旧签名准备重新计算
    data['signature'] = ""
    
    # 规范化并计算哈希
    canonical_data = canonicalize_json(data)
    
    # 执行 Ed25519 签名 (这里需要你本地的私钥)
    # sk = SigningKey(private_key_bytes) 
    # sig = sk.sign(canonical_data).signature
    # print(f"Signature: {base64.b64encode(sig).decode()}")
    
    print("已生成规范化待签数据。请在本地私密环境完成签署。")

if __name__ == "__main__":
    sign_protocol()
