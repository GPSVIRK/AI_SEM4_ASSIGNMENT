from itertools import permutations

def solve_cryptarithm():
    letters = ['T', 'W', 'O', 'F', 'U', 'R']
    digits = range(10)

    solutions = []

    for perm in permutations(digits, len(letters)):
        assign = dict(zip(letters, perm))

        # Leading zero constraint
        if assign['T'] == 0 or assign['F'] == 0:
            continue

        T, W, O, F, U, R = [assign[x] for x in letters]

        # Column 1: O + O = R + 10*C1
        sum1 = O + O
        R_calc = sum1 % 10
        C1 = sum1 // 10

        if R != R_calc:
            continue

        # Column 2: W + W + C1 = U + 10*C2
        sum2 = W + W + C1
        U_calc = sum2 % 10
        C2 = sum2 // 10

        if U != U_calc:
            continue

        # Column 3: T + T + C2 = O + 10*C3
        sum3 = T + T + C2
        O_calc = sum3 % 10
        C3 = sum3 // 10

        if O != O_calc:
            continue

        # Column 4: C3 = F
        if F != C3:
            continue

        solutions.append(assign)

    return solutions


def print_solution(sol):
    T, W, O, F, U, R = [sol[x] for x in ['T','W','O','F','U','R']]

    two = 100*T + 10*W + O
    four = 1000*F + 100*O + 10*U + R

    print(f"  {T}{W}{O}")
    print(f"+ {T}{W}{O}")
    print("------")
    print(f" {F}{O}{U}{R}")
    print()


# Driver
solutions = solve_cryptarithm()

if not solutions:
    print("No solution found.")
else:
    for i, sol in enumerate(solutions, 1):
        print(f"Solution {i}: {sol}")
        print_solution(sol)
