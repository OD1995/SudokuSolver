from src.Sudoku import Sudoku

sr = Sudoku(
    reader_type='excel',
    excel_path='Examples.xlsx',
    sheet_name='1'
)
# sr.print_sudoku(1)
sr.solve()