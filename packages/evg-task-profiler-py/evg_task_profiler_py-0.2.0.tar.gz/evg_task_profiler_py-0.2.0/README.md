# Evergreen Task Profiler

Break down the runtime of the different steps comprising an evergreen task.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/evg-task-profiler-py) [![PyPI](https://img.shields.io/pypi/v/evg-task-profiler-py.svg)](https://pypi.org/project/evg-task-profiler-py/) [![Upload Python Package](https://github.com/dbradf/evg-task-profiler.py/actions/workflows/CI.yml/badge.svg)](https://github.com/dbradf/evg-task-profiler.py/actions/workflows/CI.yml)

## Installation

Installation is done via pip:

```bash
pip install evg-task-profiler-py
```

## Usage

An example of usage is shown below. Note: You will need to retrieve the task log contents and
send it to the profiler, a tool like the [Evergreen API client](https://github.com/evergreen-ci/evergreen.py)
can be useful for this purpose.

```python
from evergreen import EvergreenApi
from evg_task_profiler_py import TaskProfiler

task_id = "some_evg_task_id"
evg_api = EvergreenApi.get_api(use_config_file=True)

profiler = TaskProfiler()
task = evg_api.task_by_id(task_id)
for line in task.stream_log("task_log"):
    profiler.process_line(line)

for event in profiler.get_events():
    print(f"{event.index}: {event.name} - {event.step}: {event.duration} ms")
```
