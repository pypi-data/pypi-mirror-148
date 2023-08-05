from typing import Optional
from phidata.types.context import PathContext, RunContext, AirflowContext
from phidata.utils.dttm import dttm_to_dttm_str, days_ago


def get_run_date(
    run_context: Optional[RunContext] = None,
    airflow_context: Optional[AirflowContext] = None,
) -> str:

    if run_context is not None and run_context.run_date is not None:
        return run_context.run_date
    if airflow_context is not None and airflow_context.logical_date is not None:
        return dttm_to_dttm_str(airflow_context.logical_date, dttm_format="%Y-%m-%d")
    return dttm_to_dttm_str(days_ago(), dttm_format="%Y-%m-%d")
