from math import ceil

class Cell:

    def __init__(
        self,
        x : int,
        y : int,
        value
    ):
        self.x = x
        self.y = y
        self.value = value
        if value is None:
            self.options =  {
                x : True
                for x in range(1,10)
            }
        else:
            self.options = {
                value : True
            }

    def is_solved(
        self
    ):
        return self.value is not None

    def set_value(
        self,
        value : int
    ):
        self.options = {
            value : True
        }
        self.value = value

    def remove_option(
        self,
        number : int
    ):
        if [self.x,self.y] == [2,3]:
            b=1
        if self.is_solved():
            return False
        if number in self.options:
            del self.options[number]
        if len(self.options) == 1:
            self.value = list(self.options.keys())[0]
            return self.value
        return False

    def get_axis_coords(
        self,
        N : int
    ):
        n = ceil(N/3)
        axis_coords = []
        for x in range((n*3)-2,(n*3)+1):
            axis_coords.append(x)
        return axis_coords

    def get_3x3_coords(self):
        ## Get the coords of all the cells in the cell's 3x3
        ##    except for itself and the cells in the same row & col
        x_coords = self.get_axis_coords(self.x)
        y_coords = self.get_axis_coords(self.y)
        cell_3x3_coords = []
        for xc in x_coords:
            for yc in y_coords:
                if (xc != self.x) & (yc != self.y):
                    cell_3x3_coords.append((xc,yc))
        return cell_3x3_coords