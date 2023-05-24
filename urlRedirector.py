import http.server
import http.client
import ssl

# Dictionary mapping URLs to proxy servers
proxy_servers = {
    'example.com': 'proxy1.example.com',
    'example.net': 'proxy2.example.com',
    # Add more mappings as needed
}

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract the requested URL
        url = self.path[1:]  # Remove leading forward slash

        # Find the appropriate proxy server for the requested URL
        proxy_server = None
        for key in proxy_servers:
            if key in url:
                proxy_server = proxy_servers[key]
                break

        if proxy_server is None:
            self.send_error(404, 'Proxy server not found')
            return

        # Connect to the proxy server
        conn = http.client.HTTPSConnection(proxy_server)

        try:
            # Forward the request to the proxy server
            conn.request('GET', url)
            response = conn.getresponse()

            # Send the response back to the client
            self.send_response(response.status)
            for header, value in response.getheaders():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.read())

        except Exception as e:
            self.send_error(500, str(e))

        finally:
            conn.close()

def run_proxy_server():
    # Create an HTTP server with the proxy handler
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, ProxyHandler)

    # Enable HTTPS support using self-signed certificate
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='certificate.pem', server_side=True)

    # Start the proxy server
    print('Proxy server is running on http://localhost:8000')
    httpd.serve_forever()

run_proxy_server()
