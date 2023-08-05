from collections import OrderedDict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Any, Dict, List, Callable, Tuple, Literal

from phidata.base import PhidataBase, PhidataBaseArgs
from phidata.asset import DataAsset
from phidata.constants import (
    SCRIPTS_DIR_ENV_VAR,
    STORAGE_DIR_ENV_VAR,
    META_DIR_ENV_VAR,
    PRODUCTS_DIR_ENV_VAR,
    NOTEBOOKS_DIR_ENV_VAR,
    WORKSPACE_CONFIG_DIR_ENV_VAR,
)
from phidata.dq import DQCheck
from phidata.exceptions.task import TaskFailure
from phidata.task import Task, PythonTask, PythonTaskType
from phidata.utils.context import get_run_date
from phidata.utils.cli_console import print_subheading, print_info
from phidata.utils.env_var import validate_env_vars
from phidata.utils.log import logger
from phidata.types.run_status import RunStatus
from phidata.types.context import PathContext, RunContext, AirflowContext


class WorkflowArgs(PhidataBaseArgs):
    # List of tasks in this Workflow
    tasks: Optional[List[Task]] = None
    # A dependency graph of the tasks in the format:
    # { upstream: [downstream_list] }
    # Ex:
    #   graph = {
    #     task_1: [task_0],
    #     task_2: [task_1, task_2],
    #     ...
    #   }
    graph: Optional[Dict[Task, List[Task]]] = None
    # What to do when a task fails, continue to next task or stop?
    on_failure: Literal["stop", "continue"] = "stop"

    # Add an EmptyOperator at the start of the workflow
    add_start_task: bool = False
    # Add an EmptyOperator at the end of the workflow
    add_end_task: bool = True

    # TO_BE_IMPLEMENTED
    # use airflow task_groups
    use_task_groups: bool = False
    # airflow task group_id for this workflow, use name if not provided
    group_id: Optional[str] = None

    # airflow dag_id for this workflow, use name if not provided
    dag_id: Optional[str] = None
    # run_context provided by wf_operator
    run_context: Optional[RunContext] = None
    # path_context provided by env variables
    path_context: Optional[PathContext] = None
    # airflow_context provided by airflow
    airflow_context: Optional[AirflowContext] = None
    # Env vars that validate Airflow is active on the containers
    # This is used to gate code blocks which should only run on
    # remote containers like creating DAGs and tasks
    validate_airflow_env: Dict[str, Any] = {"INIT_AIRFLOW": True}

    # Input DataAssets used to build sensors before kicking off the workflow
    inputs: Optional[List[DataAsset]] = None
    # DataAssets produced by this workflow, used for building the lineage graph
    outputs: Optional[List[DataAsset]] = None

    # Checks to run before the workflow
    pre_checks: Optional[List[DQCheck]] = None
    # Checks to run after the workflow
    post_checks: Optional[List[DQCheck]] = None

    # The tooltip of the TaskGroup node when displayed in the UI
    description: Optional[str] = None
    # The fill color of the TaskGroup node when displayed in the UI
    ui_color: Optional[str] = None
    # The label color of the TaskGroup node when displayed in the UI
    ui_fgcolor: Optional[str] = None

    @property
    def airflow_active(self) -> bool:
        return validate_env_vars(self.validate_airflow_env)

    @property
    def run_date(self) -> str:
        return get_run_date(self.run_context, self.airflow_context)

    @classmethod
    def from_kwargs(cls, kwargs: Optional[Dict] = None):
        if kwargs is None or not isinstance(kwargs, dict):
            return cls()
        # logger.info(f"Loading {cls.__name__} using kwargs")
        args_object = cls(**kwargs)
        validate_airflow_env = kwargs.get("validate_airflow_env", None)
        if validate_env_vars(validate_airflow_env):
            # logger.info("Creating airflow_context")
            airflow_context = AirflowContext(**kwargs)
            args_object.airflow_context = airflow_context
        return args_object


class Workflow(PhidataBase):
    """Base Class for all Workflows"""

    def __init__(
        self,
        name: Optional[str] = None,
        # List of tasks in this Workflow
        tasks: Optional[List[Task]] = None,
        # A dependency graph of the tasks in the format:
        # { upstream: [downstream_list] }
        # Ex:
        #   graph = {
        #     task_1: [task_0],
        #     task_2: [task_1, task_2],
        #     ...
        #   }
        graph: Optional[Dict[Task, List[Task]]] = None,
        # What to do when a task fails, continue to next task or stop?
        on_failure: Literal["stop", "continue"] = "stop",
        # Add an EmptyOperator at the start of the workflow
        add_start_task: bool = False,
        # Add an EmptyOperator at the end of the workflow
        add_end_task: bool = True,
        # TO_BE_IMPLEMENTED
        # use airflow task_groups
        use_task_groups: bool = True,
        # airflow task group_id for this workflow, use name if not provided
        group_id: Optional[str] = None,
        # airflow dag_id for this workflow, use name if not provided
        dag_id: Optional[str] = None,
        # run_context provided by wf_operator
        run_context: Optional[RunContext] = None,
        # path_context provided by env variables
        path_context: Optional[PathContext] = None,
        # airflow_context provided by airflow
        airflow_context: Optional[AirflowContext] = None,
        # Input DataAssets used to build sensors before kicking off the workflow
        inputs: Optional[List[DataAsset]] = None,
        # DataAssets produced by this workflow, used for building the lineage graph
        outputs: Optional[List[DataAsset]] = None,
        # Checks to run before the workflow
        pre_checks: Optional[List[DQCheck]] = None,
        # Checks to run after the workflow
        post_checks: Optional[List[DQCheck]] = None,
        # The tooltip of the TaskGroup node when displayed in the UI
        description: Optional[str] = None,
        # The fill color of the TaskGroup node when displayed in the UI
        ui_color: Optional[str] = None,
        # The label color of the TaskGroup node when displayed in the UI
        ui_fgcolor: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ):
        super().__init__()
        try:
            self.args: WorkflowArgs = WorkflowArgs(
                name=name,
                tasks=tasks,
                graph=graph,
                on_failure=on_failure,
                add_start_task=add_start_task,
                add_end_task=add_end_task,
                use_task_groups=use_task_groups,
                group_id=group_id,
                dag_id=dag_id,
                run_context=run_context,
                path_context=path_context,
                airflow_context=airflow_context,
                inputs=inputs,
                outputs=outputs,
                pre_checks=pre_checks,
                post_checks=post_checks,
                description=description,
                ui_color=ui_color,
                ui_fgcolor=ui_fgcolor,
                version=version,
                enabled=enabled,
            )
        except Exception as e:
            logger.error(f"Args for {self.__class__.__name__} are not valid")
            raise

    @property
    def tasks(self) -> Optional[List[Task]]:
        return self.args.tasks if self.args else None

    @tasks.setter
    def tasks(self, tasks: List[Task]) -> None:
        if self.args is not None and tasks is not None:
            self.args.tasks = tasks

    @property
    def graph(self) -> Optional[Dict[Task, List[Task]]]:
        return self.args.graph if self.args else None

    @graph.setter
    def graph(self, graph: Dict[Task, List[Task]]) -> None:
        if self.args is not None and graph is not None:
            self.args.graph = graph

    @property
    def on_failure(self) -> Literal["stop", "continue"]:
        return self.args.on_failure if self.args else "stop"

    @on_failure.setter
    def on_failure(self, on_failure: Literal["stop", "continue"]) -> None:
        if self.args is not None and on_failure is not None:
            self.args.on_failure = on_failure

    @property
    def add_start_task(self) -> bool:
        return self.args.add_start_task if self.args else False

    @add_start_task.setter
    def add_start_task(self, add_start_task: bool) -> None:
        if self.args is not None and add_start_task is not None:
            self.args.add_start_task = add_start_task

    @property
    def add_end_task(self) -> bool:
        return self.args.add_end_task if self.args else False

    @add_end_task.setter
    def add_end_task(self, add_end_task: bool) -> None:
        if self.args is not None and add_end_task is not None:
            self.args.add_end_task = add_end_task

    @property
    def use_task_groups(self) -> bool:
        return self.args.use_task_groups if self.args else False

    @use_task_groups.setter
    def use_task_groups(self, use_task_groups: bool) -> None:
        if self.args is not None and use_task_groups is not None:
            self.args.use_task_groups = use_task_groups

    @property
    def group_id(self) -> str:
        return self.args.group_id if (self.args and self.args.group_id) else self.name

    @group_id.setter
    def group_id(self, group_id: str) -> None:
        if self.args is not None and group_id is not None:
            self.args.group_id = group_id

    @property
    def dag_id(self) -> str:
        return self.args.dag_id if (self.args and self.args.dag_id) else self.name

    @dag_id.setter
    def dag_id(self, dag_id: str) -> None:
        if self.args is not None and dag_id is not None:
            self.args.dag_id = dag_id

    @property
    def run_context(self) -> Optional[RunContext]:
        return self.args.run_context if self.args else None

    @run_context.setter
    def run_context(self, run_context: RunContext) -> None:
        if self.args is not None and run_context is not None:
            self.args.run_context = run_context

    @property
    def path_context(self) -> Optional[PathContext]:
        # Workflow not yet initialized
        if self.args is None:
            return None

        if self.args.path_context is not None:
            # use cached value if available
            return self.args.path_context

        logger.debug(f"--++**++--> Loading PathContext from env")
        self.path_context = PathContext()

        import os

        scripts_dir = os.getenv(SCRIPTS_DIR_ENV_VAR)
        storage_dir = os.getenv(STORAGE_DIR_ENV_VAR)
        meta_dir = os.getenv(META_DIR_ENV_VAR)
        products_dir = os.getenv(PRODUCTS_DIR_ENV_VAR)
        notebooks_dir = os.getenv(NOTEBOOKS_DIR_ENV_VAR)
        workspace_config_dir = os.getenv(WORKSPACE_CONFIG_DIR_ENV_VAR)

        if storage_dir is None:
            logger.error(f"{STORAGE_DIR_ENV_VAR} not set")
        if products_dir is None:
            logger.error(f"{PRODUCTS_DIR_ENV_VAR} not set")

        try:
            if scripts_dir is not None:
                self.path_context.scripts_dir = Path(scripts_dir)
            if storage_dir is not None:
                self.path_context.storage_dir = Path(storage_dir)
            if meta_dir is not None:
                self.path_context.meta_dir = Path(meta_dir)
            if products_dir is not None:
                self.path_context.products_dir = Path(products_dir)
            if notebooks_dir is not None:
                self.path_context.notebooks_dir = Path(notebooks_dir)
            if workspace_config_dir is not None:
                self.path_context.workspace_config_dir = Path(workspace_config_dir)
        except Exception as e:
            raise
        logger.debug(f"--++**++--> PathContext loaded")
        return self.args.path_context

    @path_context.setter
    def path_context(self, path_context: PathContext) -> None:
        if self.args is not None and path_context is not None:
            self.args.path_context = path_context

    @property
    def airflow_context(self) -> Optional[AirflowContext]:
        return self.args.airflow_context if self.args else None

    @airflow_context.setter
    def airflow_context(self, airflow_context: AirflowContext) -> None:
        if self.args is not None and airflow_context is not None:
            self.args.airflow_context = airflow_context

    @property
    def inputs(self) -> Optional[List[DataAsset]]:
        return self.args.inputs if self.args else None

    @inputs.setter
    def inputs(self, inputs: List[DataAsset]) -> None:
        if self.args is not None and inputs is not None:
            self.args.inputs = inputs

    @property
    def outputs(self) -> Optional[List[DataAsset]]:
        return self.args.outputs if self.args else None

    @outputs.setter
    def outputs(self, outputs: List[DataAsset]) -> None:
        if self.args is not None and outputs is not None:
            self.args.outputs = outputs

    @property
    def pre_checks(self) -> Optional[List[DQCheck]]:
        return self.args.pre_checks if self.args else None

    @pre_checks.setter
    def pre_checks(self, pre_checks: List[DQCheck]) -> None:
        if self.args is not None and pre_checks is not None:
            self.args.pre_checks = pre_checks

    @property
    def post_checks(self) -> Optional[List[DQCheck]]:
        return self.args.post_checks if self.args else None

    @post_checks.setter
    def post_checks(self, post_checks: List[DQCheck]) -> None:
        if self.args is not None and post_checks is not None:
            self.args.post_checks = post_checks

    @property
    def description(self) -> Optional[str]:
        return self.args.description if self.args else None

    @description.setter
    def description(self, description: str) -> None:
        if self.args is not None and description is not None:
            self.args.description = description

    @property
    def ui_color(self) -> Optional[str]:
        return self.args.ui_color if self.args else None

    @ui_color.setter
    def ui_color(self, ui_color: str) -> None:
        if self.args is not None and ui_color is not None:
            self.args.ui_color = ui_color

    @property
    def ui_fgcolor(self) -> Optional[str]:
        return self.args.ui_fgcolor if self.args else None

    @ui_fgcolor.setter
    def ui_fgcolor(self, ui_fgcolor: str) -> None:
        if self.args is not None and ui_fgcolor is not None:
            self.args.ui_fgcolor = ui_fgcolor

    @property
    def airflow_active(self) -> bool:
        return validate_env_vars(self.args.validate_airflow_env)

    def __call__(self, *args, **kwargs) -> bool:
        logger.warning("Workflows should not be called directly")
        return True

    ######################################################
    ## Build workflow
    ######################################################

    def build(self) -> bool:
        logger.debug(f"@build not defined for {self.__class__.__name__}")
        return False

    ######################################################
    ## Tasks
    ######################################################

    def add_task(self, task: Task):
        if self.args.tasks is None:
            self.args.tasks = []
        self.args.tasks.append(task)

    ######################################################
    ## Checks
    ######################################################

    def add_pre_check(self, check: DQCheck):
        if self.args.pre_checks is None:
            self.args.pre_checks = []
        self.args.pre_checks.append(check)

    def add_post_check(self, check: DQCheck):
        if self.args.post_checks is None:
            self.args.post_checks = []
        self.args.post_checks.append(check)

    ######################################################
    ## Run workflow
    ######################################################

    def run_task_in_local_env(self, task: Task) -> RunStatus:
        _task_id = task.task_id
        print_info(f"\nRunning task: {_task_id}")
        # Pass down context
        task.run_context = self.run_context
        task.path_context = self.path_context
        task.airflow_context = self.airflow_context
        if self.dag_id:
            task.dag_id = self.dag_id
        run_success = task.run_in_local_env()
        logger.debug(f"Success: {run_success}")
        return RunStatus(name=_task_id, success=run_success)

    def run_in_local_env(self, task_id: Optional[str] = None) -> bool:
        """
        Runs a workflow in the local environment where phi wf is called from.

        Returns:
            run_status (bool): True if the run was successful
        """
        from phidata.utils.cli_console import print_run_status_table

        logger.info("--**-- Running Workflow locally")

        if self.tasks is None:
            logger.info("No tasks to run")
            return True

        # logger.info(f"workflow tasks: {self.tasks}")
        # logger.info(f"workflow graph: {self.graph}")
        task_run_status: List[RunStatus] = []
        try:
            if task_id is not None:
                task_id_map = {t.task_id: t for t in self.tasks}
                if task_id in task_id_map:
                    task_run_status.append(
                        self.run_task_in_local_env(task_id_map[task_id])
                    )
                else:
                    logger.error(f"Could not find {task_id} in {task_id_map.keys()}")
            else:
                for task in self.tasks:
                    run_status = self.run_task_in_local_env(task)
                    task_run_status.append(run_status)
                    if not run_status.success and self.args.on_failure == "stop":
                        raise TaskFailure(f"Task {task.task_id} failed")
        except TaskFailure as tf:
            logger.error(tf)

        print_run_status_table("Task Run Status", task_run_status)
        for run_status in task_run_status:
            if not run_status.success:
                return False
        return True

    def run_task_in_docker_env(
        self,
        task: Task,
        active_container: Any,
        docker_env: Optional[Dict[str, str]] = None,
    ) -> RunStatus:
        _task_id = task.task_id
        print_info(f"\nRunning task: {_task_id}")
        # Pass down context
        task.run_context = self.run_context
        task.path_context = self.path_context
        task.airflow_context = self.airflow_context
        task.dag_id = self.dag_id
        run_success = task.run_in_docker_container(
            active_container=active_container, docker_env=docker_env
        )
        logger.debug(f"Success: {run_success}")
        return RunStatus(name=_task_id, success=run_success)

    def run_in_docker_container(
        self,
        active_container: Any,
        docker_env: Optional[Dict[str, str]] = None,
        task_id: Optional[str] = None,
    ) -> bool:
        """
        Runs a workflow in a docker container.

        Args:
            active_container:
            docker_env:
            task_id:

        Returns:
            run_status (bool): True if the run was successful

        Notes:
            * This function runs in the local environment where phi wf is called from.
            But executes `airflow` commands in the docker container to run the workflow
            * For the airflow tasks to be available, they need to be added to the workflow DAG
            using add_airflow_tasks_to_dag()
        """
        from phidata.utils.cli_console import print_run_status_table

        logger.info("--**-- Running Workflow in docker container")

        if self.tasks is None:
            logger.info("No tasks to run")
            return True

        # logger.info(f"workflow tasks: {self.tasks}")
        # logger.info(f"workflow graph: {self.graph}")
        task_run_status: List[RunStatus] = []
        try:
            if task_id is not None:
                task_id_map = {t.task_id: t for t in self.tasks}
                if task_id in task_id_map:
                    task_run_status.append(
                        self.run_task_in_docker_env(
                            task=task_id_map[task_id],
                            active_container=active_container,
                            docker_env=docker_env,
                        )
                    )
                else:
                    logger.error(f"Could not find {task_id} in {task_id_map.keys()}")
            else:
                for task in self.tasks:
                    run_status = self.run_task_in_docker_env(
                        task=task,
                        active_container=active_container,
                        docker_env=docker_env,
                    )
                    task_run_status.append(run_status)
                    if not run_status.success and self.args.on_failure == "stop":
                        raise TaskFailure(f"Task {task.task_id} failed")
        except TaskFailure as tf:
            logger.error(tf)

        print_run_status_table("Task Run Status", task_run_status)
        for run_status in task_run_status:
            if not run_status.success:
                return False
        return True

    def run_in_k8s_container(
        self,
        pod: Any,
        k8s_api_client: Any,
        container_name: Optional[str] = None,
        k8s_env: Optional[Dict[str, str]] = None,
    ) -> bool:
        logger.info("--**-- Running Workflow in k8s container")

        if self.tasks is None:
            logger.info("No tasks to run")
            return True

        task_run_status: List[RunStatus] = []
        for idx, task in enumerate(self.tasks, start=1):
            task_name = task.name or "{}__{}".format(task.__class__.__name__, idx)
            print_subheading(f"\nRunning {task_name}")
            # Pass down context
            task.run_context = self.run_context
            task.path_context = self.path_context
            task.airflow_context = self.airflow_context
            task.dag_id = self.dag_id
            run_success = task.run_in_k8s_container(
                pod=pod,
                k8s_api_client=k8s_api_client,
                container_name=container_name,
                k8s_env=k8s_env,
            )
            task_run_status.append(RunStatus(name=task_name, success=run_success))

        print_subheading("\nTask run status:")
        print_info(
            "\n".join(
                [
                    "{}: {}".format(task.name, "Success" if task.success else "Fail")
                    for task in task_run_status
                ]
            )
        )
        print_info("")
        for run_status in task_run_status:
            if not run_status.success:
                return False
        return True

    ######################################################
    ## Airflow functions
    ######################################################

    def get_task_group(self, dag: Optional[Any]) -> Optional[Any]:

        from airflow.utils.task_group import TaskGroup

        # check group_id
        group_id = self.group_id
        if group_id is None:
            logger.error("Workflow group_id unavailable")
            return False

        # build a dict of not_null_args which are passed to the TaskGroup()
        not_null_args: Dict[str, Any] = {}
        if self.description is not None:
            not_null_args["tooltip"] = self.description
        if self.ui_color is not None:
            not_null_args["ui_color"] = self.ui_color
        if self.ui_fgcolor is not None:
            not_null_args["ui_fgcolor"] = self.ui_fgcolor

        return TaskGroup(
            group_id=group_id, dag=dag, add_suffix_on_collision=True, **not_null_args
        )

    def get_start_workflow_task(self, dag: Optional[Any]) -> Optional[Any]:

        if not self.add_start_task:
            return None

        from phidata.airflow.operators.empty import EmptyOperator

        start_task_id = f"{self.name}_start"
        return EmptyOperator(task_id=start_task_id, dag=dag)

    def get_end_workflow_task(self, dag: Optional[Any]) -> Optional[Any]:

        if not self.add_end_task:
            return None

        from phidata.airflow.operators.empty import EmptyOperator

        end_task_id = f"{self.name}_end"
        return EmptyOperator(task_id=end_task_id, dag=dag)

    def add_airflow_tasks_to_dag(self, dag: Any) -> bool:
        """
        Add tasks to the airflow DAG.

        Args:
            dag:

        Returns:

        Notes:
            * This function is called as part of the create_airflow_dag() function
        """
        # Skips DAG creation on local machines
        if not self.airflow_active:
            return False

        from airflow.models import BaseOperator
        from airflow.utils.task_group import TaskGroup
        from phidata.airflow.operators.empty import EmptyOperator

        # check tasks
        if self.tasks is None:
            logger.error(f"Workflow {self.name} has no tasks")
            return False

        # If self.use_task_groups, then the task_group variable is
        # updated using self.get_task_group()
        # So when we provide the task_group parameter to each task,
        # then task gets automatically added to the task_group()
        #   it task_group is not None
        task_group: Optional[TaskGroup] = None
        if self.use_task_groups:
            task_group = self.get_task_group(dag=dag)
            if task_group is None or not isinstance(task_group, TaskGroup):
                logger.error(f"Could not create task_group: {self.group_id}")
                return False

        # add workflow start and end tasks
        workflow_start: Optional[EmptyOperator] = self.get_start_workflow_task(dag)
        workflow_end: Optional[EmptyOperator] = self.get_end_workflow_task(dag)

        # add tasks to DAG
        airflow_tasks: Dict[str, BaseOperator] = OrderedDict()
        for task in self.tasks:
            task_id = task.task_id
            # Pass down context
            task.run_context = self.run_context
            task.path_context = self.path_context
            task.airflow_context = self.airflow_context

            airflow_task_operator = task.add_airflow_task(dag=dag)
            if airflow_task_operator is None or not isinstance(
                airflow_task_operator, BaseOperator
            ):
                logger.warning(f"Task: {task_id} could not be created")
                continue

            airflow_tasks[task_id] = airflow_task_operator
            if self.add_start_task and workflow_start is not None:
                # Add task to be downstream of workflow_start
                workflow_start.set_downstream(airflow_task_operator)
            if self.add_end_task and workflow_end is not None:
                # Add task to be upstream of workflow_end
                workflow_end.set_upstream(airflow_task_operator)

        # set dependencies
        if self.graph is not None:
            for upstream_task, downstream_task_list in self.graph.items():
                upstream_airflow_task = airflow_tasks[upstream_task.task_id]
                downstream_airflow_task_list = [
                    airflow_tasks[task.task_id] for task in downstream_task_list
                ]
                upstream_airflow_task.set_downstream(downstream_airflow_task_list)
                logger.info(f"Task: {upstream_airflow_task.task_id}")
                logger.info(f"Downstream: {upstream_airflow_task.downstream_task_ids}")

        return True

    def create_airflow_dag(
        self,
        owner: Optional[str] = "airflow",
        depends_on_past: Optional[bool] = False,
        # The description for the DAG to e.g. be shown on the webserver
        description: Optional[str] = None,
        # Defines how often that DAG runs, this
        #  timedelta object gets added to your latest task instance's
        #  execution_date to figure out the next schedule
        # Default: daily
        schedule_interval: timedelta = timedelta(days=1),
        # The timestamp from which the scheduler will
        #  attempt to backfill
        start_date: Optional[datetime] = None,
        # if start_date is not provided, use start_days_ago
        start_days_ago: int = 2,
        # A date beyond which your DAG won't run, leave to None
        #  for open ended scheduling
        end_date: Optional[datetime] = None,
        # a dictionary of macros that will be exposed
        #  in your jinja templates. For example, passing ``dict(foo='bar')``
        #  to this argument allows you to ``{{ foo }}`` in all jinja
        #  templates related to this DAG. Note that you can pass any
        #  type of object here.
        user_defined_macros: Optional[Dict] = None,
        # a dictionary of filters that will be exposed
        #  in your jinja templates. For example, passing
        #  ``dict(hello=lambda name: 'Hello %s' % name)`` to this argument allows
        #  you to ``{{ 'world' | hello }}`` in all jinja templates related to
        #  this DAG.
        user_defined_filters: Optional[Dict] = None,
        # A dictionary of default parameters to be used
        #  as constructor keyword parameters when initialising operators.
        #  Note that operators have the same hook, and precede those defined
        #  here, meaning that if your dict contains `'depends_on_past': True`
        #  here and `'depends_on_past': False` in the operator's call
        #  `default_args`, the actual value will be `False`.
        default_args: Optional[Dict] = None,
        # the number of task instances allowed to run concurrently
        concurrency: Optional[int] = None,
        # maximum number of active DAG runs, beyond this
        #  number of DAG runs in a running state, the scheduler won't create
        #  new active DAG runs
        max_active_runs: int = 8,
        doc_md: Optional[str] = None,
        # a dictionary of DAG level parameters that are made
        # accessible in templates, namespaced under `params`. These
        # params can be overridden at the task level.
        params: Optional[Dict] = None,
        is_paused_upon_creation: Optional[bool] = None,
        jinja_environment_kwargs: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
    ) -> Any:
        """
        Used to create an Airflow DAG for independent workflows.
        It is preferred to create 1 DAG for each DataProduct but not all pipelines
        have DataProducts, some just have 1 Workflow.
        """

        # Skips DAG creation on local machines
        if not self.airflow_active:
            return None

        from airflow import DAG
        from airflow.utils.dates import days_ago

        operator_default_args = default_args
        if operator_default_args is None:
            operator_default_args = {}
        operator_default_args.update(
            {
                "owner": owner,
                "depends_on_past": depends_on_past,
            }
        )
        if start_date is None:
            start_date = days_ago(start_days_ago)

        dag_id = self.dag_id
        if dag_id is None:
            logger.error("Workflow dag_id unavailable")
            return False
        dag = DAG(
            dag_id=dag_id,
            description=description,
            schedule_interval=schedule_interval,
            start_date=start_date,
            end_date=end_date,
            user_defined_macros=user_defined_macros,
            user_defined_filters=user_defined_filters,
            default_args=operator_default_args,
            concurrency=concurrency,
            max_active_runs=max_active_runs,
            doc_md=doc_md,
            params=params,
            is_paused_upon_creation=is_paused_upon_creation,
            jinja_environment_kwargs=jinja_environment_kwargs,
            tags=tags,
        )
        add_task_success = self.add_airflow_tasks_to_dag(dag=dag)
        if not add_task_success:
            logger.error(f"Tasks for workflow {self.name} could not be added")
        logger.debug(f"Airflow dag {dag_id} created")
        return dag

    def task(
        self,
        func: Optional[PythonTaskType] = None,
        *,
        name: Optional[str] = None,
        task_id: Optional[str] = None,
        version: Optional[str] = None,
        enabled: bool = True,
        args: Optional[Tuple[Any, ...]] = None,
        **kwargs,
    ) -> Callable[..., PythonTask]:
        """
        Adds a PythonTask to this workflow

        Usage:

        """
        from functools import partial

        def decorator(f: PythonTaskType) -> PythonTask:
            # logger.info(f"workflow.task func: {func}")
            # logger.info(f"workflow.task f: {f}")
            # logger.info(f"workflow.task args: {args}")
            # logger.info(f"workflow.task kwargs: {kwargs}")
            task_name = name or f.__name__
            try:
                # create a partial function that can be called by the PythonTask
                entrypoint = (
                    partial(f, *args, **kwargs)
                    if args is not None
                    else partial(f, **kwargs)
                )
                python_task = PythonTask(
                    name=task_name,
                    entrypoint=entrypoint,
                    task_id=task_id,
                    dag_id=self.dag_id,
                    entrypoint_args=args,
                    entrypoint_kwargs=kwargs,
                    version=version,
                    enabled=enabled,
                )
                self.add_task(task=python_task)
                return python_task
            except Exception as e:
                logger.error(f"Could not create task: {task_name}")
                logger.error(e)
                raise

        return decorator
