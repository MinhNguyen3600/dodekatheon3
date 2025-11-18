my_list = [10, 20, 30, 40, 50, 20]

# Find the index of the first occurrence of 30
index_of_30 = my_list.index(30)
print(f"The index of 30 is: {index_of_30}; Type: {type(index_of_30)}")

# Find the index of the first occurrence of 20
index_of_20 = my_list.index(20)
print(f"The index of 20 is: {index_of_20}; Type: {type(index_of_20)}")

# You can also specify a start and end index for the search
# Find the index of 20, starting the search from index 2
index_of_20_after_index_1 = my_list.index(20, 2)
print(f"The index of 20 (starting from index 2) is: {index_of_20_after_index_1}; Type: {type(index_of_20_after_index_1)}")