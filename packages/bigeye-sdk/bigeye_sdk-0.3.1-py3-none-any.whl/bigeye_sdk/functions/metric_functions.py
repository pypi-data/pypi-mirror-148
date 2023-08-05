from __future__ import annotations

import datetime
import logging
from typing import List, Union

from bigeye_sdk.log import get_logger
from bigeye_sdk.generated.com.torodata.models.generated import Threshold, NotificationChannel, MetricRunFailureReason, \
    ForecastModelType, MetricInfo, MetricConfiguration, MetricParameter, MetricType
from bigeye_sdk.class_ext.enum_ext import EnumExtension
from bigeye_sdk.model.enums import SimpleMetricType

log = get_logger(__file__)


def filter_metrics_by_table_ids(metrics: List[dict], table_ids: List[int]) -> List[dict]:
    log.info('Filtering Metric IDs')
    return [d for d in metrics if d['datasetId'] in table_ids]


def get_metric_ids(metrics: List[dict]) -> List[int]:
    metric_ids = [d['metricConfiguration']['id'] for d in metrics]
    return metric_ids


def table_has_metric_time(table: dict):
    # TODO: Switch to using Table class.
    for field_key, field in table["fields"].items():
        if field["metricTimeField"]:
            return True
    return False


def is_freshness_metric(metric_name: str) -> bool:
    return "HOURS_SINCE_MAX" in metric_name


def is_same_metric(metric: MetricConfiguration, metric_name: str, user_defined_name: str,
                   group_by: List[str], filters: List[str]) -> bool:
    both_freshness_metrics = is_freshness_metric(metric.metric_type.predefined_metric.metric_name.name) \
                             and is_freshness_metric(metric_name)
    has_same_user_def_name = metric.name == user_defined_name
    is_same_type = SimpleMetricType.get_metric_name(metric.metric_type) == metric_name
    same_group_by = [i.lower() for i in metric.group_bys] == [i.lower() for i in group_by]
    same_filters = [i.lower() for i in metric.filters] == [i.lower() for i in filters]
    return (is_same_type or both_freshness_metrics) and has_same_user_def_name and same_filters and same_group_by

    # Deprecated code:
    # keys = ["metricType", "predefinedMetric", "metricName"]
    # result = reduce(lambda val, key: val.get(key) if val else None, keys, metric)
    # if result is None:
    #     return False

    # return result is not None and (result == metric_name or both_metrics_freshness) \
    #        and same_group_by and same_filters


def get_column_name(metric: MetricConfiguration) -> str:
    i: MetricParameter
    for i in metric.parameters:
        if i.key == 'arg1':
            return i.column_name


def is_same_column_metric(metric: MetricConfiguration, column_name):
    return get_column_name(metric).lower() == column_name.lower


def get_proto_interval_type(interval_type):
    if "minute" in interval_type:
        return "MINUTES_TIME_INTERVAL_TYPE"
    elif "hour" in interval_type:
        return "HOURS_TIME_INTERVAL_TYPE"
    elif "weekday" in interval_type:
        return "WEEKDAYS_TIME_INTERVAL_TYPE"
    elif "day" in interval_type:
        return "DAYS_TIME_INTERVAL_TYPE"


def get_max_hours_from_cron(cron):
    cron_values = cron.split(" ")
    hours = cron_values[1]
    if hours == "*":
        return 0
    return int(hours.split(",")[-1])


def get_days_since_n_weekdays(start_date, n):
    days_since_last_business_day = 0
    weekday_ordinal = datetime.date.weekday(start_date - datetime.timedelta(days=n))
    # 5 is Saturday, 6 is Sunday
    if weekday_ordinal >= 5:
        days_since_last_business_day = 2
    return days_since_last_business_day


def get_notification_channels(notifications: List[str]) -> List[NotificationChannel]:
    channels = []
    for n in notifications:
        if n.startswith('#') or n.startswith('@'):
            channels.append(NotificationChannel.from_dict({"slackChannel": n}))
        elif '@' in n and '.' in n:
            channels.append(NotificationChannel.from_dict({"email": n}))
    return channels


def get_freshness_metric_name_for_field(table: dict, column_name: str) -> MetricType:
    # TODO: Convert tu using Table objects.
    for fk, f in table["fields"].items():
        if f.get("fieldName").lower() == column_name.lower():
            if f.get("type") == "TIMESTAMP_LIKE":
                return SimpleMetricType.PREDEFINED.factory("HOURS_SINCE_MAX_TIMESTAMP")
            elif f.get("type") == "DATE_LIKE":
                return SimpleMetricType.PREDEFINED.factory("HOURS_SINCE_MAX_DATE")


def get_file_name_for_metric(m: MetricInfo):
    mc = m.metric_configuration
    md = m.metric_metadata
    return f"{'_'.join(md.schema_name.split('.'))}_{md.dataset_name}_{md.field_name}_{mc.name.replace(' ', '_')}.json"


def is_auto_threshold(t: Threshold) -> bool:
    return "autoThreshold" in t.to_dict()


def has_auto_threshold(ts: List[Threshold]) -> bool:
    for t in ts:
        if "autoThreshold" in t.to_dict():
            return True
    return False


def set_default_model_type_for_threshold(thresholds: List[Threshold]) -> List[Threshold]:
    for t in thresholds:
        if is_auto_threshold(t):
            if not t.auto_threshold.model_type:
                t.auto_threshold.model_type = ForecastModelType.BOOTSTRAP_THRESHOLD_MODEL_TYPE

    return thresholds


def get_thresholds_for_metric(metric_name, timezone, delay_at_update,
                              update_schedule, thresholds: List[Threshold]) -> List[Threshold]:
    if thresholds:
        return thresholds
    # Current path for freshness
    if is_freshness_metric(metric_name):
        tj = {
            "freshnessScheduleThreshold": {
                "bound": {
                    "boundType": "UPPER_BOUND_SIMPLE_BOUND_TYPE",
                    "value": -1
                },
                "cron": update_schedule,
                "timezone": timezone,
                "delayAtUpdate": get_time_interval_for_delay_string(delay_at_update,
                                                                    metric_name,
                                                                    update_schedule)
            }
        }
        return [Threshold().from_dict(tj)]
    # Default to autothresholds
    return [
        Threshold().from_dict({"autoThreshold": {"bound": {"boundType": "LOWER_BOUND_SIMPLE_BOUND_TYPE", "value": -1.0},
                                                 "modelType": "BOOTSTRAP_THRESHOLD_MODEL_TYPE"}}),
        Threshold().from_dict({"autoThreshold": {"bound": {"boundType": "UPPER_BOUND_SIMPLE_BOUND_TYPE", "value": -1.0},
                                                 "modelType": "BOOTSTRAP_THRESHOLD_MODEL_TYPE"}})
    ]


def get_time_interval_for_delay_string(delay_at_update, metric_type, update_schedule):
    split_input = delay_at_update.split(" ")
    interval_value = int(split_input[0])
    interval_type = get_proto_interval_type(split_input[1])
    if metric_type == "HOURS_SINCE_MAX_DATE":
        hours_from_cron = get_max_hours_from_cron(update_schedule)
        if interval_type == "HOURS_TIME_INTERVAL_TYPE" or interval_type == "MINUTES_TIME_INTERVAL_TYPE":
            logging.warning("Delay granularity for date column must be in days, ignoring value")
            interval_type = "HOURS_TIME_INTERVAL_TYPE"
            interval_value = hours_from_cron
        elif interval_type == "WEEKDAYS_TIME_INTERVAL_TYPE":
            lookback_weekdays = interval_value + 1 if datetime.datetime.utcnow().hour <= hours_from_cron \
                else interval_value
            logging.info("Weekdays to look back {}".format(lookback_weekdays))
            days_since_last_business_day = get_days_since_n_weekdays(datetime.date.today(), lookback_weekdays)
            logging.info("total days to use for delay {}".format(days_since_last_business_day))
            interval_type = "HOURS_TIME_INTERVAL_TYPE"
            interval_value = (days_since_last_business_day + lookback_weekdays) * 24 + hours_from_cron
        else:
            interval_type = "HOURS_TIME_INTERVAL_TYPE"
            interval_value = interval_value * 24 + hours_from_cron
    return {
        "intervalValue": interval_value,
        "intervalType": interval_type
    }


def is_failed(datum: dict) -> bool:
    if 'latestMetricRuns' in datum and datum['latestMetricRuns']:
        if 'failureReason' in datum['latestMetricRuns'][-1]:
            failure_reason = datum['latestMetricRuns'][-1]['failureReason']
            log.info(failure_reason)
            return failure_reason in MetricRunFailureReason

    return False


def get_failed_code(datum: dict) -> Union[None, str]:
    if 'latestMetricRuns' in datum and datum['latestMetricRuns']:
        if 'failureReason' in datum['latestMetricRuns'][-1]:
            failure_reason = datum['latestMetricRuns'][-1]['failureReason']
            log.info(failure_reason)
            return failure_reason

    return None


def get_seconds_from_window_size(window_size):
    if window_size == "1 day":
        return 86400
    elif window_size == "1 hour":
        return 3600
    else:
        raise Exception("Can only set window size of '1 hour' or '1 day'")


class MetricTimeNotEnabledStats(EnumExtension):
    HOURS_SINCE_MAX_TIMESTAMP = 'HOURS_SINCE_MAX_TIMESTAMP'
    HOURS_SINCE_MAX_DATE = 'HOURS_SINCE_MAX_DATE'
    PERCENT_DATE_NOT_IN_FUTURE = 'PERCENT_DATE_NOT_IN_FUTURE'
    PERCENT_NOT_IN_FUTURE = 'PERCENT_NOT_IN_FUTURE'
    COUNT_DATE_NOT_IN_FUTURE = 'COUNT_DATE_NOT_IN_FUTURE'


def is_metric_time_enabled(predefined_metric_name: str):
    return predefined_metric_name.upper() in MetricTimeNotEnabledStats.list()


def enforce_lookback_type_defaults(predefined_metric_name: str, lookback_type: str) -> str:
    if is_metric_time_enabled(predefined_metric_name=predefined_metric_name):
        return 'DATE_TIME_LOOKBACK'
    elif lookback_type is None:
        return "METRIC_TIME_LOOKBACK_TYPE"
    else:
        return lookback_type
