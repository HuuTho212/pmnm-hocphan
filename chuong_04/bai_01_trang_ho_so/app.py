from flask import Flask, render_template
app = Flask(__name__)

@app.route('/profile')
def profile():
    return render_template('profile.html',
                    ho_ten='Trần Đình Hữu Thọ',
                    nam_sinh=2005,
                    nganh='Công nghệ phần mềm',
                    skills=['Python', 'Flask', 'Git', 'HTML/CSS'])