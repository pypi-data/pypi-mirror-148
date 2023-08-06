from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

from fivetran_provider.hooks.fivetran import FivetranHook

class FivetranSensor(BaseSensorOperator):

    template_fields = ["connector_id"]

    @apply_defaults
    def __init__(
        self,
        connector_id,
        fivetran_conn_id = "fivetran",
        poke_interval = 60,
        fivetran_retry_limit = 3,
        fivetran_retry_delay = 1,
        **kwargs
    ):
        super(FivetranSensor, self).__init__(**kwargs)
        self.fivetran_conn_id = fivetran_conn_id
        self.connector_id = connector_id
        self.poke_interval = poke_interval
        self.previous_completed_at = None
        self.fivetran_retry_limit = fivetran_retry_limit
        self.fivetran_retry_delay = fivetran_retry_delay
        self.hook = None

    def _get_hook(self):
        if self.hook is None:
            self.hook = FivetranHook(
                self.fivetran_conn_id,
                retry_limit=self.fivetran_retry_limit,
                retry_delay=self.fivetran_retry_delay,
            )
        return self.hook

    def poke(self, context):
        hook = self._get_hook()
        if self.previous_completed_at is None:
            self.previous_completed_at = hook.get_last_sync(self.connector_id)
        return hook.get_sync_status(self.connector_id, self.previous_completed_at)
