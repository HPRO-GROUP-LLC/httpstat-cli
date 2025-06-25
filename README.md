
Here’s a feature-complete upgrade to your httpstat-cli.py tool with a --test-proxy mode that:

✅ Tests both http:// and https://
✅ Detects CONNECT tunnel support
✅ Verifies proxy auth
✅ Measures latency
✅ Uses same credentials/params as httpstat

🧪 Usage Examples
Action	Command
Basic HTTP test	httpstat --test-proxy -x 1.2.3.4 -p 8080
Test + Auth	httpstat --test-proxy -x 1.2.3.4 -p 8080 -U user -P pass
Force SOCKS5 test	httpstat --test-proxy -x 1.2.3.4 -p 1080 --socks
Run actual HTTPStat	httpstat https://example.com -x 1.2.3.4 -p 8080 -U user -P pass


Install httpstat : pip install httpstat
