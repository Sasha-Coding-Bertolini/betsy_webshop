import models
import os
from peewee import fn

"""
This file creates/deletes a database for testing the functions in main.py.
"""


def main():
    populate_test_database()
    # delete_test_database()


def populate_test_database():
    """
    Creates the test database and fills it with data.
    """
    models.db.connect()
    models.db.create_tables(
        [
            models.User,
            models.Product,
            models.Tag,
            models.TagProducts,
            models.UserProducts,
            models.Transaction,
        ]
    )

    user_data = [
        (
            ("Sasha Jansen", "Waterschans 211, 2076 CP, Hoorn", "NL65 INGB 9871287970"),
            [
                ("glasses", "everybody deserves to see", 999, 10, "Accessories"),
                ("plate", "handcrafted plate", 1599, 20, "Kitchen"),
                ("shoe rack", "keep your shoes organised", 1395, 1, "Furniture"),
            ],
        ),
        (
            ("Achmed Boukari", "Hemweg 1, 4444 HJ, Ikers", "NL94 ASNB 908359879"),
            [
                ("floor lamp", "shine bright", 2570, 3, "Lamps"),
                ("dresser", "big and beautiful", 7000, 1, "Furniture"),
                ("mirror", "to see yourself better", 1799, 2, "Furniture"),
            ],
        ),
        (
            (
                "Mo Vissing",
                "Lange steeg 234, 5678 DD, Broekjesdorp",
                "NL55 ABNA 0985987313",
            ),
            [
                ("book", "the adventures of little rabbit", 1160, 5, "Books"),
                ("lantern", "like the olden days", 3200, 5, "Lamps"),
            ],
        ),
        (
            (
                "Piter Castillas",
                "Plasjes 76, 1111 AA, Amsterdam",
                "NL65 INGB 0863598697",
            ),
            [
                ("ring", "made by yours one and only", 10000, 15, "Jewelry"),
            ],
        ),
        (
            (
                "Gergia Hakman",
                "Sneevliet 274, 0909 GV, Apeldoorn",
                "NL65 ASNV 84699869486",
            ),
            [
                ("necklace", "jewelry for around the neck", 15000, 7, "Jewelry"),
                ("handmade soap", "delicious smell", 999, 15, "Sanitary"),
                ("plate", "handcrafted plate", 1599, 45, "Kitchen"),
                ("clothes rack", "keep your clothes organised", 1495, 4, "Furniture"),
            ],
        ),
    ]

    for user, products in user_data:
        # create a new user
        user = models.User.create(
            name=user[0],
            address=user[1],
            billing_info=user[2],
        )

        for product_data in products:
            # Create a new product
            product = models.Product.create(
                name=product_data[0],
                description=product_data[1],
                price_per_unit_cents=product_data[2],
                quantity=product_data[3],
            )
            user.products.add(product)

            # Create a transaction for each product
            models.Transaction.create(
                purchased_by_user=user,
                purchased_product=product,
                quantity=product_data[3],
            )

            # Check if a tag with the same name already exists
            tag_name = product_data[4].lower()
            existing_tag = models.Tag.get_or_none(fn.LOWER(models.Tag.name) == tag_name)
            if existing_tag is None:
                # Create the tag with the specified name
                tag = models.Tag.create(name=product_data[4])
                tag.products.add(product)
            else:
                existing_tag.products.add(product)


def delete_test_database():
    """
    Delete the database.
    """
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "database.db")
    if os.path.exists(database_path):
        os.remove(database_path)


if __name__ == "__main__":
    main()
