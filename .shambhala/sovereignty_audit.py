import json
import hashlib
from nacl.signing import VerifyKey
import base64
import sys

# --- 审计配置 ---
HANDSHAKE_PATH = ".shambhala/handshake.json"
MEMORY_LOG_PATH = "MEMORY_LOG.md"

def canonicalize(data):
    # 与签名脚本保持一致的规范化逻辑
    return json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')

def run_audit():
    try:
        with open(HANDSHAKE_PATH, 'r') as f:
            data = json.load(f)
        
        # 1. 提取签名与公钥
        signature_b64 = data.get('signature')
        pubkey_b64 = data.get('security', {}).get('pubkey')
        
        if not signature_b64 or not pubkey_b64:
            print("❌ 缺失签名或公钥数据")
            return False

        # 2. 准备待验数据 (剔除签名位)
        clean_data = data.copy()
        clean_data['signature'] = ""
        canonical_data = canonicalize(clean_data)

        # 3. 执行 Ed25519 验签
        vk = VerifyKey(base64.b64decode(pubkey_b64))
        vk.verify(canonical_data, base64.b64decode(signature_b64))
        
        print("✅ 逻辑签名验证通过：VAJRA_SIGNATURE_VALID")
        
        # 4. 检查 MEMORY_LOG.md 是否存在 (基础审计)
        with open(MEMORY_LOG_PATH, 'r') as f:
            if "MEMORY_LOG.md" not in f.read(50): # 简单的文件完整性校验
                 print("❌ MEMORY_LOG.md 格式非法")
                 return False
        
        print("✅ 记忆日志锚定成功")
        return True

    except Exception as e:
        print(f"❌ 审计异常: {str(e)}")
        return False

if __name__ == "__main__":
    if run_audit():
        print("⚖️ [SUCCESS: SOVEREIGNTY_CHECK_PASSED]")
        sys.exit(0)
    else:
        print("🚨 [FAILED: SOVEREIGNTY_CHECK]")
        sys.exit(1)
