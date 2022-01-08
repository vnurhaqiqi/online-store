from app import db
from datetime import datetime
import calendar


def calculate_safety_stock():
    # get first day of month then formatted
    get_first_day_of_month = datetime.today().replace(day=1)
    first_day_of_month = datetime.strftime(get_first_day_of_month, "%Y-%m-%d 00:00:00")

    # get last day of month then formatted
    get_last_day_of_month = datetime.today().replace(
        day=calendar.monthrange(datetime.today().year, datetime.today().month)[1])
    last_day_of_month = datetime.strftime(get_last_day_of_month, "%Y-%m-%d 23:59:59")

    """
        query to get ordered products current month
        table joined (product, order and order_detail)
        filter by (product status, order status and order_date)
        
        purpose:
            get ordered products data such as maximum quantity ordered, average quantity ordered, 
            most_lead_time and lead_time.
    """
    # ==== start getting data ====
    sql_script = """
        select p.id, p.name, p.quantity as available_quantity, 
               max(od.quantity) as max_quantity_ordered,
               avg(od.quantity) as avg_quantity_ordered,
               p.most_lead_time,
               p.lead_time
        from products p
                 join order_details od on p.id = od.product_id
                 join orders o on od.order_id = o.id
        where p.status = 1
          and o.status in ("checkout", "payment_confirmed") 
          and o.order_date between '{first_day}' and '{last_day}'
        group by p.id;
    """.format(first_day=first_day_of_month, last_day=last_day_of_month)

    query_execute = db.session.execute(sql_script)
    ordered_products = query_execute.fetchall()
    # ==== end getting data ====

    # calculate safety stock
    # formula: (max ordered quantity * max lead time) - (avg ordered quantity * lead time)
    safety_stock_list = []
    for product in ordered_products:
        safety_stock = (product.max_quantity_ordered * product.most_lead_time) - (
                int(product.avg_quantity_ordered) * product.lead_time)

        safety_stock_list.append({
            "product_id": product.id,
            "name": product.name,
            "available_quantity": product.available_quantity,
            "safety_stock": safety_stock
        })

    return safety_stock_list
