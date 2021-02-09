# CRM

Get (`GET`), update (`PUT`), create (`POST`) and delete (`DELETE`) single entities.
```
/currency
/rate
/spending
/time_registration
/contact
/payment_method
/invoice
```

List (`GET`) entities
```
/currencies
/rates
/spendings
/time_registrations
/contacts
/payment_methods
/invoices
```

# Test

## Get
```
curl --header "Content-Type: application/json" -X GET "http://127.0.0.1:5000/rate/Corp"
{
  "rates": [
    {
      "currency": {
        "symbol": "USD",
        "usd_conversion_rate": 1.0
      },
      "name": "low",
      "price": 9.99
    }
  ]
}
```

## Add
Get the USD conversion rate for a currency
```
curl --header "Content-Type: application/json" -X POST -d '{ "symbol": "CZK" }' http://127.0.0.1:5000/usd_conversion_rate
```
Add currency
```
curl --header "Content-Type: application/json" -X POST -d '{ "symbol": "USD", "usd_conversion_rate": "1.0" }' http://127.0.0.1:5000/currency
```

Add a new rate
```
curl --header "Content-Type: application/json" -X POST -d '{ "currency": { "symbol": "EUR", "usd_conversion_rate": "1.1983" }, "name": "sen-150", "price": "43.46" }' http://127.0.0.1:5000/rate
```

Add time of a certain rate
```
curl --header "Content-Type: application/json" -X POST -d '{ "name": "sen-kw5-150", "hours": "2.0" , "rate": { "currency": { "symbol": "EUR", "usd_conversion_rate": "1.1983" }, "name": "sen-150", "price": "43.46" } }' http://127.0.0.1:5000/time
```

Add spending and payment method
```
curl --header "Content-Type: application/json" -X POST -d '{ "name": "EC" }' http://127.0.0.1:5000/payment_method

curl --header "Content-Type: application/json" -X POST -d '{ "name": "coke", "": "1.00", "payment_method": { "name": "EC" } }' http://127.0.0.1:5000/spending
```

Add spedings and time registrations to invoices

## List
```
curl --header "Content-Type: application/json" -X GET http://127.0.0.1:5000/currencies
```

## Update
Use `find` to query the objects unique identifier
```
curl --header "Content-Type: application/json" -X PUT -d '{ "find": "USD", "symbol": "US Dollar", "usd_conversion_rate": "1.0" }' http://127.0.0.1:5000/currency
```

## Delete
```
curl --header "Content-Type: application/json" -X DELETE -d '{ "name": "Corp" }' "http://127.0.0.1:5000/rate"
{
  "deleted_count": 1
}
```
