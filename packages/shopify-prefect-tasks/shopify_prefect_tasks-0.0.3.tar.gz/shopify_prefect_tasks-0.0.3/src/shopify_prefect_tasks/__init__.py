"""
Tasks for interacting with Shopify.
"""
try:
    from .customer import FetchCustomer, CreateCustomer, UpdateCustomer, DeleteCustomer
    from .product import FetchProduct, CreateProduct, UpdateProduct, CountProducts, DeleteProduct
    from .variant import FetchVariant, CreateVariant, UpdateVariant, CountVariants, DeleteVariant
except ImportError:
    raise ImportError(
        'Using `prefect.tasks.shopify` requires Prefect to be installed with the "shopify" extra.'
    )
