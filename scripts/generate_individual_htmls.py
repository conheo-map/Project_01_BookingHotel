import os
import xml.sax.saxutils as saxutils

dest_dirs = [
    os.path.join(os.getcwd(), 'diagrams', 'ooad_standard'),
    r'c:\HocC\Daily\ooad_standard'
]

for d in dest_dirs:
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith('.drawio'):
            xml_path = os.path.join(d, f)
            with open(xml_path, 'r', encoding='utf-8') as xf:
                xml_data = xf.read()
            html_name = f.replace('.drawio', '.html')
            html_path = os.path.join(d, html_name)
            esc_xml = saxutils.escape(xml_data)
            title = f.replace('.drawio', '').replace('_', ' ')
            content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{title} - OOAD Standard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
    <style>body {{ background: #fff; padding: 20px; font-family: Arial, sans-serif; }}</style>
</head>
<body>
    <div class="container-fluid">
        <h3 class="text-center mb-3">{title}</h3>
        <p class="text-center text-muted small">Dự án: Hệ thống Quản lý và Đặt phòng Khách sạn Sài Gòn - Côn Đảo</p>
        <div class="mxgraph" style="max-width:100%;border:1px solid #000;background:#fff;padding:10px;" data-mxgraph="{esc_xml}"></div>
        <div class="text-center mt-3">
            <a href="{f}" download class="btn btn-sm btn-outline-dark me-2">Tải file .drawio gốc</a>
            <a href="viewer.html" class="btn btn-sm btn-dark">Về trang tổng hợp Viewer</a>
        </div>
    </div>
</body>
</html>"""
            with open(html_path, 'w', encoding='utf-8') as hf:
                hf.write(content)
            print(f"Created: {html_path}")
