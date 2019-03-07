class ItemsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS items 
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     item_name VARCHAR(50),
                                     item_image VARCHAR(400),
                                     item_price VARCHAR(10),
                                     item_info VARCHAR(500),
                                     item_count VARCHAR(9)
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, image, price, info, count):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO items 
                                  (item_name, item_image, item_price, item_info, item_count) 
                                  VALUES (?,?,?,?,?)''', (name, image, str(price), info, str(count)))
        cursor.close()
        self.connection.commit()

    def get(self, item_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (str(item_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        return rows

    def delete(self, item_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM items WHERE id = ?''', (str(item_id)))
        cursor.close()
        self.connection.commit()

    def edit(self, argument, value, item_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE items SET ? = ?
                          WHERE item_id=?''', (argument, value, item_id))
