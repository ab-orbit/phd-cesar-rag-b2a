import os
from dotenv import load_dotenv

load_dotenv()
pk = os.getenv("LANGFUSE_PUBLIC_KEY")
sk = os.getenv("LANGFUSE_SECRET_KEY")
host = os.getenv("LANGFUSE_HOST")

print("Keys carregadas:")
print("PK starts with:", str(pk)[:10] if pk else None)
print("SK starts with:", str(sk)[:10] if sk else None)
print("Host:", host)
