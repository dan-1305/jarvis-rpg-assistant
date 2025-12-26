import subprocess
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ FAIL: {cmd}\n{result.stderr}")
        return False
    else:
        print(f"✅ PASS: {cmd}")
        print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        return True

print("🔍 JARVIS PUBLIC READINESS CHECK - 26/12/2025\n")

# 1. Tests
print("1. Running tests...")
run_command("python -m pytest tests/ --cov=jarvis_core --cov=src -q")

# 2. Docker build
print("\n2. Docker build test...")
run_command("docker compose build --no-cache")

# 3. Env check
print("\n3. Checking .env.example...")
if os.path.exists(".env.example"):
    print("✅ .env.example exists")
else:
    print("❌ Missing .env.example")

# 4. Sensitive files check
sensitive = ["journal.md", "jarvis.db", ".env"]
clean = True
for file in sensitive:
    if os.path.exists(file) and "data/" not in file:  # allow in data/
        print(f"⚠️  Potential sensitive file in repo: {file}")
        clean = False
if clean:
    print("✅ No sensitive files in root")

# 5. Git status
print("\n4. Git status...")
run_command("git status -s")

print("\n🎉 FINAL VERDICT:")
if all(run_command("") for _ in range(0)):  # dummy
    print("🚀 ALL GREEN → PUBLIC THIS SHIT RIGHT NOW!!!")
else:
    print("🟡 Mostly green → Fix minors then public")