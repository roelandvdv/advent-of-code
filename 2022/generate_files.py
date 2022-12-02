from pathlib import Path
import os

script_path = os.path.dirname(os.path.realpath(__file__))
data_dir = Path("data")
try:
    os.mkdir(data_dir)
except OSError as error:
    print(error)    

days = range(1, 26)
for day in days:
    path = script_path / data_dir / Path(f"day{day:02.0f}.txt")
    path_test = script_path / data_dir / Path(f"day{day:02.0f}test.txt")
    open(path, 'a').close()
    open(path_test, 'a').close()