# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

import models
import peewee


def main():
    search("irro")
    list_user_products(1)
    list_products_per_tag(3)
    add_product_to_catalog(1, models.Product.get_by_id(10))
    update_stock(1, 9)
    purchase_product(1, 8, 2)
    remove_product(8)
    ...


def search(term):
    query = models.Product.select().where(
        (models.Product.name ** f"%{term}%") | (models.Product.description ** f"{term}")
    )
    print(query)
    return query


def list_user_products(user_id):
    query = (
        models.Product.select()
        .join(models.UserProducts)
        .join(models.User)
        .where(models.User.id == user_id)
    )
    print(query)
    return query


def list_products_per_tag(tag_id):
    query = (
        models.Product.select()
        .join(models.TagProducts)
        .join(models.Tag)
        .where(models.Tag.id == tag_id)
    )
    print(query)
    return query


def add_product_to_catalog(user_id, product):
    user = models.User.get_by_id(user_id)
    query = user.products.add(product)
    print(query)
    return query


def update_stock(product_id, new_quantity):
    query = models.Product.update(total_quantity=new_quantity).where(
        models.Product.id == product_id
    )
    print(query)
    return query


def purchase_product(product_id, buyer_id, quantity):
    buyer = models.User.get_by_id(buyer_id)
    product = models.Product.get_by_id(product_id)
    query = models.Transaction.create(
        purchased_by_user=buyer,
        purchased_product=product,
        quantity_purchased_items=quantity,
    )
    add_product_to_catalog(buyer_id, product)
    print(query)
    return query


def remove_product(product_id):
    query = models.Product.delete().where(models.Product.id == product_id)
    print(query)
    return query


if __name__ == "__main__":
    main()
