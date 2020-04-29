import sys
import win32com.client
from pathlib import Path
from PIL import Image

ALPHA_COLOR = (0, 0, 0)  # black

def main(xls_filename, ncol, nrow, filename):
    app = win32com.client.Dispatch("Excel.Application")
    abspath = str(Path(xls_filename).resolve())
    workbook = app.Workbooks.Open(abspath, UpdateLinks=0, ReadOnly=True)
    sheet = workbook.Worksheets("Sheet1")

    data = []
    for row in range(nrow):
        for col in range(ncol):
            color = int(sheet.Cells.Item(row+1, col+1).Interior.Color)
            RGB = (color % 256, color // 256 % 256, color // 256 // 256)
            alpha = 255
            if RGB == ALPHA_COLOR:
               alpha = 0
            RGBA = (color % 256, color // 256 % 256, color // 256 // 256, alpha)
            data.append(RGBA)

    img = Image.new("RGBA", (ncol, nrow))
    for row in range(nrow):
        for col in range(ncol):
            idx = row * ncol + col
            color = data[idx]
            img.putpixel((col, row), color)
    img.save(filename)

    workbook.Close()
    app.Quit()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("usege: py {} <xls filename> <ncol> <nrow> <png filename>\n".format(sys.argv[0]))
        sys.exit()
    xls_file = sys.argv[1]
    ncol = int(sys.argv[2])
    nrow = int(sys.argv[3])
    png_file = sys.argv[4]
    main(xls_file, ncol, nrow, png_file)
