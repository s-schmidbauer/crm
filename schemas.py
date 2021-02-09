from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length, NoneOf
from flask_marshmallow import Marshmallow

from app import app, ma

bad_choices = ["", " "]

class CurrencySchema(Schema):
  symbol = fields.String(required=True, unique=True, validate=[ Length(min=1, max=3), NoneOf(bad_choices)] )
  usd_conversion_rate = fields.Float(required=True)

  # def get_usd_conversion_rate(self, obj):
  #     return 0.9

  class Meta:
    ordered = True

  # _links = ma.Hyperlinks({
  #     'self': ma.URLFor('get_currency', values=dict(symbol='<symbol>')),
  #     'collection': ma.URLFor('currencies'),
  #   })

class RateSchema(Schema):
  name = fields.String(required=True, unique=True, validate=[ Length(min=1, max=20), NoneOf(bad_choices)] )
  price = fields.Float(required=True)
  currency = fields.Nested(CurrencySchema)

  class Meta:
    ordered = True

  # _links = ma.Hyperlinks({
  #     'self': ma.URLFor('get_rate', values=dict(name='<name>')),
  #     'collection': ma.URLFor('rates'),
  #   })

class TimeSchema(Schema):
  name = fields.String(required=True, unique=True, validate=[ NoneOf(bad_choices)] )
  hours = fields.Float(required=True)
  rate = fields.Nested(RateSchema, required=True)

class TimeRegistrationSchema(Schema):
  name = fields.String(required=True, unique=True, validate=[ NoneOf(bad_choices)] )
  start_date = fields.String(required=True, validate=Length(min=6, max=10))
  end_date = fields.String(required=True, validate=Length(min=6, max=10))
  times = fields.Nested(TimeSchema, required=True, many=True)

  class Meta:
    ordered = True

  # _links = ma.Hyperlinks({
  #     'self': ma.URLFor('get_time_registration', values=dict(_id='<id>')),
  #     'collection': ma.URLFor('time_registrations'),
  #   })

class PaymentMethodSchema(Schema):
  name = fields.String(required=True, unique=True, validate=[ Length(min=3, max=20), NoneOf(bad_choices)] )

  class Meta:
    ordered = True

  # _links = ma.Hyperlinks({
  #     'self': ma.URLFor('get_payment_method', values=dict(name='<name>')),
  #     'collection': ma.URLFor('payment_methods'),
  #   })

class SpendingSchema(Schema):
  name = fields.String(required=True, validate=[ Length(min=3, max=50), NoneOf(bad_choices)] )
  amount = fields.String(required=False, validate=Length(min=3, max=10))
  payment_method = fields.Nested(PaymentMethodSchema, required=False)
  reference = fields.String(required=False, validate=Length(min=3, max=20))

  class Meta:
    ordered = True

  # _links = ma.Hyperlinks({
  #     'self': ma.URLFor('get_spending', values=dict(name='<name>')),
  #     'collection': ma.URLFor('spendings'),
  #   })

class ContactSchema(Schema):
  name = fields.String(required=True, validate=[ Length(min=3, max=30), NoneOf(bad_choices)] )
  title = fields.String(required=False, validate=Length(min=2, max=10))
  job_title = fields.String(required=False, validate=Length(max=20))
  company = fields.String(required=False, validate=Length(min=3, max=20))
  description = fields.String(required=False, validate=Length(min=3, max=20))
  company_gov_id = fields.String(required=False, validate=Length(min=3, max=20))
  company_vat_id = fields.String(required=False, validate=Length(min=3, max=20))
  type = fields.String(required=False, validate=Length(min=3, max=20))
  relation = fields.String(required=False, validate=Length(min=3, max=20))
  language = fields.String(required=False, validate=Length(min=3, max=20))
  birthday = fields.String(required=False, validate=Length(min=6, max=10))
  address = fields.String(required=False, validate=Length(min=5, max=50))
  zip = fields.String(required=False, validate=Length(min=3, max=10))
  city = fields.String(required=False, validate=Length(min=3, max=20))
  country = fields.String(required=False, validate=Length(min=2))
  website = fields.URL(required=False, validate=Length(min=10, max=30))
  phone_landline = fields.String(required=False, validate=Length(min=10, max=20))
  phone_mobile = fields.String(required=False, validate=Length(min=10, max=20))
  email_contact = fields.Email(required=False, validate=Length(min=10, max=50))
  email_invoice = fields.Email(required=False, validate=Length(min=10, max=50))
  bank_iban = fields.String(required=False, validate=Length(min=20, max=30))
  payment_days = fields.Integer(required=False, validate=Length(min=1, max=2))

  class Meta:
    ordered = True

  # _links = ma.Hyperlinks({
  #     'self': ma.URLFor('get_contact', values=dict(name='<name>')),
  #     'collection': ma.URLFor('contacts'),
  #   })

class InvoiceSchema(Schema):
  number = fields.String(required=True, unique=True, validate=[ Length(min=1, max=20), NoneOf(bad_choices)] )
  customer = fields.Nested(ContactSchema, required=True)
  time_registration = fields.Nested(TimeRegistrationSchema, required=False)
  spendings = fields.Nested(SpendingSchema, required=False)
  due_date = fields.String(required=False, validate=Length(min=1, max=20))
  sent = fields.Boolean(required=False)
  reminded_first = fields.Boolean(required=False)
  reminded_second = fields.Boolean(required=False)
  reminded_third = fields.Boolean(required=False)
  payed = fields.Boolean(required=False)
  pdf = fields.URL(required=False, validate=Length(min=5, max=255))

  class Meta:
    ordered = True

  # _links = ma.Hyperlinks({
  #     'self': ma.URLFor('get_invoice', values=dict(number='<number>')),
  #     'collection': ma.URLFor('invoices'),
  #   })


# Schemas used by Marshmallow
currency_schema = CurrencySchema()
currencies_schema = CurrencySchema(many=True)
time_schema = TimeSchema()
times_schema = TimeSchema(many=True)
rate_schema = RateSchema()
rates_schema = RateSchema(many=True)
timereg_schema = TimeRegistrationSchema()
timeregs_schema = TimeRegistrationSchema(many=True)
payment_schema = PaymentMethodSchema()
payments_schema = PaymentMethodSchema(many=True)
spending_schema = SpendingSchema()
spendings_schema = SpendingSchema(many=True)
contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)
