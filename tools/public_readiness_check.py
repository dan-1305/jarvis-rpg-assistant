import subprocess
import os
import sys
import io

# Fix encoding Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_command(cmd, ignore_warning=False):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ FAIL: {cmd}\n{result.stderr.strip()}")
        return False
    else:
        output = result.stdout.strip()
        if output:
            # Ignore Docker version warning
            if ignore_warning and "the attribute `version` is obsolete" in output:
                print(f"✅ PASS: {cmd} (warning ignored)")
            else:
                print(f"✅ PASS: {cmd}")
                print(output[:500] + "..." if len(output) > 500 else output)
        else:
            print(f"✅ PASS: {cmd} (no output)")
        return True

print("🔍 JARVIS PUBLIC READINESS CHECK - 26/12/2025\n")

all_green = True

# 1. Tests
print("1. Running tests...")
if not run_command("python -m pytest tests/ --cov=jarvis_core --cov=src -q"):
    all_green = False

# 2. Docker build
print("\n2. Docker build test...")
# Ignore obsolete version warning
if not run_command("docker compose build --no-cache", ignore_warning=True):
    all_green = False

# 3. .env.example check
print("\n3. Checking .env.example...")
if os.path.exists(".env.example"):
    print("✅ .env.example exists")
else:
    print("❌ Missing .env.example")
    all_green = False

# 4. Sensitive files check
print("\n4. Sensitive files in root check...")
sensitive = [".env"]
clean = True
for file in sensitive:
    if os.path.exists(file):
        print(f"⚠️  Potential sensitive file in repo: {file}")
        clean = False
        all_green = False
if clean:
    print("✅ No sensitive files in root")

# 5. Git status
print("\n5. Git status (clean working tree?)...")
git_status = subprocess.run("git status -s", shell=True, capture_output=True, text=True).stdout.strip()
if git_status:
    print(f"⚠️  Uncommitted changes:\n{git_status}")
else:
    print("✅ Git working tree clean")

print("\n🎉 FINAL VERDICT:")
if all_green:
    print("🚀 ALL GREEN → PUBLIC THIS SHIT RIGHT NOW!!! 🎉")
    print("   Repo sẵn sàng làm portfolio flagship!")
else:
    print("🟡 Mostly green → Fix minors còn lại rồi public ngay!")
