from phongmach import login
from flask import render_template, url_for
from phongmach.admin import *
import utils
from flask_login import login_user


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/book-appoint', methods=['get', 'post'])
def book_appoint():
    err_msg = ""
    if request.method.__eq__('POST'):
        name_patient = request.form.get('name_patient')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        birth_date = request.form.get('birth_date')
        booking_date = request.form.get('booking_date')
        if utils.count_book_in_day(booking_date=booking_date) <= utils.max_patient():
            try:
                utils.add_regform(name_patient=name_patient, gender=gender, phone_number=phone_number,
                               birth_date=birth_date, booking_date=booking_date)
            except Exception as ex:
                err_msg = "Nhập thông tin bị lỗi: " + str(ex)
            else:
                return redirect(url_for('home'))
        else:
            err_msg = "Ngày bạn chọn đã hết!"

    return render_template('book_appoint.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)