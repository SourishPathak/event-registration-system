from admin import admin_menu, admin_login
from student import student_menu, student_login
from faker_data import generate_fake_data

def main():
    while True:
        print("\n--- Event Registration System ---")
        print("1. Admin Login")
        print("2. Student Login")
        print("4. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            if admin_login():
                admin_menu()
            else:
                print("❌ Invalid admin credentials.")
        elif choice == "2":
            if student_login():
                student_menu()
            else:
                print("❌ Invalid student credentials.")
        elif choice == "4":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
