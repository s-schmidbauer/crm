from flask import Flask, request, redirect, url_for
# from flask_pymongo import PyMongo
from marshmallow import Schema, fields
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretstuff'
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)

class Currency():
  def __init__(self, symbol: str, usd_conversion_rate: float):
    self.symbol = symbol
    self.usd_conversion_rate = usd_conversion_rate

class CurrencySchema(Schema):
  symbol = fields.String()
  usd_conversion_rate = fields.Float()

class Rate():
  def __init__(self, name: str, price: float, currency: str):
    self.name = name
    self.price = price
    self.currency = currency

class RateSchema(Schema):
  name = fields.String()
  price = fields.Float()
  # currency = fields.Nested(CurrencySchema)

class TimeRegistration():
  def __init__(self, start_date: str, end_date: str, rate: float):
    self.start_date = start_date
    self.end_date = end_date
    self.rate = rate

class TimeRegistrationSchema(Schema):
  start_date = fields.String()
  end_date = fields.String()
  rate = fields.Nested(RateSchema)

class PaymentMethod():
  def __init__(self, name: str):
    self.name = name

class PaymentMethodSchema(Schema):
  name = fields.String()

class Spending():
  def __init__(self, name: str, amount: float, payment_method: str, reference: str):
    self.name = name
    self.amount = amount
    self.payment_method = payment_method
    self.reference = reference

class SpendingSchema(Schema):
  name = fields.String()
  amount = fields.String()
  payment_method = fields.Nested(PaymentMethodSchema)
  reference = fields.String()

class Contact():
  def __init__(self, title: str, job_title: str, name: str, \
                 company: str, description: str, company_gov_id: str, \
                 company_vat_id: str, type: str, relation: str, language: str, \
                 birthday: str, address: str, zip: str, city: str, country: str, \
                 website: str, phone_landline: str, phone_mobile: str, \
                 email_contact: str, email_invoice: str, bank_iban: str, payment_days: int ):
    self.title = title
    self.job_title = job_title
    self.name = name
    self.company = company
    self.description = description
    self.company_gov_id = company_gov_id
    self.company_vat_id = company_vat_id
    self.type = type
    self.relation = relation
    self.language = language
    self.birthday = birthday
    self.address = address
    self.zip = zip
    self.city = city
    self.country = country
    self.website = website
    self.phone_landline = phone_landline
    self.phone_mobile = phone_mobile
    self.email_contact = email_contact
    self.email_invoice = email_invoice
    self.bank_iban = bank_iban
    self.payment_days = payment_days

class ContactSchema(Schema):
  title = fields.String()
  job_title = fields.String()
  name = fields.String()
  company = fields.String()
  description = fields.String()
  company_gov_id = fields.String()
  company_vat_id = fields.String()
  type = fields.String()
  relation = fields.String()
  language = fields.String()
  birthday = fields.String()
  address = fields.String()
  zip = fields.String()
  city = fields.String()
  country = fields.String()
  website = fields.String()
  phone_landline = fields.String()
  phone_mobile = fields.String()
  email_contact = fields.String()
  email_invoice = fields.String()
  bank_iban = fields.String()
  payment_days = fields.Integer()

class Invoice():
  def __init__(self, number: str, customer: str, time_registrations: str, spendings: str, due_date: str, \
                 sent: bool, reminded_first: bool, reminded_second: bool, reminded_third: bool, payed: bool, \
                 pdf: bool):
    self.number = number
    self.customer = customer
    self.time_registrations = time_registrations
    self.spendings = spendings
    self.due_date = due_date
    self.sent = sent
    self.reminded_first = reminded_first
    self.reminded_second = reminded_second
    self.reminded_third = reminded_third
    self.payed = payed
    self.pdf = pdf

class InvoiceSchema(Schema):
  number = fields.String()
  customer = fields.Nested(ContactSchema)
  time_registrations = fields.Nested(TimeRegistrationSchema)
  spendings = fields.Nested(SpendingSchema)
  due_date = fields.String()
  sent = fields.Boolean()
  reminded_first = fields.Boolean()
  reminded_second = fields.Boolean()
  reminded_third = fields.Boolean()
  payed = fields.Boolean()
  pdf = fields.String()

class TimeRegistrationSchema(Schema):
  start_date = fields.String()
  end_date = fields.String()
  rate = fields.Nested(RateSchema)

# if __name__ == "__main__":
currency_schema = CurrencySchema()
rate_schema = RateSchema()
timereg_schema = TimeRegistrationSchema()
payment_schema = PaymentMethodSchema()
spending_schema = SpendingSchema()
contact_schema = ContactSchema()
invoice_schema = InvoiceSchema()

# register some time
eur = Currency(symbol="EUR", usd_conversion_rate=0.9)
sentia_normal = Rate(name="Sentia 100%", price=34.00, currency=eur)
kw5 = TimeRegistration("01-02-2021", "07-02-2021", sentia_normal)

# create an invoice using time registration
sentia = Contact(title="Mr.", job_title="Team Lead", name="Fred van der Teems", company="Sentia B.V.", type="business", relation="customer", language="English", address="Einsteinbaan 4", zip="99999KB", city="Nieuwegein", country="NL", website="www.sentia.com", email_contact="teamyellow@sentia.com", email_invoice="invoices@sentia.com", bank_iban="NL99999999999", payment_days=14, description="", company_gov_id="", company_vat_id="", birthday="", phone_landline="", phone_mobile="")
visa = PaymentMethod(name="Visa")
booze = Spending(name="Vodka", amount=35.99, payment_method=visa, reference="")
invoice = Invoice(number="010014", customer=sentia, time_registrations=kw5, spendings=booze, due_date="14-02-2021", reminded_first=False, reminded_second=False, reminded_third=False, payed=False, sent=False, pdf="")

print(currency_schema.dump(eur))
print(rate_schema.dump(sentia_normal))
print(timereg_schema.dump(kw5))
print(contact_schema.dump(sentia))
print(payment_schema.dump(visa))
print(spending_schema.dump(booze))
print(invoice_schema.dump(invoice))
