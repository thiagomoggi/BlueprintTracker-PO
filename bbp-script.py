output_file = "crafting_blueprints.txt"

blueprint_types = {
    "Craft": {
        "Umbra Crystal": ["Fish Remains", "Shell Elixir", "Black Ink"],
        "Fire Seed": ["Poison", "Iron Ore", "Hidden Honey"],
    },
    "Cooking": {
        "Field Brew": ["Herbs", "Water", "Spices"]
    },
    "Manufacturing": {
        "Flash Bomb": ["Lightning Heart", "Enchanted Wood Strip", "Mystic Leaf"]
    }
}

def read_blueprints():
    try:
        with open(output_file, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def save_all_lines(lines):
    with open(output_file, "w") as f:
        f.writelines(lines)

def append_line(text):
    with open(output_file, "a") as f:
        f.write(text + "\n")

def show_existing_blueprints():
    lines = read_blueprints()
    if not lines:
        print("\n>> No blueprints saved yet.")
        return []

    categorized = {bp_type: [] for bp_type in blueprint_types.keys()}
    categorized["Unknown"] = []

    # Map blueprint name to type
    name_to_type = {}
    for bp_type, items in blueprint_types.items():
        for blueprint_name in items.keys():
            name_to_type[blueprint_name] = bp_type

    # Classify each line
    for idx, line in enumerate(lines, 1):
        blueprint_name = line.split("|")[0].strip()
        bp_type = name_to_type.get(blueprint_name, "Unknown")
        categorized[bp_type].append(f"{idx}. {line.strip()}")

    for bp_type in blueprint_types.keys():
        print(f"\n=== {bp_type} Blueprints ===")
        if categorized[bp_type]:
            for entry in categorized[bp_type]:
                print(entry)
        else:
            print("(none)")

    # Show Unknown blueprints
    if categorized["Unknown"]:
        print(f"\n=== Unknown Blueprints (not found in known types) ===")
        for entry in categorized["Unknown"]:
            print(entry)

    return lines

def delete_blueprint():
    lines = show_existing_blueprints()
    if not lines:
        return

    try:
        line_number = input("\nEnter the line number to delete (or press Enter to cancel): ")
        if line_number.strip() == "":
            print(">> Deletion canceled.")
            return

        line_number = int(line_number)
        if 1 <= line_number <= len(lines):
            deleted_line = lines.pop(line_number - 1)
            save_all_lines(lines)
            print(f">> Deleted: {deleted_line.strip()}")
        else:
            print("Invalid line number.")
    except ValueError:
        print("Invalid input. Must be a number.")


def calculate_total_materials():
    lines = read_blueprints()
    if not lines:
        print("\n>> No blueprints saved. Nothing to calculate.")
        return

    total_materials = {}

    for line in lines:
        if "|" not in line:
            continue
        try:
            parts = line.strip().split("|")
            usage_part = [p for p in parts if "Usage:" in p][0].replace("Usage:", "").strip()
            materials_part = [p for p in parts if "Materials:" in p][0].replace("Materials:", "").strip()

            usage_count = int(usage_part)
            materials_list = materials_part.split(",")

            for mat_entry in materials_list:
                mat_name, qty_per_craft = mat_entry.strip().split(":")
                total_qty = usage_count * int(qty_per_craft)

                if mat_name not in total_materials:
                    total_materials[mat_name] = 0
                total_materials[mat_name] += total_qty
        except Exception as e:
            print(f"Error reading line: {line.strip()} - Skipping.")

    print("\n=== Total Materials Needed ===")
    for mat, total in total_materials.items():
        print(f"{mat}: {total}")

def add_new_blueprints():
    print("\n=== Blueprint Types ===")
    blueprint_type_list = list(blueprint_types.keys())
    for idx, bp_type in enumerate(blueprint_type_list, 1):
        print(f"{idx}. {bp_type}")

    type_choice = input("\nSelect a blueprint type by number (or type 'back' to return to main menu): ")

    if type_choice.lower() == "back":
        return

    try:
        type_idx = int(type_choice) - 1
        selected_type = blueprint_type_list[type_idx]
    except (ValueError, IndexError):
        print("Invalid choice. Returning to main menu.")
        return

    final_items = blueprint_types[selected_type]
    print(f"\n=== Available Final Items in '{selected_type}' ===")
    final_item_list = list(final_items.keys())
    for idx, item_name in enumerate(final_item_list, 1):
        print(f"{idx}. {item_name}")

    item_choice = input("\nSelect the final item by number (or type 'back' to return): ")
    if item_choice.lower() == "back":
        return

    try:
        item_idx = int(item_choice) - 1
        item_name = final_item_list[item_idx]
    except (ValueError, IndexError):
        print("Invalid choice. Returning.")
        return

    materials = final_items[item_name]

    try:
        num_blueprints = int(input(f"\nHow many blueprints do you want to add for '{item_name}'? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for i in range(num_blueprints):
        print(f"\n--- Blueprint {i + 1} ---")
        try:
            usage_count = int(input(f"Usage Count (how many times this blueprint can be used)? "))
        except ValueError:
            print("Invalid number. Skipping this blueprint.")
            continue

        material_quantities = {}
        for material in materials:
            while True:
                try:
                    qty = int(input(f" - How many '{material}' per craft? "))
                    material_quantities[material] = qty
                    break
                except ValueError:
                    print("Please enter a valid number.")

        total_line_materials = {}
        for mat, qty in material_quantities.items():
            total_line_materials[mat] = qty * usage_count

        materials_str = ", ".join(f"{mat}:{qty}" for mat, qty in material_quantities.items())
        total_str = ", ".join(f"{mat}:{total}" for mat, total in total_line_materials.items())

        line = f"{item_name} | Usage: {usage_count} | Materials: {materials_str} | Total: {total_str}"

        append_line(line)
        print(f">> Blueprint saved: {line}")

def main():
    print(f"\n== Blueprint Tracker ==")

    while True:
        print("\n=== Main Menu ===")
        print("1. View Existing Blueprints")
        print("2. Delete a Blueprint")
        print("3. Add New Blueprints")
        print("4. View Total Materials Needed")
        print("5. Exit")

        option = input("\nSelect an option (1-5): ")

        if option == "1":
            show_existing_blueprints()

        elif option == "2":
            delete_blueprint()

        elif option == "3":
            add_new_blueprints()

        elif option == "4":
            calculate_total_materials()

        elif option == "5":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please select from 1 to 5.")

if __name__ == "__main__":
    main()
