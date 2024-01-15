import os
import json
import json
import sys

from select_table import draw_table,apply_condition

def inner_join(table1, table2, join_key, select_fields, where_condition):
    with open(f'{table1}.json') as f1, open(f'{table2}.json') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    result = []
    for row1 in data1:
        for row2 in data2:
            if row1[join_key] == row2[join_key]:
                combined_row = {**row1, **row2}
                if not where_condition or all(apply_condition(combined_row, condition) for condition in where_condition):
                    result_row = {field: combined_row[field] for field in select_fields}
                    result.append(result_row)

    keys = result[0].keys() if result else []
    max_lengths = [len(str(key)) for key in keys]
    rows = []
    for row in result:
        values = list(row.values())
        rows.append(values)
        max_lengths = [max(max_lengths[i], len(str(values[i])) if values[i] else 0) for i in range(len(values))]
    draw_table(rows, keys, max_lengths)

if __name__ == '__main__':
    inner_join('student', 'grade', 'name', ['name', 'age', 'location','subject','score'], ['score=99'])