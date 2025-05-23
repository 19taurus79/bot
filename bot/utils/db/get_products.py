from pic.tables import ProductGuide


async def get_products(product):
    products = await ProductGuide.select(
        ProductGuide.product,
    ).where(ProductGuide.product.ilike(f"%{product}%"))
    return products
