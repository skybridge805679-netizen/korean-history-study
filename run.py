from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import webbrowser
ROOT=Path(__file__).resolve().parent/'site'
PORT=8791
server=ThreadingHTTPServer(('127.0.0.1',PORT),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
url=f'http://127.0.0.1:{PORT}/'
print('사이트를 여는 중: '+url+'\n종료하려면 Ctrl+C를 누르세요.')
webbrowser.open(url)
try: server.serve_forever()
except KeyboardInterrupt: pass
finally: server.server_close()
