from functools import reduce
from operator import or_
from datetime import timedelta
import json

from django.conf import settings
from django.utils import timezone

from django.db.models import Q


from . import models


QUARTERLY = "quarterly"
ANNUAL = "annual"
MONTHLY = "monthly"

CREDIT_UNION = "credit_union"
BENCHMARK = "benchmark"
PERIODS = {
    QUARTERLY: ["q1", "q2", "q3", "q4"],
    ANNUAL: ["total"],
    MONTHLY: [
        "m01",
        "m02",
        "m03",
        "m04",
        "m05",
        "m06",
        "m07",
        "m08",
        "m09",
        "m10",
        "m11",
        "m12",
    ],
}
COMPETITORS = "competitors"
SERIES_QUERY_POSITIONS = ["series_type", "entity_subtype", "entity_subtype_id"]


def get_as_int(dict_request, key, default=None):
    try:
        return int(dict_request.get(key, default))
    except Exception:
        return default


def get_base_filters(dict_request):
    """Global keyword that come from the queryset."""
    now = timezone.now()
    period = get_period(dict_request)
    start_year = get_as_int(dict_request, "start_year", now.year - 1)
    end_year = get_as_int(dict_request, "end_year", now.year)
    return {"start_year": start_year, "end_year": end_year, "period": period}


def get_base_filters_daily(dict_request, periods):
    daily_span = get_as_int(dict_request, "daily_span", 30)
    return {"daily_span": daily_span, "period": list(periods)}


def get_base_filters_query(base_filters):
    """Get the_base_filters for the DataSummary."""

    return {
        #"year__gte": base_filters["start_year"],
        #"year__lte": base_filters["end_year"],
        "year__range": (base_filters["start_year"],base_filters["end_year"]),
        "base_data_interval": base_filters["period"],
    }


def get_minium_date(base_filters):
    daily_span = base_filters["daily_span"]
    return (timezone.now() - timedelta(days=daily_span)).date()


def get_dates_for_daily(base_filters):
    min_date = get_minium_date(base_filters)
    daily_span = base_filters["daily_span"]
    return [min_date + timedelta(days=i) for i in range(1, daily_span + 1)]


def get_base_filters_daily_query(base_filters):
    date = get_minium_date(base_filters)
    return {
        "date__gte": date,
    }


def parse_query_series(dict_request, subtypes):
    """Parse the series parameter from the url"""
    try:
        series = dict_request.get("series", "")
        series_q = series.split(",")
        results = {"series": []}
        for series in series_q:
            parsed = series.split("__")
            if len(parsed) == 2:
                # Check if base competitors
                if parsed[0] == COMPETITORS:
                    results[COMPETITORS] = int(parsed[1])
                    continue
            if 2 <= len(parsed) <= 3:
                parsed = {SERIES_QUERY_POSITIONS[i]: j for i, j in enumerate(parsed)}
                if parsed["entity_subtype"] in subtypes:
                    results["series"].append(parsed)
        return results
    except Exception as e:
        print("parse_query_series failed", e)
    return {}


def base_chart_query(base_filters, entity_ids, series):
    """Default chart with entity id ans series."""
    """Base chart assuming there is an entity id and the entity_type is credit_union."""
    return Q(
        **{
            **base_filters,
            **{
                "entity_id__in": entity_ids,
                "entity_type": CREDIT_UNION,
                "series__in": series,
            },
        }
    )


def base_daily_query(base_filters, entity_ids, charts):
    return Q(
        **{
            **base_filters,
            **{
                "entity_id__in": entity_ids,
                "entity_type": CREDIT_UNION,
                "series__in": [c.name for c in charts],
            },
        }
    )


def benchmark_query(base_filters, benchmark_kwargs, chart_series):
    """Get the query for a benchmark value."""
    for field in SERIES_QUERY_POSITIONS:
        if not field in benchmark_kwargs:
            benchmark_kwargs[f"{field}__isnull"] = True
    return Q(
        **{
            **base_filters,
            **benchmark_kwargs,
            **{"entity_type": BENCHMARK, "series__in": chart_series},
        }
    )


def get_period(parameters):
    return parameters.get("period", "quarterly")


def get_year_rage(filters):
    return range(filters["start_year"], filters["end_year"] + 1)


def get_categories(filters, period):
    return [
        f"{year} {p.upper()}"
        for year in get_year_rage(filters)
        for p in PERIODS[period]
    ]


def get_charts_series(charts):
    """Get all the unique series from a chart."""
    return {s.name for c in charts for s in c.metrics.all()}


def get_chart_subtypes(charts):
    """Get all subtypes fo charts."""
    return {
        t
        for c in charts
        for s in c.metrics.all()
        if s.subtype
        for t in s.subtype.split(",")
    }


def get_competitors_ids(entity_id, limit):
    query = (
        models.Competitor.objects.filter(company__number=entity_id)
        .exclude(competitor__isnull=True)
        .values_list("competitor__number", flat=True)
        .distinct()[:limit]
    )
    return list(query)


def parse_request_kwargs(dict_request, charts, base_filters):
    """Parse the query args to a queryset that can be used by data summary"""
    entity_id = dict_request.get("entity_id", None)
    entity_type = dict_request.get("entity_type", CREDIT_UNION)
    base_filters_q = get_base_filters_query(base_filters)
    filters = []
    data_summaries_objects = list()

    chart_series = get_charts_series(charts)
    chart_subtypes = get_chart_subtypes(charts)
    query_series = parse_query_series(dict_request, chart_subtypes)

    benchmark_series = query_series["series"]
    if entity_id and entity_type == CREDIT_UNION:
        entity_ids = [entity_id]
        if COMPETITORS in query_series:
            entity_ids.extend(get_competitors_ids(entity_id, query_series[COMPETITORS]))
        filters.append(base_chart_query(base_filters_q, entity_ids, chart_series))
        for i in entity_ids:
            for j in chart_series:
                data_summaries_objects.append(
                    models.DataSummary(entity_type=CREDIT_UNION, entity_id=i, series=j)
                )
    if benchmark_series:
        filters.extend(
            [
                benchmark_query(base_filters_q, series_filter, chart_series)
                for series_filter in benchmark_series
            ]
        )
        for i in benchmark_series:
            for series in chart_series:
                data_summaries_objects.append(
                    models.DataSummary(
                        entity_type=BENCHMARK,
                        series=series,
                        **{
                            field: i[field]
                            for field in SERIES_QUERY_POSITIONS
                            if field in i
                        },
                    )
                )
    return filters, data_summaries_objects


def parse_daily_request_kwargs(dict_request, charts, base_filters):
    """Parse arguments for a Daily model."""
    entity_id = dict_request.get("entity_id", None)
    entity_type = dict_request.get("entity_type", CREDIT_UNION)
    chart_subtypes = get_chart_subtypes(charts)
    query_series = parse_query_series(dict_request, chart_subtypes)
    base_filters_q = get_base_filters_daily_query(base_filters)

    filters = []
    daily_objects = []

    if entity_id and entity_type == CREDIT_UNION:
        entity_ids = [entity_id]
        if COMPETITORS in query_series:
            entity_ids.extend(get_competitors_ids(entity_id, query_series[COMPETITORS]))
        filters.append(base_daily_query(base_filters_q, entity_ids, charts))
        for i in entity_ids:
            for j in charts:
                daily_objects.append(
                    models.Daily(entity_type=CREDIT_UNION, entity_id=i, series=j.name)
                )

    return filters, daily_objects


def is_specific(ds):
    return (
        ds.series_type
        and ds.entity_subtype
        and ds.entity_subtype_id
        and ds.entity_type == BENCHMARK
    )


def is_general(ds):
    return ds.series_type and ds.entity_subtype and ds.entity_type == BENCHMARK


def get_key(ds):
    """Key to uniquely recognize a data series."""
    if ds.entity_id and ds.entity_type == CREDIT_UNION:
        return ("plain", ds.entity_id, ds.series)
    elif is_specific(ds):
        return (
            "complex",
            ds.series_type,
            ds.entity_subtype,
            ds.entity_subtype_id,
            ds.series,
        )
    elif is_general(ds):
        return (
            "middle",
            ds.series_type,
            ds.entity_subtype,
            ds.series,
        )


def get_daily_key(ds):
    return (
        ds.entity_type,
        ds.series,
    )


def get_series_period_values(ds, period):
    """Get the period values for a series"""
    return [
        getattr(ds, sub_period, None) if ds else None for sub_period in PERIODS[period]
    ]


def get_series_name(ds, companies, daily=False):
    """Form a series get the expected name."""
    name = ds.series
    entity_id = str(ds.entity_id or "")
    if entity_id in companies:
        name += f" {companies[entity_id].name}"
    if not daily and is_general(ds):
        name += f" {': '.join([getattr(ds, field) for field in SERIES_QUERY_POSITIONS if getattr(ds, field,None)])}"
    return name.title()


def parse_data_summary_results_results(data_summary_results):
    results_by_year = {}
    series_by_key = {}
    for ds in data_summary_results:
        key = get_key(ds)
        results_by_year.setdefault(ds.year, {})
        results_by_year[ds.year][key] = ds
        series_by_key[key] = ds
    return results_by_year, series_by_key


def parse_daily_results(daily_results):
    results_by_chart = {}
    series_by_key = {}
    for d in daily_results:
        key = get_daily_key(d)
        results_by_chart.setdefault(key, {})
        results_by_chart[key][d.date] = d
        series_by_key[key] = d

    return results_by_chart, series_by_key


def get_series(
    results_by_year,
    series_by_key,
    keys,
    companies,
    base_filters,
    period,
    main_entity_id=None,
):

    series = {}
    for year in get_year_rage(base_filters):
        for key in keys:
            if key in series_by_key:
                ds = series_by_key[key]
                if not key in series:
                    series[key] = {
                        "name": get_series_name(series_by_key[key], companies),
                        "data": [],
                        "type": "column"
                        if ds.entity_type == CREDIT_UNION
                        and str(ds.entity_id) == str(main_entity_id)
                        else "line",
                    }
                current_ds = results_by_year.get(year, {}).get(key, None)
                series[key]["data"].extend(get_series_period_values(current_ds, period))

    return list(series.values())


def get_daily_series(
    daily_results_by_chart,
    dates,
    series_by_key,
    series_keys,
    companies,
    main_entity_id=None,
):
    series = {}
    for key in set(series_keys):
        ds = series_by_key[key]
        series[key] = {
            "name": get_series_name(ds, companies, daily=True),
            "data": [],
            "type": "column"
            if ds.entity_type == CREDIT_UNION
            and str(ds.entity_id) == str(main_entity_id)
            else "line",
        }
        if key in daily_results_by_chart:
            for date in dates:
                result = daily_results_by_chart[key].get(date, models.Daily(total=None))
                series[key]["data"].append(result.total)

    return list(series.values())


def get_chart_title(charts, dss_by_key, companies_dict):
    title = ",".join([i.name for i in charts])
    if len(dss_by_key) == 1:
        ds = dss_by_key[list(dss_by_key)[0]]
        if ds.entity_id in companies_dict:
            series = get_charts_series(charts)
            title = f"{' '.join(list(series)) : companies_dict[ds.entity_id]}"
    return title


def get_chart_data(
    base_filters, period, charts, series, dss_by_key, companies_dict, categories=None
):
    # Get the categories for the chart
    categories = categories or get_categories(base_filters, period)
    chart_data = (
        json.loads(charts[0].chartstyle.highcharts_style)
        if charts[0].chartstyle_id
        else {}
    )
    chart_data.setdefault("xAxis", {})
    chart_data["xAxis"]["categories"] = categories
    chart_data["series"] = series
    chart_data.setdefault("yAxis", {})
    chart_data["yAxis"]["title"] = {"text": "#"}
    if charts and charts[0].metrics.all():
        chart_data["yAxis"]["title"] = charts[0].metrics.all()[0].unit
    chart_data["colors"] = settings.DEFAULT_COLORS
    #chart_data["title"] = {"text": get_chart_title(charts, dss_by_key, companies_dict)}
    chart_data["timeframe"] = period
    chart_data.setdefault("chart", {})
    if len(charts) == 1 and charts[0].charttype_id:
        chart_data["chart"]["type"] = getattr(
            charts[0].charttype, "chart_type", "column"
        )
    return chart_data


def parse_charts_from_request(request_dict):
    default_keys = set()
    for key, value in request_dict.items():
        if "_" in key:
            key_sep = key.split("_")
            if not key_sep[-1].isnumeric():
                default_keys.add(key)
            else:
                default_keys.add("_".join(key_sep[: len(key_sep) - 1]))
        else:
            default_keys.add(key)

    values = []
    index = 1
    while True:
        value = dict()
        non_present = list()
        for key in default_keys:
            composed_key = f"{key}_{index}"
            if composed_key in request_dict:
                value[key] = request_dict[composed_key]
            elif key in request_dict:
                non_present.append(key)
        if not value:
            break
        else:
            for i in non_present:
                value[i] = request_dict[i]
            values.append(value)
        index += 1
    if len(values) == 0:
        values.append(request_dict)
    return values


def get_charts_ids(charts_parameters):
    charts_ids = set()
    for i in charts_parameters:
        if "chart_id" in i:
            charts_ids.update(i["chart_id"].split(","))
    return list(charts_ids)


def compare_ds(ds_1, ds_2):
    if ds_1.entity_type != ds_2.entity_type:
        return False
    if ds_1.entity_type == CREDIT_UNION:
        return ds_1.series == ds_2.series and str(ds_1.entity_id) == str(ds_2.entity_id)
    elif ds_1.entity_type == BENCHMARK:
        return all(
            [
                getattr(ds_1, field) == getattr(ds_2, field)
                for field in SERIES_QUERY_POSITIONS
            ]
            + [ds_1.series == ds_2.series]
        )
    return False


def data_summaries_objects_to_series_keys(
    series_by_key, data_summaries_objects, daily=False
):
    """Convert the filter to one of the results."""
    response = dict()
    for ds in data_summaries_objects:
        key = get_key(ds) if not daily else get_daily_key(ds)
        for key_f, ds_f in series_by_key.items():
            if compare_ds(ds, ds_f):
                response.setdefault(key, set())
                response[key].add(key_f)
                continue
    return response


def get_charts_sheets_types(charts):
    return {s.timeframe_type for c in charts for s in c.sheets.all()}


def get_chart_from_request(request_dict):
    # Parse query string so parameters with _1, _2 are correctly parsed
    charts_parameters = parse_charts_from_request(request_dict)
    chart_ids = get_charts_ids(charts_parameters)
    # Get the charts preloading important data
    charts = (
        models.Chart.objects.filter(pk__in=chart_ids)
        .prefetch_related("metrics", "sheets")
        .select_related("charttype", "chartstyle")
    )
    charts_by_pk = {str(c.pk): c for c in charts}

    filters = []
    filters_daily = []
    data_summaries_objects = []
    daily_summaries_objects = []

    for parameters in charts_parameters:
        # Get years and period as it will applies and used in several parts

        chart_pk = parameters["chart_id"]
        charts_p = [
            charts_by_pk[pk] for pk in chart_pk.split(",") if pk in charts_by_pk
        ]
        parameters["charts_p"] = charts_p
        parameters["daily"] = False

        charts_types = get_charts_sheets_types(charts_p)
        if len(charts_types) > 0:
            parameters["daily"] = True
            base_filters = get_base_filters_daily(parameters, charts_types)
            filters_parameters, daily_objects_kw = parse_daily_request_kwargs(
                parameters, charts_p, base_filters
            )
            parameters["base_filters"] = base_filters
            parameters["data_daily_objects"] = daily_objects_kw
            filters_daily.extend(filters_parameters)
            daily_summaries_objects.extend(daily_objects_kw)
        else:
            base_filters = get_base_filters(parameters)

            # Get a list of Q objects that tell us which data summaries to bring
            filters_parameters, data_summaries_objects_kw = parse_request_kwargs(
                parameters, charts_p, base_filters
            )
            filters.extend(filters_parameters)
            parameters["base_filters"] = base_filters
            parameters["data_summaries_objects"] = data_summaries_objects_kw
            data_summaries_objects.extend(data_summaries_objects_kw)

    # The actual data summaries, each one represent a a period for a series
    data_summary_results = models.DataSummary.objects.none()
    daily_results = models.Daily.objects.none()
    if filters:
        data_summary_results = models.DataSummary.objects.filter(
            reduce(or_, filters)
        ).order_by("year")
    if filters_daily:
        daily_results = models.Daily.objects.filter(
            reduce(or_, filters_daily)
        ).order_by("date")

    # Ids of the companies present on the DataSummary and Daily
    companies_ids = list(
        data_summary_results.values_list("entity_id", flat=True).distinct()
    ) + list(daily_results.values_list("entity_id", flat=True).distinct())
    companies = {
        str(c.number): c
        for c in models.Company.objects.filter(number__in=companies_ids)
    }
    # Parse data summary results by year and by series
    results_by_year, series_by_key = parse_data_summary_results_results(
        data_summary_results
    )
    daily_results_by_chart, daily_series_by_key = parse_daily_results(daily_results)
    hicharts_objects = []
    data_summaries_series_by_key = data_summaries_objects_to_series_keys(
        series_by_key, data_summaries_objects
    )
    data_daily_series_by_key = data_summaries_objects_to_series_keys(
        daily_series_by_key, daily_summaries_objects, daily=True
    )
    for parameters in charts_parameters:
        # Parse the DataSummary to actual Highcarts series
        if parameters["daily"]:
            base_filters = parameters["base_filters"]
            categories = get_dates_for_daily(base_filters)
            categories_str = [str(d) for d in categories]
            charts_p = parameters["charts_p"]
            data_daily_objects = parameters["data_daily_objects"]
            series_keys = []
            for d in data_daily_objects:
                key = get_daily_key(d)
                if key in data_daily_series_by_key:
                    series_keys.extend(list(data_daily_series_by_key[key]))

            series = get_daily_series(
                daily_results_by_chart,
                categories,
                daily_series_by_key,
                series_keys,
                companies,
                main_entity_id=parameters.get("entity_id"),
            )
            hicharts_objects.append(
                get_chart_data(
                    base_filters,
                    "daily",
                    charts_p,
                    series,
                    daily_series_by_key,
                    companies,
                    categories=categories_str,
                )
            )
        else:
            base_filters = parameters["base_filters"]
            period = base_filters["period"]
            data_summaries_objects = parameters["data_summaries_objects"]
            charts_p = parameters["charts_p"]
            # chart_object = parameters["chart_object"]
            series_keys = list()
            for ds in data_summaries_objects:
                key = get_key(ds)
                if key in data_summaries_series_by_key:
                    series_keys.extend(set(data_summaries_series_by_key[key]))
            series_keys = list(dict.fromkeys(series_keys).keys())
            series = get_series(
                results_by_year,
                series_by_key,
                series_keys,
                companies,
                base_filters,
                period,
                main_entity_id=parameters.get("entity_id"),
            )
            # Add extra data to the charts, like title and styling.
            hicharts_objects.append(
                get_chart_data(
                    base_filters, period, charts_p, series, series_by_key, companies
                )
            )
        #print(hicharts_objects)
    return hicharts_objects
