from xmlrpc.client import FastParser

import numpy as np
from numpy.core.defchararray import index


class Day1:
    def __init__(self):
        self.list1 = []
        self.list2 = []
        self.totalDistance = 0
        self.similarityScore = 0

    def getLists(self):
        with open("day1.1.txt", "r") as file:
            for line in file:
                # Split each line into columns
                col1, col2 = line.strip().split()
                # Append to respective lists
                self.list1.append(int(col1))
                self.list2.append(int(col2))

        # Test values
        #self.list1 = [5, 4, 3, 2, 1]
        #self.list2 = [12, 15, 4, 25, 1]

    def compareMins(self):
        l1 = self.list1.copy()
        l2 = self.list2.copy()

        while len(l1) > 0:
            min1 = min(l1)
            min2 = min(l2)

            distance = abs(min2-min1)
            self.totalDistance += distance

            l1.remove(min1)
            l2.remove(min2)

    def setSimilarityScore(self):
        for list1Val in self.list1:
            num_times_in_list2 = self.list2.count(list1Val)
            self.similarityScore += list1Val * num_times_in_list2

    def output_day1(self):
        self.getLists()

        self.compareMins()
        print(self.totalDistance)

        self.setSimilarityScore()
        print(self.similarityScore)

class Day2:
    def __init__(self):
        self.levels_list = []
        self.num_safe_reports = 0

    def setLevels(self):
        with open("day2.1.txt", "r") as file:
            for line in file:
                levels_strs = line.split()
                levels = []
                for level_str in levels_strs:
                    levels.append(int(level_str))
                self.levels_list.append(levels)

    def get_report_safety(self, levels):
        inc_or_dec = ""
        if levels[0] < levels[1]:
            inc_or_dec = "inc"
        elif levels[0] > levels[1]:
            inc_or_dec = "dec"
        else:
            return False

        # print(len(levels), levels, inc_or_dec)
        for i in range(1, len(levels)):
            # print("test", levels[i-1], levels[i])

            if (not levels[i - 1] < levels[i]) and inc_or_dec == "inc":
                return False
            elif (not levels[i - 1] > levels[i]) and inc_or_dec == "dec":
                return False

            diff = abs(levels[i - 1] - levels[i])
            if diff > 3 or diff < 1:
                return False

        return True

    def set_num_safe_reports(self):
        for report_levels in self.levels_list:
            safe = self.get_report_safety(report_levels)

            if safe:
                self.num_safe_reports += 1
            else:
                for i in range(len(report_levels)):
                    dampener_levels = report_levels.copy()
                    dampener_levels.pop(i)

                    safe = self.get_report_safety(dampener_levels)
                    if safe:
                        self.num_safe_reports += 1
                        break

    def output_day2(self):
        self.setLevels()
        print(self.levels_list)

        self.set_num_safe_reports()
        print(self.num_safe_reports)

class Day3:
    def __init__(self):
        self.added_muls = 0
        self.full_data = ""

    def read_data(self):
        with open("day3.1.txt", "r") as file:
            for line in file:
                self.full_data += line.strip()

    def process_data(self):
        non_corr_index = 0
        non_corr_index_2 = 0
        #non_corr_index_3 = 0

        index_chars = "mul(-,-)"
        index_chars_2 = "do()"
        index_chars_3 = "don't()"
        num1 = 0
        num2 = 0

        num = 0
        digit = 1

        instr_enabled = True

        for char in self.full_data:
            #print(char, non_corr_index_2)
            # Check do() and don't()
            if char == "d":
                non_corr_index_2 = 1
                non_corr_index = 0
                digit = 1
                continue
            if non_corr_index_2 > 0:
                if char != index_chars_3[non_corr_index_2] and (non_corr_index_2 >= len(index_chars_2) or char != index_chars_2[non_corr_index_2]):
                    non_corr_index_2 = 0
                    continue

                #print("hi")
                non_corr_index_2 += 1
                if char == ")" and non_corr_index_2 == 4:
                    non_corr_index_2 = 0
                    instr_enabled = True
                elif char == ")" and non_corr_index_2 == 7:
                    non_corr_index_2 = 0
                    instr_enabled = False

                continue

            # do not do regular instructions if disabled
            if not instr_enabled:
                continue

            #Regular check, part 1
            if char.isdigit():
                if non_corr_index == 4 or non_corr_index == 6: # number calcs
                    if digit == 1:
                        digit += 1
                        num = int(char)
                    elif digit == 2 or digit == 3:
                        digit += 1
                        num = num*10 + int(char)
                    elif digit == 4:
                        digit = 1
                        non_corr_index = 0
                else:
                    non_corr_index = 0
                    digit = 1

                continue
            elif non_corr_index == 4:
                if digit == 1:
                    non_corr_index = 0
                    continue
                num1 = num
                non_corr_index += 1
            elif non_corr_index == 6:
                if digit == 1:
                    non_corr_index = 0
                    continue
                num2 = num
                non_corr_index += 1

            if non_corr_index != 4 and non_corr_index != 6: # not the numbers
                #print ("not num")
                if char != index_chars[non_corr_index]:
                    non_corr_index = 0
                    continue
                else:
                    non_corr_index += 1
                    digit = 1
                    if non_corr_index == 8:
                        # multiply the numbers
                        mult = num1 * num2
                        self.added_muls += mult

                        non_corr_index = 0
                    else:
                        continue

    def output_day3(self):
        self.read_data()
        print(self.full_data)

        self.process_data()
        print(self.added_muls)

class Day4:
    def __init__(self):
        self.grid = []
        self.word = "XMAS"
        self.word_2 = "MAS"
        self.word_len = len(self.word)

        self.num_words = 0
        self.num_crosses = 0
        self.m_s = 0

    def setGrid(self):
        with open("day4.1.txt", "r") as file:
            for line in file:
                self.grid.append(line.strip())

    def count_if_word_here(self, start_row, start_col, dir_x, dir_y):
        for i in range(self.word_len):
            if self.word[i] == self.grid[start_row - i*dir_y][start_col + i*dir_x]:
                continue
            else:
                return

        self.num_words += 1

    def countWords(self):
        num_rows = len(self.grid) # num rows
        num_cols = len(self.grid[0]) # num cols
        print("Maxes:", num_rows, num_cols)

        row = 0
        for line in self.grid:
            col = 0
            for char in line:
                #print(row, col)
                if char == "X":
                    #print("X is here")
                    good_left = col >= 3
                    good_right = col <= num_cols - 4
                    good_up = row >= 3
                    good_down = row <= num_rows - 4

                    if good_right:
                        self.count_if_word_here(row, col, 1, 0)
                        if good_up:
                            self.count_if_word_here(row, col, 1, 1)
                        if good_down:
                            self.count_if_word_here(row, col, 1, -1)
                    if good_left:
                        self.count_if_word_here(row, col, -1, 0)
                        if good_up:
                            self.count_if_word_here(row, col, -1, 1)
                        if good_down:
                            self.count_if_word_here(row, col, -1, -1)
                    if good_up:
                        self.count_if_word_here(row, col, 0, 1)
                    if good_down:
                        self.count_if_word_here(row, col, 0, -1)
                col += 1
            row += 1

    def count_if_cross_mas_here(self, start_row, start_col, dir_x, dir_y):
        r_mid, c_mid = start_row - dir_y, start_col + dir_x
        r_far, c_far = start_row - 2*dir_y, start_col + 2*dir_x
        r_x, c_x = start_row - 2*dir_y, start_col + dir_x
        r_y, c_y = start_row - dir_y, start_col + 2 * dir_x
        #print(r_mid, c_mid, r_far, c_far, r_x, c_x, r_y, c_y)
        if self.word_2[1] == self.grid[start_row - dir_y][start_col + dir_x] and\
            self.word_2[2] == self.grid[start_row - 2*dir_y][start_col + 2*dir_x] and \
                ((self.word_2[0] == self.grid[start_row][start_col + 2*dir_x] and self.word_2[2] == self.grid[start_row - 2*dir_y][start_col]) or\
                (self.word_2[2] == self.grid[start_row][start_col + 2 * dir_x] and self.word_2[0] == self.grid[start_row - 2 * dir_y][start_col])):
            self.num_crosses += 1
            #print("Cross mas here:", start_row, start_col, dir_x, dir_y)

    def count_cross_mases(self):
        num_rows = len(self.grid)  # num rows
        num_cols = len(self.grid[0])  # num cols
        print("Maxes:", num_rows, num_cols)

        row = 0
        for line in self.grid:
            col = 0
            for char in line:
                # print(row, col)
                if char == "M":
                    self.m_s += 1
                    # print("X is here")
                    good_left = col >= 2
                    good_right = col <= num_cols - 3
                    good_up = row >= 2
                    good_down = row <= num_rows - 3

                    if good_right:
                        if good_up:
                            self.count_if_cross_mas_here(row, col, 1, 1)
                        if good_down:
                            self.count_if_cross_mas_here(row, col, 1, -1)
                    if good_left:
                        if good_up:
                            self.count_if_cross_mas_here(row, col, -1, 1)
                        if good_down:
                            self.count_if_cross_mas_here(row, col, -1, -1)
                col += 1
            row += 1

        self.num_crosses /= 2

    def output_day4(self):
        self.setGrid()
        print(self.grid)

        self.countWords()
        print(self.num_words)

        self.count_cross_mases()
        print("Num crosses:", self.num_crosses)
        #print(self.m_s)

class Day5:
    def __init__(self):
        self.page_ordering_rules = []
        self.updates = []

        self.mid_sum_correct = 0
        self.mid_sum_corrected = 0

    def setGrid(self):
        with open("day5.1.txt", "r") as file:
            for line in file:
                line_str = line.split("|")
                line_nums = []
                for i in range(len(line_str)):
                    line_nums.append(int(line_str[i]))

                self.page_ordering_rules.append(line_nums)

        with open("day5.2.txt", "r") as file:
            for line in file:
                line_str = line.split(",")
                line_nums = []
                for i in range(len(line_str)):
                    line_nums.append(int(line_str[i]))

                self.updates.append(line_nums)

    def set_mid_sum_of_correct_updates(self):
        d=0
        for update in self.updates:
            correct_update = True

            altered_indexes = []
            before_nums = []
            corrections = [0]*len(update)
            for i, num1 in enumerate(update):
                #if i in altered_indexes:
                #continue
                other_page_nums = update.copy()[(i+1):]
                for page_order_rule in self.page_ordering_rules:
                    if page_order_rule[1] == num1:
                        for j, num2 in enumerate(other_page_nums):
                            k=i+j+1
                            if num2 == page_order_rule[0]:
                                correct_update = False
                                altered_indexes.append(k)
                                before_nums.append(num1)

                                corrections[i] = corrections[i] + 1
                                corrections[k] = corrections[k] - 1

                                if d < 5:
                                    print(num1, num2, k)
                        if not correct_update:
                            b=0
                if not correct_update:
                    c=0
            if correct_update:
                mid_index = (len(update) - 1) // int(2)
                mid_num = update[mid_index]
                self.mid_sum_correct += mid_num
            else:
                altered_update = update.copy()
                '''fix here'''
                '''
                for i, index in enumerate(altered_indexes):
                    left_num = update[index]
                    right_num = before_nums[i]
                    right_num_index = altered_update.index(right_num)

                    altered_update.remove(left_num)
                    altered_update.insert(right_num_index, left_num)
                '''
                '''to here; use debug statements in first few corrections to help'''
                # NEW:
                altered_update = [0]*len(update)
                for i in range(len(update)):
                    altered_update[corrections[i]+i] = update[i]

                # correct: 72 85 94 79 83
                '''
                79 72 1
                79 94 2
                79 85 4
                94 85 4
                83 85 4
                '''
                '''The trick is that each time the number is displayed on the left, its index should be to the right one, and vice versa; sometimes they cancel out too'''
                mid_index = (len(altered_update) - 1) // int(2)
                mid_num = altered_update[mid_index]
                self.mid_sum_corrected += mid_num

                if d < 5:
                    print(update, altered_update, mid_num)
                d += 1



    def output_day5(self):
        self.setGrid()
        print(self.page_ordering_rules)
        print(self.updates)

        self.set_mid_sum_of_correct_updates()
        print(self.mid_sum_correct)
        print(self.mid_sum_corrected)

day2 = Day2(); day2.output_day2()
#day4 = Day4()
#day4.output_day4()
day5 = Day5(); day5.output_day5()