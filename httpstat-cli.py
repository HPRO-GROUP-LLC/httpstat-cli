#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
httpstat-cli: Wrapper for httpstat with proxy support, SOCKS fallback, and test mode.
"""

import re
import sys
import os
import time
import argparse
import subprocess
from httpstat import main as httpstat_main

def build_proxy_url(proto, host, port, user=None, pw=None):
    auth = f'{user}:{pw}@' if user and pw else ''
    return f'{proto}://{auth}{host}:{port}'

def test_proxy(proxy_url, test_url):
    try:
        start = time.time()
        result = subprocess.run(
            ['curl', '--proxy', proxy_url, '--max-time', '5', '-I', '-s', test_url],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        latency = round((time.time() - start) * 1000)
        print(f"[✔] {test_url} OK via {proxy_url} ({latency} ms)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[✘] {test_url} failed via {proxy_url}")
        print(e.stderr.decode().strip())
        return False

def main():
    parser = argparse.ArgumentParser(description='httpstat CLI with proxy support and test mode')
    parser.add_argument('url', nargs='?', help='Target URL (e.g., https://example.com)')
    parser.add_argument('-x', '--proxy-host', help='Proxy IP or hostname')
    parser.add_argument('-p', '--proxy-port', type=int, help='Proxy port number')
    parser.add_argument('-U', '--proxy-user', help='Proxy username (optional)')
    parser.add_argument('-P', '--proxy-pass', help='Proxy password (optional)')
    parser.add_argument('--socks', action='store_true', help='Use SOCKS5 proxy instead of HTTP')
    parser.add_argument('--test-proxy', action='store_true', help='Test proxy for HTTP and HTTPS support')
    parser.add_argument('extra_args', nargs=argparse.REMAINDER, help='Extra args passed to curl via httpstat')

    args = parser.parse_args()

    if args.test_proxy:
        if not args.proxy_host or not args.proxy_port:
            print("[!] --test-proxy requires -x and -p arguments")
            sys.exit(1)
        proto = 'socks5h' if args.socks else 'http'
        proxy_url = build_proxy_url(proto, args.proxy_host, args.proxy_port, args.proxy_user, args.proxy_pass)
        print(f"[i] Testing proxy: {proxy_url}")
        test_proxy(proxy_url, 'http://example.com')
        test_proxy(proxy_url, 'https://www.google.com')
        sys.exit(0)

    if args.proxy_host and args.proxy_port:
        proto = 'socks5h' if args.socks else 'http'
        proxy_url = build_proxy_url(proto, args.proxy_host, args.proxy_port)
        os.environ['http_proxy'] = proxy_url
        os.environ['https_proxy'] = proxy_url
        args.extra_args = ['--proxy', proxy_url] + args.extra_args
        if args.proxy_user and args.proxy_pass:
            args.extra_args = ['--proxy-user', f'{args.proxy_user}:{args.proxy_pass}'] + args.extra_args

    if not args.url:
        print("[!] URL is required unless --test-proxy is used.")
        sys.exit(1)

    sys.argv = ['httpstat'] + [args.url] + args.extra_args
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(httpstat_main())

if __name__ == '__main__':
    main()
