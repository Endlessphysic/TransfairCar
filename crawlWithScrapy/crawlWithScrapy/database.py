import sqlite3

conn = sqlite3.connect('myOrders.db')
curr = conn.cursor()

# curr.execute("""create table orders_tb(
#                 price text,
#                 start text,
#                 destination text
#                 )""")

curr.execute("""insert into myOrders values """)

conn.commit()
conn.close()