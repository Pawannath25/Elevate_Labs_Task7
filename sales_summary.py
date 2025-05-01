import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS sales")

cursor.execute('''
    CREATE TABLE sales (
        product TEXT,
        quantity INTEGER,
        price REAL
    )
''')

sample_sales = [
    ('Product A', 10, 15),
    ('Product A', 5, 15),
    ('Product B', 3, 20),
    ('Product B', 7, 20),
    ('Product C', 2, 25)
]
cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", sample_sales)
conn.commit()

query = """
    SELECT 
        product, 
        SUM(quantity) AS total_qty, 
        SUM(quantity * price) AS revenue 
    FROM sales 
    GROUP BY product
"""

df = pd.read_sql_query(query, conn)

print("Sales Summary:")
print(df.to_string(index=False))

df.plot(kind='bar', x='product', y='revenue', legend=False)
plt.title('Total Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('sales_chart.png')
plt.show()

conn.close()