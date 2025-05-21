from services.inventory_service import InventoryService

class EditItemViewModel:
    def __init__(self):
        self.service = InventoryService()

    def get_item_by_code(self, code):
        item = self.service.fetch_item_details(code)
        if not item:
            return None

        # Group sizes and quantities
        sizes = {}
        for size, qty in item["sizes"]:
            sizes[size] = qty

        return {
            "item_code": item["item_code"],
            "name": item["name"],
            "description": item["description"],
            "price": item["price"],
            "sizes": sizes
        }

    def update_item(self, item_data):
        try:
            price = float(item_data["price"])
            sizes = {
                size: int(qty) if qty else 0
                for size, qty in item_data["sizes"].items()
            }
        except ValueError:
            return False, "Price and quantities must be numbers."

        if not item_data["code"] or not item_data["name"]:
            return False, "Item code and name are required."

        success = self.service.update_item_in_db(
            item_data["code"],
            item_data["name"],
            item_data["desc"],
            price,
            sizes
        )
        return (True, "Item updated successfully.") if success else (False, "Failed to update item.")
