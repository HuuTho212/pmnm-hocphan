## CÂU 1

| Gói | Phiên bản | Giấy phép | Vai trò |
|---|---|---|---|
| Werkzeug | 3.1.9 | BSD-3-Clause | Thư viện WSGI: phân tích request, tạo response, định tuyến URL, dev server |
| Jinja2 | 3.1.6 | BSD-3-Clause | Template engine, sinh HTML động |
| MarkupSafe | 3.0.3 | BSD-3-Clause | Escape chuỗi để chống tấn công XSS |
| ItsDangerous | 2.2.0 | BSD-3-Clause | Ký dữ liệu để bảo vệ session, cookie |
| Click | 8.5.0 | BSD-3-Clause | Giao diện dòng lệnh: flask run, flask routes… |
| Blinker | 1.9.0 | MIT | Hệ thống tín hiệu (signal) |

# Một số gói để trống trường giấy phép. Tìm giấy phép bằng cách pip show -v <gói>

# Công ty được dùng Flask trong phần mềm thương mại đóng mã nguồn 
BSD-3-Clause là giấy phép permissive (cho phép rất rộng): được dùng, sửa đổi, phân phối lại, kể cả đưa vào sản phẩm thương mại đóng mã nguồn, không phải công bố mã nguồn của sản phẩm. Điều kiện chỉ là:
- Giữ nguyên thông báo bản quyền, danh sách điều kiện và tuyên bố miễn trừ trách nhiệm (ví dụ ghi trong mục "Giấy phép bên thứ ba" của sản phẩm);
- không dùng tên tác giả/Pallets để quảng bá sản phẩm khi chưa được phép.

## CÂU 13
### 1. `request.path` khi chưa có request

```python
>>> from flask import request, url_for
>>> request.path
Traceback (most recent call last):
  ...
RuntimeError: Working outside of request context.

This typically means that you attempted to use functionality that needed
an active HTTP request. Consult the documentation on testing for
information about how to avoid this problem.
```

### 2. `url_for("about")` khi chưa có request

```python
>>> url_for("about")
Traceback (most recent call last):
  ...
RuntimeError: Unable to build URLs outside an active request without 'SERVER_NAME' configured. Also configure 'APPLICATION_ROOT' and 'PREFERRED_URL_SCHEME' as needed.
```

So sánh với câu 1: cả hai đều là `RuntimeError`, nhưng nguyên nhân khác nhau.
- Câu 1: **hoàn toàn không có request context**, nên `request` không trỏ tới đối tượng nào.
- Câu 2: `flask shell` đã đẩy sẵn **application context**, nên Flask vẫn biết app và bảng route (`url_map`). Cái thiếu là thông tin để dựng URL đầy đủ (host, scheme, thư mục gốc của ứng dụng), mà những thông tin này bình thường lấy từ request. Vì vậy thông báo lỗi yêu cầu cấu hình `SERVER_NAME`, `APPLICATION_ROOT`, `PREFERRED_URL_SCHEME`.

### 3. Tạo request context mô phỏng `POST /search?q=flask&page=2`

```python
>>> with app.test_request_context("/search?q=flask&page=2", method="POST"):
...     print(request.method)
...     print(request.path)
...     page = request.args.get("page", type=int)
...     print(page, type(page))
...     print(url_for("about"))
...
POST
/search
2 <class 'int'>
/about
```

- `request.method` là `POST`.
- `request.path` là `/search` (không gồm query string `?q=flask&page=2`).
- Tham số trong query string nằm ở `request.args`; `type=int` đổi chuỗi `"2"` thành số nguyên `2`.
- `url_for("about")` trả về `/about`.

### 4. Giải thích

Flask có hai loại context:

| Context | Cung cấp | Có sẵn trong `flask shell` |
|---|---|---|
| Application context | `current_app`, `g` | Có (shell tự đẩy vào) |
| Request context | `request`, `session` | Không |

- **Câu 1 lỗi**: `request` chỉ là một proxy trỏ tới request đang được xử lý. Trong shell không có request nào, nên truy cập `request.path` báo lỗi.
- **Câu 2 lỗi**: `url_for` có app context nên tìm được route `about`, nhưng thiếu request để biết host, scheme và thư mục gốc. Khi không có request, Flask chỉ dựng được URL nếu đã cấu hình `SERVER_NAME`, nên báo lỗi.
- **Câu 3** chạy được**: `app.test_request_context(path, method=...)` tạo một request giả (Flask tự dựng sẵn môi trường WSGI mô phỏng) và đẩy request context vào trong khối `with`. Trong khối này `request` có dữ liệu thật và `url_for` có đủ thông tin để dựng URL. Khi ra khỏi `with`, context được gỡ bỏ và `request` lại không dùng được như câu 1