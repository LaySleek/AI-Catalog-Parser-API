import sys

from celery.__main__ import main as celery_main


def main() -> None:
    sys.argv = [
        "celery",
        "-A",
        "src.infrastructure.queue.celery_app",
        "worker",
        "--loglevel=info",
        "-Q",
        "catalog",
        "-c",
        "1",
    ]
    celery_main()


if __name__ == "__main__":
    main()
