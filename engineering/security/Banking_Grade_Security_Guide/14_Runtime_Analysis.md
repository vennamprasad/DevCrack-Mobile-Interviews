# 🎯 Runtime Analysis, Hooking & Anti-Tamper Verification

> **Defending against runtime memory tampering, Frida instrumentation, Magisk root cloaking, and debugger attachment in high-value mobile applications.**

---

## 🛠️ Runtime Threat Tools

| Tool | Threat Vector | Common Exploitation Technique |
|:---|:---|:---|
| **[Frida](https://frida.re/)** | Dynamic Binary Instrumentation | Hooking Java/Kotlin methods & native C functions to force `return true` |
| **[Objection](https://github.com/sensepost/objection)** | Runtime Mobile Exploration | Automated root/jailbreak bypass, keystore dumping, memory search |
| **[Magisk / KernelSU](https://github.com/topjohnwu/Magisk)** | Root Privileges & Zygisk | System-level permission elevation and root hiding modules (Shamiko) |
| **GDB / LLDB** | Native Debugger | Attaching to process via `ptrace` to inspect registers and memory |

---

## 📋 Runtime Resilience Audit Checklist

### 1. Frida Instrumentation Detection
- [ ] Check for default Frida listening ports (`27042`).
- [ ] Scan `/proc/self/maps` for injected libraries containing `frida-gadget`, `frida-agent`, or `gum-js-loop`.
- [ ] Check for named pipes (`/proc/self/fd`) matching Frida's thread communications.

### 2. Root & Environment Integrity
- [ ] Test detection against modern root frameworks: **KernelSU**, **APatch**, and **Magisk with Zygisk**.
- [ ] Inspect existence of test-keys build tags (`Build.TAGS.contains("test-keys")`).
- [ ] Verify standard `su` binary paths and writable `/system` or `/vendor` partitions.

### 3. Anti-Debugging Protection
- [ ] Verify that `Debug.isDebuggerConnected()` is continuously monitored.
- [ ] Implement native C `ptrace(PTRACE_TRACEME, 0, 1, 0)` call at application startup to block external debugger attachment.
- [ ] Monitor `/proc/self/status` for `TracerPid != 0`.

### 4. Memory Scraping & Screen Capture
- [ ] Verify that `getWindow().setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE)` is invoked before rendering sensitive views.
- [ ] Verify that sensitive memory variables (PINs, passwords, keys) are zeroized immediately after use.
