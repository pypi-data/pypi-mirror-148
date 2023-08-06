from openlineage.lineage_backend import Backend
import logging
import traceback
import pathlib
import os
from airflow.lineage.backend import LineageBackend

log = logging.getLogger(__name__)


class AlvinAirflowBackend(Backend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AlvinAirflowLineageBackend(LineageBackend):
    backend: AlvinAirflowBackend = None

    def __init__(self, *args, **kwargs):

        self.copy_alvin_plugin()
        super().__init__(*args, **kwargs)

    def copy_alvin_plugin(self):
        """Copy the Alvin plugin to the airflow plugins folder."""
        filepath = os.path.join(f'{pathlib.Path(__file__).resolve().parent}', 'alvin_plugin.py')
        plugin_path = os.path.join(f'{os.getenv("AIRFLOW_HOME")}', 'plugins')
        if not os.path.exists(plugin_path):
            log.info(f'Creating plugins folder: {plugin_path}')
            os.makedirs(plugin_path)
        full_path = os.path.join(f'{plugin_path}', 'alvin_plugin.py')
        with open(full_path, 'w') as plugin_file:
            with open(filepath, 'r') as f:
                content = f.read()
                plugin_file.write(content)
        log.info(f'Plugin copied successfully to: {full_path}')

    @classmethod
    def send_lineage(cls, *args, **kwargs):
        """Alvin implementation of the send_lineage backend."""
        log.info("calling send lineage with args and kwargs")
        if not cls.backend:
            log.info("Lineage backend is none, creating it")
            cls.backend = AlvinAirflowBackend()
        return cls.backend.send_lineage(*args, **kwargs)


def alvin_callback(context, operator, is_airflow_legacy=False):
    """Alvin callback implementation.

    This function use the OpenLineage implementation of
    the Airflow Backend and call send_lineage with the
    given context.
    """
    try:
        if is_airflow_legacy:
            AlvinAirflowLineageBackend.send_lineage(context=context, operator=operator)  # noqa
        else:
            lineage_backend = AlvinAirflowLineageBackend()
            lineage_backend.send_lineage(context=context, operator=operator)
    except Exception:
        log.error(f"Alvin Callback Error: {traceback.format_exc()}")


def alvin_dag_run_extractor(dag_run):
    import requests
    import os
    from alvin_integration.producers.airflow.config import ALVIN_BACKEND_API_URL, ALVIN_BACKEND_API_KEY
    ALVIN_PLATFORM_ID = os.getenv('ALVIN_PLATFORM_ID')
    alvin_backend_metadata_url = f'{ALVIN_BACKEND_API_URL}/api/v1/lineage'

    payload = {'alvin_platform_id': ALVIN_PLATFORM_ID,
               'facets': {
                   "dag_run": {
                    "dag_id": dag_run.dag_id,
                    "run_id": dag_run.run_id,
                    "queued_at": (dag_run.queued_at.isoformat() if dag_run.queued_at else None) if hasattr(dag_run, 'queued_at') else None,
                    "execution_date": dag_run.execution_date.isoformat(),
                    "start_date": dag_run.start_date.isoformat(),
                    "end_date": dag_run.end_date.isoformat() if dag_run.end_date else None,
                    "state": dag_run.get_state()
                   }
               }}
    requests.post(alvin_backend_metadata_url, json=payload, headers={"X-API-KEY": ALVIN_BACKEND_API_KEY})
