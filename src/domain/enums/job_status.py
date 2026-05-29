from enum import StrEnum


class JobStatus(StrEnum):
    """Статус выполнения задачи."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"
