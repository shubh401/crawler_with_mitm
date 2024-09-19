FROM mcr.microsoft.com/playwright:v1.37.0-jammy

ENV PYTHONDONTWRITEBYTECODE=1
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright
ENV PYTHONUNBUFFERED=1

ARG VNC_PASS=test
ENV XVNC_PASS=$VNC_PASS

RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install python3-pip python3-tk python3-dev net-tools x11vnc xvfb fluxbox ca-certificates libnss3 libnss3-tools libatk-bridge2.0-0 libdrm-dev libxkbcommon-dev libgbm-dev libasound-dev libatspi2.0-0 libxshmfence-dev

ENV NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/cert.crt

WORKDIR /usr/local/share/ca-certificates/
COPY certificates/mitmproxy-ca-cert.cer mitmproxy-ca-cert.cer
COPY cert.crt .

WORKDIR /etc/ssl/certs/
COPY certificates/mitmproxy-ca-cert.cer mitmproxy-ca-cert.cer
COPY certificates/mitmproxy-ca-cert.pem mitmproxy-ca-cert.pem
COPY cert.pem cert.pem

RUN update-ca-certificates

RUN DEBIAN_FRONTEND=noninteractive mkdir -p $HOME/.pki/nssdb && certutil --empty-password -d $HOME/.pki/nssdb -N \
    && certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n cert.crt -i /usr/local/share/ca-certificates/cert.crt

RUN pip install playwright asyncio aiohttp mitmproxy
RUN playwright install

RUN mkdir -p ~/.vnc
RUN x11vnc -storepasswd $VNC_PASS ~/.vnc/passwd
