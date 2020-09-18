import tkinter as tk
import random
import time
import util
import functools
import numpy as np

class Graphics:

    def __init__(self, game):
        main_config = dict()
        main_config['width'] = 1200
        main_config['height'] = 1200
        main_config['bg'] = 'black'
        main_config['title'] = 'Grid'
        main_config['frame_rate'] = 5
        main_config['update_ms'] = int((1/main_config['frame_rate'])*1000)
        self.main_config = main_config
        self.game = game
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, borderwidth=0, highlightthickness=0, width = main_config['width'] or 800, height = main_config['height'] or 600, bg = main_config['bg'])
        self.flow_grid = self.create_grid(x=self.game.size[0],y=self.game.size[1])
        self.colors = util.color_array(game.num_pairs)
        self.canvas.grid()
    
    def create_grid(self, x, y, color="#E7E7E7", min_offset = 50):
        config = self.main_config
        total_width = config['width'] - 2*min_offset
        total_height = config['height'] - 2*min_offset
        square_size = min(total_height / y, total_width / x)
        x_0 = (config['width'] - x*square_size) / 2
        y_0 = (config['height'] - y*square_size) / 2
        # vertical lines:
        for i in range(x+1):
            self.canvas.create_line(x_0+ i*square_size, y_0 , x_0 + i*square_size, y_0 + y*square_size
                , tag='grid_line', width = 2, fill=color)
        # horizontal lines:
        for i in range(y+1):
            self.canvas.create_line(x_0, y_0 + i*square_size, x_0 + x*square_size, y_0 + i*square_size
                , tag='grid_line', width = 2, fill=color)
        return {'x_0': x_0, 'y_0': y_0, 'square_size': square_size, 'x': x, 'y': y}
    
    def create_circle_in_grid_pos(self, x, y, color, diameter_percent = 0.7, stipple=100, **kwargs):
        grid_obj = self.flow_grid
        x = grid_obj['x_0'] + (x+0.5)*grid_obj['square_size']
        y = grid_obj['y_0'] + (y+0.5)*grid_obj['square_size']
        r = grid_obj['square_size']*diameter_percent / 2
        stipple = '' if stipple == 100 else 'gray'+str(stipple)
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, stipple=stipple, **kwargs)

    def draw_path_line_in_grid_pos(self, x, y, direction_vector, color, diameter_percent = 0.2, **kwargs):
        grid_obj = self.flow_grid
        x = grid_obj['x_0'] + (x+0.5)*grid_obj['square_size']
        y = grid_obj['y_0'] + (y+0.5)*grid_obj['square_size']
        r = grid_obj['square_size']*diameter_percent / 2
        # x0,y0 = x+r,y+r
        # x1,y1 = x-r,y-r
        dir_x, dir_y = direction_vector
        x0,y0 = x + r - (2*r if dir_x <0 else 0), y - r + (2*r if dir_y>0 else 0)
        x1,y1 = x-dir_x*grid_obj['square_size'] - r + (2*r if dir_x <0 else 0), y-dir_y*grid_obj['square_size'] + r - (2*r if dir_y>0 else 0)
        return self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0, **kwargs)

    def init_frame(self):
        root = self.root
        config = self.main_config
        canvas = self.canvas

        # Init frame and drawing functions
        root.wm_title(config['title'])
        root.geometry(str(config['width'] or 800)+'x'+str(config['height'] or 600))
        root.configure(bg=config['bg'] or 'black')

    def draw_valves(self):
        for valve in self.game.valves:
            self.create_circle_in_grid_pos(x=valve[1][0], y=valve[1][1], color=self.colors[valve[0]])

    def draw_game(self):
        self.init_frame()
        print(util.get_duration(self.game.start_time,'game drawn'))
        self.root.after(0,self.update_from_game_state_paths)
        self.root.mainloop()

    def update_from_game_state_board(self, event=None):
        for x in range(self.game.size[0]):
            for y in range(self.game.size[1]):
                if not self.game.game_state.board_occupancy[x][y].isValve:
                    if self.game.game_state.board_occupancy[x][y].value >= 0:
                        self.create_circle_in_grid_pos(x=x, y=y, color=self.colors[self.game.game_state.board_occupancy[x][y].value], diameter_percent = 0.3)
                    elif self.game.game_state.board_occupancy[x][y].value < 0:
                        self.create_circle_in_grid_pos(x=x, y=y, color=self.main_config['bg'], diameter_percent = 0.3)
        self.root.after(self.main_config['update_ms'],self.update_from_game_state_board)

    def add_paths_to_canvas(self, game_state=None):
        if game_state is None: game_state = self.game.game_state
        for i in range(self.game.num_pairs):
            for pos_index in range(len(game_state.paths[i])):
                if pos_index == 0: continue
                pos = game_state.paths[i][pos_index]
                x,y = pos
                prev_pos = game_state.paths[i][pos_index-1]
                direction_vector = util.tupleDiff(pos,prev_pos)
                self.draw_path_line_in_grid_pos(x=x, y=y, direction_vector=direction_vector, color=self.colors[game_state.board_occupancy[x][y].value])

    def draw_game_state(self, game_state):
        self.init_frame()
        self.draw_valves()
        self.add_paths_to_canvas(game_state=game_state)
        print(util.get_duration(self.game.start_time,'game drawn'))
        self.root.mainloop()

    def update_from_game_state_paths(self, event=None):
        self.draw_valves()
        self.add_paths_to_canvas()
        self.root.after(self.main_config['update_ms'],self.update_from_game_state_paths)

    # For CNN Solutions:

    def draw_points(self,array):
        for x,y in np.ndindex(array.shape):
            if array[x,y]>-1:
                self.create_circle_in_grid_pos(x=x, y=y, color=self.colors[array[x,y]], diameter_percent = 0.3)


    def draw_game_from_2d_array(self,array):
        self.init_frame()
        self.draw_points(array)
        print(util.get_duration(self.game.start_time,'game drawn'))
        self.root.mainloop()