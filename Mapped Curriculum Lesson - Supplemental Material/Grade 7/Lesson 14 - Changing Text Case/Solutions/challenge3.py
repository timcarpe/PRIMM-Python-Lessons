password = input("New password: ")
confirm = input("Enter it again: ")
lower_password = password.lower()
lower_confirm = confirm.lower()
if password == confirm:
    print("Thank you")
elif lower_password == lower_confirm:
    print("They must be in the same case")
else:
    print("Incorrect")
