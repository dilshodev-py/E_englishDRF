#  task 1
# from collections import deque
#
# a = input("a:")
# b = input("b:")
#
# if not a.isdigit() or not b.isdigit():
#     raise Exception('please enter only number')
#
# a_list = []
# b_list = []
#
# for i in range(len(a)):
#     a_list.append(a[i])
#
# for i in range(len(b)):
#     b_list.append(b[i])
#
# length = min(len(a_list), len(b_list))
#
# my_list = deque([])
#
# len_a = len(a_list)
# len_b = len(b_list)
#
# for i in range(length):
#     my_list.appendleft(int(a_list[len_a - i - 1]) + int(b_list[len_b - i - 1]))
#     a_list.pop()
#     b_list.pop()
#
# if a_list:
#     length = len(a_list)
#     for i in range(length):
#         my_list.appendleft(int(a_list[length - i - 1]))
#         a_list.pop(length - i - 1)
# if b_list:
#     length = len(b_list)
#     for i in range(length):
#         my_list.appendleft(int(b_list[length - i - 1]))
#         b_list.pop()
#
# len_my_list = len(my_list)
# result = ''
#
# for i in range(1, len_my_list):
#     if my_list[len_my_list - i] > 9:
#         my_list[len_my_list - i - 1] += 1
#         my_list[len_my_list - i] -= 10
#
#
# for i in my_list:
#     result += str(i)
#
#
#
# print(result)


# task 2
"""
I = 1
II = 2
III = 3
IV = 4
V = 5
VI = 6
IX = 9
X = 10
L = 50
C = 100
D = 500
M = 1000
"""

# task 2
# a = input('a:')
#
# my_dict = {
#     'M': 1000,
#     'D': 500,
#     'C': 100,
#     'L': 50,
#     'X': 10,
#     'V': 5,
#     'I': 1
# }
#
# my_list = []
#
# for i in range(len(a)):
#     if not a[i] in my_dict.keys():
#         raise Exception(f"Choices are: {my_dict.keys()}")
#     my_list.append(a[i])
#
# result = 0
#
# length = len(my_list)
#
# if length == 1:
#     result = my_dict[my_list[0]]
# else:
#     for i in range(1, length + 1):
#         rim = my_list[length - i]
#         n = my_dict[rim]
#         result += n
#         my_list.pop()
#         if not my_list:
#             break
#         if my_dict[my_list[length - i - 1]] < n:
#             result -= my_dict[my_list[length - i - 1]]
#             my_list.pop()
#             length -= 1
#             continue
#
# print(result)
