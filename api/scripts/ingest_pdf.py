import pathlib
import argparse
from ..db import SessionLocal, init_db
from ..rag import add_document

def main(path: str):
    init_db()
    db = SessionLocal()
    p = pathlib.Path(path)
    content = p.read_text()
    add_document(db, title=p.stem, source=p.name, content=content)
    print("ingested", p)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    main(args.path)
