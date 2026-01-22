import sqlite3

class ShipmentProcessor:
    def __init__(self, db_path):
        self.db_path = db_path

    def process_shipment(self, item_name, quantity, log_callback):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
    
        try:
            cursor.execute(
                "UPDATE inventory SET stock_qty = stock_qty - ? WHERE item_name = ?",
                (quantity, item_name)
            )
    
            cursor.execute(
                "INSERT INTO shipment_log (item_name, qty_moved) VALUES (?, ?)",
                (item_name, quantity)
            )
    
            conn.commit()
            log_callback(">> TRANSACTION SUCCESSFUL")
    
        except Exception as e:
            conn.rollback()
            log_callback(f">> TRANSACTION FAILED: {e}")
    
        finally:
            conn.close()
    