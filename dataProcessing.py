from dataParser import parse_files
from imageParser import parse_saved_files
from util import normalize_array,denormalize_array
import numpy as np
from sklearn.model_selection import train_test_split
import itertools

def combine_data_files_and_images(max_board_size=25,file_list=[],img_list=[]):
  problems1,solutions1 = parse_files(max_board_size=max_board_size,file_list=file_list)
  problems2,solutions2 = parse_saved_files(max_board_size=max_board_size,file_list=img_list)
  problems = problems1 + problems2
  solutions = solutions1 + solutions2
  return problems,solutions

def generate_matrix_permutations(matrix,max_val):

  def generate_symmetric_group_array(n):
    return np.array([permutation for permutation in itertools.permutations([i for i in range(1,n+1)])])

  def permute_matrix(matrix,permutation,n):
    return np.array([permutation[i-1]*(matrix==i) for i in range(1,n+1)]).sum(axis=0)
  
  matrices = []
  sga = generate_symmetric_group_array(max_val)
  for permutation in sga:
    matrices.append(permute_matrix(matrix,permutation,max_val))
  return matrices

def generate_matrix_rotations(matrix):
  rotations = []
  for i in range(4):
    rotations.append(np.rot90(matrix,i))
    rotations.append(np.rot90(np.flip(matrix,i%2),i//2))
  return rotations

def process_data_for_training(max_board_size=15,file_list=[],with_permutations=False, with_rotations=False, test_size=0.05):
    problems0,solutions0 = combine_data_files_and_images(max_board_size=max_board_size,file_list=file_list)
    features=[]
    labels=[]
    
    max_val = np.max(problems0)  # note we are using 1-indexed colours here

    if not with_permutations:
      problems = problems0
      solutions = solutions0
    else:
      problems = []
      solutions = []
      if with_rotations:
        for problem in problems0:
          for permutation in generate_matrix_permutations(problem,max_val):
            for rotation in generate_matrix_rotations(permutation):
              problems.append(rotation)
        for solution in solutions0:
          for permutation in generate_matrix_permutations(solution,max_val):
            for rotation in generate_matrix_rotations(permutation):
              solutions.append(rotation)
      else:
        for problem in problems0:
          for permutation in generate_matrix_permutations(problem,max_val):
            problems.append(permutation)
        for solution in solutions0:
          for permutation in generate_matrix_permutations(solution,max_val):
            solutions.append(permutation)
    
    features = np.array(problems).reshape(len(problems),max_board_size,max_board_size,1)
    features = normalize_array(features,max_val)

    labels = np.array(solutions).reshape(len(solutions),max_board_size*max_board_size,1)

    del(problems)
    del(solutions)

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=test_size, random_state=42)
    return x_train, x_test, y_train, y_test, max_val