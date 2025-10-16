from app.db.session import SessionLocal
from app.models import Node


def main():
    db = SessionLocal()
    try:
        # Count root-level nodes (those with parent_id = NULL)
        count_root = db.query(Node).filter(Node.parent_id.is_(None)).count()
        print(f"Root-level nodes: {count_root}")

        # Optionally check total nodes
        total = db.query(Node).count()
        print(f"Total nodes in DB: {total}")

        # Print a few examples
        rows = db.query(Node).filter(Node.parent_id.is_(None)).limit(5).all()
        for n in rows:
            print(f"[{n.id}] {n.name} | share_id={n.share_id} | parent_id={n.parent_id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
