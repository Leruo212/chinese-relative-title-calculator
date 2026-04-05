"""
亲戚称呼计算器 - Web服务
使用 Python 内置 http.server，无需额外安装依赖
"""
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from calculator import get_title, search_relations, get_all_relations_by_generation
from relations import RELATION_OPTIONS, ALL_RELATIONS

class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self._serve_file("index.html", "text/html; charset=utf-8")

        elif path == "/api/all":
            data = get_all_relations_by_generation()
            self._json(data)

        elif path == "/api/options":
            result = []
            for display_name, rel_path, gender in RELATION_OPTIONS:
                result.append({
                    "display": display_name,
                    "path": rel_path,
                    "gender": gender,
                    "male_title": ALL_RELATIONS.get(rel_path, {}).get("male", ""),
                    "female_title": ALL_RELATIONS.get(rel_path, {}).get("female", ""),
                })
            self._json(result)

        elif path == "/api/calc":
            rel_path = query.get("path", [""])[0]
            target_gender = query.get("target_gender", ["male"])[0]
            my_gender = query.get("my_gender", ["male"])[0]
            if rel_path:
                result = get_title(rel_path, target_gender, my_gender)
                self._json(result)
            else:
                self._json({"error": "缺少 path 参数"}, 400)

        elif path == "/api/search":
            kw = query.get("q", [""])[0]
            results = search_relations(kw)
            self._json(results)

        else:
            self._json({"error": "Not found"}, 404)

    def _serve_file(self, filename, content_type):
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            content = filepath.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = 8765
    server = HTTPServer(("localhost", port), Handler)
    print(f"✅ 亲戚称呼计算器已启动！")
    print(f"🌐 请在浏览器访问: http://localhost:{port}")
    print(f"按 Ctrl+C 可停止服务")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止。")
