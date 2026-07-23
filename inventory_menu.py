from inventory_management.services.inventory_service import (
    add_stock,
    reduce_stock,
    check_stock,
    display_inventory,
    display_low_stock,
    stock_transaction_history
)


def inventory_menu():

    while True:

        print("\n" + "=" * 50)
        print("        INVENTORY MANAGEMENT")
        print("=" * 50)

        print("1. Add Stock")
        print("2. Reduce Stock")
        print("3. Check Stock")
        print("4. Display Inventory")
        print("5. Display Low Stock Products")
        print("6. Stock Transaction History")
        print("7. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            add_stock()

        elif choice == "2":

            reduce_stock()

        elif choice == "3":

            check_stock()

        elif choice == "4":

            display_inventory()

        elif choice == "5":

            display_low_stock()

        elif choice == "6":

            stock_transaction_history()

        elif choice == "7":

            print("Exiting Inventory Module...")
            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    inventory_menu()