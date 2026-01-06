# consumes wallet credit events, updates balances, and exposes party & payout APIs
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import threading
from sqlalchemy.orm import Session
from wallet_service import models, database, rabbitmq, schemas

app = FastAPI(title="Wallet Credit Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Ensure tables exist
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def handle_wallet_credit(message: dict):
    print(f"Received wallet.credit.requested: {message}")

    db: Session = database.SessionLocal()
    try:
        #  Update Party balance
        party = db.query(models.Party).filter(models.Party.party_id == message["party_id"]).first()
        if not party:
            print(f"Party {message['party_id']} not found in DB!")
            return

        party.total_amount += float(message["amount"])
        db.commit()
        print(f"Updated Party {party.party_id}: +{message['amount']} (New total: {party.total_amount})")

        #  Log split history
        new_split = models.Split(
            party_id=message["party_id"],
            order_id=message["order_id"],
            amount=float(message["amount"])
        )
        db.add(new_split)
        db.commit()
        print(f"Logged split record: {new_split.party_id} <- {new_split.amount}")

        # Mark Order as split complete
        order = db.query(models.Order).filter(models.Order.order_id == message["order_id"]).first()
        if order:
            order.split_status = 1  # True
            db.commit()
            print(f"Order {order.order_id} marked as split_status=True")
        else:
            print(f"Order {message['order_id']} not found in DB!")

    finally:
        db.close()

# Start RabbitMQ consumer in background
def start_consumer():
    rabbitmq.consume_wallet_credit(handle_wallet_credit)

threading.Thread(target=start_consumer, daemon=True).start()

@app.get("/")
def root():
    return {"status": "Wallet Credit Service running"}

#  Create new Party
@app.post("/parties", response_model=schemas.PartyResponse)
def create_party(party: schemas.PartyCreate, db: Session = Depends(get_db)):
    db_party = models.Party(
        party_id=party.party_id,
        party_name=party.party_name,
        split_rule=party.split_rule,
        total_amount=0.0
    )
    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    return db_party

#  Create multiple Parties
@app.post("/parties/bulk", response_model=list[schemas.PartyResponse])
def create_parties(parties: list[schemas.PartyCreate], db: Session = Depends(get_db)):
    db_parties = []
    for party in parties:
        db_party = models.Party(
            party_id=party.party_id,
            party_name=party.party_name,
            split_rule=party.split_rule,
            total_amount=0.0
        )
        db.add(db_party)
        db_parties.append(db_party)

    db.commit()

    # Refresh all parties
    for db_party in db_parties:
        db.refresh(db_party)

    return db_parties    

#  Get all Parties
@app.get("/parties", response_model=list[schemas.PartyResponse])
def get_parties(db: Session = Depends(get_db)):
    return db.query(models.Party).all()

#  Get all Split Records
@app.get("/splits", response_model=list[schemas.SplitResponse])
def get_splits(db: Session = Depends(get_db)):
    return db.query(models.Split).all()

# Payout Endpoint - Reset all party balances to zero
@app.post("/wallet/payout")
def payout_all_parties(db: Session = Depends(get_db)):
    parties = db.query(models.Party).all()
    if not parties:
        raise HTTPException(status_code=404, detail="No parties found")

    settled_parties = []
    for party in parties:
        if party.total_amount > 0:
            settled_parties.append({
                "party_id": party.party_id,
                "party_name": party.party_name,
                "settled_amount": party.total_amount
            })
            party.total_amount = 0.0
            db.add(party)

    db.commit()

    return {
        "message": "Payout completed. All balances reset to zero.",
        "settled_parties": settled_parties
    }
