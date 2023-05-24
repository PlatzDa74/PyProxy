# PyProxy
A proxy to abuse our stupid proxy, ssh tunnel chaos and firewalls

In this example, the proxy server listens on PROXY_HOST and PROXY_PORT. When a client connects, it reads the first byte of the handshake to determine the client type. If it starts with 0x16 (which is the SSL/TLS handshake start byte), it assumes the client is using HTTPS and forwards the traffic to the HTTPS server specified by HTTPS_HOST and HTTPS_PORT. Otherwise, it assumes the client is using SSH and forwards the traffic to the SSH server specified by `
