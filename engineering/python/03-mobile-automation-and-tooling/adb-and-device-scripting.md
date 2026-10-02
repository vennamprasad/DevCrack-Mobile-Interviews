# 📱 Android ADB & Device Automation with Python

> **Automate device interactions, screen recording, battery stats, monkey testing, and CI/CD test farm execution using Python and `adb`.**

---

## ⚡ 1. Direct ADB Wrapper in Python

You can interact with connected devices directly via Python using `subprocess` or `pure-python-adb`:

```python
import subprocess
import time

class ADBDevice:
    def __init__(self, serial: str = None):
        self.cmd_prefix = ["adb", "-s", serial] if serial else ["adb"]

    def run_cmd(self, *args) -> str:
        res = subprocess.run(self.cmd_prefix + list(args), capture_output=True, text=True, check=True)
        return res.stdout.strip()

    def install_apk(self, apk_path: str):
        print(f"📦 Installing {apk_path}...")
        self.run_cmd("install", "-r", "-g", apk_path)

    def launch_app(self, package_name: str, activity_name: str):
        print(f"🚀 Launching {package_name}/{activity_name}...")
        self.run_cmd("shell", "am", "start", "-n", f"{package_name}/{activity_name}")

    def take_screenshot(self, output_path: str):
        self.run_cmd("shell", "screencap", "-p", "/sdcard/screen.png")
        self.run_cmd("pull", "/sdcard/screen.png", output_path)
        self.run_cmd("shell", "rm", "/sdcard/screen.png")
        print(f"📸 Screenshot saved to {output_path}")

    def get_memory_info(self, package_name: str) -> str:
        return self.run_cmd("shell", "dumpsys", "meminfo", package_name)

# Example Usage
if __name__ == "__main__":
    device = ADBDevice()
    print("Connected devices:\n", subprocess.run(["adb", "devices"], capture_output=True, text=True).stdout)
```

---

## 🐒 2. Automated Monkey Chaos Testing

Run 5,000 pseudo-random UI events to detect ANRs and unhandled crashes:

```python
def run_monkey_test(package: str, events: int = 5000):
    cmd = [
        "adb", "shell", "monkey",
        "-p", package,
        "--throttle", "100",  # 100ms between events
        "--ignore-crashes",
        "--ignore-timeouts",
        "-v", str(events)
    ]
    print(f"🐒 Running monkey test on {package} ({events} events)...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if "CRASH" in result.stdout or "ANR" in result.stdout:
        print("⚠️ Potential crash or ANR detected!")
    else:
        print("✅ Monkey test completed without fatal exceptions.")
```
