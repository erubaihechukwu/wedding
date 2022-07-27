from datetime import datetime
import enum
from weddingapp import db 

class payment_status(enum.Enum):
    OPT1="Paid"
    OPT2="Pending"
    OPT3="Failed"
class Guests(db.Model):
    __tablename__ = 'guest'
    guest_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    guest_fname =db.Column(db.String(50), nullable=False)
    guest_lname =db.Column(db.String(50), nullable=False)
    guest_email=db.Column(db.String(80), nullable=False)
    guest_image= db.Column(db.String(80), nullable=False)
    guest_pwd =db.Column(db.String(255), nullable=False)
    guest_regdate=db.Column(db.DateTime(), default=datetime.utcnow())
    
	
class Gifts(db.Model):
    __tablename__ = 'gift'
    gift_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    gift_name =db.Column(db.String(50), nullable=False) 

class Admin(db.Model):
    __tablename__ = 'admin'
    #columname=db.Column(db.datatype())
    admin_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    admin_name =db.Column(db.String(50), nullable=False)
    admin_username =db.Column(db.String(50), nullable=False)
    admin_pwd =db.Column(db.String(30), nullable=False)

class Uniform(db.Model):
    __tablename__ = 'uniform'
    #columname=db.Column(db.datatype())
    uni_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uni_name =db.Column(db.String(50), nullable=False)
    uni_price =db.Column(db.Float(), nullable=False)
class Guest_gift(db.Model):
    __tablename__ = 'guest_gift'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_giftid = db.Column(db.Integer(), db.ForeignKey('gift.gift_id'))
    g_guestid =db.Column(db.Integer(), db.ForeignKey('guest.guest_id'))
#    gift_deets = db.relationship("Gifts", backref="dguests")
#    guest_deets = db.relationship("Guests", backref="dgifts")
# class Guest_gift(db.Model):
#     g_giftid = db.Column(db.Integer(), db.ForeignKey('gifts.gift_id'))
#     g_guestid =db.Column(db.Integer(), db.ForeignKey('guests.guest_id'))
class Contact(db.Model):
    __tablename__ = 'contact'
    con_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    con_fullname =db.Column(db.String(50), nullable=False)
    con_email =db.Column(db.String(50), nullable=False)
    con_message=db.Column(db.String(80), nullable=False)
    con_date= db.Column(db.DateTime(), default=datetime.utcnow())
class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    comment_guestid =db.Column(db.Integer(), db.ForeignKey('guest.guest_id'))
    comment_content =db.Column(db.String(50), nullable=False)
    comment_date= db.Column(db.DateTime(), default=datetime.utcnow())
class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    order_date= db.Column(db.DateTime(), default=datetime.utcnow())
    order_by = db.Column(db.Integer(), db.ForeignKey('guest.guest_id'))
    order_ref = db.Column(db.String(50), nullable=False)
    order_totalamt = db.Column(db.Float(50), nullable=True)
    order_status = db.Column(db.Enum('Completed','Pending'), nullable=False)
class Order_details(db.Model):
    __tablename__ = 'order_details'
    det_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    det_orderid = db.Column(db.Integer(), db.ForeignKey('orders.order_id'))
    det_itemid = db.Column(db.Integer(), db.ForeignKey('uniform.uni_id'))
    det_itemprice = db.Column(db.Float(50), nullable=False)
class State(db.Model):
    __tablename__ = 'state'
    state_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name =db.Column(db.String(50), nullable=False)

class Lga(db.Model):
    __tablename__ = 'lga'
    lga_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_id = db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    lga_name = db.Column(db.String(50), nullable=False)
class Payment(db.Model):
    __tablename__ = 'payment'
    pay_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    pay_date= db.Column(db.DateTime(), default=datetime.utcnow())
    pay_guestid = db.Column(db.Integer(), db.ForeignKey('guest.guest_id'))
    pay_orderid = db.Column(db.Integer(), db.ForeignKey('order.order_id'))
    pay_amt = db.Column(db.Float(50), nullable=False)
    order_status = db.Column(db.Enum(payment_status), nullable=False)
    pay_mode = db.Column(db.String(255), nullable=True)
    pay_feedback = db.Column(db.String(255), nullable=True)