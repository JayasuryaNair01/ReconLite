# ReconLite

A small multi-threaded reconnaissance CLI I wrote in Python while learning how
basic recon tools work. It's a personal learning project — for practising on
targets I'm allowed to test, not a replacement for mature tools.

## What it does

- **Subdomain enumeration** — brute-forces subdomains from a wordlist and
  reports hosts returning `200`, `301`, `302`, or `403`.
- **Directory / file discovery** — requests paths from a wordlist against a
  target URL and reports the same status codes.
- **Port scanner** — TCP connect scan across ports 1–1024.

It uses `concurrent.futures.ThreadPoolExecutor` to run requests concurrently,
and sends a browser-like `User-Agent` header so default `python-requests`
traffic is less obvious. (That's a simple header change, not a WAF bypass.)

## Requirements

- Python 3.8+
- `requests` (`pip install requests`)

## Usage

```bash
git clone https://github.com/JayasuryaNair01/ReconLite.git
cd ReconLite
pip install requests
python3 main.py
```

Then pick an option from the menu and follow the prompts (target, wordlist).

## Legal / authorized use only

Use this only against systems you own or have explicit written permission to
test (your own lab, CTFs, or in-scope bug bounty targets). Unauthorized
scanning may be illegal. You are responsible for how you use it.

## Limitations / notes

- Results depend entirely on the wordlist you supply.
- Timeouts are short, so slow hosts may be missed.
- The port scan is a basic TCP connect scan (no service/version detection).
- Built to learn; still a work in progress.

## License

MIT (see `LICENSE`).
