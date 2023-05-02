from flask import *
from werkzeug.utils import redirect

from Dbconnection import Db

app = Flask(__name__)
app.secret_key = "abc"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/bus_route')
def bus_route():
    return render_template('bus_route.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/owner')
def owner():
    return render_template('owner.html')


@app.route('/add_bus')
def add_bus():
    return render_template('add_bus.html')


@app.route('/add_time')
def add_time():
    return render_template('add_time.html')


@app.route('/confirm')
def confirm():
    return render_template('confirm.html')


@app.route('/login_post', methods=['post'])
def login_post():
    c = Db()
    uname = request.form['username']
    password = request.form['password']
    qry = "select * from login where username='" + uname + "' and `password`='" + password + "'"
    res = c.selectOne(qry)
    if res is not None:
        type = res['Type']
        if type == 'admin':
            session['username'] = res['username']
            return admin()
        elif type == 'owner':
            session['username'] = res['username']
            return owner()
        else:
            return '''<script>alert('invalid username or password');window.location='/'</script>'''
    else:
        return '''<script>alert('invalid username or password');window.location='/'</script>'''


@app.route('/register_post', methods=['post'])
def register_post():
    pname = request.form['name']
    phone = request.form['Phonenumber']
    email = request.form['email']
    owner = request.form['Owner']
    user = request.form['user']
    password = request.form['password']
    password1 = request.form['password1']
    if password == password1:
        qry = "insert into register(name,phone,email,owner,username,password,password1,status)values('" + pname + "','" + phone + "','" + email + "','" + owner + "','" + user + "','" + password + "','" + password1 + "','pending')"
        c = Db()
        c.insert(qry)
        qry1 = "insert into login(username,password,type)values('" + user + "','" + password + "','pending')"
        d = Db()
        d.insert(qry1)
        return '''<script>alert("added successfully");window.location="/"</script>'''
    else:
        return '''<script>alert("password mismatch");window.location="/"</script>'''


@app.route('/add_bus_post', methods=['post'])
def add_bus_post():
    user = session['username']
    bname = request.form['busname']
    bno = request.form['busno']
    oid = request.form['oid']
    qry = "insert into add_bus(username,busname,busno,oid)values('" + user + "','" + bname + "','" + bno + "','" + oid + "')"
    c = Db()
    c.insert(qry)
    return '''<script>alert("added successfully");window.location="/owner"</script>'''


@app.route('/add_time_post', methods=['post'])
def add_time_post():
    user = session["username"]
    bno = request.form['busno']
    fro = request.form['fr']
    too = request.form['to']
    place = request.form['place']
    time = request.form['time']

    qry = "insert into add_time(username,busno,fro,too,place,time)values('" + user + "','" + bno + "','" + fro + "','" + too + "','" + place + "','" + time + "')"
    c = Db()
    c.insert(qry)
    return '''<script>alert("added successfully");window.location="/owner"</script>'''


@app.route('/bus_no')
def bus_no():
    username = session["username"]
    c = Db()
    qry = "select busno from add_bus where username='" + str(username) + "'"
    r = c.select(qry)
    return render_template("add_time.html", data=r)


@app.route('/update_time')
def update_time():
    user = session['username']
    c = Db()
    qry = "select * from add_time where username='" + str(user) + "'"
    r = c.select(qry)
    return render_template("update_time.html", data=r)


@app.route('/view_edit_time/<username>')
def view_edit_time(username):
    qry = "select * from add_time WHERE username='" + str(username) + "'"
    db = Db()
    res = db.selectOne(qry)
    session['username'] = username
    return render_template("edit_update_time.html", data=res)


@app.route('/edit_update_time', methods=['post'])
def edit_update_time():
    db = Db()
    x = session['username']
    fr = request.form['textfield2']
    to = request.form['textfield3']
    p1 = request.form['textfield4']
    t1 = request.form['textfield5']
    qry = "update  add_time  set  fro='" + fr + "',too='" + to + "',place='" + p1 + "',time='" + t1 + "' where username='" + str(
        x) + "'"
    db.update(qry)
    return '''<script>alert("Update successfully");window.location="/update_time"</script>'''


@app.route('/view_register/<username>')
def view_register(username):
    c = Db()
    qry = "select * from register where username='" + username + "'"
    r = c.selectOne(qry)
    return render_template('register_view.html', r=r)


@app.route('/confirm_post', methods=['post'])
def confirm_post():
    username = request.form["username"]
    but = request.form["button"]
    print(but)
    if but == "accept":
        qry = "update  register set status='accept' where username='" + username + "'"
        qry1 = "update login set type='owner' where username='" + username + "'"
        print(qry)
        print(qry1)
        c = Db()
        r = c.update(qry)
        w = c.update(qry1)
    else:
        qry = "update  register set status='reject' where username='" + username + "'"
        qry1 = "update login set type='reject' where username='" + username + "'"
        print(qry)
        print(qry1)
        c = Db()
        r = c.update(qry)
        w = c.update(qry1)
    return admin()


@app.route('/admin_add_owner_request')
def admin_add_owner_request():
    c = Db()
    qry = "select * from register where status='pending'"
    r = c.select(qry)
    return render_template('confirm.html', r=r)


@app.route('/admin_view_approved_owners')
def admin_view_approved_owners():
    c = Db()
    qry = "select * from register where status='accept'"
    r = c.select(qry)
    return render_template('approved_owner.html', r=r)


@app.route('/admin_view_rejected_owners')
def admin_view_rejected_owners():
    c = Db()
    qry = "select * from register where status='reject'"
    r = c.select(qry)
    return render_template('rejected_owner.html', r=r)


@app.route('/profile')
def profile():
    username = session['username']
    qry = "select * from register where username='" + str(username) + "'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("profile.html", data=res)


@app.route('/time_delete/<id>')
def time_delete(id):
    db = Db()
    qry = "delete from add_time where id='" + str(id) + "'"
    db.delete(qry)
    return '''<script>alert("Delete Succefully");window.location="/update_time"</script>'''


@app.route('/view_search', methods=['post'])
def view_search():
    c = Db()
    place = request.form['place']
    qry = "select * from add_time where place like '%" + place + "%' order by time"
    r = c.select(qry)
    return render_template("view_bus.html", data=r)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/checkusername', methods=['POST'])
def checkusername():
    c = Db()
    print(request.form)
    email=request.form['un']
    qr="SELECT * FROM `register` WHERE `username`='"+email+"' "
    res=c.selectOne(qr)
    print(res)
    if res is None:
        resp = make_response(json.dumps(""))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = make_response(json.dumps("Username Existing"))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.route('/checkemail1', methods=['POST'])
def checkemail1():
    c = Db()
    print(request.form)
    email=request.form['em']
    qr="SELECT * FROM `register` WHERE `email`='"+email+"'"
    res=c.selectOne(qr)
    print(res)
    if res is None:
        resp = make_response(json.dumps(""))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = make_response(json.dumps("Email Existing"))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
