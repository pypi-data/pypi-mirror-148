from airflow.models import BaseOperator, BaseOperatorLink
from airflow.utils.decorators import apply_defaults

from fivetran_provider.hooks.fivetran import FivetranHook


class FivetranOperator(BaseOperator):
    template_fields = ["connector_id"]

    @apply_defaults
    def __init__(
        self,
        connector_id,
        run_name = None,
        timeout_seconds = None,
        fivetran_conn_id = "fivetran",
        fivetran_retry_limit = 3,
        fivetran_retry_delay = 1,
        poll_frequency = 15,
        schedule_type = "manual",
        **kwargs
    ):
        super(FivetranOperator, self).__init__(**kwargs)
        self.fivetran_conn_id = fivetran_conn_id
        self.fivetran_retry_limit = fivetran_retry_limit
        self.fivetran_retry_delay = fivetran_retry_delay
        self.connector_id = connector_id
        self.poll_frequency = poll_frequency
        self.schedule_type = schedule_type

    def _get_hook(self):
        return FivetranHook(
            self.fivetran_conn_id,
            retry_limit=self.fivetran_retry_limit,
            retry_delay=self.fivetran_retry_delay,
        )

    def execute(self, context):
        hook = self._get_hook()
        hook.prep_connector(self.connector_id, self.schedule_type)
        return hook.start_fivetran_sync(self.connector_id)
