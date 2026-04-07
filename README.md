# StockFlow Backend Case Study

## Overview
This project implements a backend system for StockFlow, a B2B inventory management platform designed to help companies manage products across multiple warehouses and maintain supplier relationships.

The solution focuses on building a system that is consistent, scalable, and aligned with real-world production constraints rather than just being functionally correct.

## Approach
The problem was approached in three stages:

1. Identifying and fixing correctness and reliability issues in the existing API  
2. Designing a scalable database schema for multi-warehouse inventory  
3. Implementing a business-critical API for low-stock alerts  

Special attention was given to data consistency, system design, and handling incomplete requirements.

## Part 1: Code Review and Debugging

### Key Issues Identified

#### Lack of Input Validation
The original implementation assumed all required fields were present, leading to potential runtime failures.

#### No SKU Uniqueness Enforcement
Duplicate SKUs could be created, breaking product identity and downstream processes.

#### Non-Atomic Database Operations
Separate commits for product and inventory creation could leave the system in an inconsistent state.

#### Incorrect Data Modeling
Products were incorrectly tied to a single warehouse, limiting scalability.

#### Missing Error Handling
Failures were not handled, increasing the risk of partial writes and instability.

#### Improper Price Handling
Price values were not handled with proper precision.

### Fixes Implemented

- Added validation for required fields  
- Enforced SKU uniqueness  
- Introduced transactional integrity using a single commit flow  
- Decoupled product from warehouse  
- Added structured error handling with rollback  
- Used Decimal for price accuracy  

## Part 2: Database Design

### Schema Overview

- companies – represents organizations using the platform  
- warehouses – multiple per company  
- products – global product definitions  
- inventory – maps products to warehouses with quantities  
- suppliers – supplier details  
- product_suppliers – many-to-many relationship  
- inventory_logs – tracks stock changes  
- product_bundles – supports composite products  

### Key Design Decisions

#### Separation of Product and Inventory
Products are independent entities, while inventory tracks their presence across warehouses.  
This enables multi-warehouse scalability and avoids duplication.

#### Use of Junction Table for Inventory
A structured relationship ensures each product-warehouse combination is unique and consistent.

#### Data Integrity and Constraints
Foreign keys and unique constraints are used to maintain relational consistency.

#### Extensibility
The schema supports future enhancements such as:
- advanced supplier logic  
- inventory reservations  
- demand forecasting  

### Gaps and Assumptions

During design, several ambiguities were identified:

- Definition of “recent sales activity”  
- Logic for stockout prediction  
- Supplier prioritization rules  
- Handling reserved vs available inventory  

Assumptions were made and documented to proceed with implementation.

## Part 3: Low Stock Alerts API

### Endpoint

GET /api/companies/{company_id}/alerts/low-stock


### Implementation Strategy

- Joined inventory, product, and warehouse data  
- Filtered products below their threshold  
- Scoped results to a specific company  
- Returned structured alert data  

### Key Considerations

- Supports multiple warehouses per company  
- Ensures only relevant company data is returned  
- Designed to be extensible for future business rules  

### Edge Cases Handled

- Products without inventory  
- Empty result sets  
- Missing or default thresholds  
- Multiple warehouse entries per product  

## Project Structure
app/
routes/
models/
db/
docs/
seed.py
run.py
README.md
requirements.txt
.gitignore

## How to Run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

## Seeding Initial Data
python seed.py


## Example API Usage

### Create Product
POST /api/products

### Get Low Stock Alerts
GET /api/companies/{company_id}/alerts/low-stock

## Design Trade-offs

- Used raw SQL for alert queries to maintain clarity and control over joins  
- Simplified business logic due to incomplete requirements  
- Focused on correctness and structure over premature optimization  

## Future Improvements

- Add authentication and authorization  
- Introduce caching (e.g., Redis) for alert queries  
- Implement asynchronous processing for inventory updates  
- Add demand forecasting for smarter stock predictions  

---

## Conclusion

This implementation prioritizes building a backend system that reflects real-world requirements, emphasizing data integrity, scalability, and thoughtful handling of ambiguity. The goal was to design a system that can evolve realistically in a production environment.