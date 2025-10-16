import os
import shutil
import pytz
from datetime import datetime
from loguru import logger
from tenacity import retry, wait_exponential, stop_after_attempt

from app.db.session import SessionLocal
from app.models import ArchiveRequest
from app.core.config import settings


def _ensure_dir(p): os.makedirs(p, exist_ok=True)


def _act_copy(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        _ensure_dir(os.path.dirname(dst))
        shutil.copy2(src, dst)


def _act_move(src, dst):
    _ensure_dir(os.path.dirname(dst))
    shutil.move(src, dst)


def _act_delete(src):
    shutil.rmtree(src) if os.path.isdir(src) else os.remove(src)


def _destination(base, path):
    name = os.path.basename(path)
    return os.path.join(base, name)


# def process_archive_request(req, db):
#     """Perform the archive (move or delete selected files/folders)."""
#     logger.info(f"Processing ArchiveRequest ID={req.id} for {req.share_unc}")
#
#     try:
#         paths = req.paths_json.get("paths", [])
#         if not paths:
#             logger.warning(f"No paths found in request {req.id}")
#             req.status = "failed"
#             req.result_message = "No paths provided"
#             db.commit()
#             return
#
#         # Example: Move to 'archive_output/' folder
#         output_base = os.path.join(os.getcwd(), "archive_output")
#         os.makedirs(output_base, exist_ok=True)
#
#         for path in paths:
#             try:
#                 if not os.path.exists(path):
#                     logger.warning(f"Missing path: {path}")
#                     continue
#
#                 name = os.path.basename(path)
#                 dest = os.path.join(output_base, name)
#
#                 if os.path.isdir(path):
#                     shutil.copytree(path, dest, dirs_exist_ok=True)
#                 else:
#                     shutil.copy2(path, dest)
#
#                 # Optional: Delete original after moving (enable if desired)
#                 # shutil.rmtree(path) or os.remove(path)
#
#                 logger.info(f"Archived {path} → {dest}")
#
#             except Exception as e:
#                 logger.error(f"Error archiving {path}: {e}")
#
#         req.status = "done"
#         req.result_message = f"Archived {len(paths)} items successfully"
#         db.commit()
#
#     except Exception as e:
#         logger.error(f"Request {req.id} failed: {e}")
#         req.status = "failed"
#         req.result_message = str(e)
#         db.commit()
#
#
# def run_scheduler():
#     """Check DB every run for pending archives whose time ≤ now."""
#     tz = pytz.timezone(settings.SCHED_TZ)
#     now = datetime.now(tz)
#     logger.info(f"Scheduler run started at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
#
#     db = SessionLocal()
#     try:
#         # pending = (
#         #     db.query(ArchiveRequest)
#         #     .filter(ArchiveRequest.status == "pending")
#         #     .filter(ArchiveRequest.scheduled_est <= now)
#         #     .all()
#         # )

#         pending = (
#             db.query(ArchiveRequest)
#             .filter(ArchiveRequest.status == "pending")
#             .all()
#         )
#
#         if not pending:
#             logger.info("No pending archives ready to run.")
#             return
#
#         for req in pending:
#             req.status = "running"
#             db.commit()
#             process_archive_request(req, db)
#
#     except Exception as e:
#         logger.error(f"Scheduler error: {e}")
#     finally:
#         db.close()
#         logger.info("Scheduler run complete.")
#
#
# if __name__ == "__main__":
#     run_scheduler()


@retry(wait=wait_exponential(multiplier=0.5, min=1, max=8), stop=stop_after_attempt(3))
def process_single_path(path: str, mode: str, dry_run: bool, output_base: str):
    if not os.path.exists(path):
        logger.warning(f"Missing path: {path}")
        return "missing"

    dst = _destination(output_base, path)

    if dry_run:
        logger.info(f"[DRY-RUN] {mode.upper()} {path} -> {dst}")
        return "ok"

    if mode == "copy":
        _act_copy(path, dst)
    elif mode == "move":
        _act_move(path, dst)
    elif mode == "delete":
        _act_delete(path)
        dst = "(deleted)"
    else:
        raise ValueError(f"Unsupported ARCHIVE_MODE={mode}")

    logger.info(f"{mode.upper()} {path} -> {dst}")
    return "ok"


def process_archive_request(req, db):
    tz = pytz.timezone(settings.SCHED_TZ)
    logger.info(f"Processing ArchiveRequest ID={req.id} @ {datetime.now(tz)}")
    paths = req.paths_json.get("paths", []) if req.paths_json else []
    if not paths:
        req.status = "failed";
        req.result_message = "No paths provided";
        db.commit();
        return

    mode = settings.ARCHIVE_MODE
    dry = settings.ARCHIVE_DRY_RUN
    output = settings.ARCHIVE_OUTPUT_DIR
    if mode in ("copy", "move"): _ensure_dir(output)

    ok = fail = 0
    for p in paths:
        try:
            r = process_single_path(p, mode, dry, output)
            ok += (r == "ok")
        except Exception as e:
            fail += 1
            logger.error(f"Failed on {p}: {e}")

    req.status = "done" if fail == 0 else ("partial" if ok > 0 else "failed")
    req.result_message = f"{mode} complete: ok={ok} fail={fail} dry_run={dry}"
    db.commit()


def run_scheduler():
    if settings.ARCHIVE_DRY_RUN:
        logger.warning("⚠️ DRY-RUN mode active — no files will be changed.")
    else:
        logger.warning("⚠️ LIVE MODE — files will be actually moved/copied/deleted!")

    tz = pytz.timezone(settings.SCHED_TZ)
    now = datetime.now(tz)
    logger.info(f"Scheduler run at {now:%Y-%m-%d %H:%M:%S %Z}")

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
            logger.info("No pending archives.")
            return

        for req in pending:
            req.status = "running";
            db.commit()
            try:
                process_archive_request(req, db)
            except Exception as e:
                req.status = "failed";
                req.result_message = str(e);
                db.commit()
    finally:
        db.close()
        logger.info("Scheduler run complete.")


if __name__ == "__main__":
    run_scheduler()
