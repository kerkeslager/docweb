import http.server
import os

import rendering

EXAMPLES_DIRECTORY = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'examples',
)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = os.path.join(
            EXAMPLES_DIRECTORY,
            self.path[1:] if self.path.startswith('/') else self.path,
        )

        try:
            with open(file_path, 'r') as f:
                source = f.read()

        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('File "{}" not found'.format(file_path).encode('utf-8'))

        else:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(rendering.render(source).encode('utf-8'))


if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('', 8080), Handler)
    server.serve_forever()
