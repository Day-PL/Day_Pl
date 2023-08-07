from django.shortcuts import render

#! Create your views here.
#! 고쳐야 대!!!

def login():
    if request.method == 'POST':
        id = request.form["id"]
        pwd = request.form["pwd"]
        user = User.query.filter(User._id == id).first()
        print(f"디버깅용: id: {id} pwd: {pwd}")
        if user and user.check_pwd(pwd):
            login_user(user)
            print(f'로그인에 성공했습니다.')
            return redirect(url_for('browse.browse'))
        else:
            print(f'로그인에 실패횄습니다.')
            return redirect(url_for('users.login'))
        
    return render_template('auth/login.html')

# 로그인 매니저 생성
login_manager = LoginManager()
login_manager.login_view = "login" # 로그인 페이지 URI 명시

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('browse.browse'))