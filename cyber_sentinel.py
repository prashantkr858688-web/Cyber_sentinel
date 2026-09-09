import json
import urllib.request
import urllib.error
import ssl

API_KEY ="Your Gemini Api key"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"

def run_cyber_audit(payload):
    prompt = f"""
    Analyze this message for cyber fraud in concise English:
    "{payload}"
    Output:
    - Threat Level: [SAFE / SUSPICIOUS / CRITICAL]
    - Threat Score: [0-100%]
    - Vector: (e.g. Bank Phishing, Job Scam)
    - Red Flags: (1-2 bullet points)
    - Advice: (1 line actionable advice)
    """

    req_data = {"contents": [{"parts": [{"text": prompt}]}]}
    data_bytes = json.dumps(req_data).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "Content-Type": "application/json",
            "Connection": "close",
            "User-Agent": "Mozilla/5.0"
        }
    )

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=25) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Scan Error: {e}"

print("=== CYBER-SENTINEL v1.0 ===")
print("Type 'q' to exit.\n")

while True:
    try:
        msg = input("\n[Paste text here]: ").strip()
    except:
        break

    if msg.lower() in ["q", "exit", "quit"]:
        print("\nExited.")
        break

    if not msg:
        continue

    print("[+] Analyzing...")
    print("\n" + run_cyber_audit(msg))
    print("-" * 30)
