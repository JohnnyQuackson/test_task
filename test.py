import pytest 
import polling

@pytest.fixture
def data():
    file = "products.csv"
    data, columns = polling.input_file(file)
    return data

def test_input_file(data):
    data, columns = polling.input_file("products.csv")
    assert columns == ["name", "brand", "price", "rating"]

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
