# Author Conor McAvoy
# 7 May 2018

import argparse

class Col:
    def __init__(self):
        self.numbers = []

    def __getitem__(self, key):
        return self.numbers[key]

    def __setitem__(self, key, value):
        self.numbers[key] = value

    def add(self, number):
        """Adds one element to the Col."""
        self.numbers.append(number)

    def get_numbers(self):
        return self.numbers

class Row:
    def __init__(self, numbers):
        self.numbers = [n for n in numbers]

    def __str__(self):
        return ''.join(self.numbers)

    def __getitem__(self, key):
        return self.numbers[key]

    def __setitem__(self, key, value):
        self.numbers[key] = value

    def get_numbers(self):
        return self.numbers

class Box:
    def __init__(self, first_three):
        self.numbers = [n for n in first_three]

    def __getitem__(self, key):
        return self.numbers[key]

    def __setitem__(self, key, value):
        self.numbers[key] = value

    def add(self, three_elements):
        """Adds three elements to the Box."""
        self.numbers.extend(three_elements)

    def get_numbers(self):
        return self.numbers

class Grid:
    def __init__(self):
        self.rows = []
        self.boxes = []

    def __str__(self):
        return '\n'.join(str(row) for row in self.rows)

    def add_cols(self, cols):
        self.cols = cols

    def add_row(self, row):
        self.rows.append(row)

    def add_boxes(self, boxes):
        self.boxes.extend(boxes)

    def solve(self, limit=1000):
        loop_counter = 0
        while not self.check_solved() and loop_counter < limit:
            self.simple_fills()
            loop_counter += 1

    def simple_fills(self):
        col_num = 0
        for col in self.cols:
            if col.get_numbers().count('0') == 1:
                missing_num = str(45 - sum(map(int, col.get_numbers())))
                self.update_col(col_num, col.get_numbers().index('0'),
                                missing_num)
            col_num += 1

        row_num = 0
        for row in self.rows:
            if row.get_numbers().count('0') == 1:
                missing_num = str(45 - sum(map(int, row.get_numbers())))
                self.update_row(row_num, row.get_numbers().index('0'),
                                missing_num)
            row_num += 1

        

    def update_col(self, col_num, col_pos, new_num):
        if self.cols[col_num][col_pos] == new_num:
            return
        self.cols[col_num][col_pos] = new_num
        self.update_row(col_pos, col_num, new_num)
        box_num = 3*(col_pos // 3) + col_num // 3
        box_pos = 3*(col_pos % 3) + col_num % 3
        self.update_box(box_num, box_pos, new_num)

    def update_row(self, row_num, row_pos, new_num):
        if self.rows[row_num][row_pos] == new_num:
            return
        self.update_col(row_pos, row_num, new_num)
        self.rows[row_num][row_pos] = new_num
        box_num = 3*(row_num // 3) + row_pos // 3
        box_pos = 3*(row_num % 3) + row_pos % 3
        self.update_box(box_num, box_pos, new_num)

    def update_box(self, box_num, box_pos, new_num):
        if self.boxes[box_num][box_pos] == new_num:
            return
        col_num = 3*(box_num % 3) + box_pos % 3
        col_pos = 3*(box_num // 3) + box_pos // 3
        self.update_col(col_num, col_pos, new_num)
        self.update_row(col_pos, col_num, new_num)
        self.boxes[box_num][box_pos] = new_num
            
    def check_solved(self):
        all_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for col in self.cols:
            if sorted(col.get_numbers()) != all_numbers:
                return False
            
        for row in self.rows:
            if sorted(row.get_numbers()) != all_numbers:
                return False

        for box in self.boxes:
            if sorted(box.get_numbers()) != all_numbers:
                return False

        return True

        



def main():
    parser = argparse.ArgumentParser(description="Solve sudoku puzzles.")
    parser.add_argument("filename", help="name of location of sudoku file")

    args = parser.parse_args()
    filename = args.filename

    g = Grid()
    with open(filename, 'r') as f:
        line_count = 0
        col1 = Col()
        col2 = Col()
        col3 = Col()
        col4 = Col()
        col5 = Col()
        col6 = Col()
        col7 = Col()
        col8 = Col()
        col9 = Col()
        all_cols = [col1, col2, col3, col4, col5, col6, col7, col8, col9]
        
        for line in f:
            i = 0
            for col in all_cols:
                col.add(line[i])
                i += 1
            
            row = Row(line[0:9])
            g.add_row(row)

            if line_count % 3 == 0:
                box1 = Box(line[0:3])
                box2 = Box(line[3:6])
                box3 = Box(line[6:9])
            else:
                box1.add(line[0:3])
                box2.add(line[3:6])
                box3.add(line[6:9])

            if line_count % 3 == 2:
                g.add_boxes([box1, box2, box3])

            line_count += 1
                
        g.add_cols(all_cols)

    g.solve()
    print(g.check_solved())
    print(g)
            


if __name__ == "__main__":
    main()
