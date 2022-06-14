from ast import Assign
from unicodedata import category, name
from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from flask_login import login_required
from uxapp.models import Agents, Stock_cat, Stock, Orders,Orderingitems
from uxapp import db

stock_routes = Blueprint('stock_routes', __name__)

#=========================
# Stock Categories Route
#=========================
@stock_routes.route("/stock" , methods=['GET', 'POST'])
@login_required
def stock():
    if request.method == "POST":
        if 'add-cat' in request.form:
            categ = request.form['categ']
            categ_icon = request.form.get('icon')
            categ_qu = Stock_cat.query.filter_by(categ = categ)
            if categ_qu is None:
                flash('Category Is Already Exist In Table', 'alert-danger')
            else:
                categ_qu = Stock_cat(categ = categ, cat_icon= categ_icon)
                db.session.add(categ_qu)
                db.session.commit()
                flash('Category Added', 'alert-success')
                return redirect(url_for('stock_routes.stock'))
        elif 'edit-cat' in request.form:
            categ_id = request.form['cat-id']
            categ = request.form['categ']
            categ_icon = request.form.get('icon')
            cat = Stock_cat.query.filter_by(id = categ_id).first()
            try:
                cat.categ = categ
                cat.cat_icon= categ_icon
                db.session.commit()
                flash('Category Updated', 'alert-success')
                return redirect(url_for('stock_routes.stock'))
            except:
                flash('Error: Please Try Again', 'alert-danger')
                return redirect(url_for('stock_routes.stock'))
        elif 'delete-cat' in request.form:
            categ_id = request.form['delete-cat']
            cat = Stock_cat.query.filter_by(id = categ_id).first()
            db.session.delete(cat)
            db.session.commit()
            flash('Category Deleted', 'alert-success')
            return redirect(url_for('stock_routes.stock'))
    stock_categs = Stock_cat.query.order_by(Stock_cat.id)
    return render_template("/stock/stock.html", title="Stock", stocka="active", stock_categs = stock_categs, Stock = Stock)
#=========================
# View Stock Item Route
#=========================
@stock_routes.route("/stock/stock-item-cate/<int:st_item>" , methods=['GET', 'POST'])
@login_required
def stockItem(st_item):
    if Stock_cat.query.filter_by(id = st_item).first() == None: # Check If Category is Exist or redirect to 404 page
        return render_template('404.html'), 404
    elif request.method == "POST":
        if Agents.query.filter_by(bio = request.form['add-assi']).first() != None: # check if agent is exist first in HC
            assign_agent = Agents.query.filter_by(bio = request.form['add-assi']).first().id
        elif request.form['add-assi'] == '':
            assign_agent = None
        else:
            assign_agent = None
            flash('The Agent you try to assign Not Found On HeadCount', 'alert-warning')
        try:
            stockItem = request.form['stockItem']
            serial = request.form['add-serial']
            quantity = request.form['add-quantity'] or 0
            pos = request.form['add-pos']
            comm = request.form['add-comm']
            add_item = Stock(item_name = stockItem, serial = serial, quantity = quantity, position = pos, assigned_to = assign_agent ,comment = comm, stock_categ = st_item)
            db.session.add(add_item)
            db.session.commit()
            flash('Item Added', 'alert-success')
        except:
            flash('Something went wrong, please make sure you intered valid values', 'alert-danger')
    stock_categs_items = Stock.query.filter_by(stock_categ = st_item).all()
    stock_item_cat = Stock_cat.query.filter_by(id = st_item).first()
    return render_template("/stock/stock-item.html", title="Stock Item",stocka="active", stock_categs_items = stock_categs_items, stock_item_cat=stock_item_cat)
#=========================
# Edit Stock Item Route
#=========================
@stock_routes.route("/stock/stock-edit" , methods=['GET', 'POST'])
@login_required
def stockItemEdit():
    if request.method == "POST":
        prev_url = request.referrer
        item_id = request.form['edit-id']
        cat_id = request.form.get('cat-id')
        stockItem = request.form['stockItem']
        serial = request.form['add-serial']
        quantity = request.form['add-quantity'] or 0
        pos = request.form['add-pos']
        comm = request.form['add-comm']
        itemToEdit = Stock.query.get_or_404(item_id)
        if Agents.query.filter_by(bio = request.form['edit-assi']).first() != None: # check if agent is exist first in HC
            assign_agent = Agents.query.filter_by(bio = request.form['edit-assi']).first().id
        elif request.form['edit-assi'] == '':
            assign_agent = None
        else:
            assign_agent = None
            flash('The Agent you try to assign Not Found On HeadCount', 'alert-warning')
        try:
            itemToEdit.item_name = stockItem
            itemToEdit.serial = serial
            itemToEdit.quantity = quantity
            itemToEdit.position = pos
            itemToEdit.comment = comm
            itemToEdit.assigned_to = assign_agent
            db.session.commit()
            flash('Item Updated', 'alert-success')
            return redirect(prev_url)
        except:
            return redirect(prev_url)
    else:
        flash('Something went wrong, please make sure you intered valid values', 'alert-danger')
        return redirect(request.referrer)
#=========================
# Delete Stock Item Route
#=========================
@stock_routes.route("/stock/stock-delete" , methods=['GET', 'POST'])
@login_required
def stockItemDelete():
    if request.method == "POST":
        item_id = request.form['delete-id']
        try:
            delete_item = Stock.query.get(item_id)
            db.session.delete(delete_item)
            db.session.commit()
            flash('Item Deleted', 'alert-success')
            return redirect(request.referrer)
        except:
            flash('Something went wrong, please make sure you intered valid values', 'alert-danger')
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)

#=========================
# Stock In and Out Route
#=========================
@stock_routes.route("/stock-orders" , methods=['GET', 'POST'])
@login_required
def stock_orders():
    if request.method == 'POST':
        delv_title = request.form['delv-title']
        delv_date = request.form['delv-date'] 
        add_delv_note = Orders(title = delv_title, date = delv_date)
        db.session.add(add_delv_note)
        db.session.flush()
        db.session.commit()
        flash('Addes Successfully', 'alert-success')
        return redirect(url_for('stock_routes.stock_add_order', order_id= add_delv_note.id))
    orders = Orders.query.order_by(Orders.id)
    return render_template("/stock/stock-orders.html", title="Stock Orders",stockinout="active", orders = orders)
#==================================
# Stock Orders {Order Items View}
#==================================
@stock_routes.route("/view-order/<int:order_id>" , methods=['GET', 'POST'])
@login_required
def stock_order_view(order_id):
    print(order_id)
        
        
    return render_template('/stock/stock-view-order.html', title="Order Items",stockinout="active", order_id= order_id)

#=========================
# Stock Orders {Order Items Edit}
#=========================
@stock_routes.route("/add-order/<int:order_id>" , methods=['GET', 'POST'])
@login_required
def stock_add_order(order_id):
    if request.method == 'POST':
        item_category = request.form.getlist('item-category')
        item_name = request.form.getlist('item-name')
        item_serial = request.form.getlist('item-serial')
        item_quantity = request.form.getlist('item-quantity')
        for category, name, serial, quantity in zip(item_category, item_name, item_serial, item_quantity):
            # add_to_items = Orderingitems(deliveryNote = order_id, quantity = quantity)
            get_stock_item = Stock(item_name = name, serial = serial, quantity = quantity,stock_categ = int(category))
            db.session.add(get_stock_item)
            db.session.flush()
            item_id = Stock(Stockstock_order = get_stock_item.id)
            db.session.add(item_id)
            db.session.commit()
            print(category, name, serial, quantity)
    
    categories = Stock_cat.query.order_by(Stock_cat.id)    
    return render_template('/stock/stock-add-order.html', title="Add New Order",stockinout="active", categories = categories)