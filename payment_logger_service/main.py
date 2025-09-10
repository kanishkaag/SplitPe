from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from payment_logger_service import models, database, schemas, rabbitmq

app = FastAPI(title="Payment Logger Service")

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/orders")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Idempotency check
    existing_order = db.query(models.Order).filter(
        (models.Order.idempotency_key == order.idempotency_key) |
        (models.Order.order_id == order.order_id)
    ).first()

    if existing_order:
        raise HTTPException(status_code=400, detail="Order already exists")

    new_order = models.Order(
        idempotency_key=order.idempotency_key,
        order_id=order.order_id,
        total_amount=order.total_amount,
        split_status=False
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Publish to RabbitMQ
    rabbitmq.publish_message({
        "event": "order.recorded",
        "order_id": new_order.order_id,
        "total_amount": str(new_order.total_amount),
        "idempotency_key": new_order.idempotency_key
    })

    return {"status": "success", "order_id": new_order.order_id}
