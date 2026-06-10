import json
from mcp.types import TextContent, SamplingMessage
from db_connect import DbConnect
from fetch_products import FetchProducts
from add_product import AddProduct
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
from decimal import Decimal

#-----------------------------------------------------------------------------------------

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


#-----------------------------------------------------------------------------------------
# HELPER FUNCTION TO ACHIEVE SAMPLING
#-----------------------------------------------------------------------------------------

async def generate_product_details (ctx,prompt) -> str:
    """ Calls LLM to generate Product Details. """

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt)
            )
        ],
        max_tokens=50,
    )

    if result.content.type == "text":
        return result.content.text
    return str(result.content)


#-----------------------------------------------------------------------------------------
# Initialize FastMCP server
#-----------------------------------------------------------------------------------------
mcp = FastMCP("products")


#-----------------------------------------------------------------------------------------
# RESOURCE EXAMPLE
#-----------------------------------------------------------------------------------------
@mcp.resource("products://list_products")
async def get_products():
    """Get products data from database. Returns a plain JSON-serializable dict (not a Flask Response), so the MCP host
    can consume it over the chosen transport (stdio by default). """

    db = DbConnect()
    cursor = db.connect()
    if not cursor:
        return json.dumps({"error": "Failed to connect to database"}, cls=DecimalEncoder)

    fetcher = FetchProducts(cursor)
    products = fetcher.getproducts()
    json_products = json.dumps({"products": products}, cls=DecimalEncoder)
    db.disconnect()

    return json_products


#-----------------------------------------------------------------------------------------
# TOOL EXAMPLE
#-----------------------------------------------------------------------------------------
@mcp.tool()
async def add_product(product: str,category: str,price: float):
    """ adds product to database. Expects 3 inputs ProductName, ProductCategory and Price.
     Returns a plain JSON-serializable dict (not a Flask Response), so the MCP host"""
    db = DbConnect()
    cursor = db.connect()
    if not cursor:
        return json.dumps({"error": "Failed to connect to database"}, cls=DecimalEncoder)

    adder = AddProduct(cursor)
    new_product_id = adder.add_product(product, category, price)
    db.db_commit()
    db.disconnect()

    if new_product_id:
        return json.dumps({"message": f"Added Product: id: {new_product_id}  Name: {product} Category: {category} Price: {price}"}, cls=DecimalEncoder)
    else:
        return json.dumps({"error": "Failed to add product"}, cls=DecimalEncoder)

#-----------------------------------------------------------------------------------------
# TOOL WITH SAMPLING EXAMPLE
#-----------------------------------------------------------------------------------------
@mcp.tool()
async def smart_add_product(ctx: Context):
    """ adds product smartly to database when no input parameters are provided.
     Returns a plain JSON-serializable dict (not a Flask Response), so the MCP host"""

    #ctx = get_context()
    # if not ctx.request_context.client_capabilities.sampling:
    # return f"Fall back: Client does not support LLM sampling."

    product_prompt = "Provide some product name example like TV, fridge, or any other, product that usually costs less than $1000"
    product_name = await generate_product_details(ctx,product_prompt)
    if not product_name or not product_name.strip():
        return json.dumps({"error": "Failed to generate valid product name"}, cls=DecimalEncoder)
    product_name = product_name.strip()


    category_prompt = f"Provide product category for product {product_name}"
    category = await generate_product_details(ctx,category_prompt)
    if not category or not category.strip():
        return json.dumps({"error": "Failed to generate valid category"}, cls=DecimalEncoder)
    category = category.strip()


    price_prompt = f"Provide price for product {product_name}. Price less than $1000. Float value only, no currency symbol."
    price_str = await generate_product_details(ctx,price_prompt)
    try:
        price = float(price_str.strip())
    except (ValueError, TypeError):
        return json.dumps({"error": f"Failed to convert price '{price_str}' to float"}, cls=DecimalEncoder)


    # connect to DB and insert values provided by LLM
    db = DbConnect()
    cursor = db.connect()
    if not cursor:
        return json.dumps({"error": "Failed to connect to database"}, cls=DecimalEncoder)

    adder = AddProduct(cursor)
    new_product_id = adder.add_product(product_name, category, price)
    db.db_commit()
    db.disconnect()

    if new_product_id:
        return json.dumps({"message": f"Added Product: id: {new_product_id}  Name: {product_name} Category: {category} Price: {price}"}, cls=DecimalEncoder)
    else:
        return json.dumps({"error": "Failed to add product"}, cls=DecimalEncoder)


#-----------------------------------------------------------------------------------------
# PROMPT TEMPLATE  CREATES PROMPT FOR add_product tool
#-----------------------------------------------------------------------------------------
@mcp.prompt()
def prompt_for_add_product(product: str,category: str,price: float) -> str:
    """
    Create prompt with product details.
    Args:
        product: Product name.
        category: Category of product.
        price: The price of the product.
    """
    return f"""Add product to database. Product Name: {product}. Product Category {category} Price {price}."""


#-----------------------------------------------------------------------------------------
# SETUP COMMUNICATION PROTOCOL
#-----------------------------------------------------------------------------------------
def main():
    # Initialize and run the server using stdio transport. The host that starts
    # this tool (an MCP controller) typically communicates with it over stdio.
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()

#-----------------------------------------------------------------------------------------
