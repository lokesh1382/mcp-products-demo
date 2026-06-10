
class FetchProducts:
    def __init__(self,cursor):
        #self.fetchQuery = "SELECT * FROM products"
        self.fetchQuery = "select ProductCode, ProductName,ProductCategory, cast(ProductPrice as signed) from products"
        self.fetchCursor = cursor
        self.products = None


    def getproducts(self):
        """ Fetches all products from the database and returns them as a list of tuples. """
        try:
            self.fetchCursor.execute(self.fetchQuery)
            self.products = self.fetchCursor.fetchall() ## list of tuples
            return self.products

        except Exception as e:
            print(f"Error fetching products: {e}")
            return []


    def displayproducts(self):
        """ Displays the fetched products in a readable format. """
        if self.products:
            print("** Products: *********************************************")
            for product in self.products:
                print(f"ID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: {product[3]}")
            print("**********************************************************")

        else:
            print("No products found.")

