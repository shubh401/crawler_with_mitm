from mitmproxy import http
import os

class MyAddon:
    def __init__(self):
        self.log_file = open(f"/app/extensions/proxy_logs/{os.getenv('TEST_ID')}.log", "w")

    def request(self, flow: http.HTTPFlow) -> None:
        # Log the request URL and initiator
        initiator = flow.request.headers.get('referer')
        if not initiator: initiator = flow.request.headers.get('Origin')
        log_entry = f"Request URL: {flow.request.url} --- Initiator: {initiator}\n"
        self.log_file.write(log_entry)
        self.log_file.flush()

addons = [MyAddon()]

if __name__ == "__main__":
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__] + addons)