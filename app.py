from flask import Flask, request, redirect, url_for
# from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

import sys
import json
from pprint import pprint

app = Flask(__name__)
app.secret_key = 'supersecretstuff'
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)

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

# if __name__ == "__main__":
currency_schema = CurrencySchema()
rate_schema = RateSchema()
timereg_schema = TimeRegistrationSchema()
payment_schema = PaymentMethodSchema()
spending_schema = SpendingSchema()
contact_schema = ContactSchema()
invoice_schema = InvoiceSchema()

# register some time
eur =           { "symbol": "EUR", "usd_conversion_rate": "0.9" }
sentia_normal = { "name": "Sentia 100%", "price": "34.0" }
kw_5 =          { "start_date": "01-02-2021", "end_date": "07-02-2021", "rate": sentia_normal }
sentia =        { "name": "Fred van der Teems" }
visa =          { "name": "Visa" }
spending =      { "name": "Vodka", "amount": "34.99" }
invoice =       { "number": "010014", "customer": sentia }

pprint(currency_schema.dump(eur))
pprint(rate_schema.dump(sentia_normal))
pprint(timereg_schema.dump(kw_5))
pprint(contact_schema.dump(sentia))
pprint(payment_schema.dump(visa))
pprint(spending_schema.dump(spending))
pprint(invoice_schema.dump(invoice))
