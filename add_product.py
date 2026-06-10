
class AddProduct:
    def __init__(self,cursor):
        #self.fetchQuery = "SELECT * FROM products"
        #self.fetchQuery = "select ProductCode, ProductName,ProductCategory, cast(ProductPrice as signed) from products"
        self.fetchCursor = cursor
        self.products = None


    def add_product(self,product,category,price):
        """ Fetches all products from the database and returns them as a list of tuples. """
        try:
            fetch_query = "INSERT INTO products (ProductName, ProductCategory, ProductPrice) VALUES (%s, %s, %s)"
            self.fetchCursor.execute(fetch_query, (product, category, price))
            new_product_id = self.fetchCursor.lastrowid ## list of tuples
            return new_product_id

        except Exception as e:
            print(f"Error fetching products: {e}")
            return []



