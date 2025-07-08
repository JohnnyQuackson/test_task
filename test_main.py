import pytest 
import main

@pytest.fixture
def sample_csv(tmp_path):
    content = "name,age,salary\nAlice,30,50000\nBob,25,60000\nCharlie,35,55000\n"
    file = tmp_path / "sample.csv"
    file.write_text(content)
    return str(file)

def test_input_file(sample_csv):
    path, columns = main.input_file(sample_csv)
    assert columns == ["name", "age", "salary"]

def test_find_column_exact_match():
    assert main.find_column("salary", ["name", "salary"]) == "salary"

def test_avg(sample_csv):
    with open(sample_csv) as f:
        reader = main.csv.DictReader(f)
        result = main.avg(reader, "salary", "avg")
        assert round(result[0][0]) == 55000

def test_min_or_max_min(sample_csv):
    with open(sample_csv) as f:
        reader = main.csv.DictReader(f)
        result = main.min_or_max(reader, "age", "min")
        assert result == [[25]]

def test_min_or_max_max(sample_csv):
    with open(sample_csv) as f:
        reader = main.csv.DictReader(f)
        result = main.min_or_max(reader, "age", "max")
        assert result == [[35]]
