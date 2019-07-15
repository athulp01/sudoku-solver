from suduku import *

img = cv2.imread('./images/sudoko.png')

sudoku_img = load_sudoku('./images/sudoko.png')
sudoku_as_list = get_data(sudoku_img, img)

solve(sudoku_as_list, 0, 0)

create_image(sudoku_as_list)
