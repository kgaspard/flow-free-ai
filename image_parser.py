import requests
from PIL import Image
from io import BytesIO
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.feature import peak
from skimage.feature import corner_fast, corner_peaks

x_pixel_for_line_detection = 10

def url_to_array(url):
  try:
    if url.startswith('http'):
      r = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
      im = Image.open(BytesIO(r.content))
    else:
        im = Image.open(url)
    return np.array(im)
  except Exception as e:
    print('invalid image at '+url)

def thicken_line(line, thickness=10):
  return np.tile(line,(thickness,1,1))

def get_line_peaks(line,min_distance=3,threshold_rel=0.5):
  
  def eliminate_diffs(sample,min_distance):  # we specified min_distance for peak_local_max but fails if we have flat peaks, so need this function
    sample = np.sort(sample)
    diff = np.diff(sample)
    indices_to_delete = np.where(diff<min_distance)[0]+1
    return np.delete(sample,indices_to_delete)

  sample = rgb2gray(thicken_line(line,thickness=1)).squeeze()
  peaks = peak.peak_local_max(sample,min_distance=min_distance,threshold_rel=threshold_rel)
  return eliminate_diffs(peaks.squeeze(),min_distance)

def get_array_centres(array):
  array = np.sort(array)
  return (array[:-1]+np.diff(array)*0.5).astype(int)

def get_y_pixel_for_line_detection(img,x_pixel_for_line_detection,pixels_after_line=3):
  vertical_line_sample = img[:,x_pixel_for_line_detection]
  peaks = get_line_peaks(vertical_line_sample)
  return peaks[0]+pixels_after_line

def get_centroids(img):
  y_pixel_for_line_detection = get_y_pixel_for_line_detection(img,x_pixel_for_line_detection)
  grid_x = get_line_peaks(img[y_pixel_for_line_detection])
  grid_y = get_line_peaks(img[:,x_pixel_for_line_detection])
  x_centroids = get_array_centres(grid_x)
  y_centroids = get_array_centres(grid_y)
  return x_centroids,y_centroids

def get_centroid_values(img):
  x_centroids,y_centroids = get_centroids(img)
  return img[np.ix_(y_centroids,x_centroids)]

def get_grid_square_dark_peaks(img):
  y_pixel_for_line_detection = get_y_pixel_for_line_detection(img,x_pixel_for_line_detection)
  grid_x = get_line_peaks(img[y_pixel_for_line_detection])
  grid_y = get_line_peaks(img[:,x_pixel_for_line_detection])
  output = np.zeros((len(grid_y)-1,len(grid_x)-1))
  for ix in range(len(grid_x)-1):
    for iy in range(len(grid_y)-1):
      sub_img = img[grid_y[iy]:grid_y[iy+1],grid_x[ix]:grid_x[ix+1]]
      sub_img = rgb2gray(sub_img)
      histogram,bin_edges = np.histogram(sub_img, bins=256, range=(0, 1))
      black_index = histogram[0]
      output[iy,ix] = black_index
  return output

def smart_corners(img):
  img = rgb2gray(img[128:441])
  plt.imshow(img)
  plt.show()
  a = corner_peaks(corner_fast(img, 10), min_distance=3)
  return a

def generate_solution_from_image(img,start_index=1):
  shape = get_centroid_values(img).shape
  colors = np.unique(get_centroid_values(img).reshape(shape[0]*shape[1],shape[2]),axis=0)
  solution = np.zeros((shape[0],shape[1]))
  for i,color in enumerate(colors):
    solution = solution + i*(get_centroid_values(img) == colors[i]).all(axis=2)
  return solution.astype(int)+start_index

def generate_problem_and_solution_from_image(img):
  dark_peak_values = get_grid_square_dark_peaks(img)
  average = np.average(dark_peak_values)
  solution = generate_solution_from_image(img)
  return solution * (dark_peak_values < average), solution

def export_to_file(url_list,path="data/image_parser_output.txt"):

  def array_to_string(array):
    return np.array2string(array,separator=',',max_line_width=99999999)[1:-1]
  
  f = open(path, "w")
  for url in url_list:
    try:
      img = url_to_array(url)
      problem,solution = generate_problem_and_solution_from_image(img)
      shape = problem.shape
      string_to_write = str(shape[0])+'x'+str(shape[1])+':'+array_to_string(problem.flatten())+'='+array_to_string(solution.flatten())
      f.write(string_to_write)
      f.write('\n')
    except Exception as e:
      print(url,'-------',e)
  f.close()

def url_list_generator(packs):
  url_list = []
  url_base = 'https://flowfreesolutions.com/solution-pictures/flow/'
  for pack in packs:
    start = pack[1] if len(pack)>2 else 1 
    end = pack[2]+1 if len(pack)>2 else pack[1]+1
    for i in range(start,end):
      string = url_base+pack[0]+'/flow-'+pack[0]+'-'+str(i)+'.png'
      url_list.append(string)
  return url_list

def local_file_list_generator(path):
  files = os.listdir(path)
  return [path+f for f in files]

def string_to_matrices(string, max_board_size=25):

  def string_to_matrix(string,size_x,size_y):
    array = np.array([int(elem) for elem in string.split(',')])
    array = array.reshape(size_x,size_y)
    array = np.pad(array,((0,max_board_size-size_x),(0,max_board_size-size_y)))
    return array

  size_split = string.split(':')
  board_size = size_split.pop(0).split('x')
  size_x,size_y = int(board_size[0]),int(board_size[1])
  problem,solution = size_split[0].split('=')
  problem,solution = string_to_matrix(problem,size_x,size_y),string_to_matrix(solution,size_x,size_y)
  return problem,solution

##### Parse files

def parse_saved_files(max_board_size=25,file_list=[]):
  problems = []
  solutions = []
  for f in file_list:
      levels = open(f, "r").read().splitlines()
      for level in levels:
        problem,solution = string_to_matrices(level,max_board_size=max_board_size)
  return problems,solutions

def main():
  packs = [('regular',150),('bonus',150),('green',20)]
  packs_five = [('regular',1,30),('bonus',1,30),('blue',1,30),('green',1,30),('intro',1,8),('kids',1,60)]
  url_list = url_list_generator(packs_five)
  url_list = local_file_list_generator('data/images/')
  
  export_to_file(url_list)

if __name__ == "__main__":
  main()