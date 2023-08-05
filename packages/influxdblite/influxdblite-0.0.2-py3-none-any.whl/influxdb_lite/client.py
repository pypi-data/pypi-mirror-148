from influxdb_client import InfluxDBClient
from influxdb_lite.measurement import Measurement
import datetime as dt
import time


class Client(InfluxDBClient):
    def __init__(self, url: str, token: str, org: str, **kwargs):
        super().__init__(url=url, token=token, org=org, **kwargs)
        self.url = url
        self.token = token
        self.org = org
        self.query_str = ''
        self.measurement = None
        self.select_list = ['_time']

    def query(self, measurement):
        """Defines the base query from the bucket and the name of the measurement selected. All the following
        methods need a base query to work. """
        self.measurement = measurement
        self.select_list += measurement.tags + measurement.fields
        self.query_str = '\n'.join([f'from(bucket: "{measurement.bucket}")',
                                   f'|> filter(fn: (r) => r._measurement == "{measurement.name}")'])
        return self

    def select(self, _list: list):
        """ Receives a list of fields to show in resulting table of the query. If it's not called, all the columns
        will be selected by default. """
        self.select_list = _list
        query_list = self.query_str.split('\n')
        range_idxs = [i for i in range(len(query_list)) if 'range' in query_list[i]]
        range_idx = 1 if not range_idxs else range_idxs[0]+1
        query_list.insert(
            range_idx, f'|> filter(fn: (r) => contains(value: r._field, set:{self._parse_list_into_str(_list)}))')
        return self

    def range(self, start: (int, str, dt.datetime), stop: (int, str, dt.datetime) = None):
        """ Modifies the base query adding a specified range. This range can be either relative or absolute, this will
        depend on the start argument datatype. If start is a string (for example: '-15d'), the type will be considered
        relative and if is datetime or int, it will be considered absolute. A combination of 'start', 'stop' with
        different datatypes will fail.
        If 'stop' key is not present or its value is None, now() will be considered as default. If 'start' key is not
        present method will raise an error. """
        self._validate_selection(['_time'])
        query_list = self.query_str.split('\n')
        v_start, v_stop = self._validate_range(start, stop)
        query_list.insert(1, f"|> range(start: {v_start}, stop: {v_stop})")
        self.query_str = '\n'.join(query_list)
        return self

    def _validate_range(self,  start: (int, str, dt.datetime), stop: (int, str, dt.datetime)):
        if start is None:
            raise ValueError(f"Invalid start value. ")
        elif isinstance(start, str) or isinstance(start, int):
            pass
        elif isinstance(start, dt.datetime):
            start = self._dt_to_RFC3339(start)
            stop = self._dt_to_RFC3339(stop)
        else:
            raise ValueError(f"_type {type(start)} not recognized. ")
        if stop is None:
            stop = 'now()'
        return start, stop

    def filter(self, *args):
        """ Adds filter statement to query. Receives filter statements in the form Measurement.Tag == a, ...
        where the available operations are ==, >, <, >=, <= and the in_ function.
        * The 'in_' operation for fields must be used in conjunction with the select method and only one field at a time
         to work properly. """
        query_list = self.query_str.split('\n')
        for (attr, comparator, value) in args:
            if attr in self.measurement.tags:
                if comparator != 'in':
                    query_list.append(f'|> filter(fn: (r) => r["{attr}"] {comparator} "{value}")')
                else:
                    query_list.append(f'|> filter(fn: (r) => contains(value: r["{attr}"], set: {self._parse_list_into_str(value)}))')
            elif attr in self.measurement.fields:
                if comparator != 'in':
                    query_list.append(f'|> filter(fn: (r) => r["_field"] == "{attr}" and r["_value"] {comparator} {value})')
                else:
                    query_list.append(f'|> filter(fn: (r) => contains(value: r["_value"], set: {str(value)}))')
            else:
                ValueError(f"Unrecognized attribute {attr} given in dictionary.")
        self.query_str = '\n'.join(query_list)
        return self

    def group_by(self, _list: list):
        """Group by the influxdb tables based on influxdb columns. """
        self._validate_selection(_list)
        query_list = self.query_str.split('\n')
        query_list.append(f'|> group(columns: {self._parse_list_into_str(_list)})')
        self.query_str = '\n'.join(query_list)
        return self

    def order_by(self, _list: list, desc: bool):
        """Sorts influxdb columns in descending or ascending order. """
        self._validate_selection(_list)
        query_list = self.query_str.split('\n')
        query_list.append(f'|> sort(columns: {self._parse_list_into_str(_list)}, desc: {str(desc).lower()})')
        self.query_str = '\n'.join(query_list)
        return self

    def pivot(self, row_keys: list = None, column_keys: list = None, value_column: str = '_value'):
        """Pivots a table based on row_keys, column_keys and a value_column. The default call pivots field sets into
        a sql-like table. """
        row_keys = ['_time'] if row_keys is None else row_keys
        column_keys = ['_field'] if column_keys is None else column_keys
        query_list = self.query_str.split('\n')
        query_list.append(f'|> pivot(rowKey:{self._parse_list_into_str(row_keys)}, columnKey: {self._parse_list_into_str(column_keys)}, valueColumn: "{value_column}")')
        self.query_str = '\n'.join(query_list)
        return self

    def limit(self, lmt: int):
        """Limits the amount of results to {lmt}. """
        query_list = self.query_str.split('\n')
        query_list.append(f'|> limit(n:{lmt})')
        self.query_str = '\n'.join(query_list)
        return self

    def last(self, column: str = '_value'):
        """Returns the last non-null records from selected columns. """
        query_list = self.query_str.split('\n')
        query_list.append(f'|> last(column:"{column}")')
        self.query_str = '\n'.join(query_list)
        return self

    def all(self):
        """Executes the resulting query. """
        return self.query_api().query(query=self.query_str, org=self.org)

    @staticmethod
    def _parse_list_into_str(_list):
        _str = "["
        for _int in _list[:-1]:
            _str += f"\"{str(_int)}\","
        return _str + f"\"{str(_list[-1])}\"]"

    def _validate_selection(self, _list):
        for column in _list:
            if column not in self.select_list:
                raise TypeError(f"Please include {column} in the select list.")

    def _dt_to_RFC3339(self, datetime_obj: dt.datetime = dt.datetime.now(), _format: str = 'long'):
        """Transform datetime object into string RFC3339 format (either in date, short or long format). Ignores
         timezone aware datetime objects. """
        if datetime_obj is not None:
            base = datetime_obj.isoformat()
            res = self._get_resolution(base)
            base = base.split('+')[0] if '+' in base else base
            if _format == 'date':
                return base.split('T')[0]
            elif _format == 'short':
                return base[:-res-1] + 'Z' if res == 6 else base + 'Z'
            elif _format == 'long':
                return base[:-res//2] + 'Z' if res == 6 else base + '.000Z'
            else:
                raise ValueError("Enter a format from 1 to 3")


    def _dt_to_unix(self, datetime_obj: dt.datetime = dt.datetime.now()):
        """Transform datetime object into string RFC3339 format (either in date, short or long format). Ignores
         timezone aware datetime objects. """
        if datetime_obj is not None:
           return int(time.mktime(datetime_obj.timetuple()))


    @staticmethod
    def _get_resolution(isoformat):
        if len(isoformat.split('.')) == 1:
            return -1
        else:
            return len(isoformat.split('.')[1])

"measurement1, tag_set field_set timestamp"
    #def bulk_insert(self, measurements: list):
    #    for measurement in measurements:
#
#
    #def parse_insert(insert_dicts: dict, measurement: str, tag_list: list, field_list: list, timestamp_label: str,
    #                 type_of_index: str = 'single'):
    #    out = []
    #    if type_of_index == 'single':
    #        for index in insert_dicts:
    #            tag_set = ','.join([f"{tag}={index}" for tag in tag_list])
    #            _parse_fields(insert_dicts[index], field_list, timestamp_label, measurement, tag_set, out)
    #        return out
    #    elif type_of_index == 'double':
    #        for first_index in insert_dicts:
    #            for second_index in insert_dicts[first_index]:
    #                tag_set = f"{tag_list[0]}={first_index},{tag_list[1]}={second_index}"
    #                _parse_fields(insert_dicts[first_index][second_index], field_list, timestamp_label, measurement,
    #                              tag_set, out)
    #        return out
    #    else:
    #        raise TypeError(f"Type of index {type_of_index} not recognized")
#
    #def _parse_fields(sub_dict, field_list, timestamp_label, measurement, tag_set, out):
    #    field_set = ','.join([f"{field}={sub_dict[field]}" for field in field_list
    #                          if sub_dict.get(field, None) is not None])
    #    if sub_dict.get(timestamp_label, None) is not None:
    #        con_str = f"{measurement},{tag_set} {field_set} {dt_to_long(sub_dict[timestamp_label])}"
    #    else:
    #        con_str = f"{measurement},{tag_set} {field_set}"
    #    out.append(con_str)
