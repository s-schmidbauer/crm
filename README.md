# crm

# Test
## Add
```
curl --header "Content-Type: application/json" -X POST -d '{ "name": "low", "price": "24.99" }' "http://127.0.0.1:5000/rate/"
```

## Get
```
curl --header "Content-Type: application/json" -X GET "http://127.0.0.1:5000/rate/Corp"
```

## Update
```
curl --header "Content-Type: application/json" -X PUT -d '{ "name": "Sentia 100%", "price": "54.55" }' http://127.0.0.1:5000/rate/
```
