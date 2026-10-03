> **ReconLite** is a lightweight, multi-threaded CLI reconnaissance toolkit written in Python. Designed for rapid target assessment, it combines subdomain enumeration, web directory discovery, and port scanning into a unified, high-performance tool.

---

## ⚡ Features

- **Subdomain Enumeration:** Bruteforce hidden subdomains using target wordlists with status code tracking (`200`, `301`, `302`, `403`).
- **Directory Discovery:** Perform multi-threaded endpoint and directory fuzzing against web servers.
- **Port Scanner:** Execute fast multi-threaded TCP connect scans across target ports (1–1024).
- **High Performance:** Powered by Python's `concurrent.futures.ThreadPoolExecutor` for concurrent scanning.
- **User-Agent Masquerading:** Custom request headers prevent automatic blocking by Web Application Firewalls (WAFs).
- **Styled Terminal Output:** Clean ANSI color coding and visual cues for open ports and HTTP status responses.
