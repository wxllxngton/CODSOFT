import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from manipulate_csv import CSVThings
import copy

class ContactBookApp:
    def __init__(self, file_path=r'./csv/contacts.csv'):
        """
        Initialize the ContactBookApp.

        Parameters:
        - file_path (str): The path to the CSV file.

        Returns:
        - None
        """
        self.root = ttk.Window(themename='darkly', title='PyContact Book', iconphoto=r'./assets/phone-book.png')
        self.csv_obj = CSVThings(file_path)
        self.holding_bay = [] # Holds records to be manipulated temporarily

        self.setup_ui()


    def setup_ui(self):
        """
        Set up the user interface.

        Returns:
        - None
        """
        self.dt = Tableview(
            master=self.root,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
        )
        self.dt.grid(row=0, column=0, columnspan=8)
        self.dt.build_table_data(coldata=self.csv_obj.header, rowdata=self.csv_obj.data)

        self.create_input_widgets()

        self.create_button_widgets()

        self.in_focus = ttk.Label(self.root, text=f"Contact(s) Selected: None", bootstyle="info")
        self.in_focus.grid(row=3, column=0, columnspan=8, rowspan=4)


        self.dt.view.bind('<ButtonRelease-1>', self.on_tableview_selected, add="+")


        self.root.mainloop()

    def on_tableview_selected(self, event):
        """
        Populates the holding bay with the selected record in the TableView.

        Returns:
        - None
        """
        try:
            self.holding_bay = [list(self.dt.view.item(iid, 'values')) for iid in self.dt.view.selection()]
            print(f"In focus: {self.holding_bay}")
            if len(self.holding_bay) < 3:
                self.in_focus.config(text=f"Contact(s) Selected: {self.holding_bay}")
            else:
                self.in_focus.config(text=f"Contact(s) Selected: {self.holding_bay[0]}, {self.holding_bay[1]}...")


        except Exception:
            pass

    def create_input_widgets(self):
        """
        Create input widgets for adding contacts.

        Returns:
        - None
        """
        labels = ['Name', 'PhoneNo', 'Email', 'Address']
        entries = [ttk.Entry(self.root) for _ in range(len(labels))]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            label_widget = ttk.Label(self.root, text=label)
            label_widget.grid(row=1, column=i * 2)

            entry.grid(row=1, column=i * 2 + 1)

        self.input_entries = dict(zip(labels, entries))

    def create_button_widgets(self):
        """
        Create button widgets for manipulating contacts.

        Returns:
        - None
        """
        buttons = [
            ["Add Contact", self.add_contact, "primary-outline"],
            ["Update Contact", self.update_contact, "warning-outline"],
            ["Delete Contact", self.delete_contact, "danger"],
        ]

        for index, (text_info, command_info, bootstyle_info) in enumerate(buttons):
            button = ttk.Button(self.root, text=text_info, command=command_info, bootstyle=bootstyle_info)
            button.grid(row=2, column=(0+index)*3, columnspan=2, pady=30)

    def create_messagebox_widget(self, message):
        """
        Create messagebox widget to ping after manipulating contacts.

        Returns:
        - None
        """
        if message:
            Messagebox.ok(message=message, title="Alert!")



    def add_contact(self):
        """
        Add a contact to the CSV file and update the table.

        Returns:
        - None
        """
        values = [entry.get() for entry in self.input_entries.values()]

        if all(values):
            self.csv_obj.add_record_to_csv(values)
            self.create_messagebox_widget(message="Contact added successfully.")
            self.update_table()

    def delete_contact(self):
        """
        Delete a contact in the CSV file and update the table.

        Returns:
        - None
        """
        if self.holding_bay:
            # Delete the records in the holding_bay
            self.csv_obj.delete_record_from_csv(self.holding_bay)
            self.create_messagebox_widget(message="Contact deleted successfully.")
            self.update_table()
        else:
            self.create_messagebox_widget(message="Select a record to delete first.")

    def update_contact(self):
        """
        Update a contact in the CSV file and update the table.

        Returns:
        - None
        """
        values = [entry.get() for entry in self.input_entries.values()]
        tmp = copy.deepcopy(self.holding_bay)

        for index in range(len(values)):
            if values[index]:
                tmp[0][index] = values[index]

        self.csv_obj.update_record_in_csv(self.holding_bay[0], tmp[0])
        self.create_messagebox_widget(message="Contact updated successfully.")

        self.update_table()

    def update_table(self):
        """
        Update the table with the latest data from the CSV file.

        Returns:
        - None
        """
        updated_csv_obj = CSVThings(r'./csv/contacts.csv')
        self.dt.build_table_data(coldata=updated_csv_obj.header, rowdata=updated_csv_obj.data)

if __name__ == "__main__":
    app = ContactBookApp()
