import sys
import json
import requests
from flask import Flask, request, redirect, url_for, jsonify, abort
from marshmallow import ValidationError
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_pymongo import PyMongo
from pprint import pprint

app = Flask(__name__)
app.secret_key = 'supersecretstuff'
app.config['MONGO_URI'] = 'mongodb+srv://stefan:supersecret@cluster0.n7jgd.mongodb.net/crm?retryWrites=true&w=majority'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
mongo = PyMongo(app)
ma = Marshmallow(app)

from schemas import currency_schema, \
                    currencies_schema, \
                    rate_schema, \
                    rates_schema, \
                    timereg_schema, \
                    timeregs_schema, \
                    payment_schema, \
                    payments_schema, \
                    spending_schema, \
                    spendings_schema, \
                    contact_schema, \
                    contacts_schema, \
                    invoice_schema, \
                    invoices_schema

# Required vars for adding
# eur =           { "symbol": "EUR", "usd_conversion_rate": "0.9" }
# normal =        { "name": "Corp", "price": "34.0", "currency": eur }
# kw_5 =          { "start_date": "01-02-2021", "end_date": "07-02-2021", "rate": normal }
# visa =          { "name": "Visa" }
# sentia =        { "name": "Fred Flintstone", "website": "https://www.google.com" }
# spending =      { "name": "Vodka", "amount": "34.99", "payment_method": visa }
# invoice =       { "number": "010014", "customer": sentia, "spendings": spending, "time_registrations": kw_5 }

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

# Detail Views
@app.route("/currency/<string:symbol>", methods=['GET'])
def get_currency(symbol):
    currency = mongo.db.currencies.find_one_or_404({"symbol": symbol})
    return {"currency": currency_schema.dump(currency)}

@app.route("/time_registration/<int:id>", methods=['GET'])
def get_time_registration(id):
    time_registration = mongo.db.timeregistrations.find_one_or_404({"_id": ObjectId(id)})
    return {"time_registration": timereg_schema.dump(time_registration)}

@app.route("/rate/<string:name>", methods=['GET'])
def get_rate(name):
    rate = mongo.db.rates.find_one_or_404({"name": name })
    return {"rate":rate_schema.dump(rate)}

@app.route("/payment_method/<string:name>", methods=['GET'])
def get_payment_method(name):
    payment_method = mongo.db.paymentmethods.find_one_or_404({"name": name })
    return {"payment_method": payment_schema.dump(payment_method)}

@app.route("/contact/<string:name>", methods=['GET'])
def get_contact(name):
    contact = mongo.db.contacts.find_one_or_404({"name": name })
    return {"contact": contact_schema.dump(contact)}

@app.route("/spending/<string:name>", methods=['GET'])
def get_spending(name):
    spending = mongo.db.spendings.find_one_or_404({"name": name })
    return {"spending": spending_schema.dump(spending)}

@app.route("/invoice/<string:number>", methods=['GET'])
def get_invoice(number):
    invoice = mongo.db.invoices.find_one_or_404({"number": number })
    return {"invoice":invoice_schema.dump(invoice)}

# Extra functions

# Returns the usd_conversion_rate of a currency
@app.route("/usd_conversion_rate", methods=['POST'])
def usd_conversion_rate():
    sym = request.json["symbol"]
    r = requests.get('https://api.exchangeratesapi.io/latest?base=' + sym )
    j = r.json()
    return {"usd_conversion_rate": json.dumps(j["rates"]["USD"]) }

# Add Views

@app.route("/currency", methods=['POST'])
def add_currency():
    try:
      data = request.json
      cs = currency_schema.dump(data)
      currencies = mongo.db.currencies
      currencies.insert_one(cs)
      return {"currency": currency_schema.dump(data)}
    except ValidationError:
      return {"message": "Adding currency failed"}

@app.route("/time_registration", methods=['POST'])
def add_time_registration():
    try:
      data = request.json
      tr = timereg_schema.dump(data)
      timeregistrations = mongo.db.timeregistrations
      timeregistrations.insert_one(tr)
      return {"time_registration": timereg_schema.dump(data)}
    except ValidationError:
      return {"message": "Adding time registration failed"}

@app.route("/rate", methods=['POST'])
def add_rate():
    try:
      data = request.json
      rs = rate_schema.dump(data)
      rates = mongo.db.rates
      rates.insert(rs)
      return {"rate": rate_schema.dump(data)}
    except ValidationError:
      return {"message": "Adding rate failed"}

@app.route("/payment_method", methods=['POST'])
def add_payment_method():
    try:
      data = request.json
      ps = payment_schema.dump(data)
      paymentmethods = mongo.db.paymentmethods
      paymentmethods.insert(ps)
      return {"payment_method": payment_schema.dump(data)}
    except ValidationError:
      return {"message": "Adding payment method failed"}

@app.route("/contact", methods=['POST'])
def add_contact():
    try:
      data = request.json
      cs = contact_schema.dump(data)
      contacts = mongo.db.contacts
      contacts.insert(cs)
      return {"contact": contact_schema.dump(data)}
    except ValidationError:
      return {"message": "Adding contact failed"}

@app.route("/spending", methods=['POST'])
def add_spending():
    try:
      data = request.json
      ss = spending_schema.dump(data)
      spendings = mongo.db.spendings
      spendings.insert(ss)
      return {"spending": spending_schema.dump(data)}
    except ValidationError:
      return {"message": "Adding spending failed"}

@app.route("/invoice", methods=['POST'])
def add_invoice():
    try:
      data = request.json
      inv = invoice_schema.dump(data)
      invoices = mongo.db.invoices
      invoices.insert(inv)
      return {"invoice": invoice_schema.dump(data)}
    except ValidationError:
      return {"message": "Adding invoice failed"}

# Update Views
# They validate the json input provided
# They use find data to identify the object
@app.route("/currency", methods=['PUT'])
def update_currency():
  try:
    errors = currency_schema.validate(request.json)
    sym = request.json["find"]
  except ValidationError:
    abort(400)
  c = mongo.db.currencies.replace_one({ "symbol": sym }, request.json)
  return { "matched_count": c.matched_count }

@app.route("/time_registration", methods=['PUT'])
def update_time_registration():
  try:
    errors = timereg_schema.validate(request.json)
    id = request.json["find"]
  except ValidationError:
    abort(400)
  tr = mongo.db.timeregistrations.replace_one({ "_id": ObjectId(id) }, request.json)
  return { "matched_count": tr.matched_count }

@app.route("/rate", methods=['PUT'])
def update_rate():
  try:
    errors = rate_schema.validate(request.json)
    name = request.json["find"]
  except ValidationError:
    abort(400)
  r = mongo.db.rates.replace_one({ "name": name }, request.json)
  return { "matched_count": r.matched_count }

@app.route("/payment_method", methods=['PUT'])
def update_payment_method():
  try:
    errors = payment_schema.validate(request.json)
    name = request.json["find"]
  except ValidationError:
    abort(400)
  pm = mongo.db.paymentmethods.replace_one({ "name": name }, request.json)
  return { "matched_count": pm.matched_count }

@app.route("/contact", methods=['PUT'])
def update_contact():
  try:
    errors = payment_schema.validate(request.json)
    name = request.json["find"]
  except ValidationError:
    abort(400)
  c = mongo.db.contacts.replace_one({ "name": name }, request.json)
  return { "matched_count": c.matched_count }

@app.route("/spending", methods=['PUT'])
def update_spending():
  try:
    errors = spending_schema.validate(request.json)
    name = request.json["find"]
  except ValidationError:
    abort(400)
  s = mongo.db.contacts.replace_one({ "name": name }, request.json)
  return { "matched_count": s.matched_count }

@app.route("/invoice", methods=['PUT'])
def update_invoice():
  try:
    errors = invoice_schema.validate(request.json)
    number = request.json["find"]
  except ValidationError:
    abort(400)
  i = mongo.db.contacts.replace_one({ "number": number }, request.json)
  return { "matched_count": i.matched_count }

# Delete Views
# They validate the json input provided
@app.route("/currency", methods=['DELETE'])
def delete_currency():
  try:
    errors = currency_schema.validate(request.json)
    sym = request.json["symbol"]
  except ValidationError:
    abort(400)
  c = mongo.db.currencies.delete_one({ "symbol": sym })
  return { "deleted_count": c.deleted_count }

@app.route("/time_registration", methods=['DELETE'])
def delete_time_registration():
  try:
    errors = timereg_schema.validate(request.json)
    id = request.json["id"]
  except ValidationError:
    abort(400)
  tr = mongo.db.timeregistrations.delete_one({ "_id": ObjectId(id) })
  return { "deleted_count": tr.deleted_count }

@app.route("/rate", methods=['DELETE'])
def delete_rate():
  try:
    errors = rate_schema.validate(request.json)
    name = request.json["name"]
  except ValidationError:
    abort(400)
  r = mongo.db.rates.delete_one({ "name": name })
  return { "deleted_count": r.deleted_count }

@app.route("/payment_method", methods=['DELETE'])
def delete_payment_method():
  try:
    errors = payment_schema.validate(request.json)
    name = request.json["name"]
  except ValidationError:
    abort(400)
  pm = mongo.db.paymentmethods.delete_one({ "name": name })
  return { "deleted_count": pm.deleted_count }

@app.route("/contact", methods=['DELETE'])
def delete_contact():
  try:
    errors = payment_schema.validate(request.json)
    name = request.json["name"]
  except ValidationError:
    abort(400)
  c = mongo.db.contacts.replace_one({ "name": name })
  return { "matched_count": c.matched_count }

@app.route("/spending", methods=['DELETE'])
def delete_spending():
  try:
    errors = spending_schema.validate(request.json)
    name = request.json["name"]
  except ValidationError:
    abort(400)
  s = mongo.db.contacts.replace_one({ "name": name })
  return { "matched_count": s.matched_count }

@app.route("/invoice", methods=['DELETE'])
def delete_invoice():
  try:
    errors = invoice_schema.validate(request.json)
    number = request.json["number"]
  except ValidationError:
    abort(400)
  i = mongo.db.contacts.replace_one({ "number": number })
  return { "matched_count": i.matched_count }


# List Views
@app.route("/currencies")
def currencies():
    try:
      currencies = mongo.db.currencies.find()
      return {"currencies": currencies_schema.dump(currencies)}
    except Error:
      return {"message": "An error occured"}

@app.route("/rates")
def rates():
    try:
      rates = mongo.db.rates.find()
      return {"rates": rates_schema.dump(rates)}
    except Error:
      return {"message": "An error occured"}

@app.route("/time_registrations")
def time_registrations():
    try:
      timeregistrations = mongo.db.timeregistrations.find()
      return {"time_registrations": timeregs_schema.dump(timeregistrations)}
    except Error:
      return {"message": "An error occured"}

@app.route("/payment_methods")
def payment_methods():
    try:
      paymentmethods = mongo.db.paymentmethods.find()
      return {"payment_methods": payments_schema.dump(paymentmethods)}
    except Error:
      return {"message": "An error occured"}

@app.route("/spendings")
def spendings():
    try:
      spendings = mongo.db.spendings.find()
      return {"spendings": spendings_schema.dump(spendings)}
    except Error:
      return {"message": "An error occured"}

@app.route("/contacts")
def contacts():
    try:
      contacts = mongo.db.contacts.find()
      return {"contacts": contacts_schema.dump(contacts)}
    except Error:
      return {"message": "An error occured"}

@app.route("/invoices")
def invoices():
    try:
      invoices = mongo.db.invoices.find()
      return {"invoices": invoices_schema.dump(invoices)}
    except Error:
      return {"message": "An error occured"}
