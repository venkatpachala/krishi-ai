from ..db import SessionLocal, init_db
from ..models import Officer

def main():
    init_db()
    db = SessionLocal()
    officers = [
        Officer(name="Officer A", phone="1111", lat=17.4, lon=78.5),
        Officer(name="Officer B", phone="2222", lat=17.3, lon=78.4),
        Officer(name="Officer C", phone="3333", lat=17.2, lon=78.3),
    ]
    db.add_all(officers)
    db.commit()

if __name__ == "__main__":
    main()
