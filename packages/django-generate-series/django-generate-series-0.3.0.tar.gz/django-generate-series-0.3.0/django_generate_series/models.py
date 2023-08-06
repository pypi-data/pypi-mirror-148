import decimal
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Type, Union

import django
from django.contrib.postgres import fields as pg_models
from django.db import models
from django.db.models import Field
from django.db.models.sql import Query
from django.utils.timezone import datetime as datetimetz

from django_generate_series.base import NoEffectManager, NoEffectQuerySet
from django_generate_series.exceptions import ModelFieldNotSupported

INTERVAL_UNITS = (
    "century",
    "centuries",
    "day",
    "days",
    "decade",
    "decades",
    "hour",
    "hours",
    "microsecond",
    "microseconds",
    "millennium",
    "millennia",
    "millenniums",
    "millisecond",
    "milliseconds",
    "minute",
    "minutes",
    "month",
    "months",
    "second",
    "seconds",
    "week",
    "weeks",
    "year",
    "years",
)


@dataclass
class Params:
    start: Union[int, date, datetime, datetimetz]
    stop: Union[int, date, datetime, datetimetz]
    step: Optional[Union[int, str]] = None


class AbstractBaseSeriesModel(models.Model):
    class Meta:
        abstract = True


class GenerateSeriesQuery(Query):
    def __init__(self, *args, _series_func=None, _series_func_params=None, **kwargs):
        self._series_func = _series_func
        self._series_func_params = _series_func_params
        return super().__init__(*args, **kwargs)

    def get_compiler(self, *args, **kwargs):
        compiler = super().get_compiler(*args, **kwargs)
        get_from_clause_method = compiler.get_from_clause

        def get_from_clause_wrapper(*args, **kwargs):
            source = self._series_func(self.model)
            result, params = get_from_clause_method(*args, **kwargs)
            wrapper = source.raw_query
            result[0] = f"{wrapper} AS {tuple(compiler.query.alias_map)[0]}"
            params = (source.params.start, source.params.stop, source.params.step or 1) + tuple(params)

            return result, params

        compiler.get_from_clause = get_from_clause_wrapper
        return compiler


class GenerateSeriesQuerySet(NoEffectQuerySet):
    def __init__(self, *args, query=None, _series_func=None, _series_func_params=None, **kwargs):
        empty_query = query is None
        r = super().__init__(*args, query=query, **kwargs)
        if empty_query:
            self.query = GenerateSeriesQuery(
                self.model,
                _series_func=_series_func,
                _series_func_params=_series_func_params,
            )
        return r


class GenerateSeriesManager(NoEffectManager):
    """Custom manager for creating series"""

    class FromRaw:
        def __init__(self, model: AbstractBaseSeriesModel = None, params: Params = None):
            self.term = type(model._meta.get_field("term"))
            self.params = params
            self.range = False
            self.field_type = int

            # Verify the input params match for the type of model field used

            if issubclass(self.term, (models.DecimalField, pg_models.DecimalRangeField)):
                self.check_params(
                    start_type=[int, Decimal],
                    stop_type=[int, Decimal],
                    step_type=[int, Decimal],
                )
                self.field_type = decimal.Decimal

            elif issubclass(self.term, (models.DateField, pg_models.DateRangeField)):
                self.check_params(
                    start_type=[date],
                    stop_type=[date],
                    step_type=[str],
                )
                self.field_type = datetime.date

            elif issubclass(self.term, (models.DateTimeField, pg_models.DateTimeRangeField)):
                self.check_params(
                    start_type=[datetime, datetimetz],
                    stop_type=[datetime, datetimetz],
                    step_type=[str],
                )
                self.field_type = datetimetz

            elif issubclass(
                self.term,
                (
                    models.BigIntegerField,
                    models.IntegerField,
                    pg_models.BigIntegerRangeField,
                    pg_models.IntegerRangeField,
                ),
            ):
                self.check_params(
                    start_type=[int],
                    stop_type=[int],
                    step_type=[int],
                )

                if issubclass(self.term, (models.BigIntegerField, pg_models.BigIntegerRangeField)):
                    self.field_type = "BigInteger"  # ToDo: Find a better way to standarize self.field_type

            else:
                raise ModelFieldNotSupported("Invalid model field type used to generate series")

            if issubclass(
                self.term,
                (
                    pg_models.BigIntegerRangeField,
                    pg_models.IntegerRangeField,
                    pg_models.DecimalRangeField,
                    pg_models.DateRangeField,
                    pg_models.DateTimeRangeField,
                ),
            ):
                self.range = True

            self.raw_query = f"({self.get_raw_query()})"

        def get_raw_query(self):
            if self.range:

                if self.field_type is datetimetz:
                    sql = """
                        SELECT
                            row_number() over () as id,
                            "term"
                        FROM
                            (
                                SELECT tstzrange((lag(a) OVER()), a, '[)') AS term
                                FROM generate_series(timestamptz %s, timestamptz %s, interval %s)
                                AS a OFFSET 1
                            ) AS subquery
                    """
                elif self.field_type == datetime.date:
                    sql = """
                        SELECT
                            row_number() over () as id,
                            "term"
                        FROM
                            (
                                SELECT daterange((lag(a.n) OVER()), a.n, '[)') AS term
                                FROM (
                                    SELECT generate_series(date %s, date %s, interval %s)::date
                                    AS n)
                                AS a OFFSET 1
                            ) AS seriesquery
                    """
                elif self.field_type is decimal.Decimal:
                    sql = """
                        SELECT
                            row_number() over () as id,
                            "term"
                        FROM
                            (
                                SELECT numrange(a, a + 1) AS term
                                FROM generate_series(%s, %s, %s) a
                            ) AS seriesquery
                    """
                elif self.field_type == "BigInteger":
                    sql = """
                        SELECT
                            row_number() over () as id,
                            "term"
                        FROM
                            (
                                SELECT int8range(a, a + 1) AS term
                                FROM generate_series(%s, %s, %s) a
                            ) AS subquery
                    """
                else:
                    # ToDo: Instead of `a + 1`, we could make possible other options as well
                    sql = """
                        SELECT
                            row_number() over () as id,
                            "term"
                        FROM
                            (
                                SELECT int4range(a, a + 1) AS term
                                FROM generate_series(%s, %s, %s) a
                            ) AS seriesquery
                    """
            else:
                sql = """
                    SELECT
                        row_number() over () as id,
                        "term"
                    FROM
                        (
                        SELECT
                            generate_series(%s, %s, %s) term
                        ) AS seriesquery
                """

            return sql

        def check_params(
            self,
            start_type: List[Union[Type[int], Type[decimal.Decimal], Type[date], Type[datetime], Type[datetimetz]]],
            stop_type: List[Union[Type[int], Type[decimal.Decimal], Type[date], Type[datetime], Type[datetimetz]]],
            step_type: List[Union[Type[int], Type[decimal.Decimal], Type[str]]],
        ):

            # Check that `start`, `stop`, and `step` are the correct type
            # if not any(issubclass(type(self.params.start), item) for item in start_type):
            #     raise ValueError(f"Start type of {start_type} expected, but received type {type(self.params.start)}")
            # if not any(issubclass(type(self.params.stop), item) for item in stop_type):
            #     raise ValueError(f"Stop type of {stop_type} expected, but received type {type(self.params.stop)}")
            # if self.params.step is not None and not any(
            #     issubclass(type(self.params.step), item) for item in step_type
            # ):
            #     raise ValueError(f"Step type of {step_type} expected, but received type {type(self.params.step)}")

            # Check that stop is larger than start
            if not self.params.start < self.params.stop:
                raise ValueError(f"Start value must be smaller than stop value")

            # Only numeric series can use just `start` & `stop`. Other types also need `step`
            if self.params.step is None and not isinstance(self.params.start, int):
                raise Exception(f"Step must be provided for non-integer series")

            # If step is a str, make sure it is formatted correctly
            #   Starting with a numeric value, then a space, and then a valid interval unit
            if isinstance(self.params.step, str):
                try:
                    interval, interval_unit = self.params.step.split()
                except ValueError:
                    raise Exception(
                        "Incorrect number of values for series step string. "
                        "Should be a numeric value, a space, and an interval type."
                    )

                try:
                    interval = float(interval)
                except ValueError:
                    raise ValueError("Invalid interval value. Must be capable of being converted to a numeric type.")

                if not interval_unit in INTERVAL_UNITS:
                    raise Exception("Invalid interval unit")

    # def generate_series(self, params: Params = None):
    def generate_series(self, params: Union[tuple, list, Params] = None):

        # Convert params to a Params dataclass, if needed
        if not isinstance(params, Params):
            params = Params(*params)

        # def series_func(cls, *args):
        def series_func(cls):
            model = self.model
            return self.FromRaw(model, params)

        return GenerateSeriesQuerySet(self.model, using=self._db, _series_func=series_func, _series_func_params=params)


def get_series_model(
    model_field: Field = None,
    max_digits: Optional[Union[int, None]] = None,
    decimal_places: Optional[Union[int, None]] = None,
    default_bounds: Optional[Union[str, None]] = None,
) -> models.Model:

    if model_field is None:
        raise Exception("model_field must be provided")
    if not issubclass(
        model_field,
        (
            models.BigIntegerField,
            models.IntegerField,
            models.DecimalField,
            models.DateField,
            models.DateTimeField,
            pg_models.BigIntegerRangeField,
            pg_models.IntegerRangeField,
            pg_models.DecimalRangeField,
            pg_models.DateRangeField,
            pg_models.DateTimeRangeField,
        ),
    ):
        raise ModelFieldNotSupported("Invalid model field type used to generate series")

    # Limit default_bounds to valid string values
    if default_bounds not in ["[]", "()", "[)", "(]", None]:
        raise ValueError(f"Value of default_bounds must be one of: '[]', '()', '[)', '(]'")

    class SeriesModel(AbstractBaseSeriesModel):
        if (
            issubclass(
                model_field,
                (
                    pg_models.DecimalRangeField,
                    pg_models.DateRangeField,
                    pg_models.DateTimeRangeField,
                ),
            )
            and django.VERSION >= (4, 1)
            and default_bounds is not None
        ):
            # Versions of Django > 4.1 include support for defining default range bounds for
            #   Range fields other than those based on Integer, so use it if provided.
            term = model_field(default_bounds=default_bounds)

        elif issubclass(model_field, models.DecimalField):
            term = model_field(
                max_digits=max_digits,
                decimal_places=decimal_places,
            )
        else:
            term = model_field()

        objects = GenerateSeriesManager()

        class Meta:
            abstract = True
            managed = False

    return SeriesModel
