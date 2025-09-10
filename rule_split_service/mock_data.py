from .models import Party
from .database import SessionLocal
from datetime import date

def insert_mock_data():
    db = SessionLocal()
    if db.query(Party).count() == 0:
        parties = [
            Party(party_id="P1", party_name="Merchant A", split_rule="50%", total_amount=0, date=date.today()),
            Party(party_id="P2", party_name="Partner B", split_rule="30%", total_amount=0, date=date.today()),
            Party(party_id="P3", party_name="Platform C", split_rule="20%", total_amount=0, date=date.today()),
        ]
        db.add_all(parties)
        db.commit()
        print(" Mock parties inserted")
    db.close()
