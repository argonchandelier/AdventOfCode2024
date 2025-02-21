from copy import deepcopy
import numpy as np

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

class Day21:
    def __init__(self):
        self.true_button_chars = []
        self.true_button_coords = []

        self.true_button_start_coords = [3,2]
        self.dir_button_start_coords = [0,2]



        self.numeric_of_codes = []
        self.lens_of_shortest_seqs = []
        self.complexity_sum = 0



    def set_data(self):
        with open("day21.t.txt", "r") as file:
            for line in file:
                self.true_button_chars.append([])
                self.true_button_coords.append([])
                int_str = ""
                for char in line.strip():
                    self.true_button_chars[-1].append(char)
                    coords = self.convert_true_button_coords(char)
                    self.true_button_coords[-1].append(coords)

                    if char == 'A':
                        self.numeric_of_codes.append(int(int_str))
                    else:
                        int_str = int_str + char

    def convert_true_button_coords(self, char):
        coords = None
        if char == 'A':
            coords = [3,2]
        elif char == '0':
            coords = [3,1]
        elif char == '1':
            coords = [2,0]
        elif char == '2':
            coords = [2,1]
        elif char == '3':
            coords = [2,2]
        elif char == '4':
            coords = [1,0]
        elif char == '5':
            coords = [1,1]
        elif char == '6':
            coords = [1,2]
        elif char == '7':
            coords = [0,0]
        elif char == '8':
            coords = [0,1]
        elif char == '9':
            coords = [0,2]

        return coords

    def convert_dir_button_coords(self, dir):
        coords = None
        if dir == [0,0]: # A
            coords = [0,2]
        elif dir == [-1,0]: # up
            coords = [0,1]
        elif dir == [0, -1]: # left
            coords = [1,0]
        elif dir == [1,0]: # down
            coords = [1,1]
        elif dir == [0,1]: # right
            coords = [1,2]

        return coords

    def get_dist_between_coords_set(self, coords1, coords2):
        dist = abs(coords2[0] - coords1[0]) + abs(coords2[1] - coords1[1])
        return dist

    def find_numpad_dir_data(self):
        self.numpad_full_direction_data_all_seq = []
        for i, true_coords_list in enumerate(self.true_button_coords):
            current_p = self.true_button_start_coords
            full_direction_data_in_seq = []
            for j, true_coords in enumerate(true_coords_list):
                direction_data_in_seq = [] # contains 1 or 2 lists of possible dirs
                #dist = self.get_dist_between_coords_set(true_coords, current_p)
                row_disp = true_coords[0] - current_p[0]
                col_disp = true_coords[1] - current_p[1]

                row_dirs = []
                col_dirs = []
                if row_disp < 0: # up
                    row_dirs = [[-1, 0]] * abs(row_disp)
                elif row_disp > 0: # down
                    row_dirs = [[1, 0]] * row_disp
                if col_disp < 0: # left
                    col_dirs = [[0, -1]] * abs(col_disp)
                elif col_disp > 0: # right
                    col_dirs = [[0, 1]] * col_disp

                # prioritize up (vs. l/r) and right (vs. u/d) - this avoids the dead square (in main numpad only!)
                '''
                Assumption 1: Doing all one dir, then all next dir is the fastest (2 possibilities max)
                -If above is true, then there is only 1 possibility if the other possible possibility goes thru dead square
                '''

                seq_1 = row_dirs + col_dirs
                seq_2 = col_dirs + row_dirs

                if not (len(row_dirs) > 0 and len(col_dirs) > 0): # only has 1 or 0 directions
                    # direction_data_in_seq will have 2 lists (unless dead square passed), else 1
                    direction_data_in_seq = [seq_1]
                elif true_coords[0] == 3 and current_p[1] == 0: # down then right will lead to dead square
                    direction_data_in_seq = [seq_2]
                elif current_p[0] == 3 and true_coords[1] == 0: # left then up will lead to dead square
                    direction_data_in_seq = [seq_1]
                else: # 2 possibilities
                    direction_data_in_seq = [seq_1, seq_2]

                full_direction_data_in_seq.append(direction_data_in_seq)
                current_p = true_coords
                print("direction_data_in_seq:", direction_data_in_seq)

            self.numpad_full_direction_data_all_seq.append(full_direction_data_in_seq)
            print("full_direction_data_in_seq:", full_direction_data_in_seq)

        print(self.numpad_full_direction_data_all_seq)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")

    def find_robot1_dir_data(self):
        self.robot1_full_direction_data_all_seq = []
        for i, full_direction_data_in_numpad_seq in enumerate(self.numpad_full_direction_data_all_seq):
            current_p = self.dir_button_start_coords
            full_direction_data_in_r1_seq = []
            for j, direction_data_in_numpad_seq in enumerate(full_direction_data_in_numpad_seq):
                # direction_data_in_numpad_seq: list of possible lists of dirs
                '''
                Assumption 2: Most simple bot direction data for current bot is most simple for all bots in control stack
                '''
                dir_data_in_seqs = []
                orig_current_p = current_p
                '''
                # Loops 0-2 times
                for dir_seq in direction_data_in_numpad_seq: # dir_seq: Just a list of dirs; examples: up, up, right; right, up, up
                    current_p = orig_current_p

                    dirs_to_end_up_at = []
                    dir_seq_len = len(dir_seq)
                    if dir_seq_len > 0:
                        if dir_seq[0] == dir_seq[-1]:
                            dirs_to_end_up_at = [dir_seq[0]]
                        else:
                            dirs_to_end_up_at = [dir_seq[0], dir_seq[-1]]

                    #dir_seq.append([0,0]) # the final A press at the end
                    dirs_to_end_up_at.append([0,0]) # the final A press at the end
                    for dir in dirs_to_end_up_at:
                        button_coords = self.convert_dir_button_coords(dir)

                        row_disp = button_coords[0] - current_p[0]
                        col_disp = button_coords[1] - current_p[1]

                        row_dirs = []
                        col_dirs = []
                        if row_disp < 0:  # up
                            row_dirs = [[-1, 0]] * abs(row_disp)
                        elif row_disp > 0:  # down
                            row_dirs = [[1, 0]] * row_disp
                        if col_disp < 0:  # left
                            col_dirs = [[0, -1]] * abs(col_disp)
                        elif col_disp > 0:  # right
                            col_dirs = [[0, 1]] * col_disp

                        # top left is dead square

                        seq_1 = row_dirs + col_dirs
                        seq_2 = col_dirs + row_dirs

                        if not (len(row_dirs) > 0 and len(col_dirs) > 0):  # only has 1 or 0 directions (out of u/d/l/r)
                            # direction_data_in_seq will have 2 lists (unless dead square passed), else 1
                            direction_data_in_seq = [seq_1]
                        elif button_coords[0] == 0 and current_p[1] == 0:  # down then right will lead to dead square
                            direction_data_in_seq = [seq_2]
                        elif current_p[0] == 0 and button_coords[1] == 0:  # left then up will lead to dead square
                            direction_data_in_seq = [seq_1]
                        else:  # 2 possibilities
                            direction_data_in_seq = [seq_1, seq_2]

                        dir_data_in_seqs.append(direction_data_in_seq)
                        current_p = button_coords
                '''
                for dir_seq in direction_data_in_numpad_seq:
                    dirs_on_dirs = self.find_dirs_on_dirs(dir_seq)
                    dir_data_in_seqs.extend(dirs_on_dirs)

                # dir_data_in_seqs has list of possible seqs, now cut longer ones
                ''' Actually, don't do this yet: '''
                '''
                min_length = -1
                for seq in dir_data_in_seqs:
                    seq_len = len(seq)
                    if min_length < seq_len or min_length == -1:
                        min_length = seq_len
                for k in range(len(dir_data_in_seqs)-1, -1, -1):
                    seq_len = len(dir_data_in_seqs[k])
                    if seq_len > min_length:
                        dir_data_in_seqs.pop(k)
                '''
                full_direction_data_in_r1_seq.append(dir_data_in_seqs)
                print("dir_data_in_seqs", dir_data_in_seqs)
            self.robot1_full_direction_data_all_seq.append(full_direction_data_in_r1_seq)
            print("full_direction_data_in_r1_seq", full_direction_data_in_r1_seq)

        print(self.robot1_full_direction_data_all_seq)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.all_robot_full_direction_data_all_seq = [self.robot1_full_direction_data_all_seq]

    def find_robotn_dir_data(self):
        last_robot_full_direction_data_all_seq = self.all_robot_full_direction_data_all_seq[-1]
        robotn_full_direction_data_all_seq = []
        for i, last_robot_full_direction_data_in_seq in enumerate(last_robot_full_direction_data_all_seq):
            current_p = self.dir_button_start_coords
            full_direction_data_in_r1_seq = []
            for j, last_robot_direction_data_in_seq in enumerate(last_robot_full_direction_data_in_seq):
                dir_data_in_seqs = []

                for dir_seq in last_robot_direction_data_in_seq:
                    dirs_on_dirs = self.find_dirs_on_dirs(dir_seq)
                    dir_data_in_seqs.extend(dirs_on_dirs)

                #full_direction_data_in_r1_seq.append([dir_data_in_seqs[0]]) #[list[0]]
                full_direction_data_in_r1_seq.append(dir_data_in_seqs)

                #print("dir_data_in_seqs n_bot", dir_data_in_seqs)
            robotn_full_direction_data_all_seq.append(full_direction_data_in_r1_seq)
            #print("full_direction_data_in_r1_seq n_bot", full_direction_data_in_r1_seq)
            print("len full_direction_data_in_r1_seq n_bot", len(full_direction_data_in_r1_seq))

        self.all_robot_full_direction_data_all_seq.append(robotn_full_direction_data_all_seq)
        #print("robotn_full_direction_data_all_seq", robotn_full_direction_data_all_seq)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")

    def find_dirs_on_dirs(self, dirs):
        '''
        Too much, can't prove: Assumption 3: different paths don't actually matter
        '''
        if len(dirs) == 0:
            dirs.append([0,0])
        elif dirs[-1] != [0,0]:
            dirs.append([0,0])

        data_lists = [[]] # many lists; each list represents one possibility
        current_p = self.dir_button_start_coords
        for dir in dirs:
            button_coords = self.convert_dir_button_coords(dir)

            row_disp = button_coords[0] - current_p[0]
            col_disp = button_coords[1] - current_p[1]

            row_dirs = []
            col_dirs = []
            if row_disp < 0:  # up
                row_dirs = [[-1, 0]] * abs(row_disp)
            elif row_disp > 0:  # down
                row_dirs = [[1, 0]] * row_disp
            if col_disp < 0:  # left
                col_dirs = [[0, -1]] * abs(col_disp)
            elif col_disp > 0:  # right
                col_dirs = [[0, 1]] * col_disp

            # top left is dead square

            seq_1 = row_dirs + col_dirs
            seq_2 = col_dirs + row_dirs
            seq_1.append([0,0])
            seq_2.append([0,0])

            #print("data_lists", data_lists)

            if not (len(row_dirs) > 0 and len(col_dirs) > 0):  # only has 1 or 0 directions (out of u/d/l/r)
                # direction_data_in_seq will have 2 lists (unless dead square passed), else 1
                direction_data_in_seq = seq_1
            elif button_coords[0] == 0 and current_p[1] == 0:  # down then right will lead to dead square
                direction_data_in_seq = seq_2
            elif current_p[0] == 0 and button_coords[1] == 0:  # left then up will lead to dead square
                direction_data_in_seq = seq_1
            else:  # 2 possibilities
                #direction_data_in_seq = [seq_1, seq_2]
                #print("data_lists", data_lists)
                data_lists_copy = deepcopy(data_lists)
                for i in range(len(data_lists)):
                    data_lists[i].extend(seq_1)
                    #print("data_lists e", data_lists)
                for i in range(len(data_lists_copy)):
                    data_lists_copy[i].extend(seq_2)

                #print("data_lists f", data_lists)
                data_lists.extend(data_lists_copy)
                #print("direction_data_in_2seqs:", seq_1, seq_2)
                #print("data_lists", data_lists)
                #print("data_lists copy", data_lists_copy)

                current_p = button_coords
                continue
            for i in range(len(data_lists)):
                data_lists[i].extend(direction_data_in_seq)
            #print("direction_data_in_seq:", direction_data_in_seq)
            current_p = button_coords

        return data_lists

    def find_num_inputs(self):
        relevant_robot_full_direction_data_all_seq = self.all_robot_full_direction_data_all_seq[-1]
        for i, full_direction_data_in_seq in enumerate(relevant_robot_full_direction_data_all_seq):
            len_of_shortest_seq = 0
            min_datas = []
            for j, dir_data_in_seqs in enumerate(full_direction_data_in_seq):
                #first_list_best_list = dir_data_in_seqs[0]
                #first_list_best_list = dir_data_in_seqs[-1]
                #best_list_len_for_move = len(first_list_best_list)

                min_len = -1
                min_data = []
                for k, data in enumerate(dir_data_in_seqs):
                    len_data = len(data)
                    if len_data < min_len or min_len == -1:
                        min_len = len_data
                        min_data = data

                #print("data w min len:", min_data)
                min_datas.extend(min_data)

                #len_of_shortest_seq += best_list_len_for_move
                len_of_shortest_seq += min_len
            print(len_of_shortest_seq, "data w min len:", min_datas)
            self.lens_of_shortest_seqs.append(len_of_shortest_seq)

    def find_complexity_sum(self):
        self.complexity_sum = 0
        for i in range(len(self.lens_of_shortest_seqs)):
            shortest_len = self.lens_of_shortest_seqs[i]
            numeric_of_code = self.numeric_of_codes[i]
            complexity = shortest_len*numeric_of_code

            self.complexity_sum += complexity
            print("Complexity added to sum:", shortest_len, "*", numeric_of_code, "=", complexity)

    def output(self):
        self.set_data()
        print(self.true_button_chars)
        print(self.true_button_coords)
        print(self.numeric_of_codes)

        self.find_numpad_dir_data()
        print("numpad done") # numpad > bot1

        self.find_robot1_dir_data()
        print("bot 1 done") # bot1 > bot2

        self.find_robotn_dir_data()
        print("bot 2 done") # bot2 > bot3

        #self.find_robotn_dir_data()
        #print("bot 3 done") # bot3 > you

        #self.find_robotn_dir_data() # technically you, not a bot
        #print("you done")

        #data_lists = self.find_dirs_on_dirs([[-1, 0], [-1, 0], [0, 1]])
        #print("data_lists:", data_lists)

        self.find_num_inputs()
        self.find_complexity_sum()
        print("COMPLEXITY SUM (answer):", self.complexity_sum)

class Day21_2:
    '''
    Notes:
    -while wrong the method ain't bad, perhaps try all combinations of initial sequences, and perhaps all combos of 5, 6, 9, and 10 rearrangements for out_seq
    -try any and all initial
    '''
    def __init__(self):
        self.true_button_chars = []
        self.true_button_coords = []

        self.true_button_start_coords = [3,2]
        self.dir_button_start_coords = [0,2]


        self.numeric_of_codes = []
        self.lens_of_shortest_seqs = []
        self.complexity_sum = 0

        # 0,1,2,3,4: A,up,right,down,left
        #self.out_seqs = [[0],[4,0],[3,0],[2,0],[1,0],[3,4,0],[2,1,0],[3,4,4,0],[2,2,1,0],[2,3,0],[1,4,0]] # seq of 3 can have first 2 switched
        #self.out_seqs = [[0],[4,0],[3,0],[2,0],[1,0],[4,3,0],[2,1,0],[3,4,4,0],[2,2,1,0],[2,3,0],[1,4,0]]
        #self.out_seqs = [[0],[4,0],[3,0],[2,0],[1,0],[4,3,0],[1,2,0],[3,4,4,0],[2,2,1,0],[2,3,0],[1,4,0]]
        #self.out_seqs = [[0],[4,0],[3,0],[2,0],[1,0],[4,3,0],[1,2,0],[3,4,4,0],[2,2,1,0],[3,2,0],[1,4,0]]

        self.out_seqs = [[0],[4,0],[3,0],[2,0],[1,0],[4,3,0],[1,2,0],[3,4,4,0],[2,2,1,0],[3,2,0],[4,1,0],[3,4,0],[2,1,0]]
        #self.out_seqs = [[0],[4,0],[3,0],[2,0],[1,0],[4,3,0],[2,1,0],[3,4,4,0],[2,2,1,0],[3,2,0],[4,1,0]]

        #self.dir_to_dir_grid = [[0,1,2,5,7],[3,0,9,2,5],[4,10,0,1,0],[6,4,3,0,1],[8,6,0,3,0]]
        self.dir_to_dir_grid = [[0,1,2,5,7],[3,0,9,2,11],[4,10,0,1,0],[6,4,3,0,1],[8,12,0,3,0]] # [(dir-1)_i][dir_i]
        self.dir_to_dir_list = [] #[-1] * 25
        self.dtd_deriv_count_list = [] #[-1] * 25
        self.init_dir_to_dir_list()

        self.dtd_deriv_counts_nth_step = self.dtd_deriv_count_list.copy() # step 1 on init
        self.dtd_deriv_counts_all_steps = [self.dtd_deriv_count_list]

        self.inputs_after_2nd_layer = [] # list of dirs
        self.input_indexes_after_2nd_layer = [] # list of numbers 0-4
        self.dtd_indexes_after_2nd_layer = [] # list of numbers 0-24 derived from above list (will also have same count)

        self.input_list = [[0,0], [-1,0], [0,1], [1,0], [0,-1]] # convert by using .index([dir])

        self.shortest_init_seq = []

    def set_data(self):
        with open("day21.1.txt", "r") as file:
            for line in file:
                self.true_button_chars.append([])
                self.true_button_coords.append([])
                int_str = ""
                for char in line.strip():
                    self.true_button_chars[-1].append(char)
                    coords = self.convert_true_button_coords(char)
                    self.true_button_coords[-1].append(coords)

                    if char == 'A':
                        self.numeric_of_codes.append(int(int_str))
                    else:
                        int_str = int_str + char

    def convert_true_button_coords(self, char):
        coords = None
        if char == 'A':
            coords = [3,2]
        elif char == '0':
            coords = [3,1]
        elif char == '1':
            coords = [2,0]
        elif char == '2':
            coords = [2,1]
        elif char == '3':
            coords = [2,2]
        elif char == '4':
            coords = [1,0]
        elif char == '5':
            coords = [1,1]
        elif char == '6':
            coords = [1,2]
        elif char == '7':
            coords = [0,0]
        elif char == '8':
            coords = [0,1]
        elif char == '9':
            coords = [0,2]

        return coords

    def convert_dir_button_coords(self, dir):
        coords = None
        if dir == [0,0]: # A
            coords = [0,2]
        elif dir == [-1,0]: # up
            coords = [0,1]
        elif dir == [0, -1]: # left
            coords = [1,0]
        elif dir == [1,0]: # down
            coords = [1,1]
        elif dir == [0,1]: # right
            coords = [1,2]

        return coords

    def get_dist_between_coords_set(self, coords1, coords2):
        dist = abs(coords2[0] - coords1[0]) + abs(coords2[1] - coords1[1])
        return dist

    def find_numpad_dir_data(self):
        self.numpad_full_direction_data_all_seq = []
        self.true_numpad_full_direction_data_all_seq = []
        for i, true_coords_list in enumerate(self.true_button_coords):
            current_p = self.true_button_start_coords
            full_direction_data_in_seq = []
            true_full_dir_data_in_seq = []
            for j, true_coords in enumerate(true_coords_list):
                direction_data_in_seq = [] # contains 1 or 2 lists of possible dirs
                #dist = self.get_dist_between_coords_set(true_coords, current_p)
                row_disp = true_coords[0] - current_p[0]
                col_disp = true_coords[1] - current_p[1]

                row_dirs = []
                col_dirs = []
                if row_disp < 0: # up
                    row_dirs = [[-1, 0]] * abs(row_disp)
                elif row_disp > 0: # down
                    row_dirs = [[1, 0]] * row_disp
                if col_disp < 0: # left
                    col_dirs = [[0, -1]] * abs(col_disp)
                elif col_disp > 0: # right
                    col_dirs = [[0, 1]] * col_disp

                # prioritize up (vs. l/r) and right (vs. u/d) - this avoids the dead square (in main numpad only!)
                '''
                Assumption 1: Doing all one dir, then all next dir is the fastest (2 possibilities max)
                -If above is true, then there is only 1 possibility if the other possible possibility goes thru dead square
                '''

                seq_1 = row_dirs + col_dirs
                seq_2 = col_dirs + row_dirs

                true_seq = seq_1
                #print("seq1&2", seq_1, seq_2)

                true_dir_data_in_seq = seq_1
                if not (len(row_dirs) > 0 and len(col_dirs) > 0): # only has 1 or 0 directions
                    # direction_data_in_seq will have 2 lists (unless dead square passed), else 1
                    direction_data_in_seq = [seq_1]
                    true_dir_data_in_seq = seq_1
                elif true_coords[0] == 3 and current_p[1] == 0: # down then right will lead to dead square
                    direction_data_in_seq = [seq_2]
                    true_dir_data_in_seq = seq_2
                elif current_p[0] == 3 and true_coords[1] == 0: # left then up will lead to dead square
                    direction_data_in_seq = [seq_1]
                    true_dir_data_in_seq = seq_1
                else: # 2 possibilities
                    #direction_data_in_seq = [seq_1, seq_2]
                    #direction_data_in_seq = [seq_2,seq_1]
                    if seq_2[0] == [0, 1]:
                        true_dir_data_in_seq = seq_1
                    else:
                        true_dir_data_in_seq = seq_2

                full_direction_data_in_seq.append(direction_data_in_seq)
                current_p = true_coords
                #print("*direction_data_in_seq:", direction_data_in_seq)

                #true_full_dir_data_in_seq.append(true_dir_data_in_seq)
                true_dir_data_in_seq.append([0,0])
                true_full_dir_data_in_seq.extend(true_dir_data_in_seq)

            self.numpad_full_direction_data_all_seq.append(full_direction_data_in_seq)
            #print("full_direction_data_in_seq:", full_direction_data_in_seq)

            self.true_numpad_full_direction_data_all_seq.append(true_full_dir_data_in_seq)

        print(self.numpad_full_direction_data_all_seq)
        print("TRUE INIT NUMPAD DATA:", self.true_numpad_full_direction_data_all_seq)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")

    def find_robot1_dir_data(self):
        self.robot1_full_direction_data_all_seq = []
        self.true_input_indexes_after_second_layer = []
        for i, full_direction_data_in_numpad_seq in enumerate(self.numpad_full_direction_data_all_seq):
            print("***TRUE numpad sequence", str(i) + ":", self.true_numpad_full_direction_data_all_seq[i])
            current_p = self.dir_button_start_coords
            full_direction_data_in_r1_seq = []

            # REDO TRUE STUFF MANUALLY
            dir_before = [0,0]
            coords_before = self.convert_dir_button_coords(dir_before)
            input_indexes_after_second_layer_i = []
            before_dir_index = 0
            for j, true_dir in enumerate(self.true_numpad_full_direction_data_all_seq[i]):
                #before_dir_index = self.input_list.index(dir_before)
                this_dir_index = self.input_list.index(true_dir)
                code = self.dir_to_dir_grid[before_dir_index][this_dir_index]
                new_inputs = self.out_seqs[code]
                input_indexes_after_second_layer_i.extend(new_inputs)

                before_dir_index = this_dir_index
            print("TRUE input_indexes_after_second_layer_i:", input_indexes_after_second_layer_i)
            self.true_input_indexes_after_second_layer.append(input_indexes_after_second_layer_i)
            continue



            # useless now that we have true data
            for j, direction_data_in_numpad_seq in enumerate(full_direction_data_in_numpad_seq):
                # direction_data_in_numpad_seq: list of possible lists of dirs
                '''
                Assumption 2: Most simple bot direction data for current bot is most simple for all bots in control stack
                '''
                dir_data_in_seqs = []
                orig_current_p = current_p
                '''
                # Loops 0-2 times
                for dir_seq in direction_data_in_numpad_seq: # dir_seq: Just a list of dirs; examples: up, up, right; right, up, up
                    current_p = orig_current_p

                    dirs_to_end_up_at = []
                    dir_seq_len = len(dir_seq)
                    if dir_seq_len > 0:
                        if dir_seq[0] == dir_seq[-1]:
                            dirs_to_end_up_at = [dir_seq[0]]
                        else:
                            dirs_to_end_up_at = [dir_seq[0], dir_seq[-1]]

                    #dir_seq.append([0,0]) # the final A press at the end
                    dirs_to_end_up_at.append([0,0]) # the final A press at the end
                    for dir in dirs_to_end_up_at:
                        button_coords = self.convert_dir_button_coords(dir)

                        row_disp = button_coords[0] - current_p[0]
                        col_disp = button_coords[1] - current_p[1]

                        row_dirs = []
                        col_dirs = []
                        if row_disp < 0:  # up
                            row_dirs = [[-1, 0]] * abs(row_disp)
                        elif row_disp > 0:  # down
                            row_dirs = [[1, 0]] * row_disp
                        if col_disp < 0:  # left
                            col_dirs = [[0, -1]] * abs(col_disp)
                        elif col_disp > 0:  # right
                            col_dirs = [[0, 1]] * col_disp

                        # top left is dead square

                        seq_1 = row_dirs + col_dirs
                        seq_2 = col_dirs + row_dirs

                        if not (len(row_dirs) > 0 and len(col_dirs) > 0):  # only has 1 or 0 directions (out of u/d/l/r)
                            # direction_data_in_seq will have 2 lists (unless dead square passed), else 1
                            direction_data_in_seq = [seq_1]
                        elif button_coords[0] == 0 and current_p[1] == 0:  # down then right will lead to dead square
                            direction_data_in_seq = [seq_2]
                        elif current_p[0] == 0 and button_coords[1] == 0:  # left then up will lead to dead square
                            direction_data_in_seq = [seq_1]
                        else:  # 2 possibilities
                            direction_data_in_seq = [seq_1, seq_2]

                        dir_data_in_seqs.append(direction_data_in_seq)
                        current_p = button_coords
                '''
                for dir_seq in direction_data_in_numpad_seq:
                    dirs_on_dirs = self.find_dirs_on_dirs(dir_seq)
                    dir_data_in_seqs.extend(dirs_on_dirs)

                # dir_data_in_seqs has list of possible seqs, now cut longer ones
                ''' Actually, don't do this yet: '''
                '''
                min_length = -1
                for seq in dir_data_in_seqs:
                    seq_len = len(seq)
                    if min_length < seq_len or min_length == -1:
                        min_length = seq_len
                for k in range(len(dir_data_in_seqs)-1, -1, -1):
                    seq_len = len(dir_data_in_seqs[k])
                    if seq_len > min_length:
                        dir_data_in_seqs.pop(k)
                '''
                full_direction_data_in_r1_seq.append(dir_data_in_seqs)
                #print("dir_data_in_seqs", dir_data_in_seqs)
            self.robot1_full_direction_data_all_seq.append(full_direction_data_in_r1_seq)
            #print("full_direction_data_in_r1_seq", full_direction_data_in_r1_seq)

        print(self.robot1_full_direction_data_all_seq)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.all_robot_full_direction_data_all_seq = [self.robot1_full_direction_data_all_seq]

    def find_robotn_dir_data(self):
        last_robot_full_direction_data_all_seq = self.all_robot_full_direction_data_all_seq[-1]
        robotn_full_direction_data_all_seq = []
        for i, last_robot_full_direction_data_in_seq in enumerate(last_robot_full_direction_data_all_seq):
            current_p = self.dir_button_start_coords
            full_direction_data_in_r1_seq = []
            for j, last_robot_direction_data_in_seq in enumerate(last_robot_full_direction_data_in_seq):
                dir_data_in_seqs = []

                for dir_seq in last_robot_direction_data_in_seq:
                    dirs_on_dirs = self.find_dirs_on_dirs(dir_seq)
                    dir_data_in_seqs.extend(dirs_on_dirs)

                check_comment = 0
                '''
                Just cut out the extra long ones when they occur;
                perhaps also 
                
                min_length = -1
                for seq in dir_data_in_seqs:
                    seq_len = len(seq)
                    if min_length < seq_len or min_length == -1:
                        min_length = seq_len
                for k in range(len(dir_data_in_seqs)-1, -1, -1):
                    seq_len = len(dir_data_in_seqs[k])
                    if seq_len > min_length:
                        dir_data_in_seqs.pop(k)
                '''

                #full_direction_data_in_r1_seq.append([dir_data_in_seqs[0]]) #[list[0]]
                full_direction_data_in_r1_seq.append(dir_data_in_seqs)

                #print("dir_data_in_seqs n_bot", dir_data_in_seqs)
            robotn_full_direction_data_all_seq.append(full_direction_data_in_r1_seq)
            #print("full_direction_data_in_r1_seq n_bot", full_direction_data_in_r1_seq)
            print("len full_direction_data_in_r1_seq n_bot", len(full_direction_data_in_r1_seq))

        self.all_robot_full_direction_data_all_seq.append(robotn_full_direction_data_all_seq)
        #print("robotn_full_direction_data_all_seq", robotn_full_direction_data_all_seq)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")

    def find_dirs_on_dirs(self, dirs):
        '''
        Too much, can't prove: Assumption 3: different paths don't actually matter
        '''
        if len(dirs) == 0:
            dirs.append([0,0])
        elif dirs[-1] != [0,0]:
            dirs.append([0,0])

        data_lists = [[]] # many lists; each list represents one possibility
        current_p = self.dir_button_start_coords
        for dir in dirs:
            button_coords = self.convert_dir_button_coords(dir)

            row_disp = button_coords[0] - current_p[0]
            col_disp = button_coords[1] - current_p[1]

            row_dirs = []
            col_dirs = []
            if row_disp < 0:  # up
                row_dirs = [[-1, 0]] * abs(row_disp)
            elif row_disp > 0:  # down
                row_dirs = [[1, 0]] * row_disp
            if col_disp < 0:  # left
                col_dirs = [[0, -1]] * abs(col_disp)
            elif col_disp > 0:  # right
                col_dirs = [[0, 1]] * col_disp

            # top left is dead square

            seq_1 = row_dirs + col_dirs
            seq_2 = col_dirs + row_dirs
            seq_1.append([0,0])
            seq_2.append([0,0])

            #print("data_lists", data_lists)

            if not (len(row_dirs) > 0 and len(col_dirs) > 0):  # only has 1 or 0 directions (out of u/d/l/r)
                # direction_data_in_seq will have 2 lists (unless dead square passed), else 1
                direction_data_in_seq = seq_1
            elif button_coords[0] == 0 and current_p[1] == 0:  # down then right will lead to dead square
                direction_data_in_seq = seq_2
            elif current_p[0] == 0 and button_coords[1] == 0:  # left then up will lead to dead square
                direction_data_in_seq = seq_1
            else:  # 2 possibilities
                #direction_data_in_seq = [seq_1, seq_2]
                #print("data_lists", data_lists)
                data_lists_copy = deepcopy(data_lists)
                for i in range(len(data_lists)):
                    data_lists[i].extend(seq_1)
                    #print("data_lists e", data_lists)
                for i in range(len(data_lists_copy)):
                    data_lists_copy[i].extend(seq_2)

                #print("data_lists f", data_lists)
                data_lists.extend(data_lists_copy)
                #print("direction_data_in_2seqs:", seq_1, seq_2)
                #print("data_lists", data_lists)
                #print("data_lists copy", data_lists_copy)

                current_p = button_coords
                continue
            for i in range(len(data_lists)):
                data_lists[i].extend(direction_data_in_seq)
            #print("direction_data_in_seq:", direction_data_in_seq)
            current_p = button_coords

        return data_lists

    def find_num_inputs(self):
        relevant_robot_full_direction_data_all_seq = self.all_robot_full_direction_data_all_seq[-1]
        print("what", relevant_robot_full_direction_data_all_seq)
        shortest_seq = []
        for i, full_direction_data_in_seq in enumerate(relevant_robot_full_direction_data_all_seq):
            len_of_shortest_seq = 0
            shortest_segment = []
            for j, dir_data_in_seqs in enumerate(full_direction_data_in_seq):
                #first_list_best_list = dir_data_in_seqs[0]
                #first_list_best_list = dir_data_in_seqs[-1]
                #best_list_len_for_move = len(first_list_best_list)

                min_len = -1
                for k, data in enumerate(dir_data_in_seqs):
                    len_data = len(data)
                    if len_data < min_len or min_len == -1:
                        min_len = len_data
                        shortest_segment = data

                #len_of_shortest_seq += best_list_len_for_move
                len_of_shortest_seq += min_len
            shortest_seq.append(shortest_segment)
            self.lens_of_shortest_seqs.append(len_of_shortest_seq)

        print("shortest seq", shortest_seq)
        self.shortest_init_seq = shortest_seq

    def find_complexity_sum(self):
        self.complexity_sum = 0
        print("numeric of code", self.numeric_of_codes)
        for i in range(len(self.lens_of_shortest_seqs)):
            shortest_len = self.lens_of_shortest_seqs[i]
            numeric_of_code = self.numeric_of_codes[i]
            complexity = shortest_len*numeric_of_code

            self.complexity_sum += complexity
            print("Complexity added to sum:", shortest_len, "*", numeric_of_code, "=", complexity)


    def find_inputs_after_2nd_layer(self):
        relevant_robot_full_direction_data_all_seq = self.all_robot_full_direction_data_all_seq[-1]
        print("START HERE:", relevant_robot_full_direction_data_all_seq)

        # You have to strip it all down and get all possible direction seqs


        for i, full_direction_data_in_seq in enumerate(relevant_robot_full_direction_data_all_seq):
            len_of_shortest_seq = 0
            input_seq = []
            for j, dir_data_in_seqs in enumerate(full_direction_data_in_seq):
                min_len = -1
                data_w_min_len = []
                for k, data in enumerate(dir_data_in_seqs):
                    len_data = len(data)
                    if len_data < min_len or min_len == -1:
                        min_len = len_data
                        data_w_min_len = data

                #self.inputs_after_2nd_layer.extend(data_w_min_len)
                input_seq.extend(data_w_min_len)
            self.inputs_after_2nd_layer.append(input_seq)

        print("inputs after 2nd layer:", self.inputs_after_2nd_layer)

        # Conversion 1: dirs to inputs indexes
        for i in range(len(self.inputs_after_2nd_layer)):
            input_indexes = []
            for j in range(len(self.inputs_after_2nd_layer[i])):
                coords = self.inputs_after_2nd_layer[i][j]
                input_index = self.input_list.index(coords)
                #self.input_indexes_after_2nd_layer.append(input_index)
                input_indexes.append(input_index)
            self.input_indexes_after_2nd_layer.append(input_indexes)

        print("input indexes after 2nd layer:", self.input_indexes_after_2nd_layer)





        self.input_indexes_after_2nd_layer = self.true_input_indexes_after_second_layer
        print("TRUE input indexes after 2nd layer:", self.input_indexes_after_2nd_layer)

        # Conversion 2: input indexes to dir-to-dir indexes
        for i in range(len(self.input_indexes_after_2nd_layer)):
            dtd_indexes = self.get_dtd_indexes_from_inputs(self.input_indexes_after_2nd_layer[i])
            self.dtd_indexes_after_2nd_layer.append(dtd_indexes)
        print("dtd indexes after 2nd layer:", self.dtd_indexes_after_2nd_layer)

    def get_dtd_indexes_from_inputs(self, input_seq):
        index_seq = []
        for k, input in enumerate(input_seq):
            prev_input = 0
            if k > 0:
                prev_input = input_seq[k - 1]
            true_index = prev_input * 5 + input
            index_seq.append(true_index)
        return index_seq

    def init_dir_to_dir_list(self):
        count = 0
        for i in range(5):
            for j in range(5):
                inp_seq_i = self.dir_to_dir_grid[i][j]
                out_seq = self.out_seqs[inp_seq_i]
                out_seq_len = len(out_seq)

                index_seq = self.get_dtd_indexes_from_inputs(out_seq) #[]
                '''
                for k, out in enumerate(out_seq):
                    prev_out = 0
                    if k > 0:
                        prev_out = out_seq[k-1]
                    true_index = prev_out*5 + out
                    index_seq.append(true_index)
                '''

                self.dir_to_dir_list.append(index_seq)
                self.dtd_deriv_count_list.append(out_seq_len)
                print(count, "out_seq", out_seq_len, index_seq)

                count += 1

    def find_dtd_deriv_counts_next_step(self):
        dtd_deriv_counts_next_step = [0] * 25
        for i, to_dirs in enumerate(self.dir_to_dir_list):
            dtd_deriv_count = 0
            for j, to_dir in enumerate(to_dirs):
                to_add = self.dtd_deriv_counts_nth_step[to_dir]
                dtd_deriv_count += to_add
            dtd_deriv_counts_next_step[i] = dtd_deriv_count
        self.dtd_deriv_counts_nth_step = dtd_deriv_counts_next_step
        self.dtd_deriv_counts_all_steps.append(dtd_deriv_counts_next_step)
        print("dtd_deriv_counts_next_step", dtd_deriv_counts_next_step)


    def find_true_input_lens(self):
        layers_past = 23 # original was 0, new is 23
        self.lens_of_shortest_seqs = []
        for i in range(len(self.dtd_indexes_after_2nd_layer)): # need another loop?
            sequence_size = 0
            indexes = self.dtd_indexes_after_2nd_layer[i]
            for j in range(len(self.dtd_indexes_after_2nd_layer[i])):
                dtd_index_after_2nd_layer = indexes[j]
                size_from_init = self.dtd_deriv_counts_all_steps[layers_past][dtd_index_after_2nd_layer]
                sequence_size += size_from_init
            self.lens_of_shortest_seqs.append(sequence_size)

    def output(self):
        self.set_data()
        print(self.true_button_chars)
        print(self.true_button_coords)
        print(self.numeric_of_codes)


        print("dir_to_dir_list", self.dir_to_dir_list)
        print("dtd_deriv_count_list", self.dtd_deriv_count_list)

        for i in range(35):
            self.find_dtd_deriv_counts_next_step()

        print("dtd_deriv_counts_all_steps", self.dtd_deriv_counts_all_steps)

        self.find_numpad_dir_data()
        print("numpad done") # numpad > bot1

        self.find_robot1_dir_data()
        print("bot 1 done") # bot1 > bot2

        print("1++++++++++++++++++++++++++1")
        self.find_num_inputs()
        print("2++++++++++++++++++++++++++2")

        self.find_inputs_after_2nd_layer()

        '''
        #print("aaaaa", self.dtd_indexes_after_2nd_layer)
        test_list = []
        test_list.extend(self.dtd_indexes_after_2nd_layer[0])
        test_list.extend(self.dtd_indexes_after_2nd_layer[1])
        test_list.extend(self.dtd_indexes_after_2nd_layer[2])
        test_list.extend(self.dtd_indexes_after_2nd_layer[3])
        for i, num in enumerate(self.dtd_indexes_after_2nd_layer[4]):
            print("num:", num)
            if num not in test_list:
                print("NUM NOT IN OTHER LISTS:", num)
        '''

        self.find_true_input_lens()
        print("lens_of_shortest_seqs", self.lens_of_shortest_seqs)


        #self.find_robotn_dir_data()
        #print("bot 2 done") # bot2 > bot3

        # 23 more robots
        #for n in range(23):
        #    self.find_robotn_dir_data()
        #    x=0

        #self.find_robotn_dir_data()
        #print("bot 3 done") # bot3 > you

        #self.find_robotn_dir_data() # technically you, not a bot
        #print("you done")

        #data_lists = self.find_dirs_on_dirs([[-1, 0], [-1, 0], [0, 1]])
        #print("data_lists:", data_lists)

        #self.find_num_inputs()
        self.find_complexity_sum()
        print("COMPLEXITY SUM (answer):", self.complexity_sum)

class Day22:
    '''
    [[-1,-1,0,2],6]
    Have super list of all 4 int sequences and total price gotten from each one
    Add to price each time the list is seen again (but if the list has already been seen for that buyer, it doesn't count)
    Loop through buyers
    '''
    def __init__(self):
        self.init_secret_nums = []
        self.secret_nums = []
        self.num_secret_nums = 0

        self.secret_num_sum = 0

        #self.all_secret_nums_each_step = []
        self.prices = []

        self.sequences_to_keep_track_of = []
        self.prices_of_seqs_to_keep_track_of = []

        self.alt_prices_of_seqs_tkto = [0] * 130321

        self.most_bananas = 0

    def set_data(self):
        with open("day22.1.txt", "r") as file:
            prices = []
            for line in file:
                int_str = line.strip()
                init_secret_num = int(int_str)
                self.init_secret_nums.append(init_secret_num)
                price = self.get_price_from_secret_num(init_secret_num)
                #print("price", price, init_secret_num)
                prices.append(price)
        self.secret_nums = self.init_secret_nums.copy()
        #self.all_secret_nums_each_step.append(self.secret_nums)
        self.prices.append(prices)
        self.num_secret_nums = len(self.secret_nums)

    def mix(self, value, secret_num):
        xor = value ^ secret_num
        return xor

    def prune(self, secret_num):
        return secret_num % 16777216

    def get_price_from_secret_num(self, secret_num):
        return int(str(secret_num)[-1])

    def evolve_secret_number(self, old_secret_num):
        a1 = old_secret_num*64
        a2 = self.mix(a1, old_secret_num)
        a3 = self.prune(a2)

        b1 = a3 // 32
        b2 = self.mix(b1, a3)
        b3 = self.prune(b2)

        c1 = b3*2048
        c2 = self.mix(c1, b3)
        c3 = self.prune(c2)

        return c3

    def evolve_secret_numbers_n_times(self, n=2000):
        for i in range(n):
            prices = [-1] * self.num_secret_nums
            for j, secret_number in enumerate(self.secret_nums):
                new_secret_number = self.evolve_secret_number(secret_number)
                self.secret_nums[j] = new_secret_number
                prices[j] = self.get_price_from_secret_num(new_secret_number)
            #self.all_secret_nums_each_step.append(self.secret_nums)
            self.prices.append(prices)

    def add_up_secret_nums(self):
        sum = 0
        for i, secret_num in enumerate(self.secret_nums):
            sum += secret_num

        self.secret_num_sum = sum

    def get_best_seq(self):
        for i in range(self.num_secret_nums):
            # i_th buyer
            print("buyer #" + str(i+1) + "/" + str(self.num_secret_nums))
            prev_price = -1
            diff_seq = [-11,-11,-11,-11]
            n=2001
            #n=10
            diff_seqs_seen = []
            for j in range(n):
                price = self.prices[j][i]

                if j > 0:
                    price_diff = price - prev_price
                    diff_seq = diff_seq[1:] + [price_diff]
                    if j > 3:
                        if diff_seq not in diff_seqs_seen:
                            #print("ADD")
                            diff_seqs_seen.append(diff_seq)
                            '''
                            if diff_seq in self.sequences_to_keep_track_of:
                                index = self.sequences_to_keep_track_of.index(diff_seq)
                                self.prices_of_seqs_to_keep_track_of[index] += price
                            else:
                                self.sequences_to_keep_track_of.append(diff_seq)
                                self.prices_of_seqs_to_keep_track_of.append(price)
                            '''

                            seq_index = diff_seq[0] + diff_seq[1]*19 + diff_seq[2]*19**2 + diff_seq[3]*19**3
                            self.alt_prices_of_seqs_tkto[seq_index] += price
                #print("seq", diff_seq)
                prev_price = price

        #self.most_bananas = max(self.prices_of_seqs_to_keep_track_of)
        self.most_bananas = max(self.alt_prices_of_seqs_tkto)

    def output(self):
        self.set_data()
        print("init secret nums:", len(self.init_secret_nums), self.init_secret_nums)

        print(self.mix(15, 42), self.prune(100000000), self.get_price_from_secret_num(11100544))

        self.evolve_secret_numbers_n_times()
        print("secret nums:", self.secret_nums)
        print("init prices:", self.prices[0])

        self.add_up_secret_nums()
        print("sum:", self.secret_num_sum)

        self.get_best_seq()
        #print(self.sequences_to_keep_track_of)
        #print(self.prices_of_seqs_to_keep_track_of)
        print("most bananas:", self.most_bananas)

class Day23:
    def __init__(self):
        self.computers = []
        self.comp_connections = []
        self.comp_connections_is = []

        self.three_ways = []
        self.num_three_ways = 0

        self.longest_webs = []
        self.longest_web_is = []
        self.longest_web_unsorted_comps = []
        self.sorted_longest_web_comps_str = ""

    def set_data(self):
        with open("day23.1.txt", "r") as file:
            for line in file:
                comp1 = line[:2]
                comp2 = line[3:5]
                is_comp1_in_comps = comp1 in self.computers
                is_comp2_in_comps = comp2 in self.computers

                if not is_comp1_in_comps: #comp1 not in self.computers:
                    index1 = len(self.computers)
                    self.computers.append(comp1)
                    self.comp_connections.append([comp2])
                    self.comp_connections_is.append([])
                else:
                    index1 = self.computers.index(comp1)
                    self.comp_connections[index1].append(comp2)

                if comp2 not in self.computers:
                    index2 = len(self.computers)
                    self.computers.append(comp2)
                    self.comp_connections.append([comp1])
                    self.comp_connections_is.append([])
                else:
                    index2 = self.computers.index(comp2)
                    self.comp_connections[index2].append(comp1)

                self.comp_connections_is[index1].append(self.computers.index(comp2))
                self.comp_connections_is[index2].append(self.computers.index(comp1))

    def process_data(self):
        for comp1_i, computer1 in enumerate(self.computers):
            if computer1[0] == 't':
                connections1 = self.comp_connections[comp1_i]
                for computer2 in connections1:
                    comp2_i = self.computers.index(computer2)
                    connections2 = self.comp_connections[comp2_i]
                    for computer3 in connections2:
                        if computer3 == computer1:
                            continue
                        comp3_i = self.computers.index(computer3)
                        connections3 = self.comp_connections[comp3_i]
                        if computer1 in connections3:
                            triad_set = frozenset([computer1, computer2, computer3])
                            if triad_set not in self.three_ways:
                                self.three_ways.append(triad_set)
        self.num_three_ways = len(self.three_ways)

    def process_data2(self):
        for comp1_i, computer1 in enumerate(self.computers):
            connections1 = self.comp_connections[comp1_i]
            #valid_connections = connections1.copy()
            other_comps_is = []
            connections_of_other_comps = []
            connection_web_setup = [] # list of list of the index of conn1 list in each connection1's connection

            for i, other_comp in enumerate(connections1):
                other_comp_i = self.computers.index(other_comp)
                other_comps_is.append(other_comp_i)

                other_comp_connections = self.comp_connections[other_comp_i].copy()
                other_comp_connections.remove(computer1)
                connections_of_other_comps.append(other_comp_connections)

                web_setup_list = [i]
                for other_other_comp in other_comp_connections:
                    if other_other_comp in connections1:
                        index = connections1.index(other_other_comp)
                        web_setup_list.append(index)
                connection_web_setup.append(web_setup_list)
                '''
                valid_connections = connections1.copy()
                
                other_comp_i = self.computers.index(other_comp)
                other_comp_connections = self.comp_connections[other_comp_i]
                other_comp_connections.remove(computer1) # don't want to go back to check again, inf loop
                no_longer_valid_connections = []
                for comp_should_be_in_list in valid_connections:
                    if comp_should_be_in_list not in valid_connections:
                        no_longer_valid_connections.append(comp_should_be_in_list)
                for comp_to_remove in no_longer_valid_connections:
                    valid_connections.remove(comp_to_remove)
                '''

            valid_webs = self.check_good_webs(other_comps_is[0], other_comps_is[1:])

            print("current comp & connections", computer1, connections1)
            print("other comps' indexes", other_comps_is)
            print("other comps' connections", connections_of_other_comps)
            print("connection_web_setup", connection_web_setup)
            print("valid webs", valid_webs)

            longest_web = []
            longest_web_size = 0
            for i, web in enumerate(valid_webs):
                web_len = len(web)
                if web_len > longest_web_size:
                    longest_web = web
                    longest_web_size = web_len
            longest_web.append(comp1_i)
            self.longest_webs.append(longest_web)
            print("longest web in here", longest_web)

            print("")

            #for con1_i, con1 in enumerate(connections1):
                #cons_cons = connections_of_other_comps[con1_i]

    def check_good_webs(self, check_index, unchecked_indexes):  # return good_webs (so far)
        # put into test.py and run with test lists
        #print("check index and other unchecked indexes", check_index, unchecked_indexes)
        good_webs = []  # list of webs that are all
        unchecked_indexes_len = len(unchecked_indexes)

        if unchecked_indexes_len == 0:
            #print("another return", [[check_index]])
            return [[check_index]]  # all good indexes have been taken care of

        good_indexes = []
        not_all_good = False
        for i, unchecked_index in enumerate(unchecked_indexes):
            # print("cci rel", unchecked_index, self.comp_connections_is[unchecked_index])
            if check_index in self.comp_connections_is[unchecked_index]:
                good_indexes.append(unchecked_index)
            else:
                not_all_good = True
        #print("good indexes", good_indexes, not_all_good)

        if not_all_good:
            #print("uncapture 1")
            without_check_index_try = self.check_good_webs(unchecked_indexes[0], unchecked_indexes[1:])  # add in check_index to each list in lists
            #print("capture 1", without_check_index_try)
            if len(good_indexes) > 0:
                #print("uncapture 2")
                with_check_index_try = self.check_good_webs(good_indexes[0], good_indexes[1:])
                #print("capture 2", with_check_index_try)
            else:
                # return None #[[check_index]] # not a single good index after, stop
                with_check_index_try = [[]]
            with_check_index_try = self.add_to_every_list_in_lists(check_index, with_check_index_try)
            # print(without_check_index_try)
            good_webs.extend(without_check_index_try)
            good_webs.extend(with_check_index_try)
            #print("good webs after extensions", good_webs)
        else:
            #print("uncapture 3")
            good_webs_proto = self.check_good_webs(unchecked_indexes[0], good_indexes[1:])
            good_webs = self.add_to_every_list_in_lists(check_index, good_webs_proto)
            #print("capture 3", good_webs)

        # good_webs = self.add_to_every_list_in_lists(check_index, good_webs)

        #print("a return", good_webs)
        return good_webs

    def add_to_every_list_in_lists(self, to_add, lol):
        for i in range(len(lol)):
            lol[i].append(to_add)
        return lol

    def find_true_longest_web(self):
        longest_web = []
        longest_web_size = 0
        for i, web in enumerate(self.longest_webs):
            web_len = len(web)
            if web_len > longest_web_size:
                longest_web = web
                longest_web_size = web_len

        self.longest_web_is = longest_web

        self.longest_web_unsorted_comps = []
        for i, longest_web_i in enumerate(self.longest_web_is):
            self.longest_web_unsorted_comps.append(self.computers[longest_web_i])

        self.sorted_longest_web_comps_str = ""
        for i in range(97, 123):
            char1 = chr(i)
            for j in range(97, 123):
                char2 = chr(j)
                potential_comp = char1 + char2
                if potential_comp in self.longest_web_unsorted_comps:
                    to_add = potential_comp + ','
                    self.sorted_longest_web_comps_str += to_add
        self.sorted_longest_web_comps_str = self.sorted_longest_web_comps_str[:-1]

    def output(self):
        self.set_data()
        print("computers:", self.computers)
        print("computer connections:", self.comp_connections)
        print("computer connections is:", self.comp_connections_is)

        self.process_data()
        print("three ways:", self.three_ways)
        print("num three ways:", self.num_three_ways)

        self.process_data2()

        self.find_true_longest_web()
        print("true longest web", self.longest_web_is)
        print("longest web unsorted comps", self.longest_web_unsorted_comps)
        print("longest web sorted comps (ANSWER):", self.sorted_longest_web_comps_str)

class Day24:
    '''
    Tips:
    -NO z is an operand
    -ALL non-zs ARE operands
    -xs and ys always pair with other xs and ys?
    -xs&ys can sometimes lead directly to zs
    -xs and ys seem to always have the same number when paired together
    -All xs and ys are operands twice
    -All other vars are operands 1-2 times

    -Checked each incorrect z for all eqs it depends on
    -Checked each z for all operands it depends on
    -Checked each operand for all bad zs it goes into

    -Check each operand for all z it goes into
    -Make a tree for each bad z ending at x&y vals. Check the earlier layers and see if they connect to purely good zs or any bad ones.
    -all operands that lead directly to a good z can be eliminated from leading to a bad z? - depends on the operator; depends on if the good equation changes output, as well as other operand
    -All x/y+2digits_num lead to that z num, and every z after that num except leading to 7 if x/y is before 7
    '''
    def __init__(self):
        self.vars = [] # statics: list of strings
        self.var_values = [] # NOT static: list of binary values per var, or -1 if var not yet defined
        self.var_operand_eq_pointers = [] # statics: list of list of each equation index for each var (each equation the var is an operand in)
        self.var_output_eq_pointers = []
        self.var_dicts = [] # unused rn

        self.eqs_involved = []
        self.operands_involved = []
        self.outputs_that_are_lead_to = []
        self.z_outputs_that_are_lead_to = []
        self.bad_zs_that_eqs_end_up_at = []
        self.bad_zs_that_vars_end_up_at = []

        # 222 equations; 222!/(222-8)! = 5*10^18 rough num of random swaps
        self.equations = [] # statics: [eq_id (and/xor/or), var_pointer1, var_pointer2, var_pointer3]

        self.x_vals = []
        self.y_vals = []
        self.orig_z_vals = []
        self.correct_z_vals = []

        self.x_val = 0
        self.y_val = 0
        self.orig_z_val = 0 # this is just z_answer
        self.correct_z_val = 0

        # 46 zs 00-45
        self.z_pointers = [-1] * 100 # var indexes (in vars list) of each z from z00 to z99

        self.z_answer = 0

    def set_data(self):
        with open("day24.1.o.txt", "r") as file:
            for line in file:
                line = line.strip()
                line_len = len(line)
                if line_len == 0:
                    continue
                if line[3] == ':':
                    var = line[:3]
                    var_val = int(line[5])
                    self.vars.append(var)
                    self.var_values.append(var_val)
                    self.var_operand_eq_pointers.append([])
                    self.var_output_eq_pointers.append([])
                    self.eqs_involved.append([])
                    self.operands_involved.append([])
                    self.outputs_that_are_lead_to.append([])
                    self.z_outputs_that_are_lead_to.append([])
                    self.bad_zs_that_vars_end_up_at.append([])

                    self.var_dicts = {"name": var, "val": var_val, "eq_pointers": '', "index": (len(self.vars)-1)}

                    if line[0] == 'x':
                        self.x_vals.append(var_val)
                    else:
                        self.y_vals.append(var_val)
                else:
                    eq_id_indicator = line[4]
                    eq_id = -1
                    offset = 0

                    if eq_id_indicator == 'A':
                        eq_id = 0
                    elif eq_id_indicator == 'X':
                        eq_id = 1
                    elif eq_id_indicator == 'O':
                        eq_id = 2
                        offset = -1

                    v1 = line[:3]
                    v2 = line[8+offset:11+offset]
                    v3 = line[15+offset:18+offset]

                    equation = [eq_id, -1, -1, -1]
                    this_eq_index = len(self.equations)
                    for i, var in enumerate([v1, v2, v3]):
                        var_index = -1
                        if var not in self.vars: # new var in vars
                            var_index = len(self.vars)
                            self.vars.append(var)
                            self.var_values.append(-1)
                            self.eqs_involved.append([])
                            self.operands_involved.append([])
                            self.outputs_that_are_lead_to.append([])
                            self.z_outputs_that_are_lead_to.append([])
                            self.bad_zs_that_vars_end_up_at.append([])
                            if i != 2:
                                self.var_operand_eq_pointers.append([this_eq_index])
                                self.var_output_eq_pointers.append([])
                            else:
                                self.var_operand_eq_pointers.append([])
                                self.var_output_eq_pointers.append([this_eq_index])

                            if var[0] == 'z':
                                z_num_str = var[1:3]
                                z_num = int(z_num_str)
                                self.z_pointers[z_num] = var_index
                        else: # not a new var in vars
                            var_index = self.vars.index(var)
                            if i != 2:
                                self.var_operand_eq_pointers[var_index].append(this_eq_index)
                            else:
                                self.var_output_eq_pointers[var_index].append(this_eq_index)
                        equation[i+1] = var_index
                    self.equations.append(equation)
                    self.bad_zs_that_eqs_end_up_at.append([])

        num_zs = 0
        for z_int, z_pointer in enumerate(self.z_pointers):
            if z_pointer == -1:
                num_zs = z_int
                break
        print("num zs", num_zs)
        self.z_pointers = self.z_pointers[:num_zs]

        for i, val in enumerate(self.x_vals):
            self.x_val += val * 2**i
        for i, val in enumerate(self.y_vals):
            self.y_val += val * 2**i
        self.correct_z_val = self.x_val + self.y_val
        #self.correct_z_val = 40#[0,0,0,1,0,1]
        for i in range(len(self.x_vals)+1):
            #for i in range(len(self.x_vals)):#+1):
            z_bit_i = int((self.correct_z_val // 2**i) % 2)
            self.correct_z_vals.append(z_bit_i)
        self.correct_z_vals_2 = bin(self.correct_z_val)[2:].zfill(len(self.x_vals)+1)

        # NEW EQUATIONS
        self.equations[11] = [0, 52, 7, 277]
        self.equations[178] = [1, 215, 166, 117]



        #self.equations[19] = [0, 127, 128, 299];        self.equations[181] = [1, 128, 127, 129]
        #self.equations[193] = [2, 159, 158, 128];        self.equations[215] = [0, 11, 56, 127]
        #self.equations[35] = [0, 156, 157, 273];        self.equations[131] = [1, 156, 157, 158]
        #self.equations[35] = [0, 156, 157, 159];        self.equations[36] = [0, 10, 55, 158]
        #self.equations[210] = [0, 102, 290, 259];        self.equations[180] = [0, 9, 54, 258]
        # self.equations[65] = [1, 55, 10, 159];        self.equations[36] = [0, 10, 55, 156]
        self.equations[215] = [0, 11, 56, 177]; self.equations[47] = [1, 56, 11, 128]



        self.equations[25] = [1, 139, 119, 297]
        self.equations[169] = [2, 281, 286, 134]

        self.equations[46] = [0, 174, 175, 283]
        self.equations[208] = [1, 174, 175, 176]

        sorted_list_str = str(sorted([self.vars[277], self.vars[117], self.vars[177], self.vars[128], self.vars[297], self.vars[134], self.vars[283], self.vars[176]]))
        better_str = ("".join(sorted_list_str.split())).replace("'", "")
        print("ANSWER:", better_str)

    def attempt_eq_solve(self, eq_i):
        equation = self.equations[eq_i]
        var_val1 = self.var_values[equation[1]]
        var_val2 = self.var_values[equation[2]]
        if var_val1 == -1 or var_val2 == -1:
            return

        # If we got this far, the equation is solvable! Solving equation...
        output = -1
        op_id = equation[0]
        if op_id == 0: # AND
            if var_val1 == 1 and var_val2 == 1:
                output = 1
            else:
                output = 0
        elif op_id == 1: # XOR
            if var_val1 + var_val2 == 1:
                output = 1
            else:
                output = 0
        elif op_id == 2: # OR
            if var_val1 + var_val2 > 0:
                output = 1
            else:
                output = 0

        #print("EQ SOLVED", output, equation)
        self.var_values[equation[3]] = output
        #print(self.var_values, equation[3], self.var_values[equation[3]])

        eqs_involved = [eq_i]
        eqs_involved.extend(self.eqs_involved[equation[1]])
        eqs_involved.extend(self.eqs_involved[equation[2]])
        self.eqs_involved[equation[3]] = eqs_involved

        ops_involved = [equation[1], equation[2]]
        ops_involved.extend(self.operands_involved[equation[1]])
        ops_involved.extend(self.operands_involved[equation[2]])
        unique_sorted_ops_involved = sorted(set(ops_involved))
        self.operands_involved[equation[3]] = unique_sorted_ops_involved

        # Now attempt equation solve of all equations that the output var is an operand in
        for i, other_eq_i in enumerate(self.var_operand_eq_pointers[equation[3]]):
            self.attempt_eq_solve(other_eq_i)

    def solve_equations(self):
        for eq_i, equation in enumerate(self.equations):
            self.attempt_eq_solve(eq_i)

    def calc_z_data(self):
        self.z_answer = 0
        for z_int, z_pointer in enumerate(self.z_pointers):
            if z_pointer < 0:
                continue
            z_bit = self.var_values[z_pointer] # 0 or 1 (Shouldn't be -1)
            if z_bit == -1:
                return False

            to_add = z_bit * 2**z_int
            self.z_answer += to_add
            self.orig_z_vals.append(z_bit)

        self.orig_z_val = self.z_answer
        return True

    def compare_z_vals_to_correct(self):
        print("")
        for z in range(len(self.orig_z_vals)): #range(len(self.correct_z_vals))
            correct_bit = self.correct_z_vals[z]
            #print(z, self.orig_z_vals, self.correct_z_vals)
            check_bit = self.orig_z_vals[z]
            if correct_bit != check_bit:
                eqs_involved = self.eqs_involved[self.z_pointers[z]]
                ops_involved = self.operands_involved[self.z_pointers[z]]
                unique_sorted_eqs_inv = sorted(set(eqs_involved))
                print("bit z#" + str(z) + " is incorrect, should be " + str(correct_bit) + ". Unique sorted Eqs inv:", len(unique_sorted_eqs_inv), unique_sorted_eqs_inv)
                print("Unique sorted vars involved:", len(ops_involved), ops_involved ,"\n")
                for j, eq_i in enumerate(unique_sorted_eqs_inv):
                    self.bad_zs_that_eqs_end_up_at[eq_i].append(z)
                for j, var_i in enumerate(ops_involved):
                    self.bad_zs_that_vars_end_up_at[var_i].append(z)

    def find_all_eq_that_lead_to_var_i(self, var_i): # not needed, also unverified
        eq_is = self.var_output_eq_pointers[var_i].copy()
        if len(eq_is) == 0:
            return []
        eq_i = eq_is[0] # only 1 in list
        equation = self.equations[eq_i]
        eq_i_list = [eq_i]

        for eq_op in [equation[1], equation[2]]:
            more_eq_is = self.find_all_eq_that_lead_to_var_i(eq_op)
            eq_i_list.extend(more_eq_is)

        return eq_i_list


    def post_process(self):
        print("\n++++++++++++++++++++++++++++++++++++++++++++++\n")
        for i, equation in enumerate(self.equations):
            print("Equation i#" + str(i), equation)

        print("")

        self.num_potential_bad_ops = 0
        self.potential_bad_ops = []
        for i, var in enumerate(self.vars):
            eq_i = self.var_output_eq_pointers[i]
            operand_in_eqs = self.var_operand_eq_pointers[i]
            outputs_in_eqs_lead_to = []  # important
            for j in range(len(operand_in_eqs)):
                eq = operand_in_eqs[j]
                to_add = self.equations[eq][3]
                outputs_in_eqs_lead_to.append(to_add)

            for j, other_var in enumerate(self.vars):
                #print("hhh", var, self.operands_involved[j])
                if i in self.operands_involved[j]:
                    self.outputs_that_are_lead_to[i].append(j)
                    if j in self.z_pointers:
                        z = self.z_pointers.index(j)
                        self.z_outputs_that_are_lead_to[i].append([z, j])

            eqs_that_var_is_operand_in = []
            for j in operand_in_eqs:
                eqs_that_var_is_operand_in.append(self.equations[j])

            if len(eq_i) == 0:
                print("var i#" + str(i) + ": " + self.vars[i], "val:",
                      self.var_values[i],
                      "||| operand in eq:", operand_in_eqs, "(" + str(eqs_that_var_is_operand_in) + ")", "which leads to outputs:", outputs_in_eqs_lead_to,
                      "original var")
            else:
                inputs_from = self.equations[eq_i[0]][1:3]  # important
                print("var i#" + str(i) + ": " + self.vars[i], "val:",
                      self.var_values[i],
                      "||| operand in eq:", operand_in_eqs, "(" + str(eqs_that_var_is_operand_in) + ")", "which leads to outputs:", outputs_in_eqs_lead_to,
                      "/// output in eq:", eq_i, "(" + str(self.equations[eq_i[0]]) + ")", "from inputs:",
                      inputs_from)  # [" + str(self.equations[eq_i[0]][0]) + ", " + str(self.equations[eq_i[0]][1]) + "]")
            if len(self.bad_zs_that_vars_end_up_at[i]) > 0:
                self.num_potential_bad_ops += 1
                self.potential_bad_ops.append(i)

        for i, var in enumerate(self.vars):
            print("operands involved in var i#" + str(i) + ":", self.operands_involved[i])

        for i, var in enumerate(self.vars):
            print("outputs lead to from var i#" + str(i) + ":", self.outputs_that_are_lead_to[i])
            print("z outputs lead to from var i#" + str(i) + ":", self.z_outputs_that_are_lead_to[i])
            print("bad zs lead to from var i#" + str(i) + ":", self.bad_zs_that_vars_end_up_at[i])

        self.z_outputs_sorted = []
        for i, var in enumerate(self.vars):
            z_outputs_sorted = []
            for j, z_output in enumerate(self.z_outputs_that_are_lead_to[i]):
                z_outputs_sorted.append(z_output[0])
            z_outputs_sorted = sorted(z_outputs_sorted)
            self.z_outputs_sorted.append(z_outputs_sorted)
            print("ordered z outputs lead to from var i#" + str(i) + ":", z_outputs_sorted)
            if len(z_outputs_sorted) == 0:
                continue
            minimum = min(z_outputs_sorted)
            for j in range(minimum, 46):
                if j not in z_outputs_sorted:
                    print("^^^ vari#" + str(i) + " breaks the RULE at z#" + str(j))
                    #break
        print("")
        sorted_list_of_lists = sorted(enumerate(self.z_outputs_sorted), key=lambda x: len(x[1]))
        sorted_indexes = [index for index, _ in sorted_list_of_lists]
        old_len = 0
        num_in_len = 0
        for i in range(len(self.vars)):
            sorted_index = sorted_indexes[i]
            sorted_list = self.z_outputs_sorted[sorted_index]

            if len(sorted_list) != old_len:
                old_len = len(sorted_list)
                print("amount this size:", num_in_len)
                num_in_len = 1
            else:
                num_in_len += 1
            print("doubly ordered z outputs lead to from var i#" + str(sorted_index) + ":", sorted_list)

            if len(sorted_list) == 0:
                if sorted_index not in self.z_pointers:
                    print("not a z but leads to no zs")
                else:
                    print("z", self.z_pointers.index(sorted_index))

        print("\npotential bad operands:", self.num_potential_bad_ops, self.potential_bad_ops)

    def output(self):
        self.set_data()
        print("vars:", len(self.vars), self.vars)
        print("var_values:", self.var_values)
        print("var_operand_eq_pointers:", self.var_operand_eq_pointers)
        print("var_output_eq_pointers:", self.var_output_eq_pointers)
        print("equations:", self.equations)
        print("z pointers", self.z_pointers)
        print("eqs involved before solves", len(self.eqs_involved), self.eqs_involved)

        print("")
        print("x val", self.x_val, self.x_vals)
        print("y val", self.y_val, self.y_vals)
        print("correct z val", self.correct_z_val, self.correct_z_vals)

        '''
        for z_num, z_pointer in enumerate(self.z_pointers):
            eq_pointers = self.var_op_eq_pointers[z_pointer]
            print(z_num, eq_pointers)
        for var_i, eq_pointer in enumerate(self.var_op_eq_pointers):
            if var_i not in self.z_pointers:
                print("A E O - AEO", var_i, eq_pointer)
        '''

        self.solve_equations()
        print("var values after solving equations:", self.var_values)
        print("eqs involved", self.eqs_involved)

        self.calc_z_data()
        print("z answer:", self.z_answer)
        print("orig z val", self.orig_z_val, self.orig_z_vals)

        self.compare_z_vals_to_correct()

        #self.post_process()



class Day25:
    def __init__(self):
        self.keys = []
        self.locks = []

        self.num_key_lock_pairs = 0

    def set_data(self):
        with open("day25.1.txt", "r") as file:
            block_row = 0
            block = [[-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1]]
            for line in file:
                if block_row == 7:
                    block_row = 0
                    # Turn into key/lock data here
                    data = [0, 0, 0, 0, 0]
                    for col in range(5):
                        for row in range(1,6):
                            if block[row][col] == 1:
                                data[col] += 1

                    if block[0][0] == 1:
                        self.locks.append(data)
                    else:
                        self.keys.append(data)

                    block = [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1],
                             [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]
                    continue
                char_i = 0
                for char in line.strip():
                    num = 0
                    if char == '#':
                        num = 1
                    block[block_row][char_i] = num
                    char_i += 1
                block_row += 1

    def process_data(self):
        for lock in self.locks:
            for key in self.keys:
                fits = True
                for col in range(5):
                    l = lock[col]
                    k = key[col]
                    if l+k > 5:
                        fits = False
                        break

                if fits:
                    self.num_key_lock_pairs += 1

    def output(self):
        self.set_data()
        print("keys:", self.keys)
        print("locks:", self.locks)

        self.process_data()
        print("num_key_lock_pairs:", self.num_key_lock_pairs)


#day21 = Day21(); day21.output()   # Right: [70, 66, 66, 76, 70] [68, 60, 68, 64, 64]
#day21 = Day21_2(); day21.output() # Wrong: [74, 66, 66, 80, 78] [68, 60, 68, 64, 68] # also wrong: [74, 70, 66, 76, 70]
day22 = Day22(); day22.output()
#day23 = Day23(); day23.output()
#day24 = Day24(); day24.output()
#day25 = Day25(); day25.output()
