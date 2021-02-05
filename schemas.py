from marshmallow import Schema, fields, ValidationError

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
currencies_schema = CurrencySchema(many=True)
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
