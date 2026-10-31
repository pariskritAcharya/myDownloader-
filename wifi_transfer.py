import http.server
import socketserver
import socket
import threading
import qrcode
import os
import urllib.parse
import html
import io

is_server_running = False

class MobileAppUIHandler(http.server.SimpleHTTPRequestHandler):
   def list_directory(self, path):
        """Overrides the default directory list to show files from all sub-folders"""
        
        # Build the HTML and CSS for the mobile page
        html_content = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>MyDownloader Sync</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }}
                h2 {{ color: #1c1e21; text-align: center; margin-bottom: 25px; }}
                .file-list {{ display: flex; flex-direction: column; gap: 12px; max-width: 600px; margin: 0 auto; }}
                .file-item {{ display: flex; justify-content: space-between; align-items: center; background: white; padding: 16px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
                .file-name {{ font-size: 15px; color: #333; word-break: break-word; margin-right: 15px; font-weight: 500; line-height: 1.4; }}
                .folder-tag {{ font-size: 12px; color: #888; display: block; margin-top: 4px; }}
                .download-btn {{ background-color: #007bff; color: white; text-decoration: none; padding: 10px 18px; border-radius: 8px; font-weight: bold; font-size: 14px; white-space: nowrap; box-shadow: 0 2px 4px rgba(0,123,255,0.3); }}
                .download-btn:active {{ background-color: #0056b3; transform: scale(0.98); }}
                .empty {{ text-align: center; color: #888; margin-top: 30px; font-size: 16px; }}
            </style>
        </head>
        <body>
            <h2>📱 Download Center</h2>
            <div class="file-list">
        """
        
        has_files = False
        
        # os.walk digs into the main folder AND all sub-folders (like /audio and /video)
        for root, dirs, files in os.walk(path):
            for name in sorted(files, key=lambda x: x.lower()):
                # Skip hidden files
                if name.startswith('.'):
                    continue
                    
                has_files = True
                
                # Figure out the exact relative path for the download link
                rel_dir = os.path.relpath(root, path).replace('\\', '/')
                if rel_dir == ".":
                    file_path = name
                    folder_label = ""
                else:
                    file_path = f"{rel_dir}/{name}"
                    folder_label = f"<span class='folder-tag'>📁 {rel_dir}</span>"
                
                safe_link = urllib.parse.quote(file_path)
                safe_name = html.escape(name)
                
                html_content += f"""
                    <div class="file-item">
                        <div>
                            <span class="file-name">🎬 {safe_name}</span>
                            {folder_label}
                        </div>
                        <a href="{safe_link}" download="{safe_name}" class="download-btn">Download</a>
                    </div>
                """
        
        if not has_files:
            html_content += '<div class="empty">No downloaded files found in the folder.</div>'
            
        html_content += """
            </div>
        </body>
        </html>
        """
        
        encoded = html_content.encode('utf-8', 'surrogateescape')
        import io
        buffer = io.BytesIO()
        buffer.write(encoded)
        buffer.seek(0)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        
        return buffer

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def start_server(directory, port):
    global is_server_running
    os.chdir(directory)
    
    # We now use the custom UI handler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), MobileAppUIHandler) as httpd:
        is_server_running = True
        print(f"[WIFI SYNC] Server running on port {port}")
        httpd.serve_forever()

def get_qr_image_and_start_server(download_folder_path, port=8000):
    ip = get_local_ip()
    url = f"http://{ip}:{port}"
    
    if not is_server_running:
        server_thread = threading.Thread(target=start_server, args=(download_folder_path, port), daemon=True)
        server_thread.start()
    else:
        print("[WIFI SYNC] Server is already running. Generating QR code only.")
        
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_wrapper = qr.make_image(fill_color="black", back_color="white")
    return qr_wrapper.get_image().convert("RGB")