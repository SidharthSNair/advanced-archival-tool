import os
import shutil
import pytz
from datetime import datetime
from loguru import logger

from app.db.session import SessionLocal
from app.models import ArchiveRequest
from app.core.config import settings


def process_archive_request(req, db):
    """Perform the archive (move or delete selected files/folders)."""
    logger.info(f"Processing ArchiveRequest ID={req.id} for {req.share_unc}")

    try:
        paths = req.paths_json.get("paths", [])
        if not paths:
            logger.warning(f"No paths found in request {req.id}")
            req.status = "failed"
            req.result_message = "No paths provided"
            db.commit()
            return

        # Example: Move to 'archive_output/' folder
        output_base = os.path.join(os.getcwd(), "archive_output")
        os.makedirs(output_base, exist_ok=True)

        for path in paths:
            try:
                if not os.path.exists(path):
                    logger.warning(f"Missing path: {path}")
                    continue

                name = os.path.basename(path)
                dest = os.path.join(output_base, name)

                if os.path.isdir(path):
                    shutil.copytree(path, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(path, dest)

                # Optional: Delete original after moving (enable if desired)
                # shutil.rmtree(path) or os.remove(path)

                logger.info(f"Archived {path} → {dest}")

            except Exception as e:
                logger.error(f"Error archiving {path}: {e}")

        req.status = "done"
        req.result_message = f"Archived {len(paths)} items successfully"
        db.commit()

    except Exception as e:
        logger.error(f"Request {req.id} failed: {e}")
        req.status = "failed"
        req.result_message = str(e)
        db.commit()


def run_scheduler():
    """Check DB every run for pending archives whose time ≤ now."""
    tz = pytz.timezone(settings.SCHED_TZ)
    now = datetime.now(tz)
    logger.info(f"Scheduler run started at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    db = SessionLocal()
    try:
        # pending = (
        #     db.query(ArchiveRequest)
        #     .filter(ArchiveRequest.status == "pending")
        #     .filter(ArchiveRequest.scheduled_est <= now)
        #     .all()
        # )

        pending = (
            db.query(ArchiveRequest)
            .filter(ArchiveRequest.status == "pending")
            .all()
        )

        if not pending:
            logger.info("No pending archives ready to run.")
            return

        for req in pending:
            req.status = "running"
            db.commit()
            process_archive_request(req, db)

    except Exception as e:
        logger.error(f"Scheduler error: {e}")
    finally:
        db.close()
        logger.info("Scheduler run complete.")


if __name__ == "__main__":
    run_scheduler()
