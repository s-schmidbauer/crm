# crm

# Test
## Add
Get the USD conversion rate for a currency
```
curl --header "Content-Type: application/json" -X POST -d '{ "symbol": "CZK" }' http://127.0.0.1:5000/usd_conversion_rate
```
```
curl --header "Content-Type: application/json" -X POST -d '{ "symbol": "USD", "usd_conversion_rate": "1.0" }' http://127.0.0.1:5000/currency

curl --header "Content-Type: application/json" -X POST -d '{ "name": "EC" }' http://127.0.0.1:5000/payment_method

curl --header "Content-Type: application/json" -X POST -d '{ "name": "low", "price": "9.99" , "currency": { "symbol": "USD", "usd_conversion_rate": "1.0" } }' http://127.0.0.1:5000/rate

curl --header "Content-Type: application/json" -X POST -d '{ "name": "coke", "": "1.00", "payment_method": { "name": "EC" } }' http://127.0.0.1:5000/spending

curl --header "Content-Type: application/json" -X POST -d '{ "name": "EC" }' http://127.0.0.1:5000/payment_method

```

## List
```
curl --header "Content-Type: application/json" -X GET http://127.0.0.1:5000/currencies
```

## Get
```
curl --header "Content-Type: application/json" -X GET "http://127.0.0.1:5000/rate/Corp"
```

## Update
Use `find` to query the objects unique identifier
```
curl --header "Content-Type: application/json" -X PUT -d '{ "find": "USD", "symbol": "US Dollar", "usd_conversion_rate": "0.33" }' http://127.0.0.1:5000/currency
```

## Delete
```
curl --header "Content-Type: application/json" -X DELETE -d '{ "name": "Corp" }' "http://127.0.0.1:5000/rate"
{
  "deleted_count": 1
}
```
