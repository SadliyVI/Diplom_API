my_list = [(457239033, {'likes': 10, 'date': 1732181155, 'height': 765,
            'width': 510, 'size_type': 'r'}),
           (457239032, {'likes': 10, 'date': 1732179359, 'height': 629,
            'width': 510, 'size_type': 'r'}),
           (457239027, {'likes': 6, 'date': 1732178950, 'height': 500,
            'width': 500, 'size_type': 'r'}),
           (457239029, {'likes': 0, 'date': 1732179186, 'height': 382,
            'width': 510, 'size_type': 'r'}),
           (457239034, {'likes': 12, 'date': 1732181197, 'height': 341,
            'width': 510, 'size_type': 'r'}),
           (457239028, {'likes': 12, 'date': 1732179128, 'height': 340,
            'width': 510, 'size_type': 'r'}),
           (457239030, {'likes': 12, 'date': 1732179279, 'height': 340,
            'width': 510, 'size_type': 'r'}),
           (457239031, {'likes': 7, 'date': 1732179307, 'height': 340,
            'width': 510, 'size_type': 'r'}),
           (457239035, {'likes': 7, 'date': 1732181322, 'height': 340,
            'width': 510, 'size_type': 'r'}),
           (457239036, {'likes': 0, 'date': 1732181353, 'height': 340,
            'width': 510, 'size_type': 'r'})]


def get_equal_likes_index(data_list, number):
    if data_list and number != 0:
        id_list = []
        for i in range(number-1):
            j=i
            while j != number-1:
                if data_list[i][1]['likes'] == data_list[j+1][1]['likes']:
                    if data_list[i][0] not in index_list:
                        index_list.append(data_list[i][0])
                    if data_list[j+1][0] not in index_list:
                        index_list.append(data_list[j+1][0])
                j +=1

    return id_list


list = get_equal_likes_index(my_list, 7)
print(list)