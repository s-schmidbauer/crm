# CRM

* RESTful CRM HTTP API
* Built with Flask, marshmallow and MongoDB
* Auth required for protected endpoints


# Endpoints

Login first for all write operations. They require providing a `token`
```
/login
```

Get (`GET`), update (`PUT`), create (`POST`) and delete (`DELETE`) single entities.
```
/currency
/time
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
/times
/rates
/spendings
/time_registrations
/contacts
/payment_methods
/invoices
```

Special functions
```
/usd_conversion_rate
/get_time_reg_total
```

# Test

[![Try in PWD](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/s-schmidbauer/crm/docker-compose.yml)

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
curl --header "Content-Type: application/json" -X POST -d '{ "currency": { "symbol": "EUR", "usd_conversion_rate": "1.1983" }, "name": "sen-150", "price": "75.00", "token": "secret" }' http://127.0.0.1:5000/rate
```

Add time of a certain rate
```
curl --header "Content-Type: application/json" -X POST -d '{ "name": "sen-kw5-150", "hours": "2.0" , "rate": { "currency": { "symbol": "EUR", "usd_conversion_rate": "1.1983" }, "name": "sen-150", "price": "75.00" } }, "token": "secret"' http://127.0.0.1:5000/time
```

Add spending and payment method
```
curl --header "Content-Type: application/json" -X POST -d '{ "name": "EC", "token": "secret" }' http://127.0.0.1:5000/payment_method

curl --header "Content-Type: application/json" -X POST -d '{ "name": "coke", "price": "1.00", "payment_method": { "name": "EC" }, "token": "secret" }' http://127.0.0.1:5000/spending
```

Add a list of times to a new time registration
```
curl --header "Content-Type: application/json" -X POST -d '{ "name": "sen-feb-2021", "start_date": "01-02-2021", "end_date": "31-02-2021", "times": [ {"name": "sen-kw5-100", "hours": "38.0", "rate": {"name": "sen-100", "price": "28.97", "currency": {"symbol": "EUR", "usd_conversion_rate": "1.1983" } } } ], "token": "secret" }' http://127.0.0.1:5000/time_registration
```

Get the total of a time registration by posting a time reg to that endpoint.
```
curl --header "Content-Type: application/json" -X POST -d '{ "name": "sen-feb-2021", "start_date": "01-02-2021", "end_date": "31-02-2021", "times": [ {"name": "sen-kw5-100", "hours": "38.0", "rate": {"name": "sen-100", "price": "28.97", "currency": {"symbol": "EUR", "usd_conversion_rate": "1.1983" } } }, {"name": "sen-kw5-150", "hours": "2.0", "rate": {"name": "sen-150", "price": "43.46", "currency": {"symbol": "EUR", "usd_conversion_rate": "1.1983" } } } ] }' http://127.0.0.1:5000/get_time_reg_total
{
  "calculated_total": "1187.78",
  "hours_total": "40.0",
  "sub_totals": [
    {
      "hours": 38.0,
      "price": 28.97,
      "subtotal": 1100.86,
      "symbol": "EUR"
    },
    {
      "hours": 2.0,
      "price": 43.46,
      "subtotal": 86.92,
      "symbol": "EUR"
    }
  ],
  "symbol": "EUR",
  "times_count": "2"
}

```

Add spedings and time registrations to invoices

## List
```
curl --header "Content-Type: application/json" -X GET http://127.0.0.1:5000/currencies
```

## Update
Use `find` to query the objects unique identifier
```
curl --header "Content-Type: application/json" -X PUT -d '{ "find": "USD", "symbol": "US Dollar", "usd_conversion_rate": "1.0" }, "token": "secret"' http://127.0.0.1:5000/currency
```

## Delete
```
curl --header "Content-Type: application/json" -X DELETE -d '{ "name": "Corp", "token": "secret" }' "http://127.0.0.1:5000/rate"
{
  "deleted_count": 1
}
```
