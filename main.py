import time

def read_grid(file_name):
    result = []
    with open("testes/" + file_name, 'r') as file:
        for line in file.readlines():
            result.append(list(line.strip()))
    return result

def read_word_list(file_path):
    result = []
    with open(file_path, 'r') as file:
        for word in file.readlines(10000000):
            result.append(word.replace('\n', ''))
    return result

def log_grid(grid, step, log_file):
    with open(log_file, 'a') as file:
        file.write(f"Step {step}\n")
        for row in grid:
            file.write(''.join(row) + "\n")
        file.write("\n")

def is_valid(grid, word, row, col, direction):
    def check_neighbors(r, c, letter):
        return True
        # neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        # for nr, nc in neighbors:
        #     if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
        #         if grid[nr][nc] not in ('?', letter):
        #             return False
        # return True
    
    spaces_to_fill = 0
    if direction == 'H':
        if col + len(word) > len(grid[0]):
            return False
        
        for i in range(len(word)):
            if (grid[row][col + i] != '?' and grid[row][col + i] != word[i]) or not check_neighbors(row, col + i, word[i]):
                return False
            
        for i in range(col, len(grid[0])):
            if grid[row][i] == '?':
                spaces_to_fill += 1
            else:
                break
        if len(word) != spaces_to_fill:
            return False
    elif direction == 'V':
        if row + len(word) > len(grid):
            return False
        for i in range(len(word)):
            if (grid[row + i][col] != '?'and grid[row + i][col] != word[i]) or not check_neighbors(row + i, col, word[i]):
                return False
        for i in range(row, len(grid)):
            if grid[i][col] != '.':
                spaces_to_fill += 1
            else:
                break
        if len(word) != spaces_to_fill:
            return False
    return True

def place_word(grid, word, row, col, direction):
    new_grid = [r.copy() for r in grid]
    if direction == 'H':
        for i in range(len(word)):
            new_grid[row][col + i] = word[i]
    elif direction == 'V':
        for i in range(len(word)):
            new_grid[row + i][col] = word[i]
    return new_grid

def select_next_cell(grid):
    best_cell = None
    max_options = float('-inf')

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '?':
                horizontal_length = vertical_length = 0

                for i in range(col, len(grid[0])):
                    if grid[row][i] == '?':
                        horizontal_length += 1
                    else:
                        break

                for i in range(row, len(grid)):
                    if grid[i][col] == '?':
                        vertical_length += 1
                    else:
                        break

                max_local = max(horizontal_length, vertical_length)
                if max_local > max_options:
                    max_options = max_local
                    best_cell = (row, col)

    return best_cell

def solve(grid, words, step=0):
    cell = select_next_cell(grid)
    if not cell:
        return grid

    row, col = cell

    print(cell)
    print(len(words))

    sorted_words = sorted(words, key=len, reverse=True)

    for word in sorted_words:
        for direction in ['H', 'V']:
            if is_valid(grid, word, row, col, direction):
                new_grid = place_word(grid, word, row, col, direction)
                log_grid(new_grid, step, 'log_' + file_name)
                new_words = words.copy()
                new_words.remove(word)
                result = solve(new_grid, new_words, step + 1)
                if result:
                    return result
    return None

def write_solution(grid, output_file):
    with open(output_file, 'w') as file:
        for row in grid:
            file.write(''.join(row) + "\n")

def main():
    start_time = time.time()
    global file_name
    file_name = input("Digite qual arquivo de grid você quer resolver: ")
    grid = read_grid(file_name)
    words = read_word_list('lista_palavras.txt')

    write_solution(grid, 'test.txt')

    with open('log_' + file_name, 'w') as log_file:
        log_file.write("Starting backtracking algorithm\n\n")

    solution = solve(grid, words)

    with open('log_' + file_name, 'a') as log_file:
        log_file.write(f"Total execution time: {time.time() - start_time:.4f} seconds\n")

    if solution:
        write_solution(solution, 'solution.txt')
    else:
        print("No solution found.")

main()
