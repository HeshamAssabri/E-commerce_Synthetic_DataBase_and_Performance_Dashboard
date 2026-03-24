# E‑commerce Performance Dashboard

## 📊 Overview
This project simulates a full e‑commerce business using synthetic data. It includes a MySQL database with orders, customers, products, employees, and reviews, and an interactive dashboard built in Looker Studio to analyze business performance.

## 🔧 Tools & Technologies
- **MySQL** – database design and queries
- **Python (Faker)** – synthetic data generation
- **Looker Studio** – dashboard and visualizations

## 📁 Repository Contents
- `generate_ecommerce_data.py` – Python script to generate 1,200 orders, 55 products, 20 employees, 250 customers, and 400+ reviews.
- `ecommerce_data.sql` – SQL file containing all `INSERT` statements to populate the database.
- `schema.sql` – SQL script to create all tables (employees, customers, products, orders, order_items, reviews).
- `dashboard_link.txt` – Link to the interactive Looker Studio dashboard (or note that it can be shared upon request).
- `screenshots/` – Images of the dashboard pages.

## 📈 Dashboard Pages
1. **Executive Dashboard** – high‑level KPIs, revenue trends, top products, order status.
2. **Product & Profitability** – profit by category, product‑level profit, discount impact.
3. **Customer & Employee Insights** – top customers, sales rep performance, repeat rate, geographic distribution.

## 💡 Key Insights
- Top 10 products account for 45% of total revenue.
- Clothing category has the highest profit margin (18% vs. 9.6% overall).
- 35% of customers are repeat buyers.
- The top sales rep handles 20% of all orders.

## 🚀 How to Recreate
1. Run `schema.sql` in MySQL to create the database.
2. Run `generate_data.py` to insert synthetic data.
3. Connect Looker Studio to your MySQL database (use ngrok if local).
4. Build dashboards using the provided custom SQL query or design your own.

## 📫 Contact
https://www.linkedin.com/in/hesham-assabri-34530b1a1/

hesham.assabri@gmail.com

## 🔗 Live Dashboard
https://lookerstudio.google.com/reporting/9c69d64b-1708-4a32-8a24-e975a5d8a256
