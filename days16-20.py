from copy import deepcopy
#from smtpd import program
import re
#from encodings.punycode import selective_find

import numpy as np
from numpy import array

class DayXX:
    def __init__(self):
        self.data = []

    def set_data(self):
        with open("dayXX.t.txt", "r") as file:
            for line in file:
                self.data.append([])
                for char in line.strip():
                    self.data[-1].append(char)

    def process_data(self):
        x=0

    def output(self):
        self.set_data()

class Day16:
    def __init__(self):
        self.grid = []
        self.scores_on_grid = []

        self.start_p = [0,0]
        self.end_p = [0,0]
        self.start_dir = np.array([0,1])

        self.num_rows = 0
        self.num_cols = 0

        ##############################
        # These lists should be the same size
        self.paths = [] # init val filled later
        self.dirs = [self.start_dir]
        self.path_scores = [0]
        self.paths_contd = [True]
        ####################################

        self.best_path = []
        self.best_paths = []
        self.best_path_score = -1

        self.num_best_path_tiles = 0

        self.known_best_path = [array([139,   1]), array([139,   2]), array([139,   3]), array([139,   4]), array([139,   5]), array([138,   5]), array([137,   5]), array([136,   5]), array([135,   5]), array([135,   6]), array([135,   7]), array([135,   8]), array([135,   9]), array([136,   9]), array([137,   9]), array([137,  10]), array([137,  11]), array([136,  11]), array([135,  11]), array([134,  11]), array([133,  11]), array([132,  11]), array([131,  11]), array([131,  12]), array([131,  13]), array([130,  13]), array([129,  13]), array([128,  13]), array([127,  13]), array([126,  13]), array([125,  13]), array([125,  12]), array([125,  11]), array([124,  11]), array([123,  11]), array([122,  11]), array([121,  11]), array([120,  11]), array([119,  11]), array([118,  11]), array([117,  11]), array([116,  11]), array([115,  11]), array([114,  11]), array([113,  11]), array([112,  11]), array([111,  11]), array([110,  11]), array([109,  11]), array([108,  11]), array([107,  11]), array([106,  11]), array([105,  11]), array([105,  10]), array([105,   9]), array([105,   8]), array([105,   7]), array([104,   7]), array([103,   7]), array([102,   7]), array([101,   7]), array([100,   7]), array([99,  7]), array([98,  7]), array([97,  7]), array([96,  7]), array([95,  7]), array([94,  7]), array([93,  7]), array([92,  7]), array([91,  7]), array([91,  8]), array([91,  9]), array([91, 10]), array([91, 11]), array([90, 11]), array([89, 11]), array([88, 11]), array([87, 11]), array([86, 11]), array([85, 11]), array([84, 11]), array([83, 11]), array([82, 11]), array([81, 11]), array([80, 11]), array([79, 11]), array([78, 11]), array([77, 11]), array([76, 11]), array([75, 11]), array([74, 11]), array([73, 11]), array([72, 11]), array([71, 11]), array([70, 11]), array([69, 11]), array([69, 10]), array([69,  9]), array([68,  9]), array([67,  9]), array([66,  9]), array([65,  9]), array([65,  8]), array([65,  7]), array([65,  6]), array([65,  5]), array([65,  4]), array([65,  3]), array([66,  3]), array([67,  3]), array([67,  2]), array([67,  1]), array([66,  1]), array([65,  1]), array([64,  1]), array([63,  1]), array([63,  2]), array([63,  3]), array([63,  4]), array([63,  5]), array([63,  6]), array([63,  7]), array([63,  8]), array([63,  9]), array([63, 10]), array([63, 11]), array([63, 12]), array([63, 13]), array([62, 13]), array([61, 13]), array([60, 13]), array([59, 13]), array([59, 14]), array([59, 15]), array([58, 15]), array([57, 15]), array([57, 14]), array([57, 13]), array([56, 13]), array([55, 13]), array([54, 13]), array([53, 13]), array([52, 13]), array([51, 13]), array([50, 13]), array([49, 13]), array([48, 13]), array([47, 13]), array([46, 13]), array([45, 13]), array([45, 12]), array([45, 11]), array([45, 10]), array([45,  9]), array([44,  9]), array([43,  9]), array([42,  9]), array([41,  9]), array([40,  9]), array([39,  9]), array([39,  8]), array([39,  7]), array([39,  6]), array([39,  5]), array([38,  5]), array([37,  5]), array([36,  5]), array([35,  5]), array([34,  5]), array([33,  5]), array([32,  5]), array([31,  5]), array([30,  5]), array([29,  5]), array([28,  5]), array([27,  5]), array([27,  6]), array([27,  7]), array([27,  8]), array([27,  9]), array([26,  9]), array([25,  9]), array([24,  9]), array([23,  9]), array([22,  9]), array([21,  9]), array([21,  8]), array([21,  7]), array([22,  7]), array([23,  7]), array([23,  6]), array([23,  5]), array([23,  4]), array([23,  3]), array([22,  3]), array([21,  3]), array([20,  3]), array([19,  3]), array([19,  4]), array([19,  5]), array([19,  6]), array([19,  7]), array([18,  7]), array([17,  7]), array([17,  6]), array([17,  5]), array([16,  5]), array([15,  5]), array([14,  5]), array([13,  5]), array([12,  5]), array([11,  5]), array([10,  5]), array([9, 5]), array([9, 4]), array([9, 3]), array([8, 3]), array([7, 3]), array([7, 4]), array([7, 5]), array([6, 5]), array([5, 5]), array([5, 6]), array([5, 7]), array([5, 8]), array([5, 9]), array([ 5, 10]), array([ 5, 11]), array([ 5, 12]), array([ 5, 13]), array([ 5, 14]), array([ 5, 15]), array([ 5, 16]), array([ 5, 17]), array([ 5, 18]), array([ 5, 19]), array([ 5, 20]), array([ 5, 21]), array([ 5, 22]), array([ 5, 23]), array([ 5, 24]), array([ 5, 25]), array([ 5, 26]), array([ 5, 27]), array([ 4, 27]), array([ 3, 27]), array([ 3, 28]), array([ 3, 29]), array([ 3, 30]), array([ 3, 31]), array([ 3, 32]), array([ 3, 33]), array([ 3, 34]), array([ 3, 35]), array([ 4, 35]), array([ 5, 35]), array([ 6, 35]), array([ 7, 35]), array([ 7, 36]), array([ 7, 37]), array([ 7, 38]), array([ 7, 39]), array([ 7, 40]), array([ 7, 41]), array([ 7, 42]), array([ 7, 43]), array([ 7, 44]), array([ 7, 45]), array([ 7, 46]), array([ 7, 47]), array([ 7, 48]), array([ 7, 49]), array([ 7, 50]), array([ 7, 51]), array([ 8, 51]), array([ 9, 51]), array([10, 51]), array([11, 51]), array([12, 51]), array([13, 51]), array([13, 52]), array([13, 53]), array([13, 54]), array([13, 55]), array([13, 56]), array([13, 57]), array([13, 58]), array([13, 59]), array([13, 60]), array([13, 61]), array([13, 62]), array([13, 63]), array([13, 64]), array([13, 65]), array([13, 66]), array([13, 67]), array([13, 68]), array([13, 69]), array([12, 69]), array([11, 69]), array([10, 69]), array([ 9, 69]), array([ 8, 69]), array([ 7, 69]), array([ 6, 69]), array([ 5, 69]), array([ 5, 70]), array([ 5, 71]), array([ 4, 71]), array([ 3, 71]), array([ 3, 70]), array([ 3, 69]), array([ 2, 69]), array([ 1, 69]), array([ 1, 70]), array([ 1, 71]), array([ 1, 72]), array([ 1, 73]), array([ 1, 74]), array([ 1, 75]), array([ 1, 76]), array([ 1, 77]), array([ 2, 77]), array([ 3, 77]), array([ 3, 78]), array([ 3, 79]), array([ 3, 80]), array([ 3, 81]), array([ 2, 81]), array([ 1, 81]), array([ 1, 82]), array([ 1, 83]), array([ 2, 83]), array([ 3, 83]), array([ 4, 83]), array([ 5, 83]), array([ 5, 84]), array([ 5, 85]), array([ 5, 86]), array([ 5, 87]), array([ 5, 88]), array([ 5, 89]), array([ 5, 90]), array([ 5, 91]), array([ 6, 91]), array([ 7, 91]), array([ 8, 91]), array([ 9, 91]), array([ 9, 92]), array([ 9, 93]), array([ 9, 94]), array([ 9, 95]), array([ 9, 96]), array([ 9, 97]), array([ 9, 98]), array([ 9, 99]), array([  9, 100]), array([  9, 101]), array([  9, 102]), array([  9, 103]), array([  9, 104]), array([  9, 105]), array([  9, 106]), array([  9, 107]), array([  9, 108]), array([  9, 109]), array([  9, 110]), array([  9, 111]), array([ 10, 111]), array([ 11, 111]), array([ 11, 112]), array([ 11, 113]), array([ 11, 114]), array([ 11, 115]), array([ 11, 116]), array([ 11, 117]), array([ 12, 117]), array([ 13, 117]), array([ 13, 118]), array([ 13, 119]), array([ 13, 120]), array([ 13, 121]), array([ 14, 121]), array([ 15, 121]), array([ 15, 122]), array([ 15, 123]), array([ 14, 123]), array([ 13, 123]), array([ 13, 124]), array([ 13, 125]), array([ 14, 125]), array([ 15, 125]), array([ 16, 125]), array([ 17, 125]), array([ 17, 126]), array([ 17, 127]), array([ 18, 127]), array([ 19, 127]), array([ 19, 128]), array([ 19, 129]), array([ 19, 130]), array([ 19, 131]), array([ 20, 131]), array([ 21, 131]), array([ 21, 130]), array([ 21, 129]), array([ 21, 128]), array([ 21, 127]), array([ 22, 127]), array([ 23, 127]), array([ 23, 128]), array([ 23, 129]), array([ 24, 129]), array([ 25, 129]), array([ 26, 129]), array([ 27, 129]), array([ 28, 129]), array([ 29, 129]), array([ 29, 130]), array([ 29, 131]), array([ 29, 132]), array([ 29, 133]), array([ 29, 134]), array([ 29, 135]), array([ 29, 136]), array([ 29, 137]), array([ 29, 138]), array([ 29, 139]), array([ 28, 139]), array([ 27, 139]), array([ 26, 139]), array([ 25, 139]), array([ 24, 139]), array([ 23, 139]), array([ 22, 139]), array([ 21, 139]), array([ 21, 138]), array([ 21, 137]), array([ 21, 136]), array([ 21, 135]), array([ 22, 135]), array([ 23, 135]), array([ 24, 135]), array([ 25, 135]), array([ 25, 136]), array([ 25, 137]), array([ 26, 137]), array([ 27, 137]), array([ 27, 136]), array([ 27, 135]), array([ 27, 134]), array([ 27, 133]), array([ 26, 133]), array([ 25, 133]), array([ 24, 133]), array([ 23, 133]), array([ 22, 133]), array([ 21, 133]), array([ 20, 133]), array([ 19, 133]), array([ 18, 133]), array([ 17, 133]), array([ 17, 132]), array([ 17, 131]), array([ 16, 131]), array([ 15, 131]), array([ 15, 132]), array([ 15, 133]), array([ 15, 134]), array([ 15, 135]), array([ 15, 136]), array([ 15, 137]), array([ 15, 138]), array([ 15, 139]), array([ 14, 139]), array([ 13, 139]), array([ 12, 139]), array([ 11, 139]), array([ 10, 139]), array([  9, 139]), array([  8, 139]), array([  7, 139]), array([  7, 138]), array([  7, 137]), array([  8, 137]), array([  9, 137]), array([  9, 136]), array([  9, 135]), array([ 10, 135]), array([ 11, 135]), array([ 11, 134]), array([ 11, 133]), array([ 10, 133]), array([  9, 133]), array([  9, 132]), array([  9, 131]), array([  8, 131]), array([  7, 131]), array([  6, 131]), array([  5, 131]), array([  5, 132]), array([  5, 133]), array([  4, 133]), array([  3, 133]), array([  3, 134]), array([  3, 135]), array([  2, 135]), array([  1, 135]), array([  1, 136]), array([  1, 137]), array([  1, 138]), array([  1, 139])]


    def set_data(self):
        with open("day16.1.txt", "r") as file:
            for line in file:
                self.grid.append([])
                for char in line.strip():
                    num = 0
                    if char == '#':
                        num = 1
                    elif char == 'S':
                        self.start_p = np.array([len(self.grid)-1, len(self.grid[-1])])
                    elif char == 'E':
                        self.end_p = np.array([len(self.grid) - 1, len(self.grid[-1])])
                        num = 2

                    self.grid[-1].append(num)

        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.paths = [[self.start_p]]

        self.scores_on_grid = [[]] * self.num_rows
        for i in range(len(self.scores_on_grid)):
            self.scores_on_grid[i] = [-1] * self.num_cols

    # make data for every grid tile and have the lowest score in each of them, each time
    # that a path runs into it, it either changes from -1 if it's the first time, or chooses
    # the better score
    def process_data(self):
        print("paths init:", self.paths)
        test_count = 0 # static
        test_count_max = 10**(9)
        #test_count_max = 100
        check_dirs = [np.array([-1, 0]), np.array([0, 1]), np.array([1, 0]), np.array([0, -1])]
        bad_paths_i = [] # unused in this scope
        while True and test_count < test_count_max: # loop for each step in the paths
            test_count += 1
            print("------------------------")
            print("Step #" + str(test_count), "num paths:", len(self.paths))
            #print(self.dirs)
            new_coords_to_append = []
            all_add_scores = []
            all_dirs = []
            extra_new_coords_to_append = []
            extra_all_add_scores = []
            extra_all_dirs = []
            extra_is = []

            bad_paths_i = []
            for i, path in enumerate(self.paths):
                if self.paths_contd[i] == False:
                    #new_coords_to_append.append(-1)
                    continue

                orig_score = self.path_scores[i]
                dir = self.dirs[i]

                last_pos = path[-1]
                #dir = self.start_dir
                #if len(path) > 1:
                #    dir = last_pos - path[-2]

                coords_to_append = []
                add_scores = []
                dirs = []
                good_path = False
                for check_dir in check_dirs:
                    check_pos = last_pos + check_dir
                    #print("check pos:", check_pos, last_pos, check_dir)
                    same_dir = self.coords_same(check_dir, dir)
                    if self.coords_same(check_dir, -dir): # don't check behind
                        continue
                    elif self.grid_num_at_space(check_pos) == 1: # wall hit
                        continue
                    elif self.grid_num_at_space(check_pos) == 2: # end hit
                        # make path inactive
                        self.paths[i].extend(np.array([check_pos]))
                        #self.paths[i][-1] = (np.array(check_pos))
                        self.paths_contd[i] = False
                        self.dirs[i] = check_dir
                        coords_to_append = []
                        good_path = True
                        #'''
                        if same_dir:
                            self.path_scores[i] += 1
                        else:
                            self.path_scores[i] += 1001
                        #'''

                        if self.path_scores[i] < self.best_path_score or self.best_path_score == -1:
                            self.best_path = self.paths[i].copy()
                            self.best_path_score = self.path_scores[i]

                        break
                    elif self.does_path_contain_coords(i, check_pos): # also check here if path already contains the coord
                        continue
                    else: # add to (to-add-to) path unless too far over score grid score value
                        if same_dir:
                            added_score = orig_score + 1
                            #add_scores.append(orig_score + 1)
                        else:
                            added_score = orig_score + 1001
                            #add_scores.append(orig_score + 1001)

                        score_on_grid = self.scores_on_grid[check_pos[0]][check_pos[1]]
                        if score_on_grid == -1 or score_on_grid > added_score:
                            self.scores_on_grid[check_pos[0]][check_pos[1]] = added_score
                        elif score_on_grid + 1000 < added_score: # too far over score grid score value
                            continue

                        coords_to_append.append(check_pos)
                        dirs.append(check_dir)
                        good_path = True

                        add_scores.append(added_score)

                num_coords_to_append = len(coords_to_append)
                if num_coords_to_append == 0:
                    self.paths_contd[i] = False
                    if not good_path:
                        bad_paths_i.append(i)
                    continue
                new_coords_to_append.append(coords_to_append)
                all_add_scores.append(add_scores)
                all_dirs.append(dirs)
                #print("A", new_coords_to_append, all_add_scores, all_dirs)
                #print("B", self.paths, self.dirs, self.path_scores)
                self.paths[i].extend(np.array([coords_to_append[0]]))
                #self.paths[i][-1] = (np.array(coords_to_append[0]))
                self.dirs[i] = dirs[0]
                self.path_scores[i] = add_scores[0]
                #print("C", self.paths, self.dirs, self.path_scores)
                if num_coords_to_append > 1:
                    extra_is_to_add = [i] * (num_coords_to_append - 1)
                    extra_is.extend(extra_is_to_add)

                    #print("F", coords_to_append[1:], all_add_scores[1:], all_dirs[1:])
                    extra_new_coords_to_append.extend(coords_to_append[1:])
                    extra_all_add_scores.extend(add_scores[1:])
                    extra_all_dirs.extend(dirs[1:])



            #print("paths0:", self.paths)
            #print("dirs0:", self.dirs)
            #print("scores0:", self.path_scores)
            #print("contd0:", self.paths_contd)
            #print("extra coords:", extra_new_coords_to_append)
            #print("extra scores:", extra_all_add_scores)
            #print("extra dirs:", extra_all_dirs)

            for i, new_coords in enumerate(extra_new_coords_to_append):
                orig_path_i = extra_is[i]
                new_path = self.paths[orig_path_i].copy()
                new_path[-1] = new_coords
                self.paths.append(new_path)
                self.dirs.append(extra_all_dirs[i])
                self.path_scores.append(extra_all_add_scores[i])
                self.paths_contd.append(True)

            # Get rid of dead-end paths
            for bad_path_i in bad_paths_i[::-1]:
                #print("a*********popped path:", self.paths[bad_path_i])
                #if self.does_path_contain_coords(bad_path_i, array([9,3])):
                #    print("AAAAAAA\nAAAAAAAAA")
                self.paths.pop(bad_path_i)
                self.dirs.pop(bad_path_i)
                self.path_scores.pop(bad_path_i)
                self.paths_contd.pop(bad_path_i)

            #print("paths1:", self.paths)
            #print("dirs1:", self.dirs)
            #print("scores1:", self.path_scores)
            #print("contd1:", self.paths_contd)

            # Get rid of finished paths that do not have the best score
            bad_paths_i = []
            if self.best_path_score > -1:
                for i in range(len(self.paths_contd)):
                    if not self.paths_contd[i] and self.path_scores[i] != self.best_path_score:
                        bad_paths_i.append(i)
            for bad_path_i in bad_paths_i[::-1]:
                #print("b*********popped path:", self.paths[bad_path_i])
                #if self.does_path_contain_coords(bad_path_i, array([9,3])):
                #    print("AAAAAAA\nAAAAAAAAA")
                self.paths.pop(bad_path_i)
                self.dirs.pop(bad_path_i)
                self.path_scores.pop(bad_path_i)
                self.paths_contd.pop(bad_path_i)

            #print("paths2:", self.paths)
            #print("dirs2:", self.dirs)
            #print("scores2:", self.path_scores)
            #print("contd2:", self.paths_contd)

            # Get rid of paths that run into another path with a worse score (with -1000 leeway for an extra turn)
            '''
            bad_paths_i = []
            for i, path in enumerate(self.paths):
                end_coords = path[-1]
                path_score_1 = self.path_scores[i]
                for j, path2 in enumerate(self.paths):
                    if i == j:
                        continue
                    end_coords_2 = path2[-1]
                    for k, path2_coord in enumerate(path2):
                        if end_coords[0] == path2_coord[0] and end_coords[1] == path2_coord[1]:
                            #path2_i = i + j + 1
                            path_score_2 = self.path_scores[j]
                            better_path_score = min(path_score_1, path_score_2)
                            #print("path scores 1 and 2:", path_score_1, path_score_2) # look at steps 6 and 10 in test

                            if path_score_1 - 1000 > path_score_2:
                                if i not in bad_paths_i:
                                    bad_paths_i.append(i)
                            #elif path_score_1 < path_score_2: # if path score 2 is bigger, it could just be because it is farther along the best path
                                #bad_paths_i.append(j)
                            break
            #if test_count == 98:
            #    print(bad_paths_i)
            for bad_path_i in bad_paths_i[::-1]:
                #print("c*********popped path:", self.paths[bad_path_i])
                #if self.does_path_contain_coords(bad_path_i, array([9,3])):
                #    print("AAAAAAA\nAAAAAAAAA")
                self.paths.pop(bad_path_i)
                self.dirs.pop(bad_path_i)
                self.path_scores.pop(bad_path_i)
                self.paths_contd.pop(bad_path_i)
            '''

            if True not in self.paths_contd:
                break

        print("-------------------------")

    def does_path_contain_coords(self, path_i, coords):
        for path_coords in self.paths[path_i]:
            if path_coords[0] == coords[0] and path_coords[1] == coords[1]:
                return True
        return False

    def coords_same(self, array1, array2):
        if array1[0] == array2[0] and array1[1] == array2[1]:
            return True
        return False

    def grid_num_at_space(self, coords):
        #print(coords)
        return self.grid[coords[0]][coords[1]] # returns a char

    def find_num_best_tiles(self):
        self.best_paths = [] #self.paths
        for i in range(len(self.paths)):
            if self.path_scores[i] == self.best_path_score:
                self.best_paths.append(self.paths[i])
        print("num BEST paths in the end:", len(self.best_paths))
        unique_coords = []
        for path in self.best_paths:
            for coord in path:
                l_coord = list(coord)
                if l_coord not in unique_coords:
                    unique_coords.append(l_coord)

        self.num_best_path_tiles = len(unique_coords)

    def output(self):
        self.set_data()
        print("num rows/cols:", self.num_rows, self.num_cols)
        print(self.grid)
        print("start/end ps:", self.start_p, self.end_p)

        self.process_data()
        print("num paths in the end:", len(self.paths))

        self.find_num_best_tiles()
        print("BEST PATHS:", self.best_paths)
        print("BEST SCORE:", self.best_path_score)
        print("num_best_path_tiles:", self.num_best_path_tiles)

        #len_best = len(self.known_best_path)
        #print("len best known:", len_best)

        print("scores on grid", self.scores_on_grid)

class Day17:
    def __init__(self):
        self.data = []
        self.a = 0
        self.b = 0
        self.c = 0

        # bad output: 2,7,6,5,6,0,2,3,1
        '''
        output should be: 2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0
        
        1: b = a % 8
        2: b = b ^ 5
        3: c = a // 2**b
        4: b = b ^ 6
        5: b = b ^ c
        6: OUTPUT: b % 8
        7: a = a // 8
        8: restart program unless a == 0
        
        b=2
        b^c=2
        b^6^c=2
        b^6^(a//2**b)=2
        b^5^6^(a//2**(b^5)=2
        (a%8)^101^110^(a//2**((a%8)^101) % 8=2
        '''
        self.instruction_list = []
        self.program = []

        self.output_list = []
        self.output_list_str = ""

        self.read_instructions = []

        self.target = [2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0]

    def set_data(self):
        with open("day17.1.txt", "r") as file:
            phase = 0
            int_str = ""
            current_instruction = []
            for line in file:
                line = line.strip() + '.'
                for char in (line):
                    # self.games[-1].append(char)
                    # print("char", char, "int_str:", int_str)
                    if char.isdigit():
                        int_str = int_str + char
                    elif int_str != "":
                        num = int(int_str)
                        int_str = ""
                        if phase == 0:
                            self.a = num
                        elif phase == 1:
                            self.b = num
                        elif phase == 2:
                            self.c = num
                        elif phase % 2 == 1: # opcode
                            current_instruction = [num, -1]
                            self.program.append(num)
                        else:
                            current_instruction[1] = num
                            self.instruction_list.append(current_instruction)
                            self.program.append(num)
                        phase += 1

    def get_combo_operand(self, lit_operand):
        if 0 <= lit_operand <= 3:
            return lit_operand
        elif lit_operand == 4:
            return self.a
        elif lit_operand == 5:
            return self.b
        elif lit_operand == 6:
            return self.c
        elif lit_operand == 7:
            return -1
        return -2

    def process_data_2(self):
        good_a = -1
        best_found = False
        target_len = len(self.target)
        #target_len = 6
        good_nums = [3]
        for i in range(target_len):
            index = -1-i
            new_good_nums_before = []
            for j, num in enumerate(good_nums):
                self.a = num
                self.b = 0
                self.c = 0

                self.output_list = []
                self.output_list_str = ""

                self.process_data()

                #print(self.output_list)

                if self.output_list[0] == self.program[index]:
                    new_good_nums_before.append(num)
                    good_a = num
                    if i == target_len - 1:
                        best_found = True
                        print("good a:", num, "output:", self.output_list)
                        break

            good_nums = []
            for num_before in new_good_nums_before:
                n8 = 8*num_before
                n8_nums = list(range(n8, n8+8))
                good_nums.extend(n8_nums)
            if best_found:
                break
            #print(good_nums)
        print(good_nums)
        print("ANSWER:", good_a)

    def process_data(self):
        instruction_pointer = 0
        #for i, instruction in enumerate(self.instruction_list):
        while instruction_pointer < len(self.program)-1:
            #opcode = instruction[0]
            #lit_operand = instruction[1]
            opcode = self.program[instruction_pointer]
            lit_operand = self.program[instruction_pointer+1]
            combo_operand = self.get_combo_operand(lit_operand)
            self.read_instructions.append([opcode, lit_operand])

            if opcode == 0:
                div = self.a // 2**(combo_operand)
                self.a = div
            elif opcode == 1:
                self.b = self.b ^ lit_operand
            elif opcode == 2:
                self.b = combo_operand % 8
            elif opcode == 3:
                if self.a != 0:
                    instruction_pointer = lit_operand
                    continue # won't increase by 2 at end
            elif opcode == 4:
                self.b = self.b ^ self.c
            elif opcode == 5:
                to_output = combo_operand % 8
                #print("Output:", to_output, "Read instr:", self.read_instructions)
                #print("a:", self.a, "b:", self.b, "c:", self.c, "\n")
                self.read_instructions = []
                self.output_list.append(to_output)
            elif opcode == 6:
                div = self.a // 2 ** (combo_operand)
                self.b = div
            elif opcode == 7:
                div = self.a // 2 ** (combo_operand)
                self.c = div

            instruction_pointer += 2

        self.output_list_str = str(self.output_list).replace(" ", "")[1:-1]

    def output(self):
        self.set_data()
        #      x = 0, 1, 2, 3, 4, 5, 6, 7 maps to
        # output = 3, 2, 1, 0, 5, 3, 5, 5
        self.a = 31
                   # 0 is good, x must be 3
        # Then we try x // 8 == 3, x=24-31: outputs: 3,3,1,0,1,3,6,3
        # Then y // 8 == (24,25,29,31), y=...
        # etc.
        print("a:", self.a)
        print("b:", self.b)
        print("c:", self.c)
        print("instructions:", self.instruction_list)
        print("program:", self.program)

        #self.process_data()

        self.process_data_2()
        print("program output:", self.output_list_str)

class Day18:
    def __init__(self):
        self.data = [] # list of [row, col]s

        self.orig_data_len = 0
        self.adj_len = 1024

        self.num_rows = 71
        self.num_cols = 71

        # test's conditions
        #self.num_rows = self.num_cols = 7; self.adj_len = 12

        self.new_adj_len = self.adj_len

        self.start_p = [0,0]
        self.end_p = [self.num_rows-1, self.num_cols-1]
        self.visited_spaces = [self.start_p]
        self.last_spaces_in_paths = [self.start_p]

        #self.grid_after_set_falls = [[0] * self.num_cols] * self.num_rows
        self.grid_after_set_falls = []
        for i in range(self.num_rows):
            row = [0] * self.num_cols
            self.grid_after_set_falls.append(row)

        self.min_num_steps = 0
        self.last_byte_coords = []

    def set_data(self):
        with open("day18.1.txt", "r") as file:
            for line in file:
                phase = 0
                int_str = ""
                coord_to_add = [0,0]
                for char in line:
                    # self.games[-1].append(char)
                    # print("char", char, "int_str:", int_str)
                    if char.isdigit():
                        int_str = int_str + char
                    else:
                        num = int(int_str)
                        int_str = ""
                        if phase == 0:
                            coord_to_add[1] = num
                        else:
                            coord_to_add[0] = num
                        phase += 1
                self.data.append(coord_to_add)

        self.orig_data_len = len(self.data)

    def set_grid(self):
        for i in range(self.adj_len):
            data = self.data[i]
            self.grid_after_set_falls[data[0]][data[1]] = 1

    def set_1_more_in_grid(self):
        data = self.data[self.new_adj_len]
        self.last_byte_coords = [data[1], data[0]]
        self.grid_after_set_falls[data[0]][data[1]] = 1

        self.new_adj_len += 1

    def process_data_2(self):
        end_reached = True
        while end_reached:
            self.set_1_more_in_grid()
            self.visited_spaces = [self.start_p]
            self.last_spaces_in_paths = [self.start_p]
            print("num bytes fallen:", self.new_adj_len)

            end_reached = self.process_data()


    def process_data(self):
        count = 0
        end_reached = False
        #while not end_reached and count < 2:
        while not end_reached:
            count += 1
            #print("----------------------")
            #print("Step #" + str(count))
            next_last_spaces_in_paths = []
            for i in range(len(self.last_spaces_in_paths.copy())):
                target_p = self.last_spaces_in_paths[i]
                #print("t_p", target_p)
                for m_dir in [[0,1],[1,0],[0,-1],[-1,0]]:
                    check_p_row = target_p[0] + m_dir[0]
                    check_p_col = target_p[1] + m_dir[1]
                    check_p = [check_p_row, check_p_col]
                    #print("a", check_p)
                    if (not (0 <= check_p_row < self.num_rows)) or (not (0 <= check_p_col < self.num_cols)): # outside grid
                        continue
                    if self.grid_after_set_falls[check_p_row][check_p_col] == 1:
                        continue
                    elif check_p in self.visited_spaces:
                        continue

                    if check_p == self.end_p: # put this elsewhere if we want to see other paths reach end, esp. in same num of steps
                        end_reached = True
                        break

                    self.visited_spaces.append(check_p) # put this line elsewhere if we want many paths leading to the same coord, esp. in the same num of steps
                    next_last_spaces_in_paths.append(check_p)
                    #print("vs len", len(self.visited_spaces))
                if end_reached:
                    break
            if len(next_last_spaces_in_paths) == 0:
                break
            self.last_spaces_in_paths = next_last_spaces_in_paths

        self.min_num_steps = count

        return end_reached

    def output(self):
        self.set_data()
        print(self.adj_len, self.orig_data_len, self.data)
        print(self.grid_after_set_falls)

        self.set_grid()
        for row in self.grid_after_set_falls:
            print(" ".join(map(str, row)))

        self.process_data()
        print("visited spaces:", self.visited_spaces)
        print("min num steps:", self.min_num_steps)

        self.process_data_2()
        print("num bytes fallen FINAL:", self.new_adj_len)
        print("last byte coords (ANSWER):", self.last_byte_coords)

class Day19:
    def __init__(self):
        self.available_towels = []
        self.desired_patterns = []

        self.current_pattern = ""
        self.current_towels = []

        self.biggest_towel_len = 0


        self.towels_possible_in_each_place = []
        # ^ only find towels that start with the char at the nth place,
        # ex. in gggurgwrgguuugbw, check all that start with g and can match all chars behind as well
        # such as g, gg, ggg, gggu, gggur, etc.; if ggg is not a towel and the rest are, have first list be [1, 2, 4, 5, ...]
        '''
        condensing: 
        ex.[[1,2,4,5],[1,2,3,4],[2,3,5],[1,2,3,4,5],[3]
        1 can reach pos1
        2 can reach pos2 (1 in 0th list, then 1 in 1st list, or 2 in 1st list)
        1 can reach pos3 (1 in 0th list, then 2 in 1st list; but we really check if 2nd list has 1 (no), if 1st list has 2 (yes, its num is 1 as 1 can reach pos1, so add 1), if 0th list has 3 (no))
        v output v
        '''
        self.num_patterns_possible_per_pattern_part = []


        self.chars = ['w', 'u', 'b', 'r', 'g']
        self.n_char_combos = []

        self.num_patterns_possible = 0



    def set_data(self):
        with open("day19.1.txt", "r") as file:
            line_i = 0
            for line in file:
                if line_i == 0:
                    current_towel = ""
                    for char in line:
                        if char == ' ':
                            continue
                        elif char == "," or char == "\n":
                            self.available_towels.append(current_towel)
                            current_towel_len = len(current_towel)
                            if current_towel_len > self.biggest_towel_len:
                                self.biggest_towel_len = current_towel_len
                            current_towel = ""
                        else:
                            current_towel += char

                elif line_i > 1:
                    current_pattern = str(line.strip())
                    self.desired_patterns.append(current_pattern)
                line_i += 1

    def find_num_towels_for_pattern(self):
        pattern_len = len(self.current_pattern)
        self.towels_possible_in_each_place = []
        self.num_patterns_possible_per_pattern_part = [0] * (pattern_len+1)
        self.num_patterns_possible_per_pattern_part[0] = 1
        for char_i, char in enumerate(self.current_pattern):
            #print(char_i)
            towels_possible_in_nth_place = []
            num_patterns_possible_up_to_char = 0
            chars_left = pattern_len - char_i # including current char

            for len_i in range(1, min(self.biggest_towel_len, chars_left)+1):
                #print("leni", len_i)
                cut_char_i = char_i + len_i
                check_str = self.current_pattern[char_i:cut_char_i]
                if check_str in self.available_towels:
                    towels_possible_in_nth_place.append(len_i)
                    self.num_patterns_possible_per_pattern_part[cut_char_i] += self.num_patterns_possible_per_pattern_part[char_i]

            self.towels_possible_in_each_place.append(towels_possible_in_nth_place)
            #self.num_patterns_possible_per_pattern_part.append(num_patterns_possible_up_to_char)

        print(self.towels_possible_in_each_place)

        '''
        for i, towels_possible_in_nth_place in enumerate(self.towels_possible_in_each_place):
            num = i+1
            num_patterns_possible_up_to_char = 0
            for j in range(0, max(-self.biggest_towel_len,-1), -1): # check several lists including and behind
                #print(i, j)
                if num in self.towels_possible_in_each_place[i-j]:
                    if j == 0:
                        num_to_add = self.num_patterns_possible_per_pattern_part
        '''

        print(self.num_patterns_possible_per_pattern_part[-1])
        self.num_patterns_possible += self.num_patterns_possible_per_pattern_part[-1]

    def process_data(self):
        for pattern_i, pattern in enumerate(self.desired_patterns):
            pattern_reached = False
            pattern_len = len(pattern)
            pattern_index_at = 0
            print("------------------------")
            print("on pattern i#" + str(pattern_i) + ":", pattern)
            self.current_pattern = pattern
            pattern_reached = self.check_all_towels_to_match_next_pattern_piece(0)
            if not pattern_reached:
                print("impossible pattern:", pattern)
            #else:
                #self.find_num_towels_for_pattern()
            self.find_num_towels_for_pattern()
            '''
            while not pattern_reached: # Also should break when realized no patterns are possible
                advanced_pattern = False
                for towel_i, towel in enumerate(self.available_towels):
                    towel_len = len(towel)
                    next_pattern_index = towel_len + pattern_index_at
                    if next_pattern_index > pattern_len:
                        continue
                    pattern_piece_to_match_towel = pattern[pattern_index_at:next_pattern_index]
                    print("pattern_piece_to_match_towel:", pattern_piece_to_match_towel)
                    if pattern_piece_to_match_towel == towel:
                        print("pattern match")
                        pattern_index_at = next_pattern_index
                        advanced_pattern = True
                        break # restart for loop essentially, unless pattern is reached
                if next_pattern_index == pattern_len:
                    pattern_reached = True
                    self.num_patterns_possible += 1
                elif not advanced_pattern:
                    if pattern_index_at == 0:
                        print("impossible pattern:", pattern)
                        break
                    else:
                        #pattern_index_at = 0 #############
            '''

    def check_all_towels_to_match_next_pattern_piece(self, pattern_index_at):
        pattern_len = len(self.current_pattern)
        pattern_reached = False
        self.current_towels.append("")
        for towel_i, towel in enumerate(self.available_towels):
            self.current_towels[-1] = towel
            towel_len = len(towel)
            next_pattern_index = towel_len + pattern_index_at
            if next_pattern_index > pattern_len:
                continue
            pattern_piece_to_match_towel = self.current_pattern[pattern_index_at:next_pattern_index]
            #print("pattern_piece_to_match_towel:", pattern_piece_to_match_towel)
            if pattern_piece_to_match_towel == towel:
                #print("pattern match")
                #pattern_index_at = next_pattern_index
                #advanced_pattern = True
                #break  # restart for loop essentially, unless pattern is reached

                if next_pattern_index == pattern_len:
                    #print(self.current_towels)
                    pattern_reached = True
                    #self.num_patterns_possible += 1
                    #if self.num_patterns_possible % 10_000 == 0:
                    #    print(self.num_patterns_possible, self.current_towels)
                else:
                    pattern_reached = self.check_all_towels_to_match_next_pattern_piece(next_pattern_index)
                if pattern_reached:
                    return True
        self.current_towels = self.current_towels[:-1]
        #if pattern_reached:
            #return True
        return False

    def output(self):
        self.set_data()
        print("towels:", self.available_towels)
        print("patterns:", self.desired_patterns)
        print("biggest towel len:", self.biggest_towel_len)

        self.process_data()
        print("num patterns possible:", self.num_patterns_possible)

class Day20:
    def __init__(self):
        self.grid = []

        self.secs_saved_threshold_min = 100

        self.start_p = [0, 0]
        self.end_p = [0, 0]
        #self.start_dir = np.array([0, 1])

        self.num_rows = 0
        self.num_cols = 0

        self.paths = []

        self.path_len = 0

        self.main_path = []

        self.num_good_cheats = 0

        self.num_cheat_steps = 20

        self.relative_cheat_spots = []
        self.init_relative_cheat_spots()

    def set_data(self):
        with open("day20.1.txt", "r") as file:
            for line in file:
                self.grid.append([])
                for char in line.strip():
                    num = 0
                    if char == '#':
                        num = 1
                    elif char == 'S':
                        self.start_p = [len(self.grid) - 1, len(self.grid[-1])]
                    elif char == 'E':
                        self.end_p = [len(self.grid) - 1, len(self.grid[-1])]
                        num = 2

                    self.grid[-1].append(num)

        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.paths = [[self.start_p]]

        self.visited_spaces = [self.start_p]
        self.last_spaces_in_paths = [self.start_p]

    def find_main_path(self):
        end_reached = False
        while not end_reached:
            for i, path in enumerate(self.paths):
                current_pos = path[-1]
                print(current_pos)
                to_add_to_path = []
                for dir in [[0,1],[1,0],[0,-1],[-1,0]]:
                    new_pos_r = current_pos[0]+dir[0]
                    new_pos_c = current_pos[1]+dir[1]
                    new_pos = [new_pos_r, new_pos_c]
                    if new_pos in self.visited_spaces: # already visited
                        continue
                    elif (not (0 <= new_pos_r < self.num_rows)) or (not (0 <= new_pos_c < self.num_cols)): # oob
                        continue
                    tile_state = self.grid[new_pos_r][new_pos_c]
                    if tile_state == 1: # wall
                        continue
                    elif tile_state == 2: # end
                        end_reached = True

                    to_add_to_path.append(new_pos)
                    self.visited_spaces.append(new_pos)
                print("num in add_to_path", len(to_add_to_path), to_add_to_path)
                if len(to_add_to_path) > 1:
                    print("============== ERROR ===================\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                #print("visited spaces", self.visited_spaces)
                #print("path:", self.paths[-1])
                self.paths[i].append(to_add_to_path[-1])

        self.path_len = len(self.paths[0])
        self.main_path = self.paths[0]

    def init_relative_cheat_spots(self):
        for i in range(-self.num_cheat_steps, self.num_cheat_steps+1):
            abs_i = abs(i)
            print(i)
            j_ext = self.num_cheat_steps - abs_i
            for j in range(-j_ext, j_ext+1):
                if i == 0 and j == 0:
                    continue
                self.relative_cheat_spots.append([i,j])
        print(len(self.relative_cheat_spots), self.relative_cheat_spots)

    def cheat(self):
        for main_path_i, main_path_spot in enumerate(self.main_path):
            print("cheat attempt #" + str(main_path_i+1) + "/" + str(self.path_len))
            wall_ps = []
            for dir in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                new_pos_r = main_path_spot[0] + dir[0]
                new_pos_c = main_path_spot[1] + dir[1]
                new_pos = [new_pos_r, new_pos_c]

                if (not (0 <= new_pos_r < self.num_rows)) or (not (0 <= new_pos_c < self.num_cols)):  # oob
                    continue
                tile_state = self.grid[new_pos_r][new_pos_c]
                if tile_state == 1:  # wall
                    wall_ps.append(new_pos)

            for wall_p in wall_ps:
                for dir in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                    new_pos_r = wall_p[0] + dir[0]
                    new_pos_c = wall_p[1] + dir[1]
                    new_pos = [new_pos_r, new_pos_c]

                    if (not (0 <= new_pos_r < self.num_rows)) or (not (0 <= new_pos_c < self.num_cols)):  # oob
                        continue
                    tile_state = self.grid[new_pos_r][new_pos_c]
                    if tile_state == 1:  # wall
                        continue

                    cheated_i = self.main_path.index(new_pos)
                    secs_saved = cheated_i - main_path_i - 2
                    if secs_saved >= self.secs_saved_threshold_min:
                        #print("go thru wall:", wall_p, "secs saved:", secs_saved)
                        self.num_good_cheats += 1

    def cheat2(self):
        for main_path_i, main_path_spot in enumerate(self.main_path):
            print("cheat attempt #" + str(main_path_i+1) + "/" + str(self.path_len))

            for dir in self.relative_cheat_spots:
                new_pos_r = main_path_spot[0] + dir[0]
                new_pos_c = main_path_spot[1] + dir[1]
                new_pos = [new_pos_r, new_pos_c]

                if (not (0 <= new_pos_r < self.num_rows)) or (not (0 <= new_pos_c < self.num_cols)):  # oob
                    continue
                tile_state = self.grid[new_pos_r][new_pos_c]
                if tile_state == 1:  # wall
                    continue

                cheated_i = self.main_path.index(new_pos)
                spots_moved = abs(dir[0]) + abs(dir[1])
                secs_saved = cheated_i - main_path_i - spots_moved
                if secs_saved >= self.secs_saved_threshold_min:
                    #print(secs_saved)
                    #print("go thru wall:", wall_p, "secs saved:", secs_saved)
                    self.num_good_cheats += 1

    def output(self):
        self.set_data()
        for row in self.grid:
            print(" ".join(map(str, row)))
        print("num rows/cols:", self.num_rows, self.num_cols)

        self.find_main_path()
        print("num steps:", self.path_len-1)
        print("main_path:", self.main_path)

        self.cheat2()
        print("num good cheats:", self.num_good_cheats)

#day16 = Day16()
#day16.output()
#day17 = Day17()
#day17.output()
#day18 = Day18()
#day18.output()
#day19 = Day19()
#day19.output()
day20 = Day20()
day20.output()
