from flask import Flask,render_template,request,redirect,session
from mysql.connector import connect
from flask_bcrypt import Bcrypt

con=connect(host='localhost',port=3306,database='ecourts',user='root')


app=Flask(__name__)
app.secret_key='hghfgfchhfhfh'
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def Login():
    return render_template('Login.html')

@app.route('/signup')
def signup():
    return render_template('Sign_up.html')

@app.route('/admin')
def admin():
    return render_template('admin_login.html')

@app.route('/adminlogin_validation',methods=["GET","POST"])
def adminlogin_validation():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        session['admin']=password
        if (email=="admin123@gmail.com") and (password=='admin'):
            return render_template('Admin.html')
        else:
            return "Check ur credentials"
    else:
        return render_template('admin_login.html')

@app.route('/adminpanel')
def adminPanel():
    if session.get('admin'):
        return render_template('Admin.html')
    else:
        return redirect('/admin')

@app.route('/Signup_validation',methods=["POST","GET"])
def Signup_validation():
    if request.method=="POST":
        Id=request.form['Id']
        cur=con.cursor()
        cur.execute('select * from users where Id=%s',(Id,))
        x=cur.fetchone()
        if x==None:
            pass1=request.form['pass1']
            pass2=request.form['pass2']
            if pass1 == pass2:
                cur=con.cursor()
                password=bcrypt.generate_password_hash(pass1)
                cur.execute("insert into users values(%s,%s)",(Id,password))
                con.commit()
                return redirect('/login')
            else:
                return "Please Check ur Password,Password should Match!..."
        else:
            return redirect('/login')
    else:
        return redirect('/signup')

@app.route('/login_validate',methods=["POST","GET"])
def login_validate():
    if request.method=="POST":
        Id1=request.form['Id']
        session['eid']=Id1
        cur=con.cursor()
        cur.execute("select * from users where Id=%s",(Id1,))
        x=cur.fetchone()
        if x!=None and Id1==x[0]:
            return redirect('/')
        else:
            return redirect('/signup')
    else:
        return redirect('/login')

@app.route('/add_case')
def add_case():
    if session.get('admin'):
        return render_template('AddCase_form.html')
    else:
        return render_template('admin_login.html')

@app.route('/AddingCaseInDb',methods=["GET","POST"])
def AddingCaseInDb():
    if request.method=="POST":
        cnr=request.form['cnr']
        petitioner=request.form['petitioner']
        petitioner_Adv=request.form['petitioner(A)']
        Respondent=request.form['Respondent']
        Respondent_Adv=request.form['Respondent(A)']
        filed_on=request.form['filed on']
        disposed_by=request.form['disposed by']
        Bench_name=request.form['Bench name']
        disposed_on=request.form['disposed on']
        status=request.form['Status']
        cur=con.cursor()
        cur.execute("insert into cases values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (cnr,petitioner,petitioner_Adv,Respondent,Respondent_Adv,filed_on,disposed_by,Bench_name,disposed_on,status))
        con.commit()
        return render_template('Admin.html')
    else:
        return render_template("admin_login.html")

@app.route('/editcase')
def Editcase():
    if session.get('admin'):
        return render_template('editsearchcase.html')
    else:
        return render_template('admin_login.html')


@app.route('/EditingCaseInDb',methods=["GET","POST"])
def EditingCaseInDb():
    if request.method=="POST":
        cnr=request.form['cnr']
        cur=con.cursor()
        cur.execute("select * from cases where Cnr=%s",(cnr,))
        x=cur.fetchone()
        if x==None:
            return render_template('AddCase_form.html')
        else:
            petitioner=request.form['petitioner']
            petitioner_Adv=request.form['petitioner(A)']
            Respondent=request.form['Respondent']
            Respondent_Adv=request.form['Respondent(A)']
            filed_on=request.form['filed on']
            disposed_by=request.form['disposed by']
            Bench_name=request.form['Bench name']
            disposed_on=request.form['disposed on']
            status=request.form['Status']
            cur=con.cursor()
            filed_on=request.form['filed on']
            cur.execute("update cases SET Cnr=%s,Pet=%s,PetA=%s,Res=%s,ResA=%s,FilOn=%s,DisBy=%s,BenName=%s,DisOn=%s,Status=%s where Cnr=%s",(cnr,petitioner,petitioner_Adv,Respondent,Respondent_Adv,filed_on,disposed_by,Bench_name,disposed_on,status,cnr))
            con.commit()
            return render_template('Admin.html')
    else:
        return render_template("admin_login.html")

@app.route('/admineditcase',methods=['GET','POST'])
def admineditcase():
    cnr=request.form['cnr1']
    cur=con.cursor()
    cur.execute('select * from cases where Cnr=%s',(cnr,))
    x=cur.fetchone()
    if x!=None:
        return render_template('EditCase_Form.html',x=x)
    else:
        return render_template("AddCase_Form.html")

@app.route('/Case_details')
def Case_details():
    if session.get('admin'):
        cur=con.cursor()
        cur.execute('select * from cases')
        y=cur.fetchall()
        return render_template('viewcase.html',casedetails=y)
    else:
        return render_template('admin_login.html')

@app.route('/searchcase',methods=['GET','POST'])
def Search_Case():
    global case
    if request.method=='POST':
        cnr1=request.form['cnr1']
        cur=con.cursor()
        cur.execute('select * from cases where Cnr=%s',(cnr1,))
        x=cur.fetchone()
        case=x
        if x!=None and x[0]==cnr1:
            return render_template('searchcase.html',i=x)
        else:
            return render_template('searchcase.html',i="No such case registered")
    else:
        return redirect('/')

@app.route('/savecase')
def Savecase():
    if not session.get('eid'):
        return render_template('login.html')
    else:
        cur=con.cursor()
        cur.execute('select * from savedcases where eid=%s and cnr=%s',(session.get('eid'),case[0]))

        x=cur.fetchone()

        if x==None:
            cur.execute('insert into savedcases values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(session.get('eid'),case[0],case[1],case[2],case[3],case[4],case[5],case[6],case[7],case[8],case[9]))
            con.commit()
            return redirect('/')
        else:
            return redirect('/')


@app.route('/mycases')
def Mycases():
    if session.get('eid'):
        cur=con.cursor()
        cur.execute('select * from savedcases where eid=%s',(session.get('eid'),))
        x=cur.fetchall()
        if x!=None and len(x)!=0:
            return render_template('mycases.html',mycases=x)
        else:
            return render_template('mycases.html',mycases="No saved cases yet!")
    else:
        return redirect('/login')


@app.route('/deletecase/<string:x>/<string:y>')
def DeleteCase(x,y):
    if session.get('eid'):
        cur=con.cursor()
        cur.execute('DELETE FROM savedcases WHERE eid=%s and cnr=%s',(x,y))
        con.commit()
        return redirect('/mycases')
    else:
        return redirect('/login')
    
@app.route('/password')
def Password():
    if session.get('eid'):
        return render_template('password.html')
    else:
        return redirect('/login')

@app.route('/repeatnew',methods=['GET','POST'])
def RepeatNew():
    if request.method=="POST":
        old=request.form['old1']
        new=request.form['new']
        repeatn=request.form['repeat']
        cur=con.cursor()
        cur.execute('select * from users where Id=%s',(session.get('eid'),))
        x=cur.fetchone()
        if bcrypt.check_password_hash(x[1], old):
            if new==repeatn:
                cur=con.cursor()
                password=bcrypt.generate_password_hash(new)
                cur.execute("update users SET Password=%s where Id=%s",(password,session.get('eid')))
                con.commit()
                return redirect('/logout')
            else:
                return render_template('password.html')
        else:
            return render_template('password.html')
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session['eid']=None
    return redirect('/')


@app.route('/logoutadmin')
def logoutadmin():
    session['admin']=None
    return redirect('/')

if __name__=="__main__":
     app.run(debug=True)