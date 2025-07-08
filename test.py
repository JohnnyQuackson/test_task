import pytest 
import polling
import const

def test_input_file():
    data, columns = polling.input_file("tables/products.csv")
    assert columns == ["name", "brand", "price", "rating"]




@pytest.fixture
def data():
    data, columns = polling.input_file("tables/products.csv")
    return data

def test_find_column_exact_match():
    assert polling.find_column("salary", ["name", "salary"]) == "salary"

def test_avg(data):
    result = polling.avg(data, "price", "avg")
    assert round(result[0][0]) == 602

def test_min_or_max_min(data):
    result = polling.min_or_max(data, "price", "min")
    assert result == [[149]]

def test_min_or_max_max(data):
    result = polling.min_or_max(data, "rating", "max")
    assert result == [[4.9]]

def test_show(capsys):
    data = [
        {"Name": "Alice", "Age": 30},
        {"Name": "Bob", "Age": 25}
    ]
    expected_output = "+--------+-------+\n| Name   |   Age |\n+========+=======+\n| Alice  |    30 |\n+--------+-------+\n| Bob    |    25 |\n+--------+-------+\n"
    columns = ["Name", "Age"]
    polling.show(data, columns)
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_file_error(capsys):
    class parse_args:
        file = "random_path"
        where = None
        aggregate = None

    expected_output = const.file_error + "\n"
    polling.start(parse_args)
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_where_error(data, capsys):
    polling.where(data, "brand>5", ["name", "brand", "price", "rating"])
    expected_output = const.where_error.format(">", "brand") + "\n"
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_aggregate_error(data, capsys):
    polling.aggregate(data, "brand=max", ["name", "brand", "price", "rating"])
    expected_output = const.aggregate_error.format("max", "brand") + "\n"
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_param_mistake(data, capsys):
    polling.aggregate(data, "brand=mex", ["name", "brand", "price", "rating"]) # mex instead of max
    expected_output = const.aggregate_param_mistake + "\n"
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_cmd_error(data, capsys):
    polling.where(data, "brand+samsung", ["name", "brand", "price", "rating"])
    expected_output = const.command_error + "\n"
    captured = capsys.readouterr()
    assert captured.out == expected_output