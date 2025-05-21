from services.inventory_service import InventoryService

class InventoryViewModel:
    def __init__(self):
        self.service = InventoryService()

    def get_all_items(self):
        return self.service.fetch_all_items()

    def delete_item(self, item_code):
        return self.service.delete_item_from_db(item_code)
