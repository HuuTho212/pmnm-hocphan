import csv
import io
from pydoc import html

from flask import Flask, Response, abort, redirect, url_for, request

app = Flask(__name__)

def get_xep_loai(diem):
    if diem is None: return "-"
    if diem >= 8.0: return "Giỏi"
    if diem >= 6.5: return "Khá"
    if diem >= 5.0: return "Trung bình"
    return "Yếu"

STUDENT = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A",
                   "scores": {"PMMNM": 8, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A",
                   "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B",
                   "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B",
                   "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47B",
                   "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C",
                   "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}

@app.route('/')
def index():
    total_students = len(STUDENT)
    unique_classes = len(set(s['lop'] for s in STUDENT.values()))
    return f"""
    <h1>Trang chủ</h1>
    <p>Tổng số sinh viên: {total_students}</p>
    <p>Số lớp (không trùng): {unique_classes}</p>
    
    <ul>
        <li><a href="{url_for('students_list')}">Danh sách sinh viên</a></li>
        <li><a href="{url_for('api_students')}">API Sinh viên</a></li>
    </ul>
    """

@app.route("/students")
def students_list():
    lop_filter = request.args.get('Lop', '').strip().lower()
    classes = sorted(list(set(info['lop'] for info in STUDENT.values())))
    filter_links = [f'<a href="{url_for("students_list")}">Tất cả</a>']
    for c in classes:
        filter_links.append(f'<a href="{url_for("students_list", Lop=c)}">{c}</a>')
    filter_bar = " | ".join(filter_links)
    
    filtered_students = []
    for mssv, info in STUDENT.items():
        if lop_filter and info['lop'].lower() != lop_filter:
            continue      
        scores = info.get('scores', {})
        if scores:
            diem_tb = round(sum(scores.values()) / len(scores), 2)
        else: 
            diem_tb = None    
        filtered_students.append({
            'mssv': mssv,
            'name': info['name'],
            'lop': info['lop'],
            'diem_tb': diem_tb,
            'xep_loai': get_xep_loai(diem_tb)
        })
        
    if not filtered_students:
        table_html = "<p>Không có sinh viên phù hợp.</p>"
    else:
        rows = ""
        for s in filtered_students:
            diem_hien_thi = s['diem_tb'] if s['diem_tb'] is not None else "-"
            chi_tiet_link = f"/students/{s['mssv']}"
            
            rows += f"""
            <tr>
                <td><a href="{chi_tiet_link}">{s['mssv']}</a></td>
                <td>{s['name']}</td>
                <td>{s['lop']}</td>
                <td>{diem_hien_thi}</td>
                <td>{s['xep_loai']}</td>
            </tr>
            """   
        table_html = f"""
        <table border="1" cellpadding="5" cellspacing="0" style="text-align: center;">
            <tr>
                <th>MSSV</th>
                <th>Họ tên</th>
                <th>Lớp</th>
                <th>Điểm TB</th>
                <th>Xếp loại</th>
            </tr>
            {rows}
        </table>
        """
    current_lop = request.args.get('Lop', '')
    csv_link = url_for("download_csv", Lop=current_lop)
    csv_button = f"""
    <div style="margin-top: 15px;">
        <a href="{csv_link}" style="padding: 8px 15px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px;">
            Tải danh sách CSV
        </a>
    </div>
    """

    return f"""
    <h2>Danh sách sinh viên</h2>
    <div><strong>Lọc theo lớp:</strong> {filter_bar}</div>
    <br>
    {table_html}
    {csv_button}
    <br><hr><br>
    <a href="{url_for('index')}">Về trang chủ</a>
    """
@app.route("/students/csv")
def download_csv():
    lop_filter = request.args.get('Lop', '').strip().lower()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['MSSV', 'Họ tên', 'Lớp', 'Điểm TB', 'Xếp loại'])
    for mssv, info in STUDENT.items():
        if lop_filter and info['lop'].lower() != lop_filter:
            continue
            
        scores = info.get('scores', {})
        if scores:
            diem_tb = round(sum(scores.values()) / len(scores), 2)
        else:
            diem_tb = None
            
        xep_loai = get_xep_loai(diem_tb)
        diem_hien_thi = diem_tb if diem_tb is not None else "-"
        
        cw.writerow([mssv, info['name'], info['lop'], diem_hien_thi, xep_loai])
    output = '\ufeff' + si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=danh_sach_sinh_vien.csv"}
    )

@app.route("/students/<mssv>")
def api_student(mssv):
    student = STUDENT.get(mssv)
    if not student:
        return abort(404, description=f"Không có Sinh viên với MSSV {mssv}.")
        
    scores = student.get('scores', {})
    if scores:
        diem_tb = round(sum(scores.values()) / len(scores), 2)
    else:
        diem_tb = None
        
    xep_loai = get_xep_loai(diem_tb)
    if scores:
        score_rows = ""
        for mon, diem in scores.items():
            score_rows += f"<tr><td>{mon}</td><td>{diem}</td></tr>"
            
        scores_html = f"""
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Học phần</th><th>Điểm</th></tr>
            {score_rows}
        </table>
        """
    else:
        scores_html = "<p>Chưa có điểm.</p>"
        
    return f"""
    <h2>Chi tiết sinh viên</h2>
    <p><strong>MSSV:</strong> {mssv}</p>
    <p><strong>Họ tên:</strong> {student['name']}</p>
    <p><strong>Lớp:</strong> <a href="{url_for('students_list', Lop=student['lop'])}">{student['lop']}</a></p>
    <p><strong>Điểm TB:</strong> {diem_tb if diem_tb is not None else "-"}</p>
    <p><strong>Xếp loại:</strong> {xep_loai}</p>
    
    <h3>Bảng điểm từng học phần:</h3>
    {scores_html}
    <br>
    <a href="{url_for('students_list')}">Quay lại danh sách sinh viên</a>
    """

@app.route("/sv/<mssv>")
def short_link(mssv):
    return redirect(url_for('api_student', mssv=mssv), code=301)

@app.route("/api/students")
def api_students():
    return STUDENT

@app.route("/search")
def search_student():
    q = request.args.get('q', '')
    q_safe = html.escape(q, quote=True)
    
    results = []
    if q:
        q_lower = q.lower()
        for mssv, info in STUDENT.items():
            if (q_lower in mssv.lower()) or (q_lower in info['name'].lower()):
                results.append((mssv, info['name']))
                
    form_html = f"""
    <form method="GET" action="/search">
        <input type="text" name="q" value="{q_safe}" placeholder="Nhập tên hoặc MSSV...">
        <button type="submit">Tìm kiếm</button>
    </form>
    """
    
    result_html = ""
    if q:
        result_html += f'<p>Tìm thấy {len(results)} kết quả cho "<b>{q_safe}</b>".</p>'
        if results:
            result_html += "<ul>"
            for mssv, name in results:
                link = url_for("api_student", mssv=mssv)
                result_html += f'<li><a href="{link}">{mssv} - {name}</a></li>'
            result_html += "</ul>"
            
    return f"""
    <h2>Tìm kiếm sinh viên</h2>
    {form_html}
    {result_html}
    <br>
    <a href="{url_for('index')}">Về trang chủ</a>
    """

if __name__ == '__main__':
    app.run(debug=False, port=8000)