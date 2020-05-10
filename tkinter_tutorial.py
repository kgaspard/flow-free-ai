import tkinter as tk
import random
import math
import util

main_config = dict()
main_config['width'] = 1200
main_config['height'] = 1200
main_config['bg'] = 'black'
main_config['title'] = 'Grid'

def init_frame(config):
    root = tk.Tk()

    # Define key functions
    def create_grid(self, x, y, color="#E7E7E7", min_offset = 50):
        total_width = config['width'] - 2*min_offset
        total_height = config['height'] - 2*min_offset
        square_size = min(total_height / y, total_width / x)
        x_0 = (config['width'] - x*square_size) / 2
        y_0 = (config['height'] - y*square_size) / 2
        # vertical lines:
        for i in range(x+1):
            self.create_line(x_0+ i*square_size, y_0 , x_0 + i*square_size, y_0 + y*square_size
                , tag='grid_line', width = 2, fill=color)
        # horizontal lines:
        for i in range(y+1):
            self.create_line(x_0, y_0 + i*square_size, x_0 + x*square_size, y_0 + i*square_size
                , tag='grid_line', width = 2, fill=color)
        return {'x_0': x_0, 'y_0': y_0, 'square_size': square_size, 'x': x, 'y': y}

    def create_circle_in_grid_pos(self, grid_obj, x, y, color, diameter_percent = 0.8, **kwargs):
        x = grid_obj['x_0'] + (x+0.5)*grid_obj['square_size']
        y = grid_obj['y_0'] + (y+0.5)*grid_obj['square_size']
        r = grid_obj['square_size']*diameter_percent / 2
        self.create_oval(x-r, y-r, x+r, y+r, fill=color, **kwargs)

    # Init frame
    root.wm_title(config['title'])
    root.geometry(str(config['width'] or 800)+'x'+str(config['height'] or 600))
    root.configure(bg=main_config['bg'] or 'black')
    canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0, width = config['width'] or 800, height = config['height'] or 600, bg = main_config['bg'])
    tk.Canvas.create_grid = create_grid
    tk.Canvas.create_circle_in_grid_pos = create_circle_in_grid_pos
    canvas.grid()

    # Draw objects
    flow_grid = canvas.create_grid(x=15,y=15)
    for i in range(100):
        canvas.create_circle_in_grid_pos(x=math.floor(random.uniform(0,flow_grid['x'])), y=math.floor(random.uniform(0,flow_grid['y'])), grid_obj=flow_grid, color=util.random_color())
    print(flow_grid)
    root.mainloop()






init_frame(main_config)


