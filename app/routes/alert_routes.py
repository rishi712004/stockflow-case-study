from sqlalchemy import text
from flask import Blueprint, jsonify
from app import db

alert_bp = Blueprint('alerts', __name__)

@alert_bp.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    try:
        results = db.session.execute(text("""
            SELECT 
                p.id,
                p.name,
                p.sku,
                i.quantity,
                p.low_stock_threshold
            FROM inventory i
            JOIN product p ON p.id = i.product_id
            JOIN warehouse w ON w.id = i.warehouse_id
            WHERE w.company_id = :company_id
            AND i.quantity < p.low_stock_threshold
        """), {"company_id": company_id})

        alerts = []
        for row in results:
            alerts.append({
                "product_id": row.id,
                "product_name": row.name,
                "sku": row.sku,
                "current_stock": row.quantity,
                "threshold": row.low_stock_threshold
            })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500