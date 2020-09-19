import requests
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.feature import peak

url = 'https://flowfreesolutions.com/solution-pictures/flow/regular/flow-regular-1.png'
y_pixel_for_line_detection = 134
x_pixel_for_line_detection = 10

def url_to_array(url):
  r = requests.get(url)
  im = Image.open(BytesIO(r.content))
  return np.array(im)

def thicken_line(line, thickness=10):
  return np.tile(line,(thickness,1,1))

def get_line_peaks(line):
  sample = rgb2gray(thicken_line(line,thickness=1)).squeeze()
  peaks = peak.peak_local_max(sample,min_distance=2)
  return peaks.squeeze()

img = url_to_array(url)

def get_array_centres(array):
  array = np.sort(array)
  return (array[:-1]+np.diff(array)*0.5).astype(int)

def get_centroids(img):
  grid_x = get_line_peaks(img[y_pixel_for_line_detection])
  grid_y = get_line_peaks(img[:,x_pixel_for_line_detection])
  x_centroids = get_array_centres(grid_x)
  y_centroids = get_array_centres(grid_y)
  return x_centroids,y_centroids

def get_centroid_values(img):
  x_centroids,y_centroids = get_centroids(img)
  return img[np.ix_(y_centroids,x_centroids)]

## Exported functions:

def generate_solution_from_image(img,start_index=1):
  shape = get_centroid_values(img).shape
  colors = np.unique(get_centroid_values(img).reshape(shape[0]*shape[1],shape[2]),axis=0)
  solution = np.zeros((shape[0],shape[1]))
  for i,color in enumerate(colors):
    solution = solution + i*(get_centroid_values(img) == colors[i]).all(axis=2)
  return solution.astype(int)+start_index

print(generate_solution_from_image(img))