from common.database import init_db
from product_management.add_product import add_product
from product_management.disable_product import disable_product
from product_management.manage_price import update_price
from product_management.search_product import search_by_category
from product_management.update_product import update_product


def main():
    init_db()
    while True:
        print("\n===== Product Management =====")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Search Product By Category")
        print("4. Update Product Price")
        print("5. Disable Product")
        print("6. Exit")

        choice = int(input("Enter Choice: "))
        if choice == 1:
            add_product(
                int(input("Product ID: ")),
                input("Product Name: "),
                input("Category: "),
                float(input("Price: ")),
                int(input("Quantity: ")),
            )
        elif choice == 2:
            update_product(
                int(input("Product ID: ")),
                input("New Name: "),
                input("New Category: "),
                int(input("New Quantity: ")),
            )
        elif choice == 3:
            search_by_category(input("Enter Category: "))
        elif choice == 4:
            update_price(int(input("Product ID: ")), float(input("New Price: ")))
        elif choice == 5:
            disable_product(int(input("Product ID: ")))
        elif choice == 6:
            print("Thank You")
            break
        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()
