# Author Conor McAvoy
# 7 May 2018

import argparse


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
        self.updated = False

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.rows)

    def add_cols(self, cols):
        self.cols = cols

    def add_row(self, row):
        self.rows.append(row)

    def add_boxes(self, boxes):
        self.boxes.extend(boxes)

    def solve(self, limit=1000):
        loop_counter = 0
        while not self.check_solved() and loop_counter < limit:
            self.updated = False
            self.simple_fills()
            if self.updated:
                continue

            for row_num in range(9):
                for col_num in range(9):
                    if self.rows[row_num][col_num] != '0':
                        continue
                    possible_values = {str(i) for i in range(1, 10)} \
                                      - set(self.cols[col_num]) \
                                      - set(self.rows[row_num]) \
                                      - set(self.boxes[3*(row_num//3)
                                                       + col_num//3])
                    if len(possible_values) == 1:
                        self.update_row(row_num, col_num, possible_values.pop())
            
            loop_counter += 1

    def simple_fills(self):
        col_num = 0
        for col in self.cols:
            if col.count('0') == 1:
                missing_num = str(45 - sum(map(int, col)))
                self.update_col(col_num, col.index('0'), missing_num)
            col_num += 1

        row_num = 0
        for row in self.rows:
            if row.count('0') == 1:
                missing_num = str(45 - sum(map(int, row)))
                self.update_row(row_num, row.index('0'), missing_num)
            row_num += 1

        box_num = 0
        for box in self.boxes:
            if box.get_numbers().count('0') == 1:
                missing_num = str(45 - sum(map(int, box.get_numbers())))
                self.update_box(box_num, box.get_numbers().index('0'),
                                missing_num)
            box_num += 1

    def update_col(self, col_num, col_pos, new_num):
        if self.cols[col_num][col_pos] == new_num:
            return
        self.cols[col_num][col_pos] = new_num
        self.update_row(col_pos, col_num, new_num)
        box_num = 3*(col_pos // 3) + col_num // 3
        box_pos = 3*(col_pos % 3) + col_num % 3
        self.update_box(box_num, box_pos, new_num)
        self.updated = True

    def update_row(self, row_num, row_pos, new_num):
        if self.rows[row_num][row_pos] == new_num:
            return
        self.update_col(row_pos, row_num, new_num)
        self.rows[row_num][row_pos] = new_num
        box_num = 3*(row_num // 3) + row_pos // 3
        box_pos = 3*(row_num % 3) + row_pos % 3
        self.update_box(box_num, box_pos, new_num)
        self.updated = True

    def update_box(self, box_num, box_pos, new_num):
        if self.boxes[box_num][box_pos] == new_num:
            return
        col_num = 3*(box_num % 3) + box_pos % 3
        col_pos = 3*(box_num // 3) + box_pos // 3
        self.update_col(col_num, col_pos, new_num)
        self.update_row(col_pos, col_num, new_num)
        self.boxes[box_num][box_pos] = new_num
        self.updated = True
            
    def check_solved(self):
        all_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for col in self.cols:
            if sorted(col) != all_numbers:
                return False
            
        for row in self.rows:
            if sorted(row) != all_numbers:
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
        all_cols = [[] for _ in range(9)]
        
        for line in f:
            i = 0
            for col in all_cols:
                col.append(line[i])
                i += 1
            
            g.add_row(list(line[:9]))

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
    if g.check_solved():
        print(g)
    else:
        print("Unable to solve after 1000 iterations.")


if __name__ == "__main__":
    main()
