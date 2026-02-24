# 🔍 Network Scanner

A fast, multi-threaded TCP port scanner written in Python — built for network reconnaissance and security auditing on authorized systems.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square)

---

## ✨ Features

- ⚡ **Multi-threaded scanning** — up to 500 concurrent threads
- 🧩 **Service detection** — identifies common protocols (HTTP, SSH, FTP, etc.)
- 📡 **Banner grabbing** — retrieves service version banners from open ports
- 📊 **Real-time progress bar** — live scan feedback in the terminal
- 💾 **JSON report export** — save results for further analysis
- 🎯 **Flexible port targeting** — ranges, lists, or single ports

---

## 📦 Installation

```bash
git clone https://github.com/mervesudeboler/network-scanner.git
cd network-scanner
python3 scanner.py --help
```

> No external dependencies required — uses Python standard library only.

---

## 🚀 Usage

### Basic scan (ports 1–1024)
```bash
python3 scanner.py 192.168.1.1
```

### Custom port range
```bash
python3 scanner.py 192.168.1.1 --ports 1-65535
```

### Specific ports with banner grabbing
```bash
python3 scanner.py scanme.nmap.org --ports 22,80,443,8080 --banner
```

### Full scan with JSON output
```bash
python3 scanner.py 192.168.1.1 --ports 1-1024 --threads 300 --banner --output results.json
```

---

## ⚙️ Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--ports` | `-p` | `1-1024` | Port range or list |
| `--timeout` | `-t` | `1.0` | Connection timeout in seconds |
| `--threads` | `-T` | `200` | Number of concurrent threads |
| `--banner` | `-b` | off | Enable banner grabbing |
| `--output` | `-o` | — | Save report as JSON |

---

## 📸 Sample Output

```
═══════════════════════════════════════════════════════
  🔍  Network Scanner
═══════════════════════════════════════════════════════
  Target   : scanme.nmap.org (45.33.32.156)
  Ports    : 1-1024 (1024 total)
  Threads  : 200
  Started  : 2025-02-24 16:30:00
═══════════════════════════════════════════════════════

  [OPEN]     22/tcp  ssh              -> SSH-2.0-OpenSSH_6.6.1p1
  [OPEN]     80/tcp  http             -> HTTP/1.1 200 OK
  [OPEN]    443/tcp  https

═══════════════════════════════════════════════════════
  Scan complete. 3 open port(s) found.
═══════════════════════════════════════════════════════
```

---

## ⚠️ Legal Disclaimer

> This tool is intended for **educational purposes** and **authorized penetration testing only**.
> Scanning networks or systems without explicit permission is **illegal** and unethical.
> The author is not responsible for any misuse.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Concurrency:** `concurrent.futures.ThreadPoolExecutor`
- **Networking:** `socket` (TCP connect scan)
- **CLI:** `argparse`
- **Output:** `json`

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
