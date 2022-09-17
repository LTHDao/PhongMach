from phongmach import db
from phongmach.models import User, RegistrationForm, Policy, PhieuKham, ChiTietPhieuKham, Medicine, Unit
import hashlib
from sqlalchemy import func, extract


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def max_patient():
    p = Policy.query.get(1)
    return p.max_patient


def count_book_in_day(booking_date):
    return RegistrationForm.query.filter(RegistrationForm.booking_date.__eq__(booking_date)).count()


def add_regform(name_patient, gender, phone_number, birth_date, booking_date):
    book_appoint = RegistrationForm(name_patient=name_patient, gender=gender,
                                    phone_number=phone_number,
                                    birth_date=birth_date, booking_date=booking_date)
    db.session.add(book_appoint)
    db.session.commit()


def count_patient_in_day(month, year):
    return db.session.query(extract('day', PhieuKham.created_date),
                            func.count(PhieuKham.id)) \
                            .filter(extract('year', PhieuKham.created_date) == year)\
                            .filter(extract('month', PhieuKham.created_date) == month) \
                            .group_by(extract('day', PhieuKham.created_date)).all()


def chart_medicine(month, year):
    return Medicine.query.join(ChiTietPhieuKham, ChiTietPhieuKham.medicine_id.__eq__(Medicine.id)) \
        .join(PhieuKham, ChiTietPhieuKham.phieukham_id.__eq__(PhieuKham.id)) \
        .join(Unit, Unit.id.__eq__(Medicine.unit_id)) \
        .add_column(Unit.name) \
        .add_column(func.sum(ChiTietPhieuKham.quantity)) \
        .add_column(func.count(ChiTietPhieuKham.medicine_id)) \
        .filter(extract('year', PhieuKham.created_date) == year) \
        .filter(extract('month', PhieuKham.created_date) == month) \
        .group_by(Medicine.name).all()


def total_money(month, year):
    return db.session.query(extract('day', PhieuKham.created_date),
                            (func.sum(ChiTietPhieuKham.quantity * Medicine.price) + func.sum(Policy.max_money)))\
                            .join(ChiTietPhieuKham, ChiTietPhieuKham.phieukham_id.__eq__(PhieuKham.id)) \
                            .join(Medicine, ChiTietPhieuKham.medicine_id.__eq__(Medicine.id)) \
                            .join(Policy, Policy.id.__eq__(PhieuKham.policy_id))\
                            .filter(extract('year', PhieuKham.created_date) == year) \
                            .filter(extract('month', PhieuKham.created_date) == month) \
                            .group_by(extract('day', PhieuKham.created_date))\
                            .order_by(extract('day', PhieuKham.created_date)).all()


def total_money_month(month, year):
    return db.session.query(extract('month', PhieuKham.created_date),
                            (func.sum(ChiTietPhieuKham.quantity * Medicine.price) + func.sum(Policy.max_money)))\
                            .join(ChiTietPhieuKham, ChiTietPhieuKham.phieukham_id.__eq__(PhieuKham.id)) \
                            .join(Medicine, ChiTietPhieuKham.medicine_id.__eq__(Medicine.id)) \
                            .join(Policy, Policy.id.__eq__(PhieuKham.policy_id))\
                            .filter(extract('year', PhieuKham.created_date) == year) \
                            .filter(extract('month', PhieuKham.created_date) == month) \
                            .group_by(extract('month', PhieuKham.created_date)).all()
