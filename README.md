# Crawler Extractor

## Tech Stack

+ Python 3.6 +
+ Flask
+ MongoDb For Database

**Python Packages Used**
- python-dotenv
- pymongo
- PyYAML
- Flask
- requests-html
- flask_cors

## API

- GetProductDetails
- GetProductDetailsHistory
- GetHtml
- PriceTrend
- ListAllProducts


### GetProductDetails

- Method: **GET**
- Route: */product/v1/get_product_details*
- Request Params:
	- product_sku: product unique identifier

*Example Request*

`
http://127.0.0.1:5000/product/v1/get_product_details?sku=B08B44YH71
`
```
Success Response

{
    "data": {
        "description": "Honey is a natural food and comes with tons of uses and benefits and should be used in its pure form. Pure Honey is also a healthy alternative to sugar and is considered one of the most wonderful gifts that nature has ever gifted to mankind.\n\nHowever, not all honey sold in the market are alike! Some are pure, while others may be highly adulterated. As a consumer, one needs to be watchful as adulterated honey comes with added glucose, sugar syrup, molasses, corn syrup, etc. Not every honey that reads pure necessarily stands true to its claim. A real sign of a pure honey is a product which is free from adulteration and which complies to all the FSSAI parameters and passes the NMR (Nuclear Magnetic Resonance) test for purity.\n\nSaffola Honey is natural honey in its purest form. It is tested and approved after many rigorous quality checks including the NMR test. Each bottle of Saffola Pure Honey contains natural antioxidants, has No Added Sugar and comes with a Purity certificate that is made available to its consumers.",
        "offerPrice": "₹233.00",
        "ratingsMap": {
            "1star": "10%",
            "2star": "4%",
            "3star": "11%",
            "4star": "26%",
            "5star": "50%",
            "overallCount": "5,768 global ratings"
        },
        "title": "Saffola Honey, 100% Pure NMR tested Honey, 750g (Super Saver Pack)"
    },
    "message": "success",
    "status_code": 200
}

```


### GetProductDetailsHistory

- Method: **GET**
- Route: */product/v1/get_product_details_history*
- Request Params:
	- product_sku: product unique identifier
	- time: date of the day  

*Example Request*

`
http://127.0.0.1:5000/product/v1/get_product_details_history?sku=B08B44YH71&timestamp=2021-08-14
`

```
Success Response

{
    "data": {
			        "_id": {
			            "$oid": "611552cfb15a98c0025a6242"
			        },
			        "description": "This slim, ultra-portable HP 14 laptop delivers reliable performance. With long-lasting battery life, it's easy to stay social, productive, and connected to what matters. The micro-edge display gives you lots to look at with more screen in a smaller frame.",
			        "ratingsMap": {
			            "4star": "100%",
			            "overallCount": "1 global rating"
			        },
			        "timestamp": {
			            "$date": 1628807207292
			        },
			        "title": "HP 14 Ryzen 5 3500U 14-inch(35.6 cm) FHD Thin & Light Laptop(8GB RAM/256GB SSD + 1TB HD/Windows 10/MS Office/Natural Silver/1.47 Kg), 14s-dk0501AU",
			        "unique_sku": "B0991MJLN2"
	    },
    "message": "success",
    "status_code": 200
}
```

### GetHtml

- Method: **GET**
- Route: */product/v1/get_html*
- Request Params:
	- product_sku: product unique identifier

*Example Request*
`
http://127.0.0.1:5000/product/v1/get_html?sku=B0991MJLN2
`

```
Success Response

{
    "message": "success",
    "status_code": 200
}
```

### PriceTrend

- Method: **GET**
- Route: */product/v1/price_trend*
- Request Params:
	- product_sku: product unique identifier

*Example Request*

`
http://127.0.0.1:5000/product/v1/price_trend?sku=B07JQNB7QG
`

```
Success Response
{
    "data": [
        {
            "price": "₹162.00",
            "timestamp": "2021-08-12T14:41:44Z"
        },
        {
            "price": "₹162.00",
            "timestamp": "2021-08-12T12:42:04Z"
        },
        {
            "price": "₹162.00",
            "timestamp": "2021-08-12T12:37:37Z"
        }
    ],
    "message": "ok",
    "status_code": 200
}
```


### ListAllProducts

- Method: **GET**
- Route: */product/v1/list_all_products*

*Example Request*

```
http://127.0.0.1:5000/product/v1/list_all_product
```

```
Success Response
{
    "data": [
        {
            "_id": {
                "$oid": "611584afa718dbd1da4e62c0"
            },
            "description": "Design:Classic Masala\nSaffola Masala Oats, brings to a range of delightful flavours for a delicious anytime snack. It is made with wholegrain oats, real vegetables, & chatpata mix of spices to give you a delectable warm bowl of enjoyment that balances out chatpata cravings with health. What's more is that it gets ready to eat in just 3 minutes, so that you can enjoy this delicious healthy snacks whenever you want! Devour it as a snack for anytime taste cravings or as a delicious and delightful family breakfast cereal! Available in a range of yummy flavours - Classic Masala : for the classic masaledar experience | Veggie Twist: for the comforting blend of spices and vegetables | Peppy tomato: for a tangy indulgence | Masala Coriander: for the aromatic coriander flavour. Order your pack of this delicious healthy snack today and say bye to your chatpata cravings! Did you know? Saffola Masala Oats is made with wholegrain oats , a cereal that is high in fibre and in protein, which keep you fuller for longer, controls your hunger pangs and thereby helps you manage weight.",
            "offerPrice": "₹172.00",
            "ratingsMap": {
                "1star": "3%",
                "2star": "2%",
                "3star": "8%",
                "4star": "25%",
                "5star": "61%",
                "overallCount": "8,450 global ratings"
            },
            "timestamp": {
                "$date": 1628819975940
            },
            "title": "Saffola Masala Oats, Classic Masala, 500g",
            "unique_sku": "B07D5FG9R5"
        },
        {
            "_id": {
                "$oid": "611555c0ebaa78c4bf941d74"
            },
            "ratingsMap": {},
            "timestamp": {
                "$date": 1628807960568
            },
            "unique_sku": "B0991MJLN"
        }
    ],
    "message": "ok",
    "status_code": 200
}
```

## Running Service

*Requirement*
- Python 3.6+


**Steps to Run Service**
	1. unzip assignment folder
	2. open terminal
	3. execute commands below sequentially
	
```bash
$ cd /path_to_dir
$ pip install -r requirements.txt
$ python main.py
```

### Other Features

- Proxies added in constant file to in case if amazon blocks or any website blocks.
- A page if already crawled in the last 60 minutes, it should not be crawled again.
- I have tried to keep design flexible by using `selectors.yaml` file where we can even change structures of api request and add multiple selectors using list(right now one) change and extend it in future according to use. extensible and maintainable design
- Postman Collection

###  Possibilities of Improvements
- As we are doing some time-series operation on DB we can explore Time series database for an option
- API Response could have been abstracted as class
- Unit Testing
