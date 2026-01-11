from base64    import b64encode, b64decode
from secrets   import token_bytes
from coincurve import PrivateKey
from hashlib   import sha256

class Anon:
    
    
    @staticmethod
    def publicKeyCreate(e) -> list:
        privkey = PrivateKey(bytes(e))
        publicKey = privkey.public_key.format(compressed=True)
        return list(publicKey)

    @staticmethod
    def xor(e) -> str:
        t = ""
        for n in range(len(e)):
            t += chr(e[n])
        return b64encode(t.encode('latin-1')).decode()

    @staticmethod
    def generate_keys() -> dict:
        e = token_bytes(32)
        n = Anon.publicKeyCreate(e)
        r = Anon.xor(e)
        
        return {
            "privateKey": r,
            "userPublicKey": n
        }
    
    @staticmethod
    def sign_challenge(challenge_data: bytes, key: str) -> dict:

        key_bytes: bytes = b64decode(key)
        privkey: PrivateKey = PrivateKey(key_bytes)
        signature: bytes = privkey.sign_recoverable(sha256(challenge_data).digest(), hasher=None)[:64]
        
        return {
            "challenge": b64encode(challenge_data).decode(),
            "signature": b64encode(signature).decode()
        }
