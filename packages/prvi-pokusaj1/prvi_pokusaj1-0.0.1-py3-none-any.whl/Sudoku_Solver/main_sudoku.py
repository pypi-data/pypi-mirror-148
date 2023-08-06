import sys
import os
from modules.class_sudoku import Sudoku
from modules.solver_sudoku import solve, print_matrix

if __name__ == '__main__':
    
    img = os.path.abspath(str(sys.argv[1])) 
    s1 = Sudoku(img)

    s1.edge_det()
    s1.warp_perspective()
    s1.thresholding()
    dim = s1.num_detection()
    solve(dim)
    print_matrix(dim)

