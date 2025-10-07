import os
from datetime import datetime
from pathlib import Path

from app.db.session import SessionLocal
from app.models import Node, Share

def crawl_share(share_id: int, root_path: str):
    """
    Crawl the given directory path and insert nodes into DB under share_id.
    root_path can be a UNC path (\\server\share) or local path (for dev).
    """
    db = SessionLocal()
    try:
        # Cleanup old nodes for this share
        db.query(Node).filter(Node.share_id == share_id).delete()
        db.commit()

        inserted = 0
        parent_map = {}  # path → id

        def add_node(name, path, is_dir, size, modified_at, parent_id):
            nonlocal inserted
            node = Node(
                name=name,
                path=path,
                is_dir=is_dir,
                size=size,
                modified_at=modified_at,
                parent_id=parent_id,
                share_id=share_id,
            )
            db.add(node)
            db.flush()  # assign id
            inserted += 1
            return node.id

        # Walk recursively using scandir
        def walk_dir(dir_path: str, parent_id=None):
            try:
                with os.scandir(dir_path) as it:
                    for entry in it:
                        try:
                            stat = entry.stat(follow_symlinks=False)
                            node_id = add_node(
                                name=entry.name,
                                path=str(Path(entry.path)),
                                is_dir=entry.is_dir(follow_symlinks=False),
                                size=stat.st_size if entry.is_file() else 0,
                                modified_at=datetime.fromtimestamp(stat.st_mtime),
                                parent_id=parent_id,
                            )
                            if entry.is_dir(follow_symlinks=False):
                                walk_dir(entry.path, parent_id=node_id)
                        except PermissionError:
                            print(f"⚠️ Skip permission denied: {entry.path}")
            except FileNotFoundError:
                print(f"⚠️ Path not found: {dir_path}")

        # Start walk
        walk_dir(root_path)

        db.commit()
        print(f"✅ Crawled {inserted} nodes for share {share_id} ({root_path})")

    except Exception as e:
        db.rollback()
        print(f"❌ Error while crawling: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Example: crawl share id=1, path=./sample_share for dev
    crawl_share(share_id=1, root_path="C:\\Users\\Sidharth\\PycharmProjects\\advanced-archival-tool\\sample_share")
