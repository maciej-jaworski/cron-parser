#!/usr/bin/env python3

import re
import sys


class InvalidCRON(Exception):
    pass


class Patterns:
    ALL = re.compile(r"\*")
    STEP_EVERY = re.compile(r"\*/(?P<step>[1-9]\d*)")
    SPECIFIC_NUMBERS = re.compile(r"\d+(,\d+)*")
    RANGE_WITH_OPTIONAL_STEP = re.compile(r"(?P<start>\d+)\-(?P<end>\d+)(/(?P<step>[1-9]\d*))?")


def expand_time_component(component: str, max_value: int, min_value: int = 0):
    if Patterns.ALL.fullmatch(component):
        return list(range(min_value, max_value + 1))

    if Patterns.SPECIFIC_NUMBERS.fullmatch(component):
        results = []
        for number in component.split(","):
            number = int(number)
            if number > max_value or number < min_value:
                raise InvalidCRON

            results.append(number)
        return list(sorted(results))

    step_every_match = Patterns.STEP_EVERY.fullmatch(component)
    if step_every_match:
        number = int(step_every_match.group("step"))
        if number < max_value:
            return list(range(min_value, max_value + 1, number))

    range_match = Patterns.RANGE_WITH_OPTIONAL_STEP.fullmatch(component)
    if range_match:
        start = int(range_match.group("start"))
        end = int(range_match.group("end"))
        if min_value <= start <= end <= max_value:
            step = int(range_match.group("step") or 1)
            if step <= end:
                return list(range(start, end + 1, step))

    raise InvalidCRON


def format_cron(cron_expression: str, field_name_padding=14):
    try:
        [
            cron_minute,
            cron_hour,
            cron_day_of_month,
            cron_month,
            cron_day_of_week,
            *command_components,
        ] = cron_expression.split()
    except ValueError:
        raise InvalidCRON

    days_of_week = expand_time_component(cron_day_of_week, 7, min_value=1)
    months = expand_time_component(cron_month, 12, min_value=1)
    days_of_month = expand_time_component(cron_day_of_month, 31, min_value=1)
    hours = expand_time_component(cron_hour, 23, min_value=0)
    minutes = expand_time_component(cron_minute, 59, min_value=0)

    return "\n".join(
        [
            f"{'minute'.ljust(field_name_padding)}{' '.join(map(str, minutes))}",
            f"{'hour'.ljust(field_name_padding)}{' '.join(map(str, hours))}",
            f"{'day of month'.ljust(field_name_padding)}{' '.join(map(str, days_of_month))}",
            f"{'month'.ljust(field_name_padding)}{' '.join(map(str, months))}",
            f"{'day of week'.ljust(field_name_padding)}{' '.join(map(str, days_of_week))}",
            f"{'command'.ljust(field_name_padding)}{' '.join(map(str, command_components))}",
        ]
    )


if __name__ == "__main__":
    input_string = sys.argv[-1]
    try:
        print(format_cron(input_string))
    except InvalidCRON:
        print(f"ERROR: {input_string} is not a valid CRON string", file=sys.stderr)
