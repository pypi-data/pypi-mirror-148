from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import List

from bigeye_sdk.decorators.dataclass_decorators import add_from_dict
from bigeye_sdk.log import get_logger

# create logger
from bigeye_sdk.model.enums import SimpleMetricType
from bigeye_sdk.functions.metric_functions import get_notification_channels, get_thresholds_for_metric, \
    get_freshness_metric_name_for_field, is_freshness_metric, enforce_lookback_type_defaults, \
    get_seconds_from_window_size, table_has_metric_time
from bigeye_sdk.generated.com.torodata.models.generated import TimeIntervalType, TimeInterval, MetricParameter, \
    MetricConfiguration, LookbackType, Threshold, Table

log = get_logger(__file__)


@dataclass
class SimpleUpsertMetricRequest:
    schema_name: str
    table_name: str
    column_name: str
    metric_template: SimpleMetricTemplate = None
    from_metric: int = None

    def build_upsert_request_object(self, target_table: Table):
        return self.metric_template.build_upsert_request_object(target_table=target_table,
                                                                column_name=self.column_name,
                                                                existing_metric=None)

    @classmethod
    def from_dict(cls, d: dict) -> SimpleUpsertMetricRequest:
        [cls_params, smt_params] = map(lambda keys: {x: d[x] for x in keys if x in d},
                                       [inspect.signature(cls).parameters,
                                        inspect.signature(SimpleMetricTemplate).parameters])

        cls_params["metric_template"] = SimpleMetricTemplate.from_dict(smt_params) if smt_params \
            else SimpleMetricTemplate.from_dict(cls_params["metric_template"])
        return cls(**cls_params)


@dataclass
@add_from_dict
class SimpleMetricTemplate:
    """
    Provides a simple, string based metric template for interacting with the Bigeye API.
    """
    metric_name: str  # system metric name (name of the predefined metric or the name of the template)
    user_defined_metric_name: str = None  # user defined name of metric.  Defaults to system metric name.
    metric_type: SimpleMetricType = SimpleMetricType.PREDEFINED  # the actual metric type
    notifications: List[str] = field(default_factory=lambda: [])
    thresholds: List[Threshold] = field(default_factory=lambda: [])
    filters: List[str] = field(default_factory=lambda: [])
    group_by: List[str] = field(default_factory=lambda: [])
    default_check_frequency_hours: int = 2
    update_schedule: str = None  # cron schedule.
    delay_at_update: str = "0 minutes"
    timezone: str = "UTC"
    should_backfill: bool = False
    lookback_type: str = None
    lookback_days: int = 2
    window_size: str = "1 day"
    window_size_seconds = get_seconds_from_window_size(window_size)

    def __post_init__(self):
        if self.user_defined_metric_name is None:
            # Default the user_defined_metric_name to the system metric name.
            self.user_defined_metric_name = self.metric_name

        self.lookback_type = enforce_lookback_type_defaults(predefined_metric_name=self.metric_name,
                                                            lookback_type=self.lookback_type)

    def build_upsert_request_object(self,
                                    target_table: Table,  # TODO: Consider ways to switch to Table object or other object.
                                    column_name: str = None,
                                    existing_metric: MetricConfiguration = None) -> MetricConfiguration:
        """
        Converts a SimpleMetricTemplate to a MetricConfiguration that can be used to upsert a metric to Bigeye API.
        Must include either a column name or an existing metric

        TODO: Break out any remaining logic and unit test.  Currently the table dict makes this harder to test.

        :param warehouse_id:
        :param existing_metric: Pass the existing MetricConfiguration if updating
        :param target_table: The table object to which the metric will be deployed
        :param column_name: The column name to which the metric will be deployed.
        :return:
        """

        new_metric = MetricConfiguration()
        new_metric.name = self.user_defined_metric_name
        new_metric.schedule_frequency = TimeInterval(
            interval_type=TimeIntervalType.HOURS_TIME_INTERVAL_TYPE,
            interval_value=self.default_check_frequency_hours
        )

        new_metric.thresholds = get_thresholds_for_metric(self.metric_name, self.timezone, self.delay_at_update,
                                                          self.update_schedule, self.thresholds)

        new_metric.warehouse_id = target_table.warehouse_id

        new_metric.dataset_id = target_table.id

        metric_time_exists = table_has_metric_time(target_table)

        ifm = is_freshness_metric(self.metric_name)

        if ifm:
            # Enforce correct metric name for field type.
            new_metric.metric_type = get_freshness_metric_name_for_field(target_table, column_name)
            if self.update_schedule is None:
                raise Exception("Update schedule can not be null for freshness schedule thresholds")
        else:
            new_metric.metric_type = self.metric_type.factory(self.metric_name)

        new_metric.parameters = [MetricParameter(key="arg1", column_name=column_name)]

        new_metric.lookback = TimeInterval(interval_type=TimeIntervalType.DAYS_TIME_INTERVAL_TYPE,
                                           interval_value=self.lookback_days)

        new_metric.notification_channels = get_notification_channels(self.notifications)

        new_metric.filters = self.filters

        new_metric.group_bys = self.group_by

        if metric_time_exists:
            new_metric.lookback_type = LookbackType.from_string(self.lookback_type)
            if self.lookback_type == "METRIC_TIME_LOOKBACK_TYPE":
                new_metric.grain_seconds = self.window_size_seconds

        # Update existing metric if it exists.  Currently only supports certain updates???
        if existing_metric is None:
            return new_metric
        else:
            existing_metric.name = new_metric.name
            existing_metric.thresholds = new_metric.thresholds
            existing_metric.notification_channels = new_metric.notification_channels if new_metric.notification_channels else []
            existing_metric.schedule_frequency = new_metric.schedule_frequency
            if not ifm and metric_time_exists:
                existing_metric.lookback_type = new_metric.lookback_type
                existing_metric.lookback = new_metric.lookback
                existing_metric.grain_seconds = new_metric.grain_seconds
            return existing_metric
