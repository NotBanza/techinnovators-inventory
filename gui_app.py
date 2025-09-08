import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from apex_client import get_employee_checkouts, return_item

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TechInnovators Employee Portal")
        self.root.geometry("800x600")

        # --- Input Frame ---
        input_frame = ttk.Frame(root, padding="10")
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Employee ID:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.emp_id_entry = ttk.Entry(input_frame, width=10, font=("Arial", 12))
        self.emp_id_entry.pack(side=tk.LEFT, padx=5)

        # --- Button Frame ---
        button_frame = ttk.Frame(root, padding="10")
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="View Current Checkouts", command=self.view_current).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Checkout History", command=self.view_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Return Equipment", command=self.open_return_popup).pack(side=tk.LEFT, padx=5)

        # --- Results Display ---
        self.results_text = tk.Text(root, wrap=tk.WORD, font=("Courier New", 11), height=25)
        self.results_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.results_text.config(state=tk.DISABLED) # Make it read-only

    def _get_validated_emp_id(self):
        emp_id = self.emp_id_entry.get()
        if not emp_id.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid Employee ID.")
            return None
        return emp_id

    def _display_results(self, title, checkouts):
        self.results_text.config(state=tk.NORMAL) # Enable writing
        self.results_text.delete(1.0, tk.END)

        header = f"{title}\n{'=' * 75}\n"
        header += f"{'Booking ID':<12} {'Item Name':<40} {'Date Booked':<12} {'Date Returned'}\n"
        header += f"{'-' * 75}\n"
        self.results_text.insert(tk.END, header)

        if not checkouts:
            self.results_text.insert(tk.END, "No records found.")
        else:
            for c in checkouts:
                date_returned = c.get('date_returned')
                display_return = "Checked Out" if date_returned is None else date_returned.split('T')[0]
                line = f"{str(c.get('booking_id', 'N/A')):<12} {c.get('item_name', 'N/A'):<40} {c.get('date_booked', 'N/A').split('T')[0]:<12} {display_return}\n"
                self.results_text.insert(tk.END, line)
        
        self.results_text.config(state=tk.DISABLED) # Make it read-only again

    def view_current(self):
        emp_id = self._get_validated_emp_id()
        if emp_id:
            all_checkouts = get_employee_checkouts(emp_id)
            if all_checkouts is not None:
                current = [c for c in all_checkouts if c.get('date_returned') is None]
                self._display_results(f"Current Checkouts for Employee {emp_id}", current)

    def view_history(self):
        emp_id = self._get_validated_emp_id()
        if emp_id:
            all_checkouts = get_employee_checkouts(emp_id)
            if all_checkouts is not None:
                history = [c for c in all_checkouts if c.get('date_returned') is not None]
                self._display_results(f"Checkout History for Employee {emp_id}", history)

    def open_return_popup(self):
        # This function creates the pop-up window for returning items
        popup = Toplevel(self.root)
        popup.title("Return Equipment")
        popup.geometry("350x200")

        frame = ttk.Frame(popup, padding="15")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Booking ID to Return:").pack(pady=5)
        booking_id_entry = ttk.Entry(frame)
        booking_id_entry.pack(pady=5)

        # THIS IS THE QR CODE SIMULATION
        ttk.Label(frame, text="Confirm with Employee ID (QR Scan):").pack(pady=5)
        emp_id_confirm_entry = ttk.Entry(frame)
        emp_id_confirm_entry.pack(pady=5)

        def submit_return():
            booking_id = booking_id_entry.get()
            emp_id_confirm = emp_id_confirm_entry.get()
            if not booking_id.isdigit() or not emp_id_confirm.isdigit():
                messagebox.showerror("Invalid Input", "Both Booking ID and Employee ID must be numbers.", parent=popup)
                return

            result = return_item(booking_id)
            if result and result.get('status') == 'success':
                messagebox.showinfo("Success", f"Booking ID {booking_id} has been returned successfully.", parent=popup)
                popup.destroy()
                # Refresh current view if an employee ID is entered
                if self.emp_id_entry.get():
                    self.view_current()
            else:
                messagebox.showerror("Error", f"Failed to return item. Server message: {result.get('message', 'Unknown error')}", parent=popup)

        ttk.Button(frame, text="Submit Return", command=submit_return).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()