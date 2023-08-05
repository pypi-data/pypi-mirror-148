import functools
from typing import Union

from task_flows.logging import TaskLogger


def task(
    task_name: str,
    retries: int = 0,
    alert_types: Union["email", "slack"] = ["email", "slack"],
):
    def task_decorator(func):
        @functools.wraps(func)
        def task_wrapper(*args, **kwargs):
            task_logger = TaskLogger(task_name)
            task_logger.record_task_start()
            errors = []
            for i in range(retries + 1):
                try:
                    result = func(*args, **kwargs)
                    task_logger.record_task_finish(
                        success=True, errors=errors, return_value=result, retries=i
                    )
                    task_logger.alert_task_finish(alert_types)
                    return
                except Exception as e:
                    errors.append(e)
            task_logger.record_task_finish(
                success=False, errors=errors, return_value=result, retries=i
            )
            task_logger.alert_task_finish(alert_types)

        return task_wrapper

    return task_decorator
