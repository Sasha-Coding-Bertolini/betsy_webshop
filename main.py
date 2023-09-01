# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

import models
import peewee


def main():
    search("iro")
    list_user_products(1)
    list_products_per_tag(3)
    add_product_to_catalog(1, models.Product.get_by_id(10))
    update_stock(1, 9)
    purchase_product(6, 1, 2)
    remove_product(11)
    ...


def search(term):
    query = models.Product.select().where(
        (models.Product.name ** f"%{term}%") | (models.Product.description ** f"{term}")
    )
    results = [product.name for product in query]

    for product_name in results:
        print(product_name)


def list_user_products(user_id):
    query = (
        models.Product.select()
        .join(models.UserProducts)
        .join(models.User)
        .where(models.User.id == user_id)
    )
    results = [product.name for product in query]

    for product_name in results:
        print(product_name)


def list_products_per_tag(tag_id):
    query = (
        models.Product.select()
        .join(models.TagProducts)
        .join(models.Tag)
        .where(models.Tag.id == tag_id)
    )
    results = [product.name for product in query]

    for product_name in results:
        print(product_name)


def add_product_to_catalog(user_id, product):
    user = models.User.get_by_id(user_id)
    if product not in user.products:
        user.products.add(product)
        print(f"{product.name} has been added to {user.name}'s catalog.")
    else:
        print(f"{product.name} already in {user.name}'s catalog.")


def update_stock(product_id, new_quantity):
    models.Product.update(quantity=new_quantity).where(models.Product.id == product_id)
    product = models.Product.get_by_id(product_id)
    print(f"The stock quantity of {product.name} has been updated to {new_quantity}.")


def purchase_product(product_id, buyer_id, quantity):
    buyer = models.User.get_by_id(buyer_id)
    product = models.Product.get_by_id(product_id)
    models.Transaction.insert(
        purchased_by_user=buyer,
        purchased_product=product,
        quantity=quantity,
    )

    if product not in buyer.products:
        add_product_to_catalog(buyer_id, product)
    print(f"{buyer.name} has purchased {quantity} of {product.name}.")


def remove_product(product_id):
    try:
        product = models.Product.get_by_id(product_id)
    except models.Product.DoesNotExist:
        print(f"Product with ID {product_id} does not exist.")
        return

    # If the product exists, remove it
    product.delete_instance()
    print(f"Product with ID {product_id} has been removed.")


if __name__ == "__main__":
    main()
