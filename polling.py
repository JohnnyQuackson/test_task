import csv
from tabulate import tabulate
import const

def input_file(file_path: str):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        columns = reader.fieldnames

    return data, columns


def start(parse_args, data = None):
    try:
        data, columns = input_file(parse_args.file)
    except FileNotFoundError:
        return print(const.file_error)
    

    where_kwargs = parse_args.where
    aggregate_kwargs = parse_args.aggregate

    if where_kwargs is None and aggregate_kwargs is None: 
        return show(data, columns)

    if where_kwargs is not None and aggregate_kwargs is not None:
        data = where(data, where_kwargs, columns, show = False)
    else:
        where(data, where_kwargs, columns)
    
    aggregate(data, aggregate_kwargs, columns)



def find_column(command_kwargs: str, columns: list) -> str:
    for column in columns:
        if column == command_kwargs[:len(column)]:
            return column
        
    return None


def show(data: list, columns: list):
    return print(tabulate(data, headers=columns, tablefmt="grid", floatfmt=".2f"))

def avg(data: list, chosen_column: str, param: str):
    s = 0
    count = 0
    for row in data:
        try:
            s += float(row[chosen_column])
            count += 1
        except ValueError:
            return print(const.aggregate_error.format(param, chosen_column))
    return [[s / count]]

def min_or_max(data: list, chosen_column: str, param: str):
    list_of_values = []
    for row in data:
        try:
            list_of_values.append(float(row[chosen_column]))
        except ValueError:
            print(const.aggregate_error.format(param, chosen_column))
            return
    if param == "min":
        return [[min(list_of_values)]]
    else:
        return [[max(list_of_values)]]

def aggregate(data: list, aggregate_kwargs: str, columns: list) -> None:
    if aggregate_kwargs is None: return
        
    output_value = None
    chosen_column = find_column(aggregate_kwargs, columns)
    param = None

    if chosen_column is None:
        return print(const.column_error.format(aggregate_kwargs))
    else:
        param = aggregate_kwargs[len(chosen_column) + 1:]
    
    if param not in ["avg", "min", "max"]:
        return print(const.aggregate_param_mistake)
        
    if param == "avg":
        output_value = avg(data, chosen_column, param)

    elif param == "min" or param == "max":
        output_value = min_or_max(data, chosen_column, param)

    if output_value is not None: print(tabulate(output_value, headers=[param], tablefmt="grid", floatfmt=".2f"))

def where(data: list, where_kwargs: str, columns: list, show = True) -> None:
    if where_kwargs is None: return

    chosen_column = find_column(where_kwargs, columns)
    command = None
    param = None

    if chosen_column is None:
        return print(const.column_error.format(where_kwargs))
    else:
        command = where_kwargs[len(chosen_column)]
        param = where_kwargs[len(chosen_column) + 1:]

    if command is None or command not in ["<", ">", "="]:
        return print(const.command_error)
        
    output_data = []

    if command == "=":
        for row in data:
            if row[chosen_column] == param:
                output_data.append(list(row.values()))

    elif command == ">":
        for row in data:
            try: 
                if float(row[chosen_column]) > float(param):
                    output_data.append(list(row.values()))
            except ValueError:
                return print(const.where_error.format(command, chosen_column))

    elif command == "<":
        for row in data:
            try:
                if float(row[chosen_column]) < float(param):
                    output_data.append(list(row.values()))
            except ValueError:
                return print(const.where_error.format(command, chosen_column))
                
    if show:
        if len(output_data) > 0 : 
            return print(tabulate(output_data, headers=columns, tablefmt="grid", floatfmt=".2f"))
        else: 
            return print(const.no_output_data)
    else:
        return [{columns[i] : values[i] for i in range(len(columns))} for values in output_data]