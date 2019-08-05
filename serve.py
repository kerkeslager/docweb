import http.server
import json
import os

import rendering

EXAMPLES_DIRECTORY = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'examples',
)

LITERALS = set([
    '/framework.js',
    '/script.js',
    '/style.css',
])

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('index.html', 'r') as f:
                source = f.read()

            self.send_response(200)
            self.send_header('Content-type','text/html;charset=utf-8')
            self.end_headers()
            self.wfile.write(source.encode('utf-8'))
            return

        elif self.path in LITERALS:
            with open(self.path[1:], 'r') as f:
                source = f.read()

            self.send_response(200)

            if self.path.endswith('.js'):
                self.send_header('Content-type','text/javascript;charset=utf-8')
            else:
                self.send_header('Content-type','text/html;charset=utf-8')

            self.end_headers()
            self.wfile.write(source.encode('utf-8'))
            return

        file_path = os.path.join(
            EXAMPLES_DIRECTORY,
            self.path[1:] if self.path.startswith('/') else self.path,
        )

        try:
            with open(file_path, 'r') as f:
                source = f.read()

        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type','text/plain;charset=utf-8')
            self.end_headers()
            self.wfile.write('File "{}" not found'.format(file_path).encode('utf-8'))
            return

        try:
            source_json = json.loads(source)

        except json.decoder.JSONDecodeError:
            self.send_response(500)
            self.send_header('Content-type','text/plain;charset=utf-8')
            self.end_headers()
            self.wfile.write('Invalid file "{}"'.format(file_path).encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-type','text/html;charset=utf-8')
        self.end_headers()
        self.wfile.write(
            rendering.as_page(rendering.render(source_json)).encode('utf-8')
        )


if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('', 8080), Handler)
    server.serve_forever()
