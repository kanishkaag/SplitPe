from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import threading
from rule_split_service import models, database, schemas, rabbitmq, mock_data

app = FastAPI(title="Rule Splitter Service")

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Insert mock data
# mock_data.insert_mock_data()

# Dependency for DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/parties", response_model=list[schemas.PartyResponse])
def get_parties(db: Session = Depends(get_db)):
    return db.query(models.Party).all()

def handle_order_recorded(message: dict):
    print(f"Received order.recorded: {message}")
    order_id = message["order_id"]
    amount = float(message["total_amount"])

    db = database.SessionLocal()
    parties = db.query(models.Party).all()

    # Logic for splitting
    total_split = 0
    last_party = parties[-1]

    for party in parties:
        if party == last_party:
            split_amount = round(amount - total_split, 2)
        else:
            if "%" in party.split_rule:
                percent = float(party.split_rule.replace("%", ""))
                split_amount = round(amount * (percent / 100), 2)
            else:
                split_amount = round(float(party.split_rule), 2)
        total_split += split_amount
      
        split_event = {
            "party_id": party.party_id,
            "amount": split_amount,
            "order_id": order_id
        }
        rabbitmq.publish_wallet_credit(split_event)
        print(f"Published wallet.credit.requested: {split_event}")

    db.close()

# Start RabbitMQ consumer in background
def start_consumer():
    rabbitmq.consume_order_recorded(handle_order_recorded)

threading.Thread(target=start_consumer, daemon=True).start()
