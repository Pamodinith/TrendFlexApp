from services.inventory_service import InventoryService

class AddItemViewModel:
    def __init__(self):
        self.service = InventoryService()

    def add_item(self, item_data):
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

        success = self.service.add_item_to_db(
            item_data["code"],
            item_data["name"],
            item_data["desc"],
            price,
            sizes
        )
        return (True, "Item added successfully.") if success else (False, "Item code already exists.")
