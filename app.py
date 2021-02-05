import sys
import json
from flask import Flask, request, redirect, url_for, jsonify
from marshmallow import Schema, fields, ValidationError
from datetime import datetime
from flask_pymongo import PyMongo
from pprint import pprint

app = Flask(__name__)
app.secret_key = 'supersecretstuff'
# app.config['MONGO_DBNAME'] = 'crm'
app.config['MONGO_URI'] = 'mongodb+srv://stefan:supersecret@cluster0.n7jgd.mongodb.net/crm?retryWrites=true&w=majority'

mongo = PyMongo(app)

class CurrencySchema(Schema):
  symbol = fields.String(required=True)
  usd_conversion_rate = fields.Float(required=True)

  # def get_usd_conversion_rate(self, obj):
  #     return 0.9

class RateSchema(Schema):
  name = fields.String(required=True)
  price = fields.Float(required=True)
  # currency = fields.Nested(CurrencySchema)

class TimeRegistrationSchema(Schema):
  start_date = fields.String(required=True)
  end_date = fields.String(required=True)
  rate = fields.Nested(RateSchema,required=True)

class PaymentMethodSchema(Schema):
  name = fields.String(required=True)

class SpendingSchema(Schema):
  name = fields.String(required=True)
  amount = fields.String(required=False)
  payment_method = fields.Nested(PaymentMethodSchema,required=False)
  reference = fields.String(required=False)

class ContactSchema(Schema):
  title = fields.String(required=False)
  job_title = fields.String(required=False)
  name = fields.String(required=True)
  company = fields.String(required=False)
  description = fields.String(required=False)
  company_gov_id = fields.String(required=False)
  company_vat_id = fields.String(required=False)
  type = fields.String(required=False)
  relation = fields.String(required=False)
  language = fields.String(required=False)
  birthday = fields.String(required=False)
  address = fields.String(required=False)
  zip = fields.String(required=False)
  city = fields.String(required=False)
  country = fields.String(required=False)
  website = fields.String(required=False)
  phone_landline = fields.String(required=False)
  phone_mobile = fields.String(required=False)
  email_contact = fields.String(required=False)
  email_invoice = fields.String(required=False)
  bank_iban = fields.String(required=False)
  payment_days = fields.Integer(required=False)

class InvoiceSchema(Schema):
  number = fields.String(required=True)
  customer = fields.Nested(ContactSchema,required=True)
  time_registrations = fields.Nested(TimeRegistrationSchema,required=False)
  spendings = fields.Nested(SpendingSchema,required=False)
  due_date = fields.String(required=False)
  sent = fields.Boolean(required=False)
  reminded_first = fields.Boolean(required=False)
  reminded_second = fields.Boolean(required=False)
  reminded_third = fields.Boolean(required=False)
  payed = fields.Boolean(required=False)
  pdf = fields.String(required=False)

class TimeRegistrationSchema(Schema):
  start_date = fields.String(required=True)
  end_date = fields.String(required=True)
  rate = fields.Nested(RateSchema,required=True)

# Schemas used by Marshmallow
currency_schema = CurrencySchema()
rate_schema = RateSchema()
timereg_schema = TimeRegistrationSchema()
payment_schema = PaymentMethodSchema()
spending_schema = SpendingSchema()
contact_schema = ContactSchema()
invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)

@app.route("/add_currency")
def add_currency():
    eur =           { "symbol": "EUR", "usd_conversion_rate": "0.9" }
    cs = currency_schema.dump(eur)
    currencies = mongo.db.currencies
    currencies.insert(cs)
    return eur

@app.route("/add_time_registration")
def add_time_registration():
    sentia_normal = { "name": "Sentia 100%", "price": "34.0" }
    kw_5 =          { "start_date": "01-02-2021", "end_date": "07-02-2021", "rate": sentia_normal }
    tr = timereg_schema.dump(kw_5)
    timeregistrations = mongo.db.timeregistrations
    timeregistrations.insert(tr)
    return kw_5

@app.route("/add_rate")
def add_rate():
    sentia_normal = { "name": "Sentia 100%", "price": "34.0" }
    rs = rate_schema.dump(sentia_normal)
    rates = mongo.db.rates
    rates.insert(rs)
    return sentia_normal

@app.route("/add_payment_method")
def add_payment_method():
    visa =          { "name": "Visa" }
    ps = payment_schema.dump(visa)
    paymentmethods = mongo.db.paymentmethods
    paymentmethods.insert(ps)
    return visa

@app.route("/add_contact")
def add_contact():
    sentia =        { "name": "Fred van der Teems" }
    cs = contact_schema.dump(sentia)
    contacts = mongo.db.contacts
    contacts.insert(cs)
    return sentia

@app.route("/add_spending")
def add_spending():
    visa =          { "name": "Visa" }
    spending =      { "name": "Vodka", "amount": "34.99", "payment_method": visa }
    ss = spending_schema.dump(spending)
    spendings = mongo.db.spendings
    spendings.insert(ss)
    return spending

@app.route("/add_invoice")
def add_invoice():
    # register some time
    sentia =        { "name": "Fred van der Teems" }
    visa =          { "name": "Visa" }
    spending =      { "name": "Vodka", "amount": "34.99", "payment_method": visa }
    invoice =       { "number": "010014", "customer": sentia, "spendings": spending }

    inv = invoice_schema.dump(invoice)
    invoices = mongo.db.invoices
    invoices.insert(inv)
    return invoice

@app.route("/invoices")
def invoices():
    invoices = mongo.db.invoices
    output = []

    for invoice in invoices.find():
      output.append({ "number": invoice['number'], "customer": invoice['customer']})
    return jsonify({'invoices' : output })
