StockFlow Backend Case Study
Overview
This project implements a backend system for StockFlow, a B2B inventory management platform. The system allows companies to manage products across multiple warehouses, track inventory levels, and generate low-stock alerts.
The implementation focuses on correctness, scalability, and production-oriented design rather than just functional completeness.
Part 1: Code Review and Debugging
Issues Identified
Missing Input Validation
The original implementation assumes all fields are present in the request body, which can lead to runtime errors.
No SKU Uniqueness Enforcement
Duplicate SKUs could be inserted, breaking product identity constraints.
Improper Transaction Handling
Separate commits for product and inventory creation can lead to inconsistent data if one operation fails.
Incorrect Data Modeling
Products were tied to a single warehouse, violating the requirement of multi-warehouse support.
Lack of Error Handling
Failures were not handled, potentially leaving the database in a partial state.
Price Precision Issues
Price handling did not enforce decimal precision, which is critical for financial data.
Fixes Implemented
Added request validation for required fields
Enforced SKU uniqueness at application level
Introduced transactional consistency using a single commit flow
Decoupled product from warehouse
Added structured error handling with rollback
Used Decimal for accurate price handling
Part 2: Database Design
Schema Overview
companies → stores organizations
warehouses → linked to companies
products → global product definition
inventory → junction table for product-warehouse mapping
suppliers → supplier information
product_suppliers → many-to-many relationship
inventory_logs → tracks stock changes
product_bundles → supports bundled products
Key Design Decisions
Multi-Warehouse Support
Inventory is modeled as a junction table between products and warehouses, enabling flexible storage across locations.
Data Integrity
Unique constraints and foreign keys ensure relational consistency.
Scalability
The schema supports growth in:
number of warehouses
products per company
supplier relationships
Missing Requirements Identified
Definition of recent sales activity
Rules for calculating stockout predictions
Supplier prioritization logic
Handling of reserved vs available inventory
Bundle pricing strategy
Part 3: Low Stock Alerts API
Endpoint
GET /api/companies/{company_id}/alerts/low-stock
Approach
Join inventory, products, and warehouses
Filter products below threshold
Ensure results are scoped to a company
Return structured alert data
Edge Cases Considered
Products without suppliers
Multiple warehouses per product
Missing or zero inventory
Empty result sets
Assumptions
SKU is globally unique
Low stock threshold is stored per product
Simplified logic used for stockout estimation
One supplier per product is sufficient for alerts
Project Structure
app/
  routes/
  models/
db/
docs/
seed.py
run.py
README.md
requirements.txt
How to Run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
Seeding Initial Data
python seed.py
Example API Usage
Create Product
POST /api/products
Get Low Stock Alerts
GET /api/companies/{company_id}/alerts/low-stock
Future Improvements
Add authentication and authorization
Introduce caching for alert queries
Implement asynchronous processing for inventory updates
Add demand forecasting for better stock predictions
Conclusion
This implementation focuses on building a reliable and scalable backend system that reflects real-world inventory management challenges. The design prioritizes data consistency, extensibility, and clarity in handling incomplete requirements.