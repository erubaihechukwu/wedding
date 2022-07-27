import random,os,requests
from weddingapp import app
from flask import render_template,make_response,request,abort,redirect,flash,session,url_for,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from weddingapp import db,app,csrf
from weddingapp.models import *
from weddingapp.forms import ContactForm, LoginForm
@app.route('/')
def home():
    return render_template('user/index.html')
def generate_ref():
    ref = random.random() *1000000000
    return int(ref)
@app.route('/accommodation')
def hotels():
    username="weddingapp"
    password = "1111"
    try:
        rsp = requests.get("http://127.0.0.1:8080/api/v1.0/getall", auth=(username,password))
        rsp_json = rsp.json()
        return render_template('user/accommodation.html', rsp_json=rsp_json)
    except:
        return "please try again, the server on the other end is down"
@app.route('/signup')
def signup():
    sign = LoginForm()
    if request.method =="GET":
        return render_template('user/signup.html',sign=sign)
    else:
        if sign.validate_on_submit():
            firstname = sign.firstname.data
            lastname = request.form['lastname']
            email = request.form['email']
            pswd = request.form['password']
            guest = Guests(guest_fname=firstname, guest_lname=lastname, guest_email=email, guest_pwd=pswd)
            db.session.add(guest)
            db.session.commit()
            guestid = guest.guest_id  # retrieve the guest id
            session["guest"] = guestid  # save the id in session so you can use it elsewhere
            flash('Successfully Registered!')
            return redirect('/')
        else:
            return render_template('user/signup.html', sign=sign)

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method =="GET":
        return render_template('user/login.html')
    else:
        email = request.form["email"]
        password = request.form["password"]
        userdeets = Guests.query.filter(Guests.guest_email==email).first()
        if userdeets and check_password_hash(userdeets.guest_pwd,password):
            session["guest"] = userdeets.guest_id
            return redirect('/profile')
        else:
            flash("Invalid Credentials")
            return redirect("/login")
@app.route('/message')
def message_us():
    cform = ContactForm()
    return render_template('user/contactus.html', cform=cform)
@app.route('/submitcontact', methods=["POST","GET"])
def sc():
    cform = ContactForm()
    if cform.validate_on_submit():
        fullname = request.form['fullname']
        email = request.form['email']
        msg = request.form['message']
        contact = Contact(con_fullname=fullname,con_email=email,con_message=msg)
        db.session.add(contact)
        db.session.commit()
        flash('Message sent!')
        return redirect('/')
    else:
        return render_template('user/contactus.html', cform=cform)
@app.route('/submitlogin', methods=["POST","GET"])
def sl():
    lform = LoginForm()
    if lform.validate_on_submit():
        firstname = lform.firstname.data
        lastname = request.form['lastname']
        email = request.form['email']
        pswd = request.form['password']
        hashed = generate_password_hash(pswd)
        guest = Guests(guest_fname=firstname,guest_lname=lastname,guest_email=email,guest_pwd=hashed)
        db.session.add(guest)
        db.session.commit()
        guestid = guest.guest_id #retrieve the guest id
        session["guest"] = guestid #save the id in session so you can use it elsewhere
        flash('Successfully Registered!')
        return redirect('/')
    else:
        return render_template('user/signup.html', lform=lform)
@app.route('/logout')
def guest_logout():
    session.pop('guest',None)
    return redirect('/')
@app.route('/profile')
def user_profile():
    loggedin = session.get("guest")
    if loggedin != None:
        guest_deets = db.session.query(Guests).filter(Guests.guest_id==loggedin).first()
        return render_template('user/profile.html',guest_deets=guest_deets)
    else:
        flash("you must be logged in to view this page")
        return redirect("/login")
@app.route('/user/edit')
def edit_user_profile():
    loggedin = session.get("guest")
    if loggedin != None:
        guest_deets = db.session.query(Guests).filter(Guests.guest_id==loggedin).first()
        return render_template('user/editprofile.html',guest_deets=guest_deets)
    else:
        return redirect("/")
@app.route('/user/update')
def update_user():
    loggedin = session.get("guest")
    if loggedin != None:
        fname = request.form['fname']
        lname = request.form['lname']
        address = request.form['address']
        record = db.session.query(Guests).get(loggedin)
        record.guest_fname = fname
        record.guest_lname = lname
        record.guest_address = address
        db.session.commit()
        flash("delails updated")
        return redirect('/profile')
    else:
        return redirect('/login')
@app.route('/user/upload')
def upload_pics():
    loggedin = session.get("guest")
    if loggedin != None:
        guest_deets = db.session.query(Guests).filter(Guests.guest_id == loggedin).first()
        return render_template("user/upprofile.html",guest_deets=guest_deets)
    else:
        return redirect("/")
@app.route('/user/submit_upload',methods=["POST"])
def submit_upload():
    loggedin = session.get("guest")
    if loggedin != None:
        #retrieve for data and upload
        if request.files != "":
            allowed = ['.jpg','.png','.jpeg']
            id = session.get("guest")
            fileobj = request.files['profilepix']
            name = fileobj.filename

            newname = random.random() * 10000000
            picturename, ext = os.path.splitext(name)#splits file into two parts on the extension
            if ext in allowed:
                path = "weddingapp/static/uploads/" + str(newname) + ext
                fileobj.save(f"{path}")

                post = db.session.query(Guests).get(id)
                post.guest_image = str(newname) + ext
                db.session.commit()
                flash("image successfully uploaded")
                return redirect('/profile')
            else:
                flash("invalid format")
            return redirect('/profile')
        else:
            flash('please select a valid image')
            return redirect('/user/upload')
    else:
        return redirect("/")
@app.route('/registry')
def gifts_registry():
    loggedin = session.get("guest")
    if loggedin != None:
        promised_gifts = []
        promised = db.session.query(Guest_gift).filter(Guest_gift.g_guestid == loggedin).all()
        if promised:
            for p in promised:
                promised_gifts.append(p.g_giftid)
        gifts = db.session.query(Gifts).all()
        return render_template('user/gift_registry.html', gifts=gifts,promised_gifts=promised_gifts)
    else:
        return redirect("/")
@app.route('/submit/registry',methods=["post"])
def submit_registory():
    loggedin = session.get("guest")
    if loggedin != None:
        selected = request.form.getlist('selected_gift')
#        d = Guest_gift.query.filter(Guest_gift.g_guestid==loggedin).all()
        db.session.execute(f"DELETE FROM guest_gift WHERE g_guestid='{loggedin}'")
        db.session.commit()
        for s in selected:
            gg = Guest_gift()
            db.session.add(gg)
            gg.g_giftid = s
            gg.g_guestid = loggedin
            db.session.commit()
        flash('Thank you. Gifts recorded')
        return redirect('/registry')
    else:
        flash("ypu need to be logged in to view this page")
        return redirect("/login")
@app.route('/send_forum',methods=["POST"])
def send_forum():
    loggedin = session.get("guest")
    if loggedin != None:
        loggedin = session.get("guest")
        data = request.args.get('suggestion')
        comment = Comment(comment_content=data, comment_guestid=loggedin)
        db.session.add(comment)
        db.session.commit()
        return f"sent"
    else:
        return redirect("/login")
'''below are for ajax errors'''
@app.route('/ajaxtests')
def ajaxtexts():
    s = db.session.query(State).all()
    return render_template('user/testing.html',s=s)
@app.route('/ajaxtests/checkusername',methods=['POST','GET'])
def ajaxtexts_submit():
    user = request.values.get('username')#works for post or get
    chk = db.session.query(Guests).filter(Guests.guest_email==user).first()
    if chk != None:
        return "<span class='alert alert-danger'>username has been taken</span>"
    else:
        return "<span class='alert alert-success'>username is availablle</span>"
@app.route('/ajaxtests/state')
def ajaxtexts_state():
    selected = request.args.get('stateid')
    #write a query to fetch all nLGAs where stateid == selected.all()
    lgas = db.session.query(Lga).filter(Lga.state_id == selected).all()
    retstr= ""
    for i in lgas:
        retstr = retstr + f"<option value='{i.lga_id}'>{i.lga_name}</option>"
        return retstr
@app.route('/ajaxtests/final',methods=["POST"])
def final_test():
    appended_data = request.form.get('missing')
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    #rretrieve the file
    fileobj = request.files['image']
    original_filename = fileobj.filename
    fileobj.save(f'weddingapp/static/images/{original_filename}')
    #insert into guest table
    return jsonify(firstname=firstname,lastname=lastname,appended_data=appended_data,filename=original_filename)
@app.route('/asoebi',methods=["POST","GET"])
def asoebi():
    loggedin = session.get('guest')
    if loggedin != None:
        if request.method=='GET':
            uni = db.session.query(Uniform).all()
            return render_template('user/aso_ebi.html',uni=uni)
        else:
            uniform_selected = request.form.getlist('uniform')
            if uniform_selected:
                #insert into order table
                ref = generate_ref()
                session['reference'] = ref
                ord = Orders(order_by=loggedin,order_status='pending',order_ref=ref)
                db.session.add(ord)
                db.session.commit()
                #insert into order details
                orderid = ord.order_id
                total =0
                for i in uniform_selected:
                    price = get_price(i)
                    ord_det = Order_details(det_orderid=orderid,det_itemid=i,det_itemprice=price)
                    total = total+price
                    db.session.add(ord_det)
                ord.order_totalamt=total
                db.session.commit()
                return redirect('/confirmation')
            else:
                flash('please make a selection')
                return redirect('/asoebi')
    else:
        return redirect('/login')
def get_price(itemid):
    deets = Uniform.query.get(itemid)
    if deets != None:
        return deets.uni_price
    else:
        return 0
@app.route('/confirmation')
def confirmation():
    loggedin = session.get("guest")
    ref = session.get('reference')
    if loggedin != None:

        deets = Orders.query.join(Order_details,Orders.order_id==Order_details.det_orderid).join(Uniform,Order_details.det_itemid==Uniform.uni_id).filter(Orders.order_ref==ref).add_columns(Order_details,Uniform).all()

        t = Orders.query.filter(Orders.order_ref==ref).first()

        return render_template('user/confirmation_page.html', deets=deets,total=t.order_totalamt)
    else:
        return redirect('/login')
