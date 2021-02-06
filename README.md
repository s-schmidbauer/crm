# crm

# Test
## Add
```
curl --header "Content-Type: application/json" -X POST -d '{ "symbol": "USD", "usd_conversion_rate": "1.0" }' http://127.0.0.1:5000/currency
{
  "_links": {
    "collection": "/currencies", 
    "self": "/currency/USD"
  }, 
  "symbol": "USD", 
  "usd_conversion_rate": 1.0
}
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
```
curl --header "Content-Type: application/json" -X PUT -d '{ "name": "Sentia 100%", "price": "54.55" }' http://127.0.0.1:5000/rate/
```

## Delete
```
curl --header "Content-Type: application/json" -X DELETE -d '{ "name": "Corp" }' "http://127.0.0.1:5000/rate/"
{
  "deleted_count": 1
}
```
