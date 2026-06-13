import random
import string
import sys
from faker import Faker

# Initialize the Faker generator
fake = Faker()

def generate_field(field_type):
    """Generates a single piece of fake data based on type."""
    if field_type == "IP":
        return fake.ipv4()
    elif field_type == "MAC":
        return fake.mac_address()
    elif field_type == "Location":
        return f"{fake.city()}, {fake.country()}"
    elif field_type == "Password":
        pool = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choice(pool) for _ in range(14))
    elif field_type == "Name":
        return fake.name()
    elif field_type == "Username":
        return fake.user_name()
    elif field_type == "Phone Number":
        return fake.phone_number()
    elif field_type == "Company":
        return fake.company()
    elif field_type == "Job Title":
        return fake.job()
    elif field_type == "Credit Card":
        return fake.credit_card_number()
    elif field_type == "Birthdate":
        return str(fake.date_of_birth(minimum_age=18, maximum_age=70))
    return "Unknown Field"

def main():
    # 1. Warning That a Chance of real infos being shown
    print("====================================================")
    print("WARNING: This tool generates data dynamically.")
    print("There is a mathematical chance that generated values")
    print("(like IPs or Names) may match real-world information.")
    print("====================================================\n")

    # Mapping numbers to choices (Expanded List)
    options = {
        "1": "IP",
        "2": "MAC",
        "3": "Location",
        "4": "Password",
        "5": "Name",
        "6": "Username",
        "7": "Phone Number",
        "8": "Company",
        "9": "Job Title",
        "10": "Credit Card",
        "11": "Birthdate"
    }

    # 2. How many things i want to randomize
    print("Available options to randomize:")
    for num, name in options.items():
        print(f"[{num}] {name}")
        
    try:
        count = int(input("\nHow many fields do you want to randomize? "))
    except ValueError:
        print("Please enter a valid number.")
        sys.exit()

    # 3. Ask What i Want To Fake/Randomize
    selected_fields = []
    print("\nEnter the numbers of the choices you want to include:")
    for i in range(count):
        choice = input(f"Field {i+1}: ").strip()
        if choice in options:
            selected_fields.append(options[choice])
        else:
            print("Invalid choice, skipping.")

    if not selected_fields:
        print("No valid fields selected. Exiting.")
        sys.exit()

    # 4. Show the Fake Infos
    print("\n--- Generated Fake Infos ---")
    generated_data = {}
    for field in selected_fields:
        val = generate_field(field)
        generated_data[field] = val
        print(f"{field}: {val}")
    print("----------------------------\n")

    # 5. Ask if you want to save them
    save_choice = input("Do you want to save these infos? (yes/no): ").strip().lower()

    # 6. If Yes = Save As F_infos.chesty
    if save_choice in ["yes", "y"]:
        filename = "F_infos.chesty"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for key, value in generated_data.items():
                    # Formatted cleanly so your C compiler can parse it easily
                    f.write(f"{key}={value}\n")
            print(f"Successfully saved data to '{filename}'!")
        except Exception as e:
            print(f"Error saving file: {e}")
            
    # 7. If NO = don't save
    else:
        print("Data was not saved.")

if __name__ == "__main__":
    main()
