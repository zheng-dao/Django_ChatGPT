import json
from django.conf import settings
from django.db.models.query import QuerySet
from app.models import Chart, Report, Location
import re
import copy
import collections
from operator import attrgetter

def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split("(\d+)", text)]

def split_dimensions(dimensions):
    kwargs = {}
    if dimensions:
        dim_list = dimensions.split(',')
        for d in dim_list:
            key, value = d.split('__')
            kwargs[key.lower()] = value.lower()
    return kwargs

def get_color_(i, style):
    """
    This is for getting linear gradient color
    """
    list_of_colors = settings.DEFAULT_GRADIENT_COLORS
    # list_of_colors = ["#00B1BC","#265BB6"]
    list_of_text_colors = settings.DEFAULT_COLORS
    #if style.get("colors"):
    #    list_of_colors = style["colors"]
    #    list_of_text_colors = style["colors"]
    #else:
    #    list_of_colors = settings.DEFAULT_GRADIENT_COLORS
    #    # list_of_colors = ["#00B1BC","#265BB6"]
    #    list_of_text_colors = settings.DEFAULT_COLORS
    #print(i)
    zero_color = list_of_text_colors[i]
    try:
        one_color = list_of_colors[len(list_of_colors)%i]
    except:
        one_color = list_of_colors[0]
    color = {
        "linearGradient": {
            "x1": 0,
            "x2": 0,
            "y1": 0,
            "y2": 1,
        },
        "stops": [
            [0, zero_color],
            [1, one_color],
        ],
    }
    return color


def get_radial_color(i):
    """
    This is for generating the color called radial color used in pie chart
    """
    list_of_colors = settings.DEFAULT_GRADIENT_COLORS
    list_of_text_colors = settings.DEFAULT_COLORS
    try:
        zero_color = list_of_colors[i]
        one_color = list_of_text_colors[i]
    except:
        one_color = ""
        zero_color = ""
    color = {
        "radialGradient": {
            "cx": 0.5,
            "cy": 0.3,
            "r": 0.7,
        },
        "stops": [
            [0, zero_color],
            [1, one_color],
        ],
    }
    return color


def update_data(chart, data, style, timeframe, **kwargs):
    if isinstance(data, QuerySet):
        orig_data = copy.deepcopy(data)
        metrics = chart.metrics.all()
        if metrics and not metrics[0].subtype:
            fields = get_datasummary_fields(timeframe)
            style['xAxis'] = {'categories':[m.label for m in metrics]}
            data = [attrgetter(*fields)(d) for d in data]
            style['series'][0]['data'] = data
    else:
        data_series = data["series"]
        print(data_series)
        updated_series = []
        #if isinstance(data_series, list):
        #    style['series'][0]['data'] = data_series
        #    style['series'][0]['color'] = settings.DEFAULT_GRADIENT_COLORS[:len(data_series)]
        #else:
        #if not isinstance(data_series, list):
        if 'gauge' in style['chart']['type']:
            style['series'] = [{'data':data_series, 'color':settings.DEFAULT_COLORS[0]}]
        else:
            for i, data_s in enumerate(data_series):
                #data_s["color"] = get_color_(i, style)
                data_temp = {}
                if isinstance(data_s, list):
                    data_temp['data'] = data_s
                    data_temp["color"] = settings.DEFAULT_COLORS[i]
                elif isinstance(data_s, int):
                    data_temp['data'] = [data_s]
                    data_temp["color"] = settings.DEFAULT_COLORS[0]
                else:
                    print('not list or int')
                    data_temp['data'] = data_s['data']
                    data_temp["color"] = settings.DEFAULT_COLORS[i]
                if style['chart']['type'] == 'sankey':
                    data_temp['keys'] = ['from', 'to', 'weight']
                print(data_temp)
                updated_series.append(data_temp.copy())
            style["series"] = updated_series
    if "xAxis" in data and "categories" in data["xAxis"]:
        if not "xAxis" in style:
            style["xAxis"] = {"categories": None}
        style["xAxis"]["categories"] = data["xAxis"]["categories"]

    if not style.get("colors"):
        style["colors"] = settings.DEFAULT_COLORS
    if 'title' not in list(style.keys()):
        style['title'] = {}
        style['title']['text'] = None
    elif 'title' in data and 'title' in style:
        style["title"]["text"] = data["title"]["text"]
    else:
        style['title'] = {}
        style['title']['text'] = None
    if 'subtitle' in data:
        style["subtitle"] = data["subtitle"]
    style.update(kwargs)
    return style


def update_pie_chart(chart, data, style, **kwargs):
    """
    This is for only pie chart need to extend it to update_data
    """
    # import pdb;pdb.set_trace()
    print(data)
    print(style)
    data_series = data["series"][0]["data"]
    updated_series = []
    #print(data_series)
    # import pdb;pdb.set_trace()
    for i, data_s in enumerate(data_series):
        #data_s["color"] = get_radial_color(i)
        updated_series.append(data_s)
    # import pdb;pdb.set_trace()
    style["series"][0]["data"] = updated_series
    if not style.get("colors"):
        style["colors"] = settings.DEFAULT_COLORS
    if 'title' in data:
        style["title"] = {}
        style["title"]["text"] = data["title"]["text"]
    if "subtitle" in data:
        style["subtitle"] = data["subtitle"]
    style.update(kwargs)
    return style

def update_negative_bar_chart(chart, data, style, **kwargs):
    style1 = copy.deepcopy(style)
    style1['xAxis'][0]['categories'] = data['categories']
    style1['xAxis'][1]['categories'] = data['categories']
    style1['series'] = data['series']
    return style1

def update_dumbbell_chart(chart, data, style, **kwargs):
    data_series = data['series'][0]
    print('ds', data_series)
    data_dumbbell = []
    categories = []
    for i, d in enumerate(data_series):
        print(d)
        n, r = divmod(i,2)
        if r == 0:
            t = {'name':data['xAxis']['categories'][i]}
            t['high'] = d
        else:
            t['low'] = d
            categories.append(data['xAxis']['categories'][i])
            data_dumbbell.append(t.copy())
            t = {}
    style['xAxis']['categories'] = categories
    style['series'] = [{'data':data_dumbbell}]
    return style

def get_datasummary_fields(period, chart=None):
    fields = ['total']
    if str(period).isdigit():
        fields = ['last' + str(period)]
    elif period == 'monthly':
        fields = [f"{m:02d}" for m in range(1,13)]
    elif period == 'quarterly':
        fields = [f"{q:02d}" for q in range(1,5)]
    if chart and chart.extra_instance_fields:
        fields += chart.extra_instance_fields.split(',')
    return fields

def update_table_data(chart, chart_response, kwargs):
    from operator import attrgetter
    final_table = {'headers':[], 'data':{}}
    data = chart_response['data']
    if data:
        metrics = chart.metrics.all()
        if metrics and not metrics[0].subtype:
            print(chart_response)
            timeframe = chart_response['timeframe']
            fields = get_datasummary_fields(timeframe, chart)
            final_table['headers'] = [m.label for m in metrics]
            if chart.extra_instance_field_labels:
                final_table['headers'] += chart.extra_instance_field_labels.split(',')
            print(fields)
            if kwargs['show_multiple'] and chart.extra_instance_fields:
                for d in data:
                    if getattr(d, chart.extra_instance_fields.split(',')[0]) not in final_table['data']:
                        pass
            else:
                final_table['data'] = [[attrgetter(*fields)(d) for d in data]]
            print(final_table)
        else:
            for i, data_chunk in enumerate(data):
                if i == 0:
                    final_table['headers'] = [st.strip() for st in metrics[i].subtype.split(',')]
                    if metrics[i].subtype_labels:
                        final_table['headers'] = [st.strip() for st in metrics[i].subtype_labels.split(',')]
                else:
                    if metrics[i].subtype_labels:
                        final_table['headers'] += [st.strip() for st in metrics[i].subtype_labels.split(',')[1:]]
                    else:
                        final_table['headers'] += [st.strip() for st in metrics[i].subtype.split(',')[1:]]
                for item in data_chunk:
                    #print(item)
                    if item[0] not in final_table['data']:
                        final_table['data'][item[0]] = list(item)
                    else:
                        final_table['data'][data_chunk[i][0]] += list(item[1:])
            final_table['data'] = list(final_table['data'].values())
    return final_table

def update_map_data(chart, chart_response, kwargs, field_replace_label='value'):
    #print(chart_response)
    print(kwargs)
    chart_response['state'] = 'all'
    locations = []
    if not 'locations' in chart_response:
        chart_response['locations'] = []
    metrics = chart.metrics.all()
    print(metrics)
    data = list(chart_response['data'])
    if metrics.count() == 1:
        for i in data:
            i[field_replace_label] = i.pop(metrics[0].name)
        chart_response['data'] = data
    if 'map_dimensions' in kwargs:
        map_dimensions  = split_dimensions(kwargs['map_dimensions'])
        print(map_dimensions)
        if 'state' in map_dimensions:
            chart_response['state'] = map_dimensions['state'].lower()
        branches = map_dimensions.get('branches', None)
        if branches == 'entity_id':
            locations = Location().get_lat_lon(kwargs['entity_id'])
        elif branches == 'state':
            locations = Location().get_lat_lon(state=map_dimensions['state'])
        elif branches == 'county':
            locations = Location().get_lat_lon()
        elif branches == 'all':
            locations = Location().get_lat_lon()
    if locations:
        chart_response['locations'].append(locations)
    return chart_response

def process_get_chart_data(chart_object, **kwargs):
    print(">>>>>>>>>>>>>>>",kwargs)
    chart_response = chart_object.get_chart(**kwargs)
    chart_type = chart_object.charttype.chart_type
    # This will check if chart_response in list which means it contains the list of chart
    #print(chart_response)
    if chart_type == 'table':
        updated_data = update_table_data(chart_object, chart_response, kwargs)
    elif chart_type[:3] == 'map':
        updated_data = update_map_data(chart_object, chart_response, kwargs)
        #print(updated_data, kwargs)
    else:
        if isinstance(chart_response, list):
            print('it is a list')
            # for bar_negative only for now
            list_of_updated_data = []
            for chart_res in chart_response:
                data_res = {}
                data_res = update_negative_bar_chart(chart_object, **chart_res)
                list_of_updated_data.append(data_res.copy())
            updated_data = list_of_updated_data
        elif chart_object.charttype.chart_type in ['pie', 'donut']:
            updated_data = update_pie_chart(chart_object, **chart_response)
        elif chart_object.charttype.chart_type == 'dumbbell':
            updated_data = update_dumbbell_chart(chart_object, **chart_response)
        elif chart_object.charttype.chart_type == 'bar_negative':
            updated_data = update_negative_bar_chart(chart_object, **chart_response)
        else:
            if not 'timeframe' in chart_response:
                chart_response['timeframe'] = None
            updated_data = update_data(chart_object, **chart_response)
        
    # This will be updated for chart utils 
    style_override = chart_object.style_override
    if style_override:
        print('style override')
        style_overide_json = json.loads(style_override)
        # This happens when we are sending the list of updated data 
        if isinstance(updated_data, list):
            list_of_updated_data = []
            for chart_data_previous in updated_data:
                list_of_updated_data.append(deep_update(chart_data_previous, style_overide_json))
            updated_data = list_of_updated_data
        else:
            updated_data = deep_update(updated_data, style_overide_json)
        
    return updated_data


def order_categories(chart1, chart2):
    categories1 = chart1.get("xAxis", {}).get("categories", [])
    categories2 = chart2.get("xAxis", {}).get("categories", [])
    all_categories = list(set(categories1 + categories2))
    all_categories.sort(key=natural_keys)
    return all_categories


def parse_chart_series(chart_response, categories, extra={}):
    for i in chart_response["series"]:
        i["type"] = chart_response["chart"].get("type")
        i["name"] = chart_response["title"]["text"]
        if "name" in extra:
            i["name"] = extra['name']
        categories_chart = chart_response.get("xAxis", {}).get("categories", [])

        series_per_category = {
            categories_chart[j]: i["data"][j] for j in range(len(categories_chart))
        }
        i["data"] = [series_per_category.get(c) for c in categories]
        if "color" in i:
            del i["color"]
        i.update(extra)


def build_combo_chart(chart_id, entity_id, chart=None, **kwargs):
    """Assumes chart 1 is the credit_union and chart_2 is the benchmark."""
    if not chart:
        chart_1 = Chart.objects.get(pk=chart_id)
    else:
        chart_1 = chart
    if chart_1:
        dimensions = kwargs.pop("dimensions", None)
        entity_type = kwargs.pop("entity_type", None)
        chart_1_response = process_get_chart_data(
            chart_1, entity_id=entity_id, entity_type="credit_union", **kwargs
        )
        chart_2_response = process_get_chart_data(
            chart_1, entity_type="benchmark", dimensions=dimensions, **kwargs
        )
        # if 'xAxis' in chart_1_response and 'xAxis' in chart_2_response:
        #    categories = order_categories(
        #            chart_1_response["xAxis"]["categories"], chart_2_response["xAxis"]["categories"]
        #    )
        categories = order_categories(
            chart_1_response,
            chart_2_response,
        )
        colors = chart_1_response["colors"]
        parse_chart_series(chart_1_response, categories, extra={"type": "column", "name":"Credit Union"})
        parse_chart_series(
            chart_2_response, categories, extra={"type": "area", "opacity": 0.5, "name":"Benchmark"}
        )

        series = []
        #print('series')
        series.extend(chart_1_response["series"])
        #print(chart_1_response["series"][0])
        series.extend(chart_2_response["series"])
        #print(chart_2_response["series"][0]['name'])
        # for removing of y Axis is one
        if 'yAxis' in chart_1_response and isinstance(chart_1_response["yAxis"], list):
            chart_1_response["yAxis"][0]["labels"] = False
        # import pdb;pdb.set_trace()
        final_response = {
            "chart": {"backgroundColor": "transparent"},
            "colors": colors,
            "yAxis": chart_1_response.get("yAxis"),
            "tooltip": {"shared": True},
            "xAxis": {
                **chart_1_response.get("xAxis"),
                "categories": categories,
                "labels": {"rotation": 90},
            },
            "series": series,
        }
        if 'title' in chart_1_response:
            final_response['title'] = {
                **chart_1_response["title"],
                #"text": f"{chart_1_response['title']['text']} <br/> {chart_2_response['title']['text']}",
                "text": chart_1_response['title']['text'],
            },
        final_response['credits'] = {'enabled':False}
        return final_response
    return {}

def get_series(chart, index):
    data =  chart.get('series',[])
    if data:
        for j,i in enumerate(data):
            i['color'] = get_color_(index+j, None)
        return data

def combine_charts(charts_ids=[], reports_ids=[], **kwargs):
    as_combo = kwargs.pop('as_combo',None)
    if as_combo:
        entity_id = kwargs.pop('entity_id',None)
    ids_from_report = {
        i
        for i in Report.objects.filter(pk__in=reports_ids).values_list(
            "chart__id", flat=True
        )
    }
    
    ids = set(ids_from_report) | set(charts_ids)
    
    charts = Chart.objects.filter(pk__in=ids)
    charts_data = []
    chart_data = {}
    for chart in charts:
        try:
            if as_combo:
                charts_data.append(build_combo_chart(chart=chart,entity_id=entity_id, **kwargs))
            else:
                charts_data.append(process_get_chart_data(chart, **kwargs))
        except Exception as e:
            print(e)
    if len(charts_data) > 0:
        chart_data = charts_data[0] or {}
        new_series = []
        current_series = get_series(chart_data,0)
        if current_series:
            new_series.extend(current_series)
        for index,i in enumerate(charts_data[1:]):
            current_series = get_series(i,index+1)
            if current_series:
                new_series.extend(current_series)
        chart_data.setdefault('title',{})
        chart_data['title'] = {'text':'Combined chart'} 
        chart_data['series'] = new_series

    return chart_data



def parse_request_kwargs(dict_request):
    entity_id = dict_request.get('entity_id', None)
    entity_type = dict_request.get('entity_type', None)
    dimensions = dict_request.get('dimensions', None)
    start_year = dict_request.get('start_year', None)
    daily_span = dict_request.get('daily_span', None)
    show_competitors = dict_request.get('show_competitors', None)
    if start_year:
        start_year = int(start_year)
    end_year = dict_request.get('end_year', None)
    if end_year:
        end_year = int(end_year)
    if daily_span:
        daily_span = int(daily_span)
    as_combo = dict_request.get('as_combo', None)
    charts_ids = dict_request.get('charts_ids', None)
    if charts_ids:
        charts_ids=charts_ids.split(',')
    reports_ids = dict_request.get('reports_ids', None)
    if reports_ids:
        reports_ids=reports_ids.split(',')
    kwargs = {
        'entity_id': entity_id,
        'entity_type': entity_type,
        'dimensions': dimensions,
        'start_year': start_year,
        'end_year': end_year,
        'daily_span': daily_span,
        'show_competitors': int(show_competitors) if show_competitors else False,
        'show_multiple': int(show_multiple) if show_multiple else False,
        'as_combo': as_combo,
        'reports_ids': reports_ids,
        'charts_ids': charts_ids,
    }            
    for i in list(kwargs.keys()):
        if kwargs[i] is None:
            del kwargs[i]
    return kwargs

def deep_update(d, other):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for k, v in other.items():

        # Issues aries for the list one
    
    
        d_v = d.get(k)
        
        if isinstance(v, collections.Mapping) and isinstance(d_v, collections.Mapping):
            deep_update(d_v, v)
        else:
            d[k] = copy.deepcopy(v)
    # or d[k] = v if you know what you're doing
    return d