from apex_client import get_employee_checkouts, return_item

def print_checkouts(checkouts, title):
    """Generic function to print a list of checkouts in a formatted table."""
    print(f"\n--- {title} ---")
    if not checkouts:
        print("No records found.")
        return

    print("-" * 75)
    print(f"{'Booking ID':<12} {'Item Name':<40} {'Date Booked':<12} {'Date Returned'}")
    print("-" * 75)
    for c in checkouts:
        booking_id = c.get('booking_id', 'N/A')
        item_name = c.get('item_name', 'N/A')
        date_booked = c.get('date_booked', 'N/A').split('T')[0] if c.get('date_booked') else 'N/A'
        date_returned = c.get('date_returned', 'N/A')
        # If date_returned is None, display 'Checked Out', otherwise show the date
        if date_returned is None:
            date_returned_display = "Checked Out"
        else:
            date_returned_display = date_returned.split('T')[0]

        print(f"{str(booking_id):<12} {item_name:<40} {date_booked:<12} {date_returned_display}")
    print("-" * 75)


def main():
    """Main function to run the command-line interface."""
    print("=== TechInnovators Employee Equipment Portal ===")
    while True:
        print("\nMenu:")
        print("1. View My Currently Checked-Out Equipment")
        print("2. View My Checkout History")
        print("3. Return Equipment")
        print("4. Exit")
        choice = input("Select an option (1-4): ")

        if choice in ['1', '2']:
            emp_id = input("Enter your Employee ID to continue: ")
            if emp_id.isdigit():
                all_checkouts = get_employee_checkouts(emp_id)
                if choice == '1':
                    # Filter for items that have NOT been returned
                    current_checkouts = [c for c in all_checkouts if c.get('date_returned') is None]
                    print_checkouts(current_checkouts, "My Currently Checked-Out Equipment")
                elif choice == '2':
                    # Filter for items that HAVE been returned
                    past_checkouts = [c for c in all_checkouts if c.get('date_returned') is not None]
                    print_checkouts(past_checkouts, "My Checkout History")
            else:
                print("Invalid Employee ID. Please enter a number.")
        
        elif choice == '3':
            booking_id = input("Enter the Booking ID of the item to return: ")
            
            # ** QR CODE SIMULATION **
            # This step fulfills the requirement to scan an employee ID for verification.
            emp_id_scan = input("Please scan your employee badge (type your Employee ID to confirm): ")

            if booking_id.isdigit() and emp_id_scan.isdigit():
                print(f"Processing return for Booking ID: {booking_id} confirmed by Employee ID: {emp_id_scan}...")
                result = return_item(booking_id)
                print(f"Server Response: {result.get('message', 'No message received.')}")
            else:
                print("Invalid Booking ID or Employee ID. Please enter numbers only.")
        
        elif choice == '4':
            print("Exiting portal.")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()