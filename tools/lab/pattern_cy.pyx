cpdef str get_pattern_c(str guess, str solution):
    """generates the patterns for a guess"""

    py_guess = guess.encode('UTF-8') 
    cdef char* c_guess = py_guess 
    py_solution = solution.encode('UTF-8') 
    cdef char* c_solution = py_solution

    cdef dict letter_budget = {}
    cdef char letter_solution
    for letter_solution in solution:
        if letter_solution in letter_budget:
            letter_budget[letter_solution] += 1
        else:
            letter_budget[letter_solution] = 1
            
    cdef list hint = [None] * len(guess)

    cdef int index
    cdef char letter_guess
    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if letter_guess == letter_solution:
            hint[index] = "g"
            letter_budget[letter_guess] -= 1
    
    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if not letter_guess in letter_budget:
            hint[index] = "b"
        elif letter_guess != letter_solution:
            if letter_budget[letter_guess] > 0:
                hint[index] = "y"
                letter_budget[letter_guess] -= 1
            else:
                hint[index] = "b"

    return "".join(hint)