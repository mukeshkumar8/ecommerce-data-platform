import psycopg2
import pandas as pd
import logging
import os
from dotenv import load_dotenv


# ==========================================
# 1. ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# ==========================================
# 2. LOGGING SETUP
# ==========================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("==========================================")
logger.info("ETL process started")
logger.info("==========================================")


# ==========================================
# 3. DATABASE CONNECTION
# ==========================================

conn = None

try:

    logger.info("Connecting to PostgreSQL database...")

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    logger.info("Database connection successful")
    print("Database connection successful!")


    # ==========================================
    # 4. READ DATA FROM POSTGRESQL
    # ==========================================

    logger.info("Reading customers table...")

    customers = pd.read_sql(
        "SELECT * FROM customers",
        conn
    )

    logger.info(f"Customers records loaded: {len(customers)}")
    print(f"Customers loaded: {len(customers)}")


    logger.info("Reading products table...")

    products = pd.read_sql(
        "SELECT * FROM products",
        conn
    )

    logger.info(f"Products records loaded: {len(products)}")
    print(f"Products loaded: {len(products)}")


    logger.info("Reading orders table...")

    orders = pd.read_sql(
        "SELECT * FROM orders",
        conn
    )

    logger.info(f"Orders records loaded: {len(orders)}")
    print(f"Orders loaded: {len(orders)}")


    logger.info("Reading order_items table...")

    order_items = pd.read_sql(
        "SELECT * FROM order_items",
        conn
    )

    logger.info(f"Order items records loaded: {len(order_items)}")
    print(f"Order items loaded: {len(order_items)}")


    logger.info("Reading payments table...")

    payments = pd.read_sql(
        "SELECT * FROM payments",
        conn
    )

    logger.info(f"Payments records loaded: {len(payments)}")
    print(f"Payments loaded: {len(payments)}")


    # ==========================================
    # 5. DATA CLEANING
    # ==========================================

    logger.info("Starting data cleaning...")


    # Customers
    customers["first_name"] = customers["first_name"].str.strip()
    customers["last_name"] = customers["last_name"].fillna("")
    customers["email"] = customers["email"].str.strip().str.lower()
    customers["city"] = customers["city"].str.strip()

    logger.info("Customers cleaning completed")


    # Products
    products["product_name"] = products["product_name"].str.strip()
    products["category"] = products["category"].str.strip()

    products["price"] = pd.to_numeric(
        products["price"],
        errors="coerce"
    )

    products["stock_quantity"] = pd.to_numeric(
        products["stock_quantity"],
        errors="coerce"
    )

    logger.info("Products cleaning completed")


    # Orders
    orders["total_amount"] = pd.to_numeric(
        orders["total_amount"],
        errors="coerce"
    )

    orders["status"] = orders["status"].str.strip()

    logger.info("Orders cleaning completed")


    # Order Items
    order_items["quantity"] = pd.to_numeric(
        order_items["quantity"],
        errors="coerce"
    )

    order_items["unit_price"] = pd.to_numeric(
        order_items["unit_price"],
        errors="coerce"
    )

    logger.info("Order items cleaning completed")


    # Payments
    payments["amount"] = pd.to_numeric(
        payments["amount"],
        errors="coerce"
    )

    payments["payment_method"] = payments[
        "payment_method"
    ].str.strip()

    payments["payment_status"] = payments[
        "payment_status"
    ].str.strip()

    logger.info("Payments cleaning completed")


    # ==========================================
    # 6. DUPLICATE CHECK
    # ==========================================

    logger.info("Checking duplicate records...")


    customer_duplicates = customers.duplicated().sum()
    product_duplicates = products.duplicated().sum()
    order_duplicates = orders.duplicated().sum()
    order_item_duplicates = order_items.duplicated().sum()
    payment_duplicates = payments.duplicated().sum()


    logger.info(
        f"Duplicate records - Customers: {customer_duplicates}, "
        f"Products: {product_duplicates}, "
        f"Orders: {order_duplicates}, "
        f"Order Items: {order_item_duplicates}, "
        f"Payments: {payment_duplicates}"
    )


    # Remove duplicates

    customers = customers.drop_duplicates()
    products = products.drop_duplicates()
    orders = orders.drop_duplicates()
    order_items = order_items.drop_duplicates()
    payments = payments.drop_duplicates()


    logger.info("Duplicate handling completed")


    # ==========================================
    # 7. INVALID DATA CHECK
    # ==========================================

    logger.info("Checking invalid data...")


    invalid_products = products[
        (products["price"] <= 0) |
        (products["stock_quantity"] < 0)
    ]

    invalid_orders = orders[
        orders["total_amount"] < 0
    ]

    invalid_order_items = order_items[
        (order_items["quantity"] <= 0) |
        (order_items["unit_price"] < 0)
    ]

    invalid_payments = payments[
        payments["amount"] < 0
    ]


    logger.info(
        f"Invalid products: {len(invalid_products)}"
    )

    logger.info(
        f"Invalid orders: {len(invalid_orders)}"
    )

    logger.info(
        f"Invalid order items: {len(invalid_order_items)}"
    )

    logger.info(
        f"Invalid payments: {len(invalid_payments)}"
    )


    # ==========================================
    # 8. ORDER AMOUNT VALIDATION
    # ==========================================

    logger.info("Starting order amount validation...")


    order_items["calculated_amount"] = (
        order_items["quantity"] *
        order_items["unit_price"]
    )


    order_totals = (
        order_items
        .groupby("order_id")["calculated_amount"]
        .sum()
        .reset_index()
    )


    order_validation = orders.merge(
        order_totals,
        on="order_id",
        how="left"
    )


    order_validation["calculated_amount"] = (
        order_validation["calculated_amount"]
        .fillna(0)
    )


    order_validation["difference"] = (
        order_validation["total_amount"] -
        order_validation["calculated_amount"]
    )


    order_mismatches = order_validation[
        order_validation["difference"].abs() > 0.01
    ]


    logger.info(
        f"Order amount mismatches found: "
        f"{len(order_mismatches)}"
    )


    # ==========================================
    # 9. PAYMENT VALIDATION
    # ==========================================

    logger.info("Starting payment validation...")


    payment_totals = (
        payments
        .groupby("order_id")["amount"]
        .sum()
        .reset_index()
    )


    payment_validation = orders.merge(
        payment_totals,
        on="order_id",
        how="left"
    )


    payment_validation["amount"] = (
        payment_validation["amount"]
        .fillna(0)
    )


    payment_validation["payment_difference"] = (
        payment_validation["total_amount"] -
        payment_validation["amount"]
    )


    payment_mismatches = payment_validation[
        payment_validation["payment_difference"].abs() > 0.01
    ]


    logger.info(
        f"Payment mismatches found: "
        f"{len(payment_mismatches)}"
    )


    # ==========================================
    # 10. CUSTOMER REPORT
    # ==========================================

    logger.info("Creating customer report...")


    customer_order_report = customers.merge(
        orders,
        on="customer_id",
        how="left"
    )


    customer_order_report = customer_order_report[
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "city",
            "order_id",
            "order_date",
            "total_amount",
            "status"
        ]
    ]


    logger.info("Customer report created")


    # ==========================================
    # 11. CUSTOMER SPENDING REPORT
    # ==========================================

    logger.info("Creating customer spending report...")


    customer_spending = (
        orders
        .groupby("customer_id")["total_amount"]
        .sum()
        .reset_index()
    )


    customer_spending = customer_spending.merge(
        customers[
            [
                "customer_id",
                "first_name",
                "last_name",
                "city"
            ]
        ],
        on="customer_id",
        how="left"
    )


    customer_spending = customer_spending[
        [
            "customer_id",
            "first_name",
            "last_name",
            "city",
            "total_amount"
        ]
    ]


    customer_spending = customer_spending.sort_values(
        "total_amount",
        ascending=False
    )


    logger.info("Customer spending report created")


    # ==========================================
    # 12. PRODUCT SALES REPORT
    # ==========================================

    logger.info("Creating product sales report...")


    product_sales = order_items.merge(
        products[
            [
                "product_id",
                "product_name",
                "category"
            ]
        ],
        on="product_id",
        how="left"
    )


    product_sales["sales_amount"] = (
        product_sales["quantity"] *
        product_sales["unit_price"]
    )


    product_sales_report = (
        product_sales
        .groupby(
            [
                "product_id",
                "product_name",
                "category"
            ]
        )
        .agg(
            total_quantity=("quantity", "sum"),
            total_sales=("sales_amount", "sum")
        )
        .reset_index()
    )


    product_sales_report = product_sales_report.sort_values(
        "total_sales",
        ascending=False
    )


    logger.info("Product sales report created")


    # ==========================================
    # 13. CATEGORY SALES REPORT
    # ==========================================

    logger.info("Creating category sales report...")


    category_sales_report = (
        product_sales
        .groupby("category")["sales_amount"]
        .sum()
        .reset_index()
    )


    category_sales_report = category_sales_report.sort_values(
        "sales_amount",
        ascending=False
    )


    logger.info("Category sales report created")


    # ==========================================
    # 14. DATA QUALITY REPORT
    # ==========================================

    logger.info("Creating data quality report...")


    data_quality_report = pd.DataFrame({
        "table": [
            "customers",
            "products",
            "orders",
            "order_items",
            "payments"
        ],
        "total_records": [
            len(customers),
            len(products),
            len(orders),
            len(order_items),
            len(payments)
        ],
        "duplicate_records": [
            customer_duplicates,
            product_duplicates,
            order_duplicates,
            order_item_duplicates,
            payment_duplicates
        ]
    })


    logger.info("Data quality report created")


    # ==========================================
    # 15. EXPORT CLEANED DATA
    # ==========================================

    logger.info("Exporting cleaned datasets...")


    os.makedirs("data/cleaned", exist_ok=True)


    customers.to_csv(
        "data/cleaned/customers_cleaned.csv",
        index=False
    )

    products.to_csv(
        "data/cleaned/products_cleaned.csv",
        index=False
    )

    orders.to_csv(
        "data/cleaned/orders_cleaned.csv",
        index=False
    )

    order_items.to_csv(
        "data/cleaned/order_items_cleaned.csv",
        index=False
    )

    payments.to_csv(
        "data/cleaned/payments_cleaned.csv",
        index=False
    )


    logger.info("Cleaned datasets exported")


    # ==========================================
    # 16. EXPORT REPORTS
    # ==========================================

    logger.info("Exporting reports...")


    os.makedirs("data/reports", exist_ok=True)


    data_quality_report.to_csv(
        "data/reports/data_quality_report.csv",
        index=False
    )

    order_mismatches.to_csv(
        "data/reports/order_amount_mismatches.csv",
        index=False
    )

    payment_mismatches.to_csv(
        "data/reports/payment_mismatches.csv",
        index=False
    )

    customer_order_report.to_csv(
        "data/reports/customer_order_report.csv",
        index=False
    )

    customer_spending.to_csv(
        "data/reports/customer_spending_report.csv",
        index=False
    )

    product_sales_report.to_csv(
        "data/reports/product_sales_report.csv",
        index=False
    )

    category_sales_report.to_csv(
        "data/reports/category_sales_report.csv",
        index=False
    )


    logger.info("Reports exported successfully")


    # ==========================================
    # 17. FINAL SUCCESS MESSAGE
    # ==========================================

    logger.info("==========================================")
    logger.info("ETL process completed successfully")
    logger.info("==========================================")


    print()
    print("==========================================")
    print("ETL process completed successfully!")
    print("==========================================")
    print()
    print("Cleaned datasets exported to:")
    print("data/cleaned/")
    print()
    print("Reports exported to:")
    print("data/reports/")
    print()
    print("Log file:")
    print("logs/etl.log")


except Exception as e:

    # ==========================================
    # ERROR HANDLING
    # ==========================================

    logger.exception("ETL process failed")

    print()
    print("==========================================")
    print("ETL process failed!")
    print("==========================================")
    print(f"Error: {e}")
    print()
    print("Check logs/etl.log for detailed error information.")


finally:

    # ==========================================
    # DATABASE CONNECTION CLOSE
    # ==========================================

    if conn is not None and not conn.closed:

        conn.close()

        logger.info("Database connection closed")

        print("Database connection closed.")