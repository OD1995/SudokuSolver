from datetime import datetime
from re import T
from src.SudokuReader.ExcelReader import ExcelReader
from src.Cell import Cell
from math import ceil
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Border, Side, Alignment

class Sudoku:

    def __init__(
        self,
        reader_type : str,
        *args,
        **kwargs
    ):
        if reader_type == "excel":
            reader = ExcelReader(*args,**kwargs)
        # else:
        #     print('h2')
        self.position_to_value = reader.position_to_value
        self.value_to_positions = reader.value_to_positions
        self.cells = self.get_cells()

    def get_cells(self):
        cells = {}
        for (x,y),val in self.position_to_value.items():
            cells[(x,y)] = Cell(x,y,val)
        return cells

    def solve(self):
        self.print_sudoku(0,0)
        self.number_fully_solved = {
            num : False
            for num in range(1,10)
        }
        print_count = 0
        while not all(self.number_fully_solved.values()):
            for num in range(1,10):
                if not self.number_fully_solved[num]:
                    new_solved = []
                    for x,y in self.value_to_positions[num]:
                        new_solved.extend(
                            self.remove_options_for_surrounding_cells(x,y,num)
                        )
                    new_solved.extend(self.check_all_groups(num))
                    new_solveds_exist = len(new_solved) > 0
                    if new_solveds_exist:
                        version = 0
                        new_solved_dict = {
                            version : new_solved
                        }
                        while new_solveds_exist:
                            version += 1
                            new_solved_dict[version] = []
                            for c in new_solved_dict[version-1]:
                                new_solved_dict[version].extend(
                                    self.remove_options_for_surrounding_cells(*c)
                                )
                                new_solved_dict[version].extend(
                                    self.check_all_relevant_groups(*c)
                                )
                                self.value_to_positions[c[2]].append((c[0],c[1]))
                            new_solveds_exist = len(new_solved_dict[version]) > 0
                    
                    self.number_fully_solved[num] = self.is_number_fully_solved(num)
                    print_count += 1
                    self.print_sudoku(num,print_count)

    def check_all_relevant_groups(
        self,
        x : int,
        y : int,
        num : int
    ):
        more_new_solveds = []
        R = self.check_row(num,y)
        if R:
            more_new_solveds.append(R)
        C = self.check_col(num,x)
        if C:
            more_new_solveds.append(C)
        G = self.check_3x3(
            num,
            ceil(y/3),
            ceil(x/3)
        )
        if G:
            more_new_solveds.append(G)   
        return more_new_solveds     

    def check_all_groups(
        self,
        num : int
    ):
        more_new_solveds = []
        for i in range(1,10):
            R = self.check_row(num,i)
            if R:
                more_new_solveds.append(R)
            C = self.check_col(num,i)
            if C:
                more_new_solveds.append(C)
        for j in range(1,4):
            for k in range(1,4):
                G = self.check_3x3(num,j,k)
                if G:
                    more_new_solveds.append(G)
        return more_new_solveds


    def check_row(
        self,
        value : int,
        row_num : int
    ):
        ## Check if `value` has only one possible answer in the row
        possible_answer = None
        for xc in range(1,10):
            cell = self.cells[xc,row_num]
            if value == cell.value:
                return False
            elif value in cell.options:
                if possible_answer is not None:
                    return False
                else:
                    possible_answer = (xc,row_num)
        ## If we've got to this point then `possible_answer` is the only option
        self.cells[possible_answer[0],possible_answer[1]].set_value(value)
        return (possible_answer[0],possible_answer[1],value)

    def check_col(
        self,
        value : int,
        col_num : int
    ):
        ## Check if `value` has only one possible answer in the col
        possible_answer = None
        for yc in range(1,10):
            cell = self.cells[col_num,yc]
            if value == cell.value:
                return False
            elif value in cell.options:
                if possible_answer is not None:
                    return False
                else:
                    possible_answer = (col_num,yc)
        ## If we've got to this point then `possible_answer` is the only option
        self.cells[possible_answer[0],possible_answer[1]].set_value(value)
        return (possible_answer[0],possible_answer[1],value)

    def check_3x3(
        self,
        value : int,
        row_ix : int,
        col_ix : int
    ):
        if (value,row_ix,col_ix) == (8,1,1):
            c=1
        ## Check if `value` has only one possible answer in the 3x3
        possible_answer = None
        for x,y in self.get_3x3_coords(col_ix,row_ix):
            cell = self.cells[x,y]
            if value == cell.value:
                return False
            elif value in cell.options:
                if possible_answer is not None:
                    return False
                else:
                    possible_answer = (x,y)
        ## If we've got to this point then `possible_answer` is the only option
        self.cells[possible_answer[0],possible_answer[1]].set_value(value)
        return (possible_answer[0],possible_answer[1],value)


    def get_3x3_coords(
        self,
        col_ix : int,
        row_ix : int
    ):
        return_me = []
        for x in range((3*col_ix)-2,(3*col_ix)+1):
            for y in range((3*row_ix)-2,(3*row_ix)+1):
                return_me.append((x,y))
        return return_me

    def remove_options_for_surrounding_cells(
        self,
        x : int,
        y : int,
        num : int
    ):
        if (x,y) == (4,1):
            a=1
        new_solved = []
        ## Remove `num` as an option for all the cells in the same row
        for y0 in range(1,10):
            if y0 != y:
                solved_val = self.cells[(x,y0)].remove_option(num)
                if solved_val:
                    new_solved.append((x,y0,solved_val))
        ## Remove `num` as an option for all the cells in the same row
        for x0 in range(1,10):
            if x0 != x:
                solved_val = self.cells[(x0,y)].remove_option(num)
                if solved_val:
                    new_solved.append((x0,y,solved_val))
        ## Remove `num` as an option for all the cells in the same 3x3
        for x1,y1 in self.cells[(x,y)].get_3x3_coords():
            solved_val = self.cells[(x1,y1)].remove_option(num)
            if solved_val:
                new_solved.append((x1,y1,solved_val))
        return new_solved

    def is_number_fully_solved(
        self,
        num : int
    ):
        return len(self.value_to_positions[num]) == 9

    def to_excel(
        self
    ):
        wb = Workbook()
        ws = wb.active
        filename = f"{datetime.now().timestamp()}.xlsx"
        black = Side(border_style='thin', color='000000')
        white = None#Side(border_style='thin', color='FFFFFF')
        for x in range(1,10):
            for y in range(1,10):
                cell = self.cells[x,y]
                address = f"{get_column_letter(x+1)}{y+1}"
                if cell.value is not None:
                    ws[address] = cell.value
                    ws[address].font = Font(bold=True)
                T = black if y == 1 else white
                L = black if x == 1 else white
                B = black if (y % 3) == 0 else white
                R = black if (x % 3) == 0 else white
                ws[address].border = Border(top=T,bottom=B,left=L,right=R)
                ws[address].alignment = Alignment(horizontal='center')
            ws.column_dimensions[get_column_letter(x+1)].width = 3.429
        wb.save(filename)

    def print_sudoku(
        self,
        num : int,
        print_count : int,
        A=False
    ):
        Ps = []
        ns = 0
        for y in range(1,10):
            print_me = "|"
            for x in range(1,10):
                raw_val = self.cells[(x,y)].value
                if raw_val is None:
                    val = " "
                else:
                    val = str(raw_val)
                    ns += 1
                print_me += val
                if x % 3 == 0:
                    print_me += "|"
            Ps.append(print_me)
            if y % 3 == 0:
                Ps.append("-"*13)
        print("-------------------------------------")
        print(f"Focusing on {num}")
        print(f"Print count: {print_count}")
        print(f"Numbers solved: {ns}")
        if A:
            print("-"*13)
            for P in Ps:
                print(P)

        if print_count > 50:
            self.to_excel()
            raise ValueError('too many prints')