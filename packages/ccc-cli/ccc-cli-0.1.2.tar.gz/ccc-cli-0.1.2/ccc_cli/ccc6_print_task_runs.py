#!/usr/bin/env python3

import subprocess
import itertools
from collections import namedtuple
from collections.abc import Iterable
# from pprint import pprint
# import operator
import tabulate

ccc_path = '/Applications/Carbon Copy Cloner.app/Contents/MacOS/ccc'
task_record = namedtuple('Task_Record', [
    'name', 'src', 'dest', 'when', 'time_elapsed', 'data_copied', 'result',
    'files_copied'
])


def record2task_record(record: str) -> task_record:
    return task_record(*[field for field in record.split('|')])


def get_task_records() -> list[task_record]:
    hist = subprocess.run([ccc_path, '--history'], capture_output=True)
    hist_records = hist.stdout.decode().splitlines()
    task_records = list(map(record2task_record, hist_records))
    return task_records


def task_records2task_groups(task_records: list[task_record]):
    trs = task_records
    tasks_grouped_by_name = itertools.groupby(sorted(trs,
                                                     key=lambda x: (x.name)),
                                              key=lambda x: x.name)
    return tasks_grouped_by_name


def task_groups2last_runs(task_groups: Iterable) -> list[tuple[str]]:
    last_runs = [(i, next((k for k in j), None)) for (i, j) in task_groups]

    t7 = [(i[1].name, i[1].when, i[1].data_copied, i[1].files_copied)
          for i in last_runs if 'T7' in i[1].name]
    non_t7 = [(i[1].name, i[1].when, i[1].data_copied, i[1].files_copied)
              for i in last_runs if 'T7' not in i[1].name]
    all_runs_with_t7s_first = t7 + non_t7
    return all_runs_with_t7s_first


def main() -> None:
    task_records = get_task_records()
    task_groups = task_records2task_groups(task_records)
    last_runs = task_groups2last_runs(task_groups)
    headers = ['Task', 'When', 'Data Copied', 'Files Copied']
    print(tabulate.tabulate(last_runs, headers=headers, tablefmt='psql'))


if __name__ == '__main__':
    main()
