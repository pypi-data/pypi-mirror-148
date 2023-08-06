TABLE_HEADER = ['metric_name', 'source_column', 'target_column', 'source_value',
                'target_value', 'difference', 'source_table', 'target_table']

left_rule = {'<': ':', '^': ':', '>': '-'}
right_rule = {'<': '-', '^': ':', '>': ':'}

fields = [0, 1, 2, 3, 4, 5, 6, 7]

alignment = [('^', '^'), ('^', '^'), ('^', '^'), ('^', '^'), ('^', '^'),
             ('^', '^'), ('^', '^'), ('^', '^')]
