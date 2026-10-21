import json
import os

DATA_FILE = "business_data.json"

# Initial data structure
CATEGORIES = {
    "services": "Digital Services",
    "programs": "Technology Programs",
    "internships": "Internship Programs",
    "customers": "Customers",
    "inquiries": "Customer Inquiries"
}


def load_data():
    """Load saved business data."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            for category in CATEGORIES:
                data.setdefault(category, [])

            return data

        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read saved data.")

    return {category: [] for category in CATEGORIES}


def save_data(data):
    """Save business data to JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def display_records(records):
    """Display records in a readable format."""
    if not records:
        print("No records found.")
        return

    for record in records:
        print("-" * 40)
        for key, value in record.items():
            print(f"{key.title()}: {value}")
    print("-" * 40)


def add_record(data, category):
    """Add a new record to a selected category."""
    print(f"\nAdd {CATEGORIES[category]}")

    record_id = input("Enter unique ID: ").strip()

    if not record_id:
        print("ID cannot be empty.")
        return

    if any(
        record["id"].lower() == record_id.lower()
        for record in data[category]
    ):
        print("This ID already exists in this category.")
        return

    name = input("Enter name/title: ").strip()

    if not name:
        print("Name/title cannot be empty.")
        return

    description = input("Enter description: ").strip()
    status = input("Enter status (Active/Pending/Closed): ").strip()

    if not status:
        status = "Active"

    record = {
        "id": record_id,
        "name": name,
        "description": description,
        "status": status
    }

    # Additional fields for inquiries and customers
    if category == "customers":
        record["contact"] = input("Enter contact information: ").strip()

    elif category == "inquiries":
        record["customer"] = input("Enter customer name: ").strip()
        record["priority"] = input("Enter priority (Low/Medium/High): ").strip()

    data[category].append(record)
    save_data(data)

    print("Record added successfully!")


def view_records(data, category):
    """View all records in a category."""
    print(f"\n{CATEGORIES[category]} Records")
    display_records(data[category])


def search_records(data):
    """Search records across all categories."""
    keyword = input("Enter ID, name, description, or status to search: ")
    keyword = keyword.strip().lower()

    if not keyword:
        print("Please enter a search keyword.")
        return

    found = False

    for category, records in data.items():
        for record in records:
            searchable_text = " ".join(
                str(value) for value in record.values()
            ).lower()

            if keyword in searchable_text:
                print(f"\nCategory: {CATEGORIES[category]}")
                display_records([record])
                found = True

    if not found:
        print("No matching records found.")


def filter_records(data):
    """Filter records by category and status."""
    print("\nSelect category:")

    category_list = list(CATEGORIES.keys())

    for number, category in enumerate(category_list, start=1):
        print(f"{number}. {CATEGORIES[category]}")

    try:
        choice = int(input("Enter category number: "))

        if choice < 1 or choice > len(category_list):
            print("Invalid category.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    category = category_list[choice - 1]
    status = input("Enter status to filter by: ").strip().lower()

    results = [
        record for record in data[category]
        if status in str(record.get("status", "")).lower()
    ]

    print(f"\nFiltered {CATEGORIES[category]}:")
    display_records(results)


def update_record(data):
    """Update a record using its category and ID."""
    print("\nSelect the category to update:")

    category_list = list(CATEGORIES.keys())

    for number, category in enumerate(category_list, start=1):
        print(f"{number}. {CATEGORIES[category]}")

    try:
        choice = int(input("Enter category number: "))

        if choice < 1 or choice > len(category_list):
            print("Invalid category.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    category = category_list[choice - 1]
    record_id = input("Enter record ID: ").strip()

    for record in data[category]:
        if record["id"].lower() == record_id.lower():
            print("Leave a field blank to keep its current value.")

            for field, value in record.items():
                new_value = input(f"{field.title()} [{value}]: ").strip()

                if new_value:
                    record[field] = new_value

            save_data(data)
            print("Record updated successfully!")
            return

    print("Record not found.")


def delete_record(data):
    """Delete a record using its category and ID."""
    print("\nSelect category:")

    category_list = list(CATEGORIES.keys())

    for number, category in enumerate(category_list, start=1):
        print(f"{number}. {CATEGORIES[category]}")

    try:
        choice = int(input("Enter category number: "))

        if choice < 1 or choice > len(category_list):
            print("Invalid category.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    category = category_list[choice - 1]
    record_id = input("Enter record ID to delete: ").strip()

    for record in data[category]:
        if record["id"].lower() == record_id.lower():
            confirm = input(
                f"Delete '{record['name']}'? (yes/no): "
            ).strip().lower()

            if confirm == "yes":
                data[category].remove(record)
                save_data(data)
                print("Record deleted successfully!")
            else:
                print("Deletion cancelled.")
            return

    print("Record not found.")


def business_report(data):
    """Generate a summary of all business records."""
    print("\n===== BUSINESS SUMMARY REPORT =====")

    total_records = 0

    for category, records in data.items():
        total_records += len(records)
        active = sum(
            1 for record in records
            if record.get("status", "").lower() == "active"
        )

        print(f"{CATEGORIES[category]}: {len(records)}")
        print(f"  Active records: {active}")

    print("-" * 35)
    print(f"Total records: {total_records}")

    open_inquiries = sum(
        1 for record in data["inquiries"]
        if record.get("status", "").lower() in ("pending", "open")
    )

    print(f"Pending/open inquiries: {open_inquiries}")


def main():
    data = load_data()

    while True:
        print("\n========================================")
        print(" BUSINESS & SERVICE MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Add Service")
        print("2. Add Technology Program")
        print("3. Add Internship Program")
        print("4. Add Customer")
        print("5. Add Customer Inquiry")
        print("6. View Records")
        print("7. Search Records")
        print("8. Filter Records by Status")
        print("9. Update Record")
        print("10. Delete Record")
        print("11. Business Summary Report")
        print("12. Exit")

        choice = input("Enter your choice (1-12): ").strip()

        if choice == "1":
            add_record(data, "services")
        elif choice == "2":
            add_record(data, "programs")
        elif choice == "3":
            add_record(data, "internships")
        elif choice == "4":
            add_record(data, "customers")
        elif choice == "5":
            add_record(data, "inquiries")
        elif choice == "6":
            print("\nSelect category:")
            category_list = list(CATEGORIES.keys())

            for number, category in enumerate(category_list, start=1):
                print(f"{number}. {CATEGORIES[category]}")

            try:
                selected = int(input("Enter category number: "))

                if 1 <= selected <= len(category_list):
                    view_records(data, category_list[selected - 1])
                else:
                    print("Invalid category.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "7":
            search_records(data)
        elif choice == "8":
            filter_records(data)
        elif choice == "9":
            update_record(data)
        elif choice == "10":
            delete_record(data)
        elif choice == "11":
            business_report(data)
        elif choice == "12":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Please select 1-12.")


if __name__ == "__main__":
    main()