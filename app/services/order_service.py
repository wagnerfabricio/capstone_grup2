from dataclasses import asdict

from flask import current_app
from sqlalchemy.orm import Session, Query
from app.models import Order, OrderStatus, OrderPayment,UserModel
from app.models.order_product_model import OrderProduct


def retrieve_orders_admin():
    session: Session = current_app.db.session

    orders = session.query(Order).all()

    list_orders = []
    for order in orders:
        mapped_order = {**asdict(order), "user": order.user, "total": order.total}
        list_orders.append(mapped_order)

    return list_orders


def retrieve_orders_detail(id):
    """
    SELECT
        u."name",u."email",
        p."name",p."price",
        o."total",
        os."type",
        opy."payment",
        op."product_quantity"
    FROM orders o
    JOIN orders_products op
        ON o.id = op.order_id
    JOIN orders_status os
        on os.id = o.status_id
    JOIN orders_payments opy
        on opy.id = o.payment_id
    JOIN products p
        ON p.id = op.product_id
    WHERE
        o.id = {id}
    """

    session = current_app.db.session

    query: Query = (
        session.query(
            "Product".id,
            "Product".name,
            OrderProduct.total,
            OrderProduct.product_quantity,
            Order.id,
            Order.total,
            OrderStatus.type,
            OrderPayment.type,
            OrderPayment.status,
        )
        .select_from(Order)
        .join(OrderProduct)
        .join(OrderStatus)
        .join(OrderPayment)
        .join("Product")
        .filter(Order.id == id)
        .first()
    )

    # response = [item._asdict() for item in query]

    return query


def retrieve_orders_user():
    session: Session = current_app.db.session

    orders = session.query(Order).all()

    list_orders = [{**asdict(order), "payment": order.payment} for order in orders]

    return list_orders
