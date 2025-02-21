from copy import deepcopy
import numpy as np
import math
from PIL import Image

#from numpy.doc.constants import lines


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

class Day11:
    def __init__(self):
        self.current_stones = []
        self.already_stones = [] # unique num list
        self.a_s_references = []
        self.already_stones_init_usages = [] # double list: first usage blink, (2nd usage, 3rd, ...)
        self.num_stones_each_time = [] # double list: num_stones at 0 blinks, (at 1, 2, ...)
        self.adds = []

        self.ref_indexes = []

        self.already_stones_count = 0
        self.already_stones_checked = []

        self.new_stones = []
        self.blink = 0

        # splitter: num, num, id, id, num

        self.num_stones = 0

        self.orig_num_stones = 0

    def set_data(self):
        with open("day11.1.txt", "r") as file:
            for line in file: # 1 line
                self.current_stones = list(map(int, line.strip().split()))

        self.already_stones = self.current_stones.copy()
        #self.already_stones_blinks = [1] * len(self.current_stones)
        for i in range(len(self.current_stones)):
            self.num_stones_each_time.append([1])
            self.already_stones_init_usages.append([0])

        self.orig_num_stones = len(self.current_stones)
        print("orig", self.orig_num_stones)

    def check_stone(self, stone):
        if stone not in self.already_stones:
            self.already_stones.append(stone)
            self.already_stones_init_usages.append([self.blink])
            self.num_stones_each_time.append([1])
            self.already_stones_count += 1
            self.already_stones_checked.append(True)
        else:
            already_stones_index = self.already_stones.index(stone)
            self.already_stones_init_usages[already_stones_index].append()

    def process_already_stones(self):
        x=0

    def process_stone(self, i, old_stone, new_stone):
        #self.a_s_references[-1].append(new_stone)

        #self.a_s_references[-1].append([new_stone, (self.blink+1)])
        if new_stone not in self.already_stones:
            #print("new stone", new_stone)
            self.already_stones.append(new_stone)
            self.already_stones_init_usages.append([self.blink+1]) # init also looks wrong
            self.num_stones_each_time.append([1]) #[1]
            self.already_stones_count += 1
            #self.already_stones_checked.append(True) # ?
        else:
            already_stones_index = self.already_stones.index(new_stone)
            self.already_stones_init_usages[already_stones_index].append(self.blink+1)
            # if not already_stones_checked[already_stones_index]:
        after_blink = self.blink + 1
        a_s_index = self.already_stones.index(new_stone)
        init_w_index = self.already_stones_init_usages[a_s_index][0]
        diff = after_blink - init_w_index
        #print("Diff:", diff)
        self.a_s_references[-1].append([new_stone, diff])

    def process_stones2(self):
        print("S already stones", self.already_stones)
        print("S references", self.a_s_references)
        print("S init", self.already_stones_init_usages)
        print("S num blinks", self.num_stones_each_time)

        num_blinks_to_do = 75
        for blink in range(num_blinks_to_do+1):  # 25/75
            self.blink = blink
            print("blink", blink)
            self.new_stones = []

            for i, old_stone in enumerate(self.already_stones.copy()):  # self.already_stones: #self.current_stones:
                # print("i, old_stone:", i, old_stone)
                if i >= len(self.a_s_references):
                    self.a_s_references.append([])
                    #self.ref_indexes.append([])
                    num_dig = len(str(old_stone))
                    if old_stone == 0:
                        self.process_stone(i, old_stone, 1)
                    elif num_dig % 2 == 0:
                        half_dig = num_dig // int(2)
                        stone_str = str(old_stone)
                        stone_1_str = stone_str[:half_dig]
                        stone_2_str = stone_str[half_dig:]

                        self.process_stone(i, old_stone, int(stone_1_str))
                        self.process_stone(i, old_stone, int(stone_2_str))
                    else:
                        self.process_stone(i, old_stone, 2024 * old_stone)

        print("already stones:", self.already_stones)
        print("refs:", self.a_s_references)

        already_stones_processed = self.already_stones[:len(self.a_s_references)]
        print("already stones processed:", already_stones_processed)

        blink_n_end_stone_lens = [] # filled for blink 1 already, blink 0 (before blinking) would just be all 1s

        for i in range(len(self.a_s_references)):
            ref_nums = self.a_s_references[i]
            future_ref_indexes = []
            for j in range(len(ref_nums)):
                ref_num = ref_nums[j][0]
                index = self.already_stones.index(ref_num)
                future_ref_indexes.append(index)
            self.ref_indexes.append(future_ref_indexes)
            blink_n_end_stone_lens.append(len(ref_nums))

        print("ref indexes:", self.ref_indexes)

        small_len = len(self.ref_indexes)
        big_len = len(self.already_stones)
        extra_len = len(self.already_stones) - len(self.ref_indexes)
        for i in range(extra_len):
            self.ref_indexes.append([small_len])
            blink_n_end_stone_lens.append(0)

        print("ref indexes processed:", self.ref_indexes)
        print("blink_n_end_stone_lens n=1 processed", blink_n_end_stone_lens)

        for blink in range(2, num_blinks_to_do+1):
            new_blink_n_end_stone_lens = [0] * big_len
            for i in range(big_len):
                new_num = 0
                refs = self.ref_indexes[i]
                for ref in refs:
                    #print("blink_n_end_stone_lens[ref]", blink_n_end_stone_lens[ref])
                    new_num += blink_n_end_stone_lens[ref]
                new_blink_n_end_stone_lens[i] = new_num
            blink_n_end_stone_lens = new_blink_n_end_stone_lens.copy()
            print("blink_n_end_stone_lens for blink", blink, " is:", blink_n_end_stone_lens)

        self.num_stones = 0
        for i in range(self.orig_num_stones):
            self.num_stones += blink_n_end_stone_lens[i]

        print("num stones:", self.num_stones)

    def process_stones(self):
        print("S already stones", self.already_stones)
        print("S references", self.a_s_references)
        print("S init", self.already_stones_init_usages)
        print("S num blinks", self.num_stones_each_time)

        num_blinks_to_do = 25
        for blink in range(num_blinks_to_do): # 25/75
            self.blink = blink
            print("blink", blink)
            self.new_stones = []
            #self.already_stones_checked = [False] * len(self.already_stones)
            #self.adds = [0] * len(self.already_stones)

            for i, old_stone in enumerate(self.already_stones.copy()): # self.already_stones: #self.current_stones:
                #print("i, old_stone:", i, old_stone)
                if i >= len(self.a_s_references):
                    self.a_s_references.append([])
                    num_dig = len(str(old_stone))
                    if old_stone == 0:
                        #self.new_stones.append(1)
                        self.process_stone(i, old_stone, 1)

                    elif num_dig % 2 == 0:
                        half_dig = num_dig // int(2)
                        stone_str = str(old_stone)
                        stone_1_str = stone_str[:half_dig]
                        stone_2_str = stone_str[half_dig:]
                        # print(stone_1_str, stone_2_str)

                        #self.new_stones.append(int(stone_1_str))
                        #self.new_stones.append(int(stone_2_str))
                        self.process_stone(i, old_stone, int(stone_1_str))
                        self.process_stone(i, old_stone, int(stone_2_str))

                        #print("?", i, self.adds, self.already_stones)
                        #self.adds[i] = 1
                    else:
                        #self.new_stones.append(2024 * old_stone)
                        self.process_stone(i, old_stone, 2024 * old_stone)

            #print("references", self.a_s_references)
            #print("adds_before", self.adds)
            #print("num blinks before", self.num_stones_each_time)

            num_stones_each_time_copy = deepcopy(self.num_stones_each_time)
            wait_to_add = []

            # Add to adds in old stones
            for i in range(len(self.a_s_references)-1, -1, -1):
                #references = self.a_s_references[i]
                references = self.a_s_references[i]
                #print("refs:", references)
                to_add = 0
                for reference in references:
                    index = self.already_stones.index(reference[0])
                    diff = reference[1]

                    '''
                    if index >= len(self.a_s_references):
                        break
                        #to_add += 1
                    else:
                        to_add += self.adds[index]
                    '''
                    # Not always [-1], see note in notebook; this is what init is for...
                    #print("diff:", diff, index, reference,  self.num_stones_each_time[index])

                    #print("diff:", diff, index, self.already_stones[index], self.num_stones_each_time[index], self.num_stones_each_time[index][-diff])
                    #print("+num stones each time", self.num_stones_each_time)

                    #to_add += self.num_stones_each_time[index][-1]
                    #continue

                    if diff == 0:
                        #to_add += self.num_stones_each_time[index][-1]
                        to_add += num_stones_each_time_copy[index][-1]
                    elif diff == 1:
                        #print("*diff*:", diff, index, self.already_stones[index], self.num_stones_each_time[index][-diff])
                        #um = self.num_stones_each_time[index]

                        #print("^diff:", diff, index, self.already_stones[index], self.num_stones_each_time[index], self.num_stones_each_time[index][-diff])
                        #print("^already stones", self.already_stones)
                        #print("^references", self.a_s_references)
                        #print("^init", self.already_stones_init_usages)
                        #print("^num blinks", self.num_stones_each_time)

                        if len(self.num_stones_each_time[index]) == 1:
                            wait_to_add.append([i, index])
                        else:
                            to_add += self.num_stones_each_time[index][-2]
                        # true: 172484; [index][-1]: 162160; just += 1: 162160
                        '''
                        if len(self.num_stones_each_time[index]) == 1:
                            #to_add += self.num_stones_each_time[index][-1]
                            to_add += 1
                        else:
                            to_add += self.num_stones_each_time[index][-2]
                        '''
                    else:
                        #print("diff:", diff, index, self.already_stones[index], self.num_stones_each_time[index][-diff] )
                        #to_add += self.num_stones_each_time[index][-diff]
                        #to_add += self.num_stones_each_time[index][-1-diff]
                        #to_add += num_stones_each_time_copy[index][-1-diff]
                        to_add += num_stones_each_time_copy[index][-diff]

                        '''
                        if diff >= len(self.num_stones_each_time[index]):
                            to_add += 1
                        else:
                            to_add += self.num_stones_each_time[index][-diff-1] # but why the if/else???
                        '''
                    #print("self.num_stones_each_time[index]", self.num_stones_each_time[index], self.num_stones_each_time[index][diff-1])
                #self.adds[i] = to_add

                #self.num_stones_each_time[i].append(to_add)
                num_stones_each_time_copy[i].append(to_add)

            # Fill wait_to_add:
            for i in range(len(wait_to_add)):
                to_add_data = wait_to_add[i]
                #num_stones_each_time_copy[to_add_data[0]].append() no append since it's already there, the number just didnt go through (and is 0 or (other ref value))
                print("!!!!", to_add_data, "...", num_stones_each_time_copy)
                num_stones_each_time_copy[to_add_data[0]][-1] += num_stones_each_time_copy[to_add_data[1]][-2]


            self.num_stones_each_time = deepcopy(num_stones_each_time_copy)


            '''
            for i in range(len(self.adds)):
                # self.already_stones_blinks: num stones over times
                #print("a",self.already_stones_blinks, self.adds, i)
                #print("b",self.already_stones_blinks[i][-1], self.adds[i])

                num_stones_from_here = self.already_stones_blinks[i][-1] + self.adds[i]
                self.already_stones_blinks[i].append(num_stones_from_here)
            '''

            #self.current_stones = self.new_stones
            #print(blink, self.current_stones)
            #print("adds", self.adds)

            print("already stones", self.already_stones)
            print("references", self.a_s_references)
            print("init", self.already_stones_init_usages)
            print("num blinks", self.num_stones_each_time)

            self.count_num_stones() # comment out in the end to save some processing time
            print("----------------------------------")

        #self.num_stones = len(self.current_stones)
        #self.num_stones = self.num_stones_each_time[0][-1]
        self.count_num_stones()
        # 125&17: already stones [125, 17, 253000, 1, 7, 253, 0, 2024, 14168, 512072, 20, 24, 28676032, 512, 72, 2, 4, 2867, 6032, 1036288, 4048, 8096, 28, 67, 60,
        # 32, 2097446912, 40, 48, 80, 96, 8, 6, 3]
        # num blinks both [[1, 1, 2, 2, 3, 5, 8], [1, 2, 2, 3, 6, 8, 15], [1, 2, 2, 3, 5, 8], [1, 1, 2, 4, 4, 7], [1, 1, 1, 2, 4, 8], [1, 1, 2, 3, 4], [1, 1, 1, 2, 4],
        # [1, 2, 4, 4, 7], [1, 1, 2, 4, 8], [1, 2, 3, 4], [1, 2, 2, 3], [1, 2, 2, 4], [1, 2, 4, 8], [1, 1, 1], [1, 2, 3], [1, 1, 2], [1, 1, 2], [1, 2, 4], [1, 2, 4],
        # [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1], [1], [1], [1], [1], [1], [1], [1]]

        # 125: already stones [125, 253000, 253, 0, 512072, 1, 512, 72, 2024, 1036288, 7, 2, 20, 24, 2097446912, 14168, 4048, 4]
        # num blinks first [[1, 1, 2, 2, 3, 5, 7], [1, 2, 2, 3, 5, 7], [1, 1, 2, 3, 3], [1, 1, 1, 2, 4], [1, 2, 3, 3], [1, 1, 2, 4],
        # [1, 1, 1], [1, 2, 2], [1, 2, 4], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1], [1], [1], [1]]

    def count_num_stones(self):
        self.num_stones = 0
        for i in range(self.orig_num_stones):
            self.num_stones += self.num_stones_each_time[i][-1]

        print("num stones:", self.num_stones)

    def output(self):
        self.set_data()
        #print(self.current_stones)

        #self.process_stones()
        self.process_stones2()
        print("Blinks", self.blink)

class Day12:
    def __init__(self):
        self.data = []
        self.regions = [] # [reg1, reg2, ...]-> reg:[coord1, c2, ...]-> coords:[row,col]
        self.region_perimeters = [] # [reg1 perim, reg2 perim, ...]
        self.region_chars = [] # just for seeing chars

        self.region_proto_sides = [] # [[up],[left],[down],[right]] ... [[coord1, coord2, ...],[],[],[]]
        #[([[r,c],[r,c]],[],[],[]), ...]
        self.region_true_sides = [] # [reg1 num sides, reg2 num sides, ...]

        # Full: 140x140
        self.num_rows = 0
        self.num_cols = 0

        self.total_price = 0

    def set_data(self):
        with open("day12.1.txt", "r") as file:
            for line in file:
                self.data.append([])
                for char in line.strip():
                    self.data[-1].append(char)

        self.num_rows = len(self.data)
        self.num_cols = len(self.data[0])

    def get_region_i_of_coords(self, coords):
        #print("CHECK", coords)
        #print("...", self.regions)
        for i, region in enumerate(self.regions):
            for check_coords in region:
                if check_coords == coords:
                    return i
        return -1

    def combine_regions(self, region1_i, region2_i):
        region_i = min(region1_i, region2_i)
        other_region_i = max(region1_i, region2_i)
        other_region = self.regions[other_region_i]
        for coords in other_region:
            self.regions[region_i].append(coords)

        self.region_perimeters[region_i] += self.region_perimeters[other_region_i]

        #print("Proto side combine:", self.region_proto_sides[region_i], "--with--", self.region_proto_sides[other_region_i])
        for proto_side in range(4):
            self.region_proto_sides[region_i][proto_side].extend(self.region_proto_sides[other_region_i][proto_side])
        #print("Proto side combine after:", self.region_proto_sides[region_i])

        self.regions.pop(other_region_i)
        self.region_perimeters.pop(other_region_i)
        self.region_proto_sides.pop(other_region_i)
        self.region_chars.pop(other_region_i)

        return region_i

    def process_data(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                char = self.data[row][col]
                region_up_i = -1
                region_left_i = -1
                current_region_i = -1
                perim_to_add = 0
                proto_side_tracker = []
                if row - 1 >= 0 and self.data[row-1][col] == char: # up
                    region_up_i = self.get_region_i_of_coords([row - 1, col])
                    current_region_i = region_up_i
                    #print("-region_up_i set", region_up_i)
                else:
                    perim_to_add += 1
                    proto_side_tracker.append(0)
                if col - 1 >= 0 and self.data[row][col-1] == char: # left
                    region_left_i = self.get_region_i_of_coords([row, col - 1])
                    current_region_i = region_left_i
                    #print("-region_left_i set", region_left_i)
                else:
                    perim_to_add += 1
                    proto_side_tracker.append(1)
                if row + 1 >= self.num_rows or self.data[row+1][col] != char: # down
                    perim_to_add += 1
                    proto_side_tracker.append(2)
                if col + 1 >= self.num_cols or self.data[row][col+1] != char: # right
                    perim_to_add += 1
                    proto_side_tracker.append(3)

                print("char, current, up, left", char, current_region_i, region_up_i, region_left_i)
                if region_up_i != -1 and region_left_i != -1 and region_up_i != region_left_i: # regions need combining
                    current_region_i = self.combine_regions(region_up_i, region_left_i)
                    self.regions[current_region_i].append([row, col])
                elif current_region_i == -1: # make a new region
                    current_region_i = len(self.regions)
                    self.regions.append([[row, col]])
                    self.region_perimeters.append(0)
                    self.region_chars.append(char)
                    self.region_proto_sides.append([[],[],[],[]])
                    #print("**region and perim added", [row, col])
                else: # combine with top or left region
                    self.regions[current_region_i].append([row, col])

                for proto_side in proto_side_tracker:
                    self.region_proto_sides[current_region_i][proto_side].append([row, col])
                #print("Proto sides:", self.region_proto_sides)

                print("row, col, perim to add:", [row, col], perim_to_add)
                print("-----------------")
                self.region_perimeters[current_region_i] += perim_to_add

        self.calc_true_sides()

    # Remember that left & right sides must be vertically linked
    def calc_true_sides(self):
        num_regions = len(self.regions)
        self.region_true_sides = []
        print("++++++++++++++++")
        for region_i, proto_side_region in enumerate(self.region_proto_sides):
            print("Side Getter - Region fraction:", (region_i+1), "of", num_regions)
            region_sides = 0
            for side_i, side_coords_list in enumerate(proto_side_region): # Runs 4 times, 1 for each side
                list = deepcopy(side_coords_list)
                # List of coords that if parallel and joined have the same side

                num_sides_to_add = 0
                if side_i % 2 == 0: # up/down
                    rows_checked_list = []
                    for i, coords in enumerate(side_coords_list):
                        if coords[0] not in rows_checked_list:
                            #num_sides_to_add += 1
                            rows_checked_list.append(coords[0])
                            cols = [coords[1]]
                            for coords2 in side_coords_list[(i+1):]:
                                if coords2[0] == coords[0]:
                                    cols.append(coords2[1])
                            cols.sort()
                            prev_col = -10
                            #print("row and cols", coords[0], cols)
                            for col in cols:
                                if col > prev_col + 1:
                                    num_sides_to_add += 1
                                prev_col = col
                else: # left/right
                    cols_checked_list = []
                    for i, coords in enumerate(side_coords_list):
                        if coords[1] not in cols_checked_list:
                            cols_checked_list.append((coords[1]))
                            rows = [coords[0]]
                            for coords2 in side_coords_list[(i+1):]:
                                if coords2[1] == coords[1]:
                                    rows.append(coords2[0])
                            rows.sort()
                            prev_row = -10
                            for row in rows:
                                if row > prev_row + 1:
                                    num_sides_to_add += 1
                                prev_row = row
                region_sides += num_sides_to_add
                #print("side type, sides added:", side_i, num_sides_to_add)

            self.region_true_sides.append(region_sides)
            print("Region sides:", region_sides)
            print("++++++++++++++++")

    def get_total_price(self):
        self.total_price = 0
        for i, region in enumerate(self.regions):
            perimeter = self.region_perimeters[i]
            num_sides = self.region_true_sides[i]
            area = len(region)
            #price = perimeter * area
            price = num_sides * area
            print("Char, Perim, Num sides, Area, Price:", self.region_chars[i], perimeter, num_sides, area, price)
            self.total_price += price

    def show_processed_new_grid(self):
        new_grid = []
        for i in range(len(self.data)):
            new_grid.append([])
            for j in range(len(self.data[i])):
                new_grid[i].append('.')
        print(new_grid)
        unicode_int = 65  # starting with 'A'
        for region in self.regions:
            for coord in region:
                #print(coord)
                new_grid[coord[0]][coord[1]] = chr(unicode_int)
            unicode_int += 1
        for row in new_grid:
            print(" ".join(map(str, row)))

    def output(self):
        self.set_data()
        print(self.data)

        self.process_data()
        print("regions:", self.regions)
        print("perimeters:", self.region_perimeters)
        print("chars:", self.region_chars)
        print("proto sides:", self.region_proto_sides)
        print(len(self.regions), len(self.region_perimeters), len(self.region_proto_sides))
        print("true sides:", self.region_true_sides)

        self.get_total_price()
        print("total price:", self.total_price)

        #self.show_processed_new_grid()

class Day13:
    def __init__(self):
        self.games = []

        self.num_prizes = 0
        self.num_tokens = 0

    def set_data(self):
        special = 0
        special = 10000000000000 # 10 trillion
        with open("day13.1.txt", "r") as file:
            phase = 0
            game = [[], [], []]
            int_str = ""
            for line in file:
                #self.games.append([[],[],[]])
                for char in line.strip():
                    #self.games[-1].append(char)
                    #print("char", char, "int_str:", int_str)
                    if char.isdigit():
                        int_str = int_str + char
                    elif int_str != "":
                        num = int(int_str)
                        if phase // 2 == 2:
                            num += special
                        int_str = ""
                        game[phase // 2].append(num)
                        phase += 1
                        if phase == 6:
                            phase = 0
                            self.games.append(game)
                            game = [[], [], []]
                    else:
                        continue
            game[2].append(int(int_str) + special)
            self.games.append(game)
            #print("g", game, int_str)

    def mag(self, vector):
        summ = 0
        for coord in vector:
            summ += coord**2
        return np.sqrt(summ)

    def norm(self, vector):
        mag = self.mag(vector)
        return vector / mag

    def process_data(self):

        for game in self.games:
            a = np.array(game[0])
            b = np.array(game[1])
            prize = np.array(game[2])
            print("a, b, prize", a, b, prize)
            #print(a+b)
            #norm_a = self.norm(a)
            #norm_b = self.norm(b)
            #norm_prize = self.norm(prize)
            #print("Norms:", norm_a, norm_b, norm_prize)

            most_a = min(prize[0] // a[0] + 1, prize[1] // a[1] + 1, 100)
            most_b = min(prize[0] // b[0] + 1, prize[1] // b[1] + 1, 100)
            #print(most_a, most_b)

            prize_locks = []
            for i in range(most_a):
                for j in range(most_b):
                    lin_com = i*a + b*j
                    if lin_com[0] == prize[0] and lin_com[1] == prize[1]:
                        prize_locks.append(3*i+j)

            if len(prize_locks) > 0:
                self.num_tokens += min(prize_locks)
                self.num_prizes += 1

    def process_data_2(self):
        for game in self.games:
            print("------------------------------------")
            a = np.array(game[0])
            b = np.array(game[1])
            prize = np.array(game[2])
            print("a, b, prize", a, b, prize)

            x_a_offset = prize[0] % a[0]
            x_a_times_max = prize[0] // a[0]
            print("offsets_x:", x_a_offset)
            # 22*x = 72+94*y check from y=0-22 (not inclusive), then divide by num times within that range
            # b[0]*x = offset+a[0]*y

            count_x = 0
            valid_a_times_x = -1
            valid_b_times_x = -1
            num_less_tokens_a_gets_for_cycle_x = -1
            num_more_tokens_b_gets_for_cycle_x = -1
            for opp_a_times in range(b[0]):
                offset_formula = x_a_offset+a[0]*opp_a_times
                #print("offset_formula:", offset_formula)
                if offset_formula % b[0] == 0:
                    a_times = x_a_times_max - opp_a_times
                    b_times = offset_formula // b[0]
                    print("a/b times:", a_times, b_times, "FORMULA OUTPUT:", a_times*a[0]+b_times*b[0], opp_a_times)
                    if count_x == 0:
                        valid_a_times_x = a_times
                        valid_b_times_x = b_times
                    count_x += 1
            if valid_a_times_x > -1:
                num_less_tokens_a_gets_for_cycle_x = b[0] // count_x
                num_more_tokens_b_gets_for_cycle_x = num_less_tokens_a_gets_for_cycle_x*a[0] // b[0]
            else:
                continue
            print("VALID a/b times x, num_less/more_tokens_a/b_gets_for_cycle_x:", valid_a_times_x, valid_b_times_x, num_less_tokens_a_gets_for_cycle_x, num_more_tokens_b_gets_for_cycle_x)

            y_a_offset = prize[1] % a[1]
            y_a_times_max = prize[1] // a[1]
            print("offsets_y:", y_a_offset)
            count_y = 0
            valid_a_times_y = -1
            valid_b_times_y = -1
            num_less_tokens_a_gets_for_cycle_y = -1
            num_more_tokens_b_gets_for_cycle_y = -1
            for opp_a_times in range(b[1]):
                offset_formula = y_a_offset + a[1] * opp_a_times
                # print("offset_formula:", offset_formula)
                if offset_formula % b[1] == 0:
                    a_times = y_a_times_max - opp_a_times
                    b_times = offset_formula // b[1]
                    print("a/b times:", a_times, b_times, "FORMULA OUTPUT:", a_times * a[1] + b_times * b[1],
                          opp_a_times)
                    if count_y == 0:
                        valid_a_times_y = a_times
                        valid_b_times_y = b_times
                    count_y += 1
            if valid_a_times_y > -1:
                num_less_tokens_a_gets_for_cycle_y = b[1] // count_y
                num_more_tokens_b_gets_for_cycle_y = num_less_tokens_a_gets_for_cycle_y * a[0] // b[0]
            else:
                continue
            print("VALID a/b times y, num_less/more_tokens_a/b_gets_for_cycle_y:", valid_a_times_y, valid_b_times_y,
                  num_less_tokens_a_gets_for_cycle_y, num_more_tokens_b_gets_for_cycle_y)

            # Check x and y together to see if any toys are possible
            min_a_x = valid_a_times_x % num_less_tokens_a_gets_for_cycle_x
            min_a_y = valid_a_times_y % num_less_tokens_a_gets_for_cycle_y
            gcf = math.gcd(num_less_tokens_a_gets_for_cycle_x, num_less_tokens_a_gets_for_cycle_y)
            a_x_plus = num_less_tokens_a_gets_for_cycle_x // gcf
            a_y_plus = num_less_tokens_a_gets_for_cycle_y // gcf
            min_of_mins = min(min_a_x, min_a_y)
            min_a_x_f = min_a_x
            min_a_y_f = min_a_y

            a_x_list = []
            a_y_list = []

            if min_of_mins == min_a_y:
                while min_a_y_f < min_a_x:
                    min_a_y_f += a_y_plus
            else:
                while min_a_x_f < min_a_y:
                    min_a_x_f += a_x_plus

            a_plus = a_x_plus * a_y_plus
            a_x_list_max = min_a_x_f + a_plus
            a_y_list_max = min_a_y_f + a_plus
            #a_x_list = list(range(min_a_x_f, a_y_plus, a_x_plus))
            a_x_list = list(range(min_a_x_f, a_x_list_max, a_x_plus))
            #a_y_list = list(range(min_a_y_f, a_x_plus, a_y_plus))
            a_y_list = list(range(min_a_y_f, a_y_list_max, a_y_plus))
            print(a_x_list)
            print(a_y_list)

            common_nums_set = set(a_x_list) & set(a_y_list)
            if not common_nums_set:
                continue
            truer_min_a = list(common_nums_set)[0]
            print("SET / COMMON NUMS:", common_nums_set, truer_min_a, "+ n *", a_plus)

            # True a is on the line (truer_min_a+a_plus*n), where n is an integer >= 0



        print("------------------------------------")

    def convert_if_close_to_int(self, value):
        tolerance = 1e-2
        # Check if the float is within the tolerance of its rounded integer
        if abs(value - round(value)) <= tolerance:
            return int(round(value))  # Convert to int
        return -1  # Return as is if not close

    def process_data_3(self):
        self.num_prizes = 0
        self.num_tokens = 0
        for game in self.games:
            print("-----------------------------")
            a = np.array(game[0])
            b = np.array(game[1])
            prize = np.array(game[2])
            print("a, b, prize", a, b, prize)

            #x_t = (b[0]*prize[1]-b[1]) / (a[1]*b[0]/a[0]-b[1])
            #x_t = (prize[1]-b[1]/b[0]) / (a[1]/a[0] - b[1]/b[0])
            m_a = a[1]/a[0]
            m_b = b[1]/b[0]

            x_t = (-m_b*prize[0] + prize[1]) / (m_a-m_b)
            y_t = x_t * a[1] / a[0]
            print("x/y_t:", x_t, y_t, (-m_b*prize[0] + prize[1]) % (m_a-m_b))
            '''
            if (-m_b*prize[0] + prize[1]) % (m_a-m_b) > 0:
                print("FIRST INT CHECK FAILED")
                continue
            if (x_t*a[1]) % a[0] > 0:
                print("SECOND INT CHECK FAILED")
                continue
            '''
            print("x/y_t:", x_t, y_t)
            x_t = self.convert_if_close_to_int(x_t)
            y_t = self.convert_if_close_to_int(y_t)
            #x_t = int(x_t)
            #y_t = int(y_t)
            if x_t == -1 or y_t == -1:
                print("INT CHECK FAILED")
                continue

            a_presses = x_t//a[0]
            b_presses = (prize[0]-x_t)//b[0]

            combo = a_presses*a + b_presses*b
            if combo[0] != prize[0] or combo[1] != prize[1]:
                print("LAST CHECK FAILED:", combo, prize)
                continue

            print("a/b presses:", a_presses, b_presses)

            num_tokens = 3*a_presses + b_presses
            self.num_tokens += num_tokens
            self.num_prizes += 1

    def output_day13(self):
        self.set_data()
        print(self.games)

        #self.process_data()
        self.process_data_3()
        print("Num prizes, tokens:", self.num_prizes, self.num_tokens)

class Day14:
    def __init__(self):
        self.init_ps = []
        self.init_vs = []

        self.num_rows = 103
        self.num_cols = 101
        #self.num_rows = 7
        #self.num_cols = 11

        # indexes of middle tiles
        self.half_rows = (self.num_rows-1) // 2
        self.half_cols = (self.num_cols-1) // 2

        self.final_ps = []
        self.quads = [0, 0, 0, 0]
        self.safety_factor = 0

    def set_data(self):
        with open("day14.1.txt", "r") as file:
            phase = 0
            current_p = []
            current_v = []
            int_str = ""
            for line in file:
                for char in line.strip():
                    # self.games[-1].append(char)
                    # print("char", char, "int_str:", int_str)
                    if char.isdigit() or char == "-":
                        int_str = int_str + char
                    elif int_str != "":
                        num = int(int_str)
                        int_str = ""
                        if phase // 2 == 0:
                            current_p.append(num)
                        else:
                            current_v.append(num)
                        phase += 1
                        if phase == 4:
                            phase = 0
                            self.init_ps.append(np.array(current_p.copy()))
                            self.init_vs.append(np.array(current_v.copy()))
                            current_p = []
                            current_v = []
                    else:
                        continue
            current_v.append(int(int_str))
            self.init_ps.append(np.array(current_p.copy()))
            self.init_vs.append(np.array(current_v.copy()))

    def process_data(self):
        n = 100
        for i in range(len(self.init_ps)):
            print("---------------------------")
            p = np.array(self.init_ps[i])
            v = np.array(self.init_vs[i])
            print("p, v", p, v)

            full_p_n = p + n*v
            print("full p:", full_p_n)
            final_p_x = full_p_n[0] % self.num_cols
            final_p_y = full_p_n[1] % self.num_rows
            print("final p:", [final_p_x, final_p_y])
            # -6 + 7 = 1; 7*1
            # -18 + 21 = 3; 7*3
            # -18//7 = 2 ->+1 = 3 ->*7 = 21 ->+-18 = 3
            # -7 ->+1 =...                7 ->+-7 = 0

            x_half = 1
            y_half = 1
            if 0 <= final_p_x < self.half_cols:
                x_half = 0
            elif final_p_x == self.half_cols:
                continue
            if 0 <= final_p_y < self.half_rows:
                y_half = 0
            elif final_p_y == self.half_rows:
                continue

            quad_i = x_half + y_half*2
            self.quads[quad_i] += 1
        self.safety_factor = self.quads[0] * self.quads[1] * self.quads[2] * self.quads[3]

    def christmas_tree(self):
        base_grid = [["."] * self.num_cols for _ in range(self.num_rows)]
        #num_iterations = 1
        num_iterations = self.num_rows*self.num_cols
        with open("day14.o2.txt", "w") as file:
            current_ps = deepcopy(self.init_ps)
            for second in range(1,num_iterations+1):

                grid = deepcopy(base_grid)


                # update step
                for i in range(len(self.init_ps)):
                    current_ps_unmodded = current_ps[i] + self.init_vs[i]
                    #print(current_ps_unmodded[0] % self.num_cols)
                    current_ps[i][0] = col = current_ps_unmodded[0] % self.num_cols
                    current_ps[i][1] = row = current_ps_unmodded[1] % self.num_rows

                    # fill grid
                    if second % 101 != 99:
                        continue
                    if grid[row][col] == "#":
                        grid[row][col] = "@"
                    elif grid[row][col] == ".":
                        grid[row][col] = "#"

                if second % 101 != 99:
                    continue
                file.write(str(second) + ":\n")
                for row in grid:
                    line = "".join(row)
                    file.write(line + "\n")
                file.write("------\n")

    def christmas_tree_2(self):
        # Dimensions of the image
        num_pixel_rows = self.num_rows*(self.num_rows+1)-1
        num_pixel_cols = self.num_cols*(self.num_cols+1)-1

        # Create a blank image (white background)
        image = Image.new("RGB", (num_pixel_cols, num_pixel_rows), "black")  # "RGB" mode and black background

        red = (255, 0, 0)
        green = (0, 255, 0)
        gold = (255, 215, 0)
        black = (0,0,0)

        nums = [
            []
        ]

        # Load the pixel map for editing
        pixels = image.load()

        # Make dividers
        for i in range(1,self.num_rows): # Horizontal divider lines
            pixel_row = (self.num_rows+1)*i-1
            for j in range(num_pixel_cols):
                pixels[j, pixel_row] = red
        for i in range(1,self.num_cols): # Vertical divider lines
            pixel_col = (self.num_cols+1)*i-1
            for j in range(num_pixel_rows):
                pixels[pixel_col, j] = red

        #num_iterations = 200
        num_iterations = self.num_rows * self.num_cols
        print("full num iterations:", num_iterations)
        base_grid = [[black] * self.num_cols for _ in range(self.num_rows)]
        current_ps = deepcopy(self.init_ps)
        for second in range(1, num_iterations + 1):
            if second % 500 == 0:
                print("on second", second)
            iter_i = second - 1

            grid = deepcopy(base_grid)

            # update step
            for i in range(len(self.init_ps)):
                current_ps_unmodded = current_ps[i] + self.init_vs[i]
                # print(current_ps_unmodded[0] % self.num_cols)
                current_ps[i][0] = col = current_ps_unmodded[0] % self.num_cols
                current_ps[i][1] = row = current_ps_unmodded[1] % self.num_rows

                # fill grid
                grid[row][col] = green

            pixel_row_offset = (iter_i // self.num_cols)*(self.num_rows+1)
            pixel_col_offset = (iter_i % self.num_cols)*(self.num_cols+1)
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    #if iter_i > 98:
                    #    print(iter_i, row, col, row+pixel_row_offset, col+pixel_col_offset)
                    pixels[col+pixel_col_offset,row+pixel_row_offset] = grid[row][col]
        '''
        99 102 99 102 10197
        99 102 100 102 10198
        100 0 0 0 10200
        100 0 1 0 10201
        ...
        100 102 100 102 10300
        101 0 0 104 10302
        '''

        # Save or display the image
        image.save("all_iterations.png")

    def output(self):
        self.set_data()
        print("init poses:", self.init_ps)
        print("init vs:", self.init_vs)

        #self.process_data()
        #print(self.quads)
        #print(self.safety_factor)

        #self.christmas_tree()
        self.christmas_tree_2()

class Day15:
    def __init__(self):
        self.grid = []
        self.move_inputs = []

        self.robot_p = []

        self.num_rows = 0
        self.num_cols = 0

        self.gps_sum = 0

    def set_data(self):
        grid_fill = True
        with open("day15.1.txt", "r") as file:
            for line in file:
                if grid_fill: # fill grid
                    if line[0] == "\n":
                        grid_fill = False
                        continue
                    self.grid.append([])
                    for char in line.strip():
                        self.grid[-1].append(char)
                        if char == '@':
                            self.robot_p = np.array([len(self.grid)-1, len(self.grid[-1])-1])
                else: # fill inputs
                    for char in line.strip():
                        #self.move_inputs.append(char)
                        input = [0,0] # movement through [row,col]
                        if char == "^":
                            input = [-1,0]
                        if char == ">":
                            input = [0,1]
                        elif char == "v":
                            input = [1,0]
                        elif char == "<":
                            input = [0,-1]
                        input = np.array(input)
                        self.move_inputs.append(input)

        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])

    def process_data(self):
        for input in self.move_inputs:
            can_move = False
            check_pos = self.robot_p + input
            check_pos_list = [self.robot_p, check_pos]
            while True:
                check_pos_char = self.grid[check_pos[0]][check_pos[1]]
                if check_pos_char == ".":
                    can_move = True
                    break
                elif check_pos_char == "#":
                    can_move = False
                    break
                check_pos = check_pos + input
                check_pos_list.append(check_pos)
            #print("Can move & check pos list:", can_move, check_pos_list)

            if can_move:
                self.grid[check_pos_list[0][0]][check_pos_list[0][1]] = '.'
                self.grid[check_pos_list[1][0]][check_pos_list[1][1]] = '@'
                if len(check_pos_list) > 2:
                    self.grid[check_pos_list[-1][0]][check_pos_list[-1][1]] = 'O'
                self.robot_p = check_pos_list[1]

    def find_boxes_gps_sum(self):
        for row, line in enumerate(self.grid):
            for col, char in enumerate(self.grid[row]):
                if char == "O":
                    gps = 100*row + col
                    self.gps_sum += gps

    def output(self):
        self.set_data()
        print("grid:", self.grid)
        #print("inputs:", self.move_inputs)
        print("robot p:", self.robot_p)
        print("num rows and cols:", self.num_rows, self.num_cols)

        self.process_data()
        print(self.grid)

        self.find_boxes_gps_sum()
        print("GPS Sum:", self.gps_sum)

class Day15_2:
    def __init__(self):
        self.grid = []
        self.move_inputs = []

        self.robot_p = []

        self.num_rows = 0
        self.num_cols = 0

        self.gps_sum = 0

    def set_data(self):
        grid_fill = True
        with open("day15.1.txt", "r") as file:
            for line in file:
                if grid_fill: # fill grid
                    if line[0] == "\n":
                        grid_fill = False
                        continue
                    self.grid.append([])
                    for char in line.strip():
                        #self.grid[-1].append(char)
                        if char == "#":
                            self.grid[-1].extend(['#','#'])
                        elif char == ".":
                            self.grid[-1].extend(['.','.'])
                        elif char == "O":
                            self.grid[-1].extend(['[', ']'])
                        if char == '@':
                            self.grid[-1].extend(['@','.'])
                            self.robot_p = np.array([len(self.grid)-1, len(self.grid[-1])-2])
                else: # fill inputs
                    for char in line.strip():
                        #self.move_inputs.append(char)
                        input = [0,0] # movement through [row,col]
                        if char == "^":
                            input = [-1,0]
                        if char == ">":
                            input = [0,1]
                        elif char == "v":
                            input = [1,0]
                        elif char == "<":
                            input = [0,-1]
                        input = np.array(input)
                        self.move_inputs.append(input)

        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])


    def process_data(self):
        for input in self.move_inputs:
            #for row in self.grid:
                #print(" ".join(map(str, row)))
            #print("input:", input)
            horiz = False
            if input[0] == 0:
                horiz = True

            check_pos = self.robot_p + input
            check_pos_char = self.grid[check_pos[0]][check_pos[1]]
            if check_pos_char == '#':
                continue

            if horiz or check_pos_char == '.':
                can_move = False
                check_pos_list = [self.robot_p, check_pos]
                while True:
                    check_pos_char = self.grid[check_pos[0]][check_pos[1]]
                    if check_pos_char == ".":
                        can_move = True
                        break
                    elif check_pos_char == "#":
                        can_move = False
                        break
                    check_pos = check_pos + input
                    check_pos_list.append(check_pos)
                #print("Can move & check pos list:", can_move, check_pos_list)

                if can_move: # horizontal
                    #print(check_pos_list, check_pos_list[0][0], check_pos_list[0][1])
                    #print(self.grid)
                    #print(self.grid[check_pos_list[0][0]][check_pos_list[0][1]])
                    self.grid[check_pos_list[0][0]][check_pos_list[0][1]] = '.'
                    self.grid[check_pos_list[1][0]][check_pos_list[1][1]] = '@'
                    if len(check_pos_list) > 2:
                        #self.grid[check_pos_list[-1][0]][check_pos_list[-1][1]] = 'O'
                        #print("HORIZ FILL")
                        chars_to_fill = []
                        last_char = '&'
                        for i, checked_pos in enumerate(check_pos_list[2:]):
                            char = self.grid[checked_pos[0]][checked_pos[1]]
                            #print("char:", char)
                            if char == '[':
                                #self.grid[checked_pos[0]][checked_pos[1]] = ']'
                                chars_to_fill.append(']')
                            elif char == ']':
                                #self.grid[checked_pos[0]][checked_pos[1]] = '['
                                chars_to_fill.append('[')
                            else:
                                chars_to_fill.append(last_char)
                            last_char = char
                        for i, checked_pos in enumerate(check_pos_list[2:]):
                            self.grid[checked_pos[0]][checked_pos[1]] = chars_to_fill[i]

                    self.robot_p = check_pos_list[1]
            else: # if vertical and moving boxes in any way
                #print("VERTICAL PUSHING ON BOXES, may or may not move")
                wall_hit = False
                box_rows = [[self.robot_p]] # 0th box row make robot
                box_row = []
                wide_box = self.get_wide_box(check_pos)
                box_row.extend(wide_box)
                box_rows.append(box_row)
                #print("init box rows:", box_rows)

                more_boxes = True
                while (more_boxes and not wall_hit):
                    more_boxes = False
                    next_box_row = []
                    for box_pos in box_row:
                        next_pos = box_pos + input
                        next_pos_char = self.grid[next_pos[0]][next_pos[1]]
                        if next_pos_char == '#':
                            wall_hit = True
                            break
                        elif next_pos_char != '.':
                            more_boxes = True
                            wide_box = self.get_wide_box(next_pos)
                            #print("...", wide_box, (next_box_row), (next_pos))
                            #if list(next_pos) not in list(next_box_row):
                            in_next_box_row = False
                            for box_pos_try in next_box_row:
                                if box_pos_try[0] == next_pos[0] and box_pos_try[1] == next_pos[1]:
                                    in_next_box_row = True
                                    break
                            #if any(np.array_equal(next_pos, arr) for arr in next_box_row):
                            if not in_next_box_row:
                                #print("HERE")
                                next_box_row.extend(wide_box)
                    if len(next_box_row) == 0 or wall_hit:
                        break
                    box_row = deepcopy(next_box_row)
                    #print("next box row:", next_box_row)
                    box_rows.append(box_row)
                #print("all box rows:", box_rows)

                if not wall_hit: # can move
                    # fill in each (box plot + input) with (box plot's char)
                    # Also, if (box plot - input) is not in (next box_row), then fill (box_plot) with '.'
                    self.robot_p = self.robot_p + input
                    for i in range(len(box_rows)-1, -1, -1):
                        box_row = box_rows[i]
                        prev_box_row = []
                        if i > 0:
                            prev_box_row = box_rows[i-1]
                        for box_pos in box_row:
                            new_box_pos = box_pos + input
                            char = self.grid[box_pos[0]][box_pos[1]]
                            self.grid[new_box_pos[0]][new_box_pos[1]] = char

                            opp_box_pos = box_pos - input
                            opp_box_pos_incl = False
                            for box_pos_try in prev_box_row:
                                if box_pos_try[0] == opp_box_pos[0] and box_pos_try[1] == opp_box_pos[1]:
                                    opp_box_pos_incl = True
                                    break
                            if not opp_box_pos_incl:
                                self.grid[box_pos[0]][box_pos[1]] = '.'


    def get_wide_box(self, check_pos):
        check_pos_char = self.grid[check_pos[0]][check_pos[1]]
        wide_box = [check_pos]
        if check_pos_char == ']':
            wide_box.append(check_pos + np.array([0, -1]))
        else:
            wide_box.append(check_pos + np.array([0, 1]))

        return wide_box

    def find_boxes_gps_sum(self):
        for row, line in enumerate(self.grid):
            for col, char in enumerate(self.grid[row]):
                if char == "[":
                    gps = 100*row + col
                    self.gps_sum += gps

    def output(self):
        self.set_data()
        #print("grid:", self.grid)
        for row in self.grid:
            print(" ".join(map(str, row)))
        #print("inputs:", self.move_inputs)
        print("robot p:", self.robot_p)
        print("num rows and cols:", self.num_rows, self.num_cols)

        self.process_data()
        #print(self.grid)
        for row in self.grid:
            print(" ".join(map(str, row)))

        self.find_boxes_gps_sum()
        print("GPS Sum:", self.gps_sum)

#day11 = Day11()
#day11.output()
#day12 = Day12()
#day12.output()
#day13 = Day13()
#day13.output_day13()
day14 = Day14(); day14.output()
#day15 = Day15_2(); day15.output()
