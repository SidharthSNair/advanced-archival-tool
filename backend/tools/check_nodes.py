from app.db.session import SessionLocal
from app.models import Node

def check_nodes(limit=10):
    db = SessionLocal()
    try:
        print(f"{'ID':<5} {'IS_DIR':<7} {'NAME':<20} PATH")
        print("-" * 60)
        for node in db.query(Node).limit(limit).all():
            print(f"{node.id:<5} {str(node.is_dir):<7} {node.name:<20} {node.path}")
    finally:
        db.close()

if __name__ == "__main__":
    check_nodes(20)
