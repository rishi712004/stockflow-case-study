from app import create_app, db
from app.models.models import Company, Warehouse

app = create_app()

with app.app_context():
    company = Company(name="Demo Company")
    db.session.add(company)
    db.session.commit()

    warehouse = Warehouse(name="Main Warehouse", company_id=company.id)
    db.session.add(warehouse)
    db.session.commit()

    print("Company ID:", company.id)
    print("Warehouse ID:", warehouse.id)