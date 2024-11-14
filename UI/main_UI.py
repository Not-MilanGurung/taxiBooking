import tkinter as tk

root = tk.Tk()
root.title('Taxi Booking System')

tk.Label(root, text="Login").grid(row=0,column=1)

tk.Label(root, text="User Name").grid(row=1)
user = tk.Entry(root)
user.grid(row=1,column=1)

tk.Label(root, text="Password").grid(row=2)
password = tk.Entry(root)
password.grid(row=2,column=1)

tk.Button(root, text="LOGIN", width=20, command= root.destroy).grid(row=4, column=1)

root.mainloop()