import os
from weddingapp import app
from flask import render_template,make_response,request,abort,redirect,flash,session,url_for
from datetime import datetime
from weddingapp import db,app,csrf
from weddingapp.models import *
@app.route('/admin', methods=['POST','GET'])
@csrf.exempt
def admin_home():
    if request.method=='GET':
        return render_template('admin/admin_login.html')
    else:
        username = request.form['username']
        pwd = request.form['pswd']

        ad = Admin.query.filter(Admin.admin_username==username,Admin.admin_pwd==pwd).first()
        if ad:
            adminid = ad.admin_id
            admin_fullname = ad.admin_name
            session['adminid'] = adminid
            session['adminname'] = admin_fullname
            return redirect('/admin/dashboard')
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('adminid') != None and session.get('adminname')!= None:
        return render_template('admin/admin_panel.html')
    return redirect('/admin')
@app.route('/admin/logout')
def admin_logout():
    session.pop('adminid',None)
    return redirect('/admin/dashboard')
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
@app.route('/admin/manage_gifts')
def manage_gifts():
    gifts = db.session.query(Gifts).all()
    if session.get('adminid') != None and session.get('adminname') != None:
        gifts = db.session.query(Gifts).order_by(Gifts.gift_id)
        return render_template('admin/all_gifts.html',gifts=gifts)
    else:
        return redirect('/admin')
@app.route('/admin/manage_guests')
def manage_guest():
    guests = db.session.query(Guests).all()
    if session.get('adminid') != None and session.get('adminname') != None:
        return render_template('admin/all_guests.html', guests=guests)
    else:
        return redirect('/admin')
@app.route('/admin/add_gifts', methods=['GET','POST'])
def add_gifts():
    if session.get('adminid') != None and session.get('adminname') != None:
        if request.method =='GET':
            return render_template('admin/add_gifts.html')
        else:
            return 'form submitted'
    else:
        return redirect('/admin')
@app.route('/add',methods=['POST','GET'])
def add():
    r = request.form['giftname']
    rp = Gifts(gift_name=r)
    db.session.add(rp)
    db.session.commit()
    return redirect('/admin/manage_gifts')
@app.route('/admin/edit/<id>')
def edit(id):
    deets = Gifts.query.get(id)
    return render_template('admin/edit_gifts.html', deets=deets)
@app.route('/admin/delete/<id>')
def delete_gift(id):
    x = db.session.query(Gifts).get(id)
    db.session.delete(x)
    db.session.commit()
    flash('Gift Deleted')
    return redirect('/admin/manage_gifts')
@app.route('/admin/update', methods=['GET','POST'])
def update_gift():
    newname = request.form['giftname']
    id = request.form['id']
    gift = db.session.query(Gifts).get(id)
    gift.gift_name=newname
    db.session.commit()
    flash("Gift was successfully updated")
    return redirect('/admin/manage_gifts')
@app.route('/forum')
def forum():
    return render_template('user/forum.html')