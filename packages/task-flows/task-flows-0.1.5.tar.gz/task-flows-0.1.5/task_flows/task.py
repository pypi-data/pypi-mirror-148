import functools
import sys
from typing import Union

from task_flows.logging import TaskLogger


def task(
    task_name: str,
    retries: int = 0,
    alert_types: Union["email", "slack"] = ["email", "slack"],
    exit_on_complete: bool = False,
):
    """Decorator for turning functions into managed/monitored tasks.

    Args:
        task_name (str): _description_
        retries (int, optional): _description_. Defaults to 0.
        alert_types (Union[&quot;email&quot;, &quot;slack&quot;], optional): _description_. Defaults to ["email", "slack"].
        exit_on_complete (bool, optional): _description_. Defaults to True.
    """

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
                    if exit_on_complete:
                        sys.exit(0)
                    return
                except Exception as e:
                    errors.append(e)
            task_logger.record_task_finish(
                success=False, errors=errors, retries=retries
            )
            task_logger.alert_task_finish(alert_types)
            if exit_on_complete:
                sys.exit(1)

        return task_wrapper

    return task_decorator
