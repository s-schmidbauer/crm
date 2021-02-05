import sys
import json
from flask import Flask, request, redirect, url_for, jsonify
from marshmallow import Schema, fields, ValidationError
from datetime import datetime
from flask_pymongo import PyMongo
from pprint import pprint

app = Flask(__name__)
app.secret_key = 'supersecretstuff'
app.config['MONGO_URI'] = 'mongodb+srv://stefan:supersecret@cluster0.n7jgd.mongodb.net/crm?retryWrites=true&w=majority'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

mongo = PyMongo(app)

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

# Detail Views
@app.route("/currency/<string:symbol>")
def get_currency(symbol):
    currency = mongo.db.currencies.find_one({"symbol": symbol})
    return currency_schema.dump(currency)

@app.route("/time_registration/<int:id>")
def get_time_registration(id):
    time_registration = mongo.db.timeregistrations.find_one({"_id": ObjectId(id)})
    return timereg_schema.dump(time_registration)

@app.route("/rate/<string:name>")
def get_rate(name):
    rate = mongo.db.rates.find_one({"name": name })
    return rate_schema.dump(rate)

@app.route("/payment_method/<string:name>")
def get_payment_method(name):
    payment_method = mongo.db.paymentmethods.find_one({"name": name })
    return payment_schema.dump(payment_method)

@app.route("/contact/<string:name>")
def get_contact(name):
    contact = mongo.db.contacts.find_one({"name": name })
    return contact_schema.dump(contact)

@app.route("/spending/<string:name>")
def get_spending(name):
    spending = mongo.db.spendings.find_one({"name": name })
    return spending_schema.dump(spending)

@app.route("/invoice/<string:number>")
def get_invoice(number):
    invoice = mongo.db.invoices.find_one({"number": number })
    return invoice_schema.dump(invoice)

# Add Views
@app.route("/add_currency")
def add_currency():
    eur =           { "symbol": "EUR", "usd_conversion_rate": "0.9" }
    cs = currency_schema.dump(eur)
    currencies = mongo.db.currencies
    currencies.insert(cs)
    return currency_schema.dump(eur)

@app.route("/add_time_registration")
def add_time_registration():
    sentia_normal = { "name": "Sentia 100%", "price": "34.0" }
    kw_5 =          { "start_date": "01-02-2021", "end_date": "07-02-2021", "rate": sentia_normal }
    tr = timereg_schema.dump(kw_5)
    timeregistrations = mongo.db.timeregistrations
    timeregistrations.insert(tr)
    return timereg_schema.dump(kw_5)

@app.route("/add_rate")
def add_rate():
    sentia_normal = { "name": "Sentia 100%", "price": "34.0" }
    rs = rate_schema.dump(sentia_normal)
    rates = mongo.db.rates
    rates.insert(rs)
    return rate_schema.dump(sentia_normal)

@app.route("/add_payment_method")
def add_payment_method():
    visa =          { "name": "Visa" }
    ps = payment_schema.dump(visa)
    paymentmethods = mongo.db.paymentmethods
    paymentmethods.insert(ps)
    return payment_schema.dump(visa)

@app.route("/add_contact")
def add_contact():
    sentia =        { "name": "Fred van der Teems" }
    cs = contact_schema.dump(sentia)
    contacts = mongo.db.contacts
    contacts.insert(cs)
    return contact_schema.dump(sentia)

@app.route("/add_spending")
def add_spending():
    visa =          { "name": "Visa" }
    spending =      { "name": "Vodka", "amount": "34.99", "payment_method": visa }
    ss = spending_schema.dump(spending)
    spendings = mongo.db.spendings
    spendings.insert(ss)
    return spending_schema.dump(spending)

@app.route("/add_invoice")
def add_invoice():
    # register some time
    sentia =        { "name": "Fred van der Teems" }
    visa =          { "name": "Visa" }
    spending =      { "name": "Vodka", "amount": "34.99", "payment_method": visa }
    sentia_normal = { "name": "Sentia 100%", "price": "34.0" }
    kw_5 =          { "start_date": "01-02-2021", "end_date": "07-02-2021", "rate": sentia_normal }
    invoice =       { "number": "010014", "customer": sentia, "spendings": spending, "time_registrations": kw_5 }

    inv = invoice_schema.dump(invoice)
    invoices = mongo.db.invoices
    invoices.insert(inv)
    return invoice_schema.dump(invoice)

# List Views
@app.route("/currencies")
def currencies():
    currencies = mongo.db.currencies.find()
    return {"currencies": currencies_schema.dump(currencies)}

@app.route("/rates")
def rates():
    rates = mongo.db.rates.find()
    return {"rates": rates_schema.dump(rates)}

@app.route("/time_registrations")
def time_registrations():
    timeregistrations = mongo.db.timeregistrations.find()
    return {"time_registrations": timeregs_schema.dump(timeregistrations)}

@app.route("/payment_methods")
def payment_methods():
    paymentmethods = mongo.db.paymentmethods.find()
    return {"payment_methods": payments_schema.dump(paymentmethods)}

@app.route("/spendings")
def spendings():
    spendings = mongo.db.spendings.find()
    return {"spendings": spendings_schema.dump(spendings)}

@app.route("/contacts")
def contacts():
    contacts = mongo.db.contacts.find()
    return {"contacts": contacts_schema.dump(contacts)}

@app.route("/invoices")
def invoices():
    invoices = mongo.db.invoices.find()
    return {"invoices": invoices_schema.dump(invoices)}
