import json
from time import sleep

import requests
from requests import PreparedRequest, exceptions as requests_exceptions
import pendulum

from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook

class FivetranHook(BaseHook):
    conn_name_attr = 'fivetran_conn_id'
    conn_type = 'http'
    hook_name = 'Fivetran'
    api_user_agent = 'airflow_provider_fivetran/python2'
    api_protocol = 'https'
    api_host = 'api.fivetran.com'
    api_path_connectors = 'v1/connectors/'
    def __init__(
        self,
        fivetran_conn_id = "fivetran_default",
        fivetran_conn = None,
        timeout_seconds = 180,
        retry_limit = 3,
        retry_delay = 1.0,
    ):
        #super().__init__(None)
        self.conn_id = fivetran_conn_id
        self.fivetran_conn = self.get_connection(fivetran_conn_id)
        self.timeout_seconds = timeout_seconds
        if retry_limit < 1:
            raise ValueError("Retry limit must be greater than equal to 1")
        self.retry_limit = retry_limit
        self.retry_delay = retry_delay

    def _do_api_call(self, endpoint_info, json=None):
        method, endpoint = endpoint_info
        if self.fivetran_conn is None:
            self.fivetran_conn = self.get_connection(self.conn_id)
        auth = (self.fivetran_conn.login, self.fivetran_conn.password)
        url = self.api_protocol + '://' + self.api_host + '/' + endpoint
        headers = {
            "User-Agent": self.api_user_agent
        }
        if method == "GET":
            request_func = requests.get
        elif method == "POST":
            request_func = requests.post
        elif method == "PATCH":
            request_func = requests.patch
            headers.update({"Content-Type": "application/json;version=2"})
        else:
            raise AirflowException("Unexpected HTTP Method: " + method)
        attempt_num = 1
        while True:
            try:
                response = request_func(
                    url,
                    data=json if method in ("POST", "PATCH") else None,
                    params=json if method in ("GET") else None,
                    auth=auth,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except requests_exceptions.RequestException as e:
                if not _retryable_error(e):
                    # In this case, the user probably made a mistake.
                    # Don't retry.
                    raise AirflowException(
                        "Response: " + e.response.content + "\n" + 
                        "Status Code: " + str(e.response.status_code)
                    )
                self._log_request_error(attempt_num, e)
            if attempt_num == self.retry_limit:
                raise AirflowException(
                    "API request to Fivetran failed " + self.retry_limit + " times." + "\n" +
                    "Giving up."
                )
            attempt_num += 1
            sleep(self.retry_delay)

    def _log_request_error(self, attempt_num, error):
        self.log.error(
            "Attempt %s API Request to Fivetran failed with reason: %s",
            attempt_num,
            error,
        )

    def _connector_ui_url(self, service_name, schema_name):
        return (
            "https://fivetran.com/dashboard/connectors/" + service_name + "/" + schema_name
        )

    def _connector_ui_url_logs(self, service_name, schema_name):
        return self._connector_ui_url(service_name, schema_name) + "/logs"

    def _connector_ui_url_setup(self, service_name, schema_name):
        return self._connector_ui_url(service_name, schema_name) + "/setup" 

    def get_connector(self, connector_id):
        if connector_id == "":
            raise ValueError("No value specified for connector_id")
        endpoint = self.api_path_connectors + connector_id
        resp = self._do_api_call(("GET", endpoint))
        return resp["data"]

    def check_connector(self, connector_id):
        connector_details = self.get_connector(connector_id)
        service_name = connector_details["service"]
        schema_name = connector_details["schema"]
        setup_state = connector_details["status"]["setup_state"]
        if setup_state != "connected":
            raise AirflowException(
                "Fivetran connector " + connector_id + " not correctly configured, " + "\n" +
                "status: " + setup_state + "\nPlease see: " + "\n" +
                self._connector_ui_url_setup(service_name, schema_name)
            )
        self.log.info(
            "Connector type: " + service_name + ", connector schema: " + schema_name
        )
        self.log.info(
            "Connectors logs at " + self._connector_ui_url_logs(service_name, schema_name)
        )
        return True

    def set_schedule_type(self, connector_id, schedule_type):
        endpoint = self.api_path_connectors + connector_id
        return self._do_api_call(
            ("PATCH", endpoint),
            json.dumps({"schedule_type": schedule_type})
        )

    def prep_connector(self, connector_id, schedule_type):
        self.check_connector(connector_id)
        if schedule_type not in {"manual", "auto"}:
            raise ValueError('schedule_type must be either "manual" or "auto"')
        if self.get_connector(connector_id)['schedule_type'] != schedule_type:
            return self.set_schedule_type(connector_id, schedule_type)
        return True

    def start_fivetran_sync(self, connector_id):
        endpoint = self.api_path_connectors + connector_id + "/force"
        return self._do_api_call(("POST", endpoint))

    def start_fivetran_resync(self, connector_id):
        endpoint = self.api_path_connectors + connector_id + "/schemas/tables/resync"
        return self._do_api_call(("POST", endpoint))

    def get_last_sync(self, connector_id):
        connector_details = self.get_connector(connector_id)
        succeeded_at = self._parse_timestamp(connector_details["succeeded_at"])
        failed_at = self._parse_timestamp(connector_details["failed_at"])
        return succeeded_at if succeeded_at > failed_at else failed_at

    def get_sync_status(self, connector_id, previous_completed_at):
        connector_details = self.get_connector(connector_id)
        succeeded_at = self._parse_timestamp(connector_details["succeeded_at"])
        failed_at = self._parse_timestamp(connector_details["failed_at"])
        current_completed_at = (
            succeeded_at if succeeded_at > failed_at else failed_at
        )
        if failed_at > previous_completed_at:
            service_name = connector_details["service"]
            schema_name = connector_details["schema"]
            raise AirflowException(
                "Fivetran sync for connector " + connector_id + " failed; " + "\n" +
                "please see logs at " + "\n" +
                self._connector_ui_url_logs(service_name, schema_name)
            )
        sync_state = connector_details["status"]["sync_state"]
        self.log.info("Connector " + connector_id + ": sync_state = " + sync_state)
        if current_completed_at > previous_completed_at:
            self.log.info('Connector "{}": succeeded_at: {}'.format(
                connector_id, succeeded_at.to_iso8601_string())
            )
            return True
        else:
            return False

    def _parse_timestamp(self, api_time):
        return (
            pendulum.parse(api_time)
            if api_time is not None
            else pendulum.from_timestamp(-1)
        )

def _retryable_error(exception):
    return (
        isinstance(
            exception,
            (requests_exceptions.ConnectionError, requests_exceptions.Timeout),
        )
        or exception.response is not None
        and exception.response.status_code >= 500
    )
