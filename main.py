import csv
import argparse
from tabulate import tabulate
import const

def input_file(file_path: str):
    f = open(file_path)
    columns = list(csv.DictReader(f).__next__().keys())
    f.close()
    
    return file_path, columns


def find_column(command_kwargs: str, columns: list) -> str:
    for column in columns:
        if column == command_kwargs[:len(column)]:
            return column
        
    return None


def show(file: str, columns: list):
    f = open(file)
    reader = csv.DictReader(f)
    data = [list(row.values()) for row in reader]

    print(tabulate(data, headers=columns, tablefmt="grid"), floatfmt=".2f")

def avg(reader, choosed_column: str, param: str):
    s = 0
    count = 0
    for row in reader:
        try:
            s += float(row[choosed_column])
            count += 1
        except:
            return print(const.aggregate_error.format(param, choosed_column))
            
    
    return [[s / count]]

def min_or_max(reader, choosed_column: str, param: str):
    list_of_values = []

    for row in reader:
        try:
            list_of_values.append(float(row[choosed_column]))
        except:
            print(const.aggregate_error.format(param, choosed_column))
            return
    if param == "min":
        return [[min(list_of_values)]]
    else:
        return [[max(list_of_values)]]

def aggregate(file: str, aggregate_kwargs: str, columns: list, data: list) -> None:
    if aggregate_kwargs == None: return

    f = open(file)
    reader = csv.DictReader(f)
    if data != None:
        reader = data
        if len(data) == 0:
            return
        
    output_value = None
    choosed_column = find_column(aggregate_kwargs, columns)
    param = None

    if choosed_column == None:
        return print(const.column_error)
    else:
        param = aggregate_kwargs[len(choosed_column) + 1:]

    
    if param not in ["avg", "min", "max"]:
        return print(const.aggregate_param_mistake)
        
    
    if param == "avg":
        output_value = avg(reader, choosed_column, param)

    elif param == "min" or param == "max":
        output_value = min_or_max(reader, choosed_column, param)

    if output_value != None: print(tabulate(output_value, headers=[param], tablefmt="grid"), floatfmt=".2f")

def where(file: str, where_kwargs: str, columns: list, show = True) -> None:
    if where_kwargs == None: return

    choosed_column = find_column(where_kwargs, columns)
    command = None
    param = None


    if choosed_column == None:
        return print(const.column_error)
    else:
        command = where_kwargs[len(choosed_column)]
        param = where_kwargs[len(choosed_column) + 1:]

    if command == None or command not in ["<", ">", "="]:
        return print(const.command_error)
        
    
    f = open(file)
    reader = csv.DictReader(f)
    data = []
    
    if command == "=":
        for row in reader:
            if row[choosed_column] == param:
                data.append(list(row.values()))

    elif command == ">":
        for row in reader:
            try: 
                if float(row[choosed_column]) > float(param):
                    data.append(list(row.values()))
            except:
                return print(const.where_error.format(command, choosed_column))
                

    elif command == "<":
        for row in reader:
            try:
                if float(row[choosed_column]) < float(param):
                    data.append(list(row.values()))
            except TypeError:
                return print(const.where_error.format(command, choosed_column))
                

    if show:
        if len(data) > 0 : 
            return print(tabulate(data, headers=columns, tablefmt="grid"), floatfmt=".2f")
        else: 
            return print(const.no_data)
    else:
        return [{columns[i] : values[i] for i in range(len(columns))} for values in data]


def start(parse_args, data = None):
    try:
        file, columns = input_file(parse_args.file)
    except:
        return print(const.file_error)
    
    
    where_kwargs = parse_args.where
    aggregate_kwargs = parse_args.aggregate

    if where_kwargs == None and aggregate_kwargs == None: 
        return show(file, columns)

    if aggregate_kwargs != None:
        data = where(file, where_kwargs, columns, show = False)
    else:
        return where(file, where_kwargs, columns)
    
    aggregate(file, aggregate_kwargs, columns, data)

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--file', type=str, help=const.file_help)
    parser.add_argument('--where', type=str, help=const.where_help)
    parser.add_argument('--aggregate', type=str, help=const.aggregate_help)

    parse_args = parser.parse_args()

    if parse_args.file == None: return parser.print_help()

    start(parse_args)

if __name__ == "__main__":
    main()