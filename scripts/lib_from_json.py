"""
This script reads a json file created from the .rds file in R and loads data into the database.
"""

import json
import pandas as pd

# display all column
pd.set_option('display.max_column', None)


def parse_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def isolate_non_table_variables(variables):
    """
    Isolate variables that are not in tabular format.
    """
    non_table_variables = {}
    for key, item in variables.items():
        # if item is not a table and does not contain double colon:
        if item['format'][0] != 'table' and '::' not in key:
            # if start or end in item.keys(), replace them with min or max
            if 'start' in item.keys():
                item['min'] = item.pop('start')
            if 'end' in item.keys():
                item['max'] = item.pop('end')
            # if item['item'] len is 1 take the first element otherwise leave the element as is
            if 'option' in item.keys():
                item['option'] = {k: v[0] if len(v) == 1 else v for k, v in item['option'].items()}
            item = {k: v[0] if len(v) == 1 else v for k, v in item.items()}
            # append to non_table_variables
            non_table_variables[key] = item

    return non_table_variables


def isolate_table_variables(variables):
    """
    Isolate variables that are in tabular format.
    """
    table_variables = {}
    for key, item in variables.items():
        if '::' in key:
            table_name, column_name = key.split('::')
            # remove unnecessary square brackets from the column_info dict
            column_info = {column_name: {k: v[0] if len(v) == 1 else v for k, v in item.items()}}

            if table_name in table_variables:
                table_variables[table_name]['column'].append(column_info)
            else:
                table_variables[table_name] = {'column': [column_info]}
        elif item['format'][0] == 'table':
            if key not in table_variables:
                table_variables[key] = {'column': []}
            table_variables[key].update({k: v[0] for k, v in item.items() if k != 'column'})

    return table_variables


def format_table_vars(table_variables):
    table_variables_list = [{'name': key,
                             'column': value['column'],
                             **{k: value[k] for k in value if k != 'column'}} for key, value in
                            table_variables.items()]
    return table_variables_list


def main(input_json, output_dir):
    variables = parse_json(input_json)
    non_table_variables = isolate_non_table_variables(variables)
    table_variables = format_table_vars(isolate_table_variables(variables))

    # Create a dataframe from non-table variables
    df_non_table = pd.DataFrame.from_dict(non_table_variables, orient='index').set_index('name')
    df_table = pd.DataFrame(table_variables)

    df_non_table.to_csv(path_or_buf=output_dir + r'\lib_non_table_variables.csv',
                        index=True,
                        index_label='name',
                        header=True)
    df_table.to_csv(path_or_buf=output_dir + r'\lib_table_variables.csv',
                    index=False,
                    header=True)


output_file_dir = r'C:\Users\zawad\PycharmProjects\pySWAP_django\pySWAP'
parameter_json = r'C:\Users\zawad\PycharmProjects\pySWAP_django\pySWAP\all_variables.json'

# main(parameter_json, output_file_dir)


def main_dataframes(input_json):
    variables = parse_json(input_json)
    non_table_variables = isolate_non_table_variables(variables)
    table_variables = format_table_vars(isolate_table_variables(variables))

    # Create a dataframe from non-table variables
    df_non_table = pd.DataFrame.from_dict(non_table_variables, orient='index').set_index('name')
    df_table = pd.DataFrame(table_variables)

    return df_non_table, df_table

import math
def make_fixture(model, input) -> None:

    data = [
        {
            "model": f"library.{model}",
            "fields": {k: [v] if k in ('format', 'unit') else v for k, v in element.items()},
        }
    for element in input
    ]
    # Replace NaN values with None
    for item in data:
        fields = item["fields"]
        for key, value in fields.items():
            if isinstance(value, list) and any(isinstance(v, float) and math.isnan(v) for v in value):
                fields[key] = [None if isinstance(v, float) and math.isnan(v) else v for v in value]
                if key == 'unit' and fields[key] == [None]:
                    fields[key] = None
            elif isinstance(value, float) and math.isnan(value):
                fields[key] = None

    with open(fr'C:\Users\zawad\PycharmProjects\pySWAP_django\pySWAP\library\fixtures\init_{model}.json',
              'w', encoding='utf-8') as f:
        json.dump(data, f)


def main_to_dict(input_json):
    variables = parse_json(input_json)
    non_table_variables = isolate_non_table_variables(variables)
    table_variables = format_table_vars(isolate_table_variables(variables))

    # Create a dataframe from non-table variables
    json_non_table = pd.DataFrame.from_dict(non_table_variables,
                                            orient='index').reset_index().\
        rename(columns={'level_0': 'name'}).\
        to_dict(orient='records')

    make_fixture('modelparameter', json_non_table)
    json_table = pd.DataFrame(table_variables).to_dict(orient='records')
    make_fixture('modelparametertable', json_table)


main_to_dict(parameter_json)


#make django fixtures for model_parameter




