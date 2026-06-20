from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from plyer import notification
except ImportError:
    notification = None

# FIX: use logging instead of bare print() so output can be redirected/controlled
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path(__file__).with_name("config.json")


@dataclass(frozen=True)
class NotificationItem:
    title: str
    message: str
    interval_seconds: int


def load_config(config_path: Path) -> dict[str, Any]:
    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            data = json.load(config_file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Config file not found: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in config file: {config_path}") from exc

    if not isinstance(data, dict):
        raise ValueError("Config file must contain a JSON object.")
    return data


def parse_notifications(config_data: dict[str, Any]) -> tuple[str, int, list[NotificationItem]]:
    app_name = str(config_data.get("app_name", "Notification Scheduler"))
    default_timeout = int(config_data.get("default_timeout", 10))
    raw_notifications = config_data.get("notifications", [])

    if not isinstance(raw_notifications, list) or not raw_notifications:
        raise ValueError("Config must include a non-empty 'notifications' list.")

    notifications: list[NotificationItem] = []
    for index, item in enumerate(raw_notifications, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Notification #{index} must be a JSON object.")

        title = str(item.get("title", "Untitled notification")).strip()
        message = str(item.get("message", "")).strip()
        interval_seconds = int(item.get("interval_seconds", 0))

        if not title:
            raise ValueError(f"Notification #{index} is missing a title.")
        if not message:
            raise ValueError(f"Notification #{index} is missing a message.")
        if interval_seconds <= 0:
            raise ValueError(f"Notification #{index} must have interval_seconds > 0.")

        notifications.append(NotificationItem(title, message, interval_seconds))

    return app_name, default_timeout, notifications


def send_notification(app_name: str, item: NotificationItem, timeout: int) -> None:
    if notification is None:
        # FIX: use logger instead of print
        logger.info("[fallback] %s: %s", item.title, item.message)
        return

    notification.notify(
        title=item.title,
        message=item.message,
        app_name=app_name,
        timeout=timeout,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send recurring desktop notifications from JSON config.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to the notification config JSON file.",
    )

    # FIX: replaced confusing --cycles 0 = infinite with an explicit --infinite flag
    cycle_group = parser.add_mutually_exclusive_group()
    cycle_group.add_argument(
        "--cycles",
        type=int,
        default=1,
        help="Number of times to run through the notification list (default: 1).",
    )
    cycle_group.add_argument(
        "--infinite",
        action="store_true",
        help="Run forever (overrides --cycles).",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        config_data = load_config(args.config)
        app_name, default_timeout, notifications = parse_notifications(config_data)
    except (OSError, ValueError) as exc:
        # FIX: use logger.error instead of print to stderr
        logger.error("Startup error: %s", exc)
        return 1

    run_forever = args.infinite
    cycle_count = 0

    logger.info("Starting %s. Cycles: %s", app_name, "infinite" if run_forever else args.cycles)

    while True:
        cycle_count += 1
        for item in notifications:
            # FIX: use logger.info instead of print
            logger.info("Sending notification: %s", item.title)
            send_notification(app_name, item, default_timeout)
            time.sleep(item.interval_seconds)

        if not run_forever and cycle_count >= args.cycles:
            break

    logger.info("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
