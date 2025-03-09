from customtkinter import *


# Load existing contacts from file
def load_contacts():
    try:
        with open("phonebook_data", "r") as f:
            return [line.strip().split(",") for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []


def save_contact(name, phone):
    with open("phonebook_data", "a") as f:
        f.write(f"{name},{phone}\n")


def delete_contact(name, phone):
    global contacts_list
    contacts_list = [c for c in contacts_list if c != [name, phone]]
    with open("phonebook_data", "w") as f:
        for contact in contacts_list:
            f.write(f"{contact[0]},{contact[1]}\n")
    display_contacts()


def display_contacts(filtered_contacts=None):
    for widget in scroll_frame.winfo_children():  # Clear all previous contacts including headers
        widget.destroy()

    header_name = CTkLabel(scroll_frame, text="Name", font=("Arial", 14, "bold"))
    header_name.grid(row=0, column=0, padx=50, pady=5)
    header_phone = CTkLabel(scroll_frame, text="Phone", font=("Arial", 14, "bold"))
    header_phone.grid(row=0, column=1, padx=30, pady=5)
    header_action = CTkLabel(scroll_frame, text="Action", font=("Arial", 14, "bold"))
    header_action.grid(row=0, column=2, padx=10, pady=5)

    contacts = filtered_contacts if filtered_contacts is not None else contacts_list
    for i, (name, phone) in enumerate(contacts, start=1):
        CTkLabel(scroll_frame, text=name).grid(row=i, column=0, padx=50)
        CTkLabel(scroll_frame, text=phone).grid(row=i, column=1, padx=30)
        delete_button = CTkButton(scroll_frame, text="Delete", width=10,
                                  command=lambda n=name, p=phone: delete_contact(n, p))
        delete_button.grid(row=i, column=2, padx=10)


def add_contact():
    name, phone = entry.get(), phone_entry.get()
    if name and phone:
        contacts_list.append([name, phone])
        save_contact(name, phone)
        display_contacts()
        entry.delete(0, END)
        phone_entry.delete(0, END)


def on_typing(event=None):
    query = entry.get().lower()
    filtered = [c for c in contacts_list if query in c[0].lower()]
    display_contacts(filtered)


# GUI setup
set_appearance_mode("light")
app = CTk()
app.geometry("480x500")

contacts_list = load_contacts()

label1 = CTkLabel(app, text="PHONE BOOK", font=("Arial", 20, "bold"))
label1.pack(pady=20, padx=20)

frame1 = CTkFrame(app)
frame1.pack()

entry = CTkEntry(frame1, placeholder_text="Type name here...")
entry.grid(row=0, column=1)
entry.bind("<KeyRelease>", on_typing)

phone_entry = CTkEntry(frame1, placeholder_text="Phone number...")
phone_entry.grid(row=0, column=2)

add_button = CTkButton(frame1, text="Add", width=10, command=add_contact)
add_button.grid(row=0, column=3)

scroll_frame = CTkScrollableFrame(app, width=380, height=250)
scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

display_contacts()
app.mainloop()
