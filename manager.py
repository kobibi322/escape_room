from rooms import show_all_rooms, show_room_by_id, print_rooms_menu, add_new_room, update_room, change_room_status
from orders import (
    print_orders_menu, make_order, show_all_orders, show_order_by_id,
    show_orders_by_customer, show_orders_by_date, update_order, cancel_order
)
from validations import validate_int
from reports import print_reports_menu, show_room_occupancy_rate, show_orders_per_room, show_active_revenue, show_most_popular_room, show_active_orders_count, show_cancelled_orders_count, show_cancellation_fees_total


def print_main_menu():
    print("""
=================================
       ESCAPE ROOM SYSTEM        
=================================

1. Rooms Management
2. Orders Management
3. Reports
4. Exit
""")


def main_manager():
    user_choice = ""
    while user_choice != "4":      
        print_main_menu()
        user_choice = input("Enter choice: ")
        if user_choice == "1":
            rooms_manager()
        elif user_choice == "2":
            orders_manager()
        elif user_choice == "3":
            reports_manager()
        elif user_choice == "4":
            print("bye!🙋")
            break
        else:
            print("Invalid choice! Please choose a number between 1 and 4.")

def rooms_manager():
    user_choice = ""
    while user_choice != "6":
        print_rooms_menu()
        user_choice = input("Choose an option (1-6):")
        if user_choice == "1":
            show_all_rooms()
        elif user_choice == "2":
            show_room_by_id()
        elif user_choice == "3":
            add_new_room()
        elif user_choice == "4":
            update_room()
        elif user_choice == "5":
            change_room_status()
        elif user_choice == "6":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice! Please choose a number between 1 and 6.")

def orders_manager():
    user_choice = ""
    while user_choice != "8":
        print_orders_menu()
        user_choice = input("Choose an option (1-8):")
        if choice == "1":
            make_order()
        elif choice == "2":
            show_all_orders()
        elif choice == "3":
            show_order_by_id()
        elif choice == "4":
            show_orders_by_customer()
        elif choice == "5":
            show_orders_by_date()
        elif choice == "6":
            update_order()
        elif choice == "7":
            cancel_order()
        elif choice == "8":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice! Please choose a number between 1 and 8.")

def reports_manager():
    user_choice = ""
    while user_choice != "8":
        print_reports_menu()
        user_choice = input("Choose an option (1-8): ").strip()
        try:
            if user_choice == "1":
                show_active_orders_count()
            elif user_choice == "2":
                show_cancelled_orders_count()
            elif user_choice == "3":
                show_active_revenue()
            elif user_choice == "4":
                show_cancellation_fees_total()
            elif user_choice == "5":
                show_most_popular_room()
            elif user_choice == "6":
                show_orders_per_room()
            elif user_choice == "7":
                show_room_occupancy_rate()
            elif user_choice == "8":
                print("Returning to Main Menu...")
                break
            else:
                print("Invalid choice! Please choose 1-8.")
        except Exception as e:
            print(f"Error: {e}")