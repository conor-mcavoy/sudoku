# Author Conor McAvoy
# 7 May 2018

import argparse

class Col:
    def __init__(self):
        self.numbers = []

    def add(self, number):
        """Adds one element to the Col."""
        self.numbers.append(number)

class Row:
    def __init__(self, numbers):
        self.numbers = [n for n in numbers]

    def __str__(self):
        return ''.join(self.numbers)

class Box:
    def __init__(self, first_three):
        self.numbers = [n for n in first_three]

    def add(self, three_elements):
        """Adds three elements to the Box."""
        self.numbers.extend(three_elements)

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

    print(g)
            


if __name__ == "__main__":
    main()
