from db_connect import DbConnect
from fetch_products import FetchProducts
from add_product import AddProduct

#-------------------------------------------------------------------------------------

print("\nSelect operation to be performed:\n1. Fetch and Display Products \n2. Add Product\n")
choice = input("Enter your choice 1 or 2: ")

#-------------------------------------------------------------------------------------

# Connect to DB and get cursor
db = DbConnect()
cursor = db.connect()

#-------------------------------------------------------------------------------------

if choice == "1":
    # Execute fetch Query for Products and then Display
    products = FetchProducts(cursor)
    products.getproducts()
    products.displayproducts()

#-------------------------------------------------------------------------------------

if choice == "2":
    # Execute insert Query for Products and then Display
    product_name = input("Provide Product Name: ")
    product_category = input("Provide Product Category: ")
    product_price = float(input("Provide Product Price: "))
    new_product = AddProduct(cursor)
    product_id = new_product.add_product(product_name, product_category, product_price)
    db.db_commit()
    if product_id:
        print(f"Added Product: id: {product_id}  Name: {product_name} Category: {product_category} Price: {product_price}")

#-------------------------------------------------------------------------------------

# Close DB Connection
 ## commit any pending transactions before disconnecting
db.disconnect()

#-------------------------------------------------------------------------------------

