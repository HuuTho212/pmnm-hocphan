from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, func


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SECRET_KEY"] = "longngu123danhngu123hyngu123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///qlsv.db"

db.init_app(app)


class Student(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    mssv: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    gpa: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self):
        return f"<Student {self.mssv} {self.name} >"


with app.app_context():
    db.create_all()


@app.get("/them-mau")
def add_sample():
    total = db.session.scalar(db.select(func.count(Student.id)))
    if total > 0:
        return render_template(
            "them_mau.html",
            message=f"Đã có {total} sinh viên, không thêm nữa.",
        )

    an = Student(mssv="23T1020001", name="Nguyễn Văn An", gpa=8.5)
    before = an.id  # None vì chưa add/commit
    db.session.add(an)
    db.session.add_all([
        Student(mssv="23T1020002", name="Nguyễn Văn Bình", gpa=7.5),
        Student(mssv="23T1020003", name="Nguyễn Văn Cường", gpa=6.5),
        Student(mssv="23T1020004", name="Nguyễn Văn Dũng", gpa=9.5),
        Student(mssv="23T1020005", name="Nguyễn Văn Hùng", gpa=5.5),
    ])
    db.session.commit()

    students = db.session.execute(db.select(Student)).scalars().all()
    return render_template(
        "them_mau.html",
        students=students,
        before=before,
        after=an.id,
    )


@app.get("/thu-truy-van")
def try_queries():
    count = db.session.scalar(db.select(func.count(Student.id)))
    if count == 0:
        return render_template(
            "thu_truy_van.html",
            message="Chưa có cơ sở dữ liệu, hãy mở /them-mau trước.",
        )

    everyone = db.session.execute(db.select(Student)).scalars().all()

    stmt = (
        db.select(Student)
        .where(Student.gpa >= 8.0)
        .order_by(Student.gpa.desc())
    )
    good = db.session.execute(stmt).scalars().all()

    binh = db.session.scalar(
        db.select(Student).where(Student.mssv == "23T1020002")
    )
    avg = db.session.scalar(db.select(func.avg(Student.gpa)))

    return render_template(
        "thu_truy_van.html",
        sv3=db.session.get(Student, 3),
        sv99=db.session.get(Student, 99),
        everyone=everyone,
        good=good,
        binh=binh,
        count=count,
        avg=avg,
    )


if __name__ == "__main__":
    app.run(debug=True)