from copy import deepcopy
import re

class Day6:
    def __init__(self):
        self.poses_visited = 0 # Counts up at the end after calcs
        self.num_loop_obs = 0

        self.guard_pos = [0,0] # row, col (0 incl.)
        self.guard_pos_orig = [0,0]
        self.guard_dir = [0,1] # x, y (facing up; different orientation than guard_pos: Convert x,y -> -y,x when adding to guard pos)
        self.map_grid = [] # static
        self.map_grid_alt = []
        self.visited_grid = [] # fill with 1 each space moved to

        self.num_rows = 0
        self.num_cols = 0

    def reset_data(self):
        self.guard_pos[0] = self.guard_pos_orig[0]
        self.guard_pos[1] = self.guard_pos_orig[1]
        self.guard_dir = [0, 1]
        self.poses_visited = 0

        self.visited_grid = []
        for i in range(len(self.map_grid)):
            self.visited_grid.append([])
            for j in range(len(self.map_grid[0])):
                self.visited_grid[-1].append(0)
        self.visited_grid[self.guard_pos[0]][self.guard_pos[1]] = 1

        self.map_grid_alt = deepcopy(self.map_grid)

    def set_data(self):
        with open("day6.1.txt", "r") as file:
            for line in file:
                self.map_grid.append([])
                for char in line:
                    if char == ".":
                        self.map_grid[-1].append(0)
                    elif char == "^":
                        self.guard_pos_orig[0] = len(self.map_grid) - 1
                        self.guard_pos_orig[1] = len(self.map_grid[-1])
                        self.map_grid[-1].append(0)
                    elif char != "\n":
                        self.map_grid[-1].append(1)

        self.num_rows = len(self.map_grid)
        self.num_cols = len(self.map_grid[0])

        self.reset_data()

    def change_dir(self):
        # Turn 90 degrees to the right
        if self.guard_dir == [0,1]:
            self.guard_dir = [1,0]
        elif self.guard_dir == [1,0]:
            self.guard_dir = [0,-1]
        elif self.guard_dir == [0,-1]:
            self.guard_dir = [-1,0]
        elif self.guard_dir == [-1,0]:
            self.guard_dir = [0,1]

    def parse_set_visiting_grid(self):
        # Returns true on loop
        if self.guard_dir == [0, 1]:
            self.visited_grid[self.guard_pos[0]][self.guard_pos[1]] += 1
        elif self.guard_dir == [1, 0]:
            self.visited_grid[self.guard_pos[0]][self.guard_pos[1]] += 10
        elif self.guard_dir == [0, -1]:
            self.visited_grid[self.guard_pos[0]][self.guard_pos[1]] += 100
        elif self.guard_dir == [-1, 0]:
            self.visited_grid[self.guard_pos[0]][self.guard_pos[1]] += 1000

        check_val = self.visited_grid[self.guard_pos[0]][self.guard_pos[1]]

        if check_val % 10 > 1 or (check_val % 100) // int(10) > 1 or (check_val % 1000) // int(100) > 1 or (check_val % 10000) // int(1000) > 1:
            return True
        else:
            return False

    def go_thru_path(self):
        is_loop = False
        while True:
            # Check space in front of guard pos
            front_row = self.guard_pos[0] - self.guard_dir[1]
            front_col = self.guard_pos[1] + self.guard_dir[0]

            # Check if front space is outside map
            if front_row < 0 or self.num_rows <= front_row or\
                front_col < 0 or self.num_cols <= front_col:
                break

            front_space = self.map_grid_alt[front_row][front_col]
            if front_space == 0: # Move guard forward if path clear
                self.guard_pos[0] -= self.guard_dir[1]
                self.guard_pos[1] += self.guard_dir[0]

                is_loop = self.parse_set_visiting_grid()
                if is_loop:
                    break
                #self.visited_grid[self.guard_pos[0]][self.guard_pos[1]] = 1
            elif front_space == 1: # Turn right if path obstructed
                self.change_dir()

        #print(is_loop)
        return is_loop

    def calc_poses_visited(self):
        for i in range(len(self.visited_grid)):
            for j in range(len(self.visited_grid[0])):
                if self.visited_grid[i][j] > 0:
                    self.poses_visited += 1

    def put_obstacle_in_each_spot(self):
        for i in range(self.num_rows):
            print("Putting obstacle in row", i)
            for j in range(self.num_cols):
                #print("Put obstacle in", i, j)
                #print(i,j,self.num_rows,self.num_cols,len(self.map_grid),len(self.map_grid[0]))
                #print(self.map_grid[i],self.map_grid[i][j])
                if self.map_grid[i][j] == 0:
                    self.reset_data()
                    self.map_grid_alt[i][j] = 1

                    is_loop = self.go_thru_path()
                    if is_loop:
                        self.num_loop_obs += 1

    def output_day6(self):
        self.set_data()
        print(self.guard_pos, self.num_rows, self.num_cols)
        print(self.map_grid)
        print(self.visited_grid)

        is_loop = self.go_thru_path()
        print(self.visited_grid)
        print(is_loop)

        self.calc_poses_visited()
        print("#1: poses_visited",self.poses_visited)

        self.put_obstacle_in_each_spot()
        print("#2: num_loop_obs", self.num_loop_obs)

class Day7:
    def __init__(self):
        self.data = []

        self.total_cal_result = 0

    def set_data(self):
        with open("day7.1.txt", "r") as file:
            for line in file:
                self.data.append([int(num) for num in re.findall(r'\d+', line)])

    def get_ops(self, i, base_num_operators, num_operators):
        ops = []
        num = i
        while num > 0:
            ops.append(num % base_num_operators)  # Get the last digit in the desired base
            num //= base_num_operators  # Integer division by the base
        # Reverse the digits to get the correct order
        ops = ops[::-1]
        # Pad with leading zeros to match the desired digit length
        ops = [0] * (num_operators - len(ops)) + ops

        return ops

    def concatenation_op(self, a, b):
        return a * 10**(len(str(b))) + b

    def add_to_cal_if_good(self, line):
        print("Checking line:", line)
        num_operators = len(line) - 2
        operators = [0] * num_operators # 0 is '*'; 1 is '+'; 2 is '||' (concatenation)
        base_num_operators = 3
        for i in range(base_num_operators**num_operators):
            ops = self.get_ops(i, base_num_operators, num_operators)
            #print("ops:",ops)
            total = line[1]
            for j in range(len(ops)):
                #print("ops, j:",ops, j)
                if ops[j] == 0:
                    total *= line[j+2]
                elif ops[j] == 1:
                    total += line[j+2]
                elif ops[j] == 2:
                    total = self.concatenation_op(total, line[j+2])

                if total > line[0]: # too big with only + and *
                    continue
            if total == line[0]:
                self.total_cal_result += line[0]
                print("added to cal:", line[0])
                return

    def test_all_lines(self):
        self.total_cal_result = 0
        for line in self.data:
            self.add_to_cal_if_good(line)

    def output_day7(self):
        self.set_data()
        print(self.data)

        self.test_all_lines()
        print(self.total_cal_result)

class Day8:
    def __init__(self):
        self.x = 0
        self.grid = []
        self.num_rows = 0
        self.num_cols = 0

        self.antennas = []
        self.antenna_types = []

        self.antinode_grid = []
        self.antinode_locs = 0

    def set_data(self):
        with open("day8.1.txt", "r") as file:
            row_num = 0
            for line in file:
                if self.num_rows == 0:
                    self.num_cols = len(line.strip())
                self.num_rows += 1
                self.grid.append([])
                self.antinode_grid.append([])
                col_num = 0
                for char in line.strip():
                    self.grid[-1].append(char)
                    if char != '.':
                        self.antinode_grid[-1].append(1)
                        self.antennas.append([char, row_num, col_num])
                        type_exists = False
                        for i, type in enumerate(self.antenna_types):
                            if type[0] == char:
                                type_exists = True
                                self.antenna_types[i].append([row_num, col_num])
                                break
                        if not type_exists:
                            self.antenna_types.append([char, [row_num, col_num]])
                    else:
                        self.antinode_grid[-1].append(0)

                    col_num += 1
                row_num += 1

    def process(self):
        for i, type_list in enumerate(self.antenna_types):
            antenna_type_list = self.antenna_types[i]
            char = antenna_type_list[0]
            antennas = antenna_type_list.copy()[1:]
            for j, antenna in enumerate(antennas):
                #print(antenna, i)
                for k, antenna_2 in enumerate(antennas[(j+1):]):
                    #print(antenna, antenna_2, i, j)
                    col_dir = antenna_2[0] - antenna[0]
                    row_dir = antenna_2[1] - antenna[1]
                    an_1_c = -row_dir + antenna[1]
                    an_1_r = -col_dir + antenna[0]
                    an_2_c = row_dir + antenna_2[1]
                    an_2_r = col_dir + antenna_2[0]

                    print(antenna, antenna_2, row_dir, col_dir, "an:", an_1_r, an_1_c, an_2_r, an_2_c)

                    while 0 <= an_1_r < self.num_rows and 0 <= an_1_c < self.num_cols:
                        self.antinode_grid[an_1_r][an_1_c] = 1
                        print("fill_1", an_1_r, an_1_c)
                        an_1_r -= col_dir
                        an_1_c -= row_dir
                    while 0 <= an_2_r < self.num_rows and 0 <= an_2_c < self.num_cols:
                        self.antinode_grid[an_2_r][an_2_c] = 1
                        an_2_r += col_dir
                        an_2_c += row_dir
                        print("fill_2", an_2_r, an_2_c)

    def count_antinode_locs(self):
        self.antinode_locs = 0
        for i in range(len(self.antinode_grid)):
            for j in range(len(self.antinode_grid[i])):
                if self.antinode_grid[i][j] == 1:
                    self.antinode_locs += 1

    def output_day8(self):
        self.set_data()
        print(self.num_rows)
        print(self.num_cols)
        print(self.grid)
        print(self.antennas)
        print(self.antenna_types)
        print(self.antinode_grid)

        self.process()
        print(self.antinode_grid)

        self.count_antinode_locs()
        print(self.antinode_locs)

class Day9:
    def __init__(self):
        self.data = []
        self.data_len = 0
        self.files = []
        self.free_spaces = []
        self.num_data_spaces = 0
        self.num_free_spaces = 0
        self.num_all_spaces = 0

        self.moved_files = []

        self.checksum = 0

    def set_data(self):
        with open("day9.1.txt", "r") as file:
            for line in file: # 1 line btw
                for i, char in enumerate(line):
                    num = int(char)
                    self.data.append(num)
                    if i % 2 == 0:
                        self.files.append(num)
                        self.num_data_spaces += num
                    else:
                        self.free_spaces.append(num)
                        self.num_free_spaces += num

        self.num_all_spaces = self.num_free_spaces + self.num_data_spaces

        #self.moved_files = [None] * self.num_data_spaces
        #print("RRRR", len(self.moved_files))
        self.data_len = len(self.data)
        print(len(self.data))

    def move_files(self):
        #for i in range(self.num_data_spaces):
        data_c = self.data.copy()
        count = 0
        step = 0
        neg_count = -1
        file_step = 1 # -1 if on free space step
        while count < self.num_data_spaces:
            if count == self.num_data_spaces:
                break

            print("step", step, len(self.data))
            current_num = self.data[step]
            #print("step:", step, file_step, current_num)
            if file_step == 1:
                id_num = step // int(2)
                #print("count", count)
                for i in range(current_num):
                    if count == self.num_data_spaces:
                        break
                    #self.moved_files[count] = id_num
                    self.moved_files.append(id_num)
                    count += 1
            else:
                #print("HHH", current_num)
                for i in range(current_num):
                    if count == self.num_data_spaces:
                        break

                    # Fill with data but backwards
                    end_step_id = (self.data_len + neg_count) // int(2)
                    #neg_data = self.data[neg_count] # fix
                    self.data[neg_count] -= 1
                    if self.data[neg_count] == 0:
                        neg_count -= 2
                    #self.moved_files[count] = end_step_id

                    self.moved_files.append(end_step_id)
                    #self.moved_files.append(-1)

                    count += 1

            step += 1
            file_step *= -1

    def move_files_p2(self):
        data_c = self.data.copy()
        spots_before_file_block = []
        spots_before_free_space_block = []

        count = 0
        step = 0
        neg_count = -1
        file_step = 1  # -1 if on free space step
        while step < self.data_len:
            #print("step", step, len(self.data))
            current_num = self.data[step]
            #print("step:", step, file_step, current_num)
            if file_step == 1:
                spots_before_file_block.append(count)
                id_num = step // int(2)
                # print("count", count)
                for i in range(current_num):
                    # self.moved_files[count] = id_num
                    self.moved_files.append(id_num)
                    count += 1
            else:
                # print("HHH", current_num)
                spots_before_free_space_block.append(count)
                for i in range(current_num):

                    # Fill with data but backwards
                    end_step_id = (self.data_len + neg_count) // int(2)
                    # neg_data = self.data[neg_count] # fix
                    data_c[neg_count] -= 1
                    if data_c[neg_count] == 0:
                        neg_count -= 2
                    # self.moved_files[count] = end_step_id

                    #self.moved_files.append(end_step_id)
                    self.moved_files.append(-1)
                    count += 1

            step += 1
            file_step *= -1

        #print("spots_before_free_space_block:", spots_before_free_space_block)
        #print("spots_before_file_block:",spots_before_file_block)

        # Push data in blocks from end
        free_spaces_mod = self.free_spaces.copy()
        for i in range(len(self.files) - 1, -1, -1): # decrease file ids; i is the id
            moved = False
            for j in range(i): # check all blank spots from the left up to file id area
                if self.files[i] <= free_spaces_mod[j] and free_spaces_mod[j] > 0: # Can fit in free space
                    free_spaces_mod[j] -= self.files[i]

                    # In the jth free space block, fill in self.files[i] number of spaces equal with i
                    start_index = spots_before_free_space_block[j]
                    for k in range(start_index, start_index + self.files[i]):
                        self.moved_files[k] = i
                    start_index_2 = spots_before_file_block[i]
                    for k in range(start_index_2, start_index_2 + self.files[i]):
                        self.moved_files[k] = -1

                    spots_before_free_space_block[j] += self.files[i]

                    #print(i, "- moded moved_files:", self.moved_files)
                    #print(free_spaces_mod)
                    moved = True
                    break
                #print("didn't move:", i, j)
            if not moved:
                x=0
                #print("didn't move at all:", i)

    def find_checksum(self):
        for i in range(len(self.moved_files)):
            if self.moved_files[i] > 0:
                self.checksum += i*self.moved_files[i]

    def output_day9(self):
        self.set_data()
        print("data:",self.data)
        print("files:",self.files)
        print("free spaces:",self.free_spaces)
        print(self.num_free_spaces)
        print(self.num_data_spaces)
        print(self.num_all_spaces)

        #self.move_files()
        self.move_files_p2()
        print(self.moved_files)

        self.find_checksum()
        print(self.checksum)

class Day10:
    def __init__(self):
        self.grid = []
        self.trailheads = []

        self.num_rows = 0
        self.num_cols = 0

        self.sum_scores = 0

    def set_data(self):
        with open("day10.1.txt", "r") as file:
            row_num = 0
            for line in file:
                self.grid.append([])
                col_num = 0
                for char in line.strip():
                    num = int(char)
                    self.grid[-1].append(num)
                    if num == 0:
                        self.trailheads.append([row_num, col_num])
                    col_num += 1
                row_num += 1

        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])

    def calc_sum_scores(self):
        for th_i, trailhead in enumerate(self.trailheads):
            paths = [[trailhead]] # path: [[starting row, starting col], (not filled yet...)]; paths = [path0, ...]; paths->path->coords->row,col triple list
            #print("paths:", paths)
            for level in range(1,10):
                new_paths = []
                #print("pathss:", paths.copy())
                #print("new_paths:", new_paths)
                for path in paths.copy():
                    # current space is last on the current path, and space has row, col
                    row = path[-1][0]
                    col = path[-1][1]
                    for new_row, new_col in zip([row, row+1, row, row-1], [col+1, col, col-1, col]): # check +col, +row, -col, -row; right, down, left, up
                        #print("new_row/col:", new_row, new_col)
                        if 0 <= new_row < self.num_rows and 0 <= new_col < self.num_cols\
                            and self.grid[new_row][new_col] == level:
                            path_to_add = path.copy() + [[new_row, new_col]]
                            new_paths.append(path_to_add)
                            '''
                            valid = True # Valid check avoids having a bunch of paths that end the same way
                            for new_path in new_paths:
                                if [new_row, new_col] == new_path[-1]:
                                    valid = False
                                    break
                            if valid:
                                path_to_add = path.copy() + [[new_row, new_col]]
                                #print("pta:", path_to_add)

                                new_paths.append(path_to_add)
                                #new_paths[]
                            '''

                paths = new_paths.copy()
                if len(new_paths) == 0:
                    break

            #print("Paths at end:", paths)
            '''
            trail_ends = []
            for path in paths:
                if path[-1] not in trail_ends:
                    trail_ends.append(path[-1])
            score = len(trail_ends)
            
            '''
            score = len(paths)
            print("Score:", score)
            self.sum_scores += score

    def output_day10(self):
        self.set_data()
        print(self.grid)
        print(self.trailheads)
        print(self.num_rows, self.num_cols)

        self.calc_sum_scores()
        print(self.sum_scores)

#day6 = Day6()
#day6.output_day6()
#day7 = Day7()
#day7.output_day7()
#day8 = Day8()
#day8.output_day8()
#day9 = Day9()
#day9.output_day9()
day10 = Day10()
day10.output_day10()
