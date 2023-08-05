from datetime import datetime
from typing import Any, List, Optional, Union

import sqlalchemy as sa
from alert_msgs import KV, FontColors, FontSize, Text, send_alert
from ready_logger import get_logger
from sqlalchemy.engine import Engine

from .tables import task_table
from .utils import get_engine

logger = get_logger("task-flows")


class TaskLogger:
    def __init__(self, task_name: str, engine: Optional[Engine] = None):
        self.task_name = task_name
        self.engine = engine or get_engine()
        self._task_start_recorded = False
        self._task_finish_recorded = False

    def record_task_start(self):
        self.start_time = datetime.utcnow()
        statement = sa.insert(task_table).values(
            {"name": self.task_name, "started": self.start_time}
        )
        with self.engine.begin() as conn:
            conn.execute(statement)
        self._task_start_recorded = True

    def record_task_finish(
        self,
        success: bool,
        errors: List[Any],
        return_value: Any = None,
        retries: int = 0,
    ):

        if not self._task_start_recorded:
            raise RuntimeError(
                "Task finish can not be recorded unless task start is recoded first."
            )

        self.finish_time = datetime.utcnow()
        self.success = success
        self.errors = errors
        self.return_value = return_value
        self.retries = retries
        self.status = "success" if success else "failed"

        statement = (
            sa.update(task_table)
            .where(
                task_table.c.name == self.task_name,
                task_table.c.started == self.start_time,
            )
            .values(
                finished=self.finish_time,
                retries=self.retries,
                status=self.status,
                errors="\n".join([str(e) for e in self.errors]),
                return_value=self.return_value,
            )
        )
        with self.engine.begin() as conn:
            conn.execute(statement)

        self._task_finish_recorded = True

    def alert_task_finish(
        self,
        alert_types: Union["email", "slack"] = ["email", "slack"],
    ):
        if not self._task_finish_recorded:
            raise RuntimeError(
                "Task finish alert can not be created unless task finish is recoded first (record_task_finish)"
            )

        if isinstance(alert_types, str):
            alert_types = [alert_types]

        subject = f"{self.status}: {self.task_name}"
        components = [
            Text(
                subject,
                size=FontSize.LARGE,
                color=FontColors.IMPORTANT if self.success else FontColors.ERROR,
            ),
            KV(
                {
                    "Start": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Finish": self.finish_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Return Value": self.return_value,
                }
            ),
        ]
        if self.errors:
            components.append(
                Text(
                    "ERRORS",
                    size=FontSize.LARGE,
                    color=FontColors.ERROR,
                )
            )
            for e in self.errors:
                components.append(
                    Text(
                        f"{type(e)}: {e}",
                        size=FontSize.MEDIUM,
                        color=FontColors.INFO,
                    )
                )
        for alert_type in alert_types:
            kwargs = {"subject": subject} if alert_type == "email" else {}
            try:
                send_alert(alert_type, components, **kwargs)
            except Exception as e:
                logger.error(f"Error sending alert: {type(e)} -- {e}")
