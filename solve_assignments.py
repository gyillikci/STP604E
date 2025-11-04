#!/usr/bin/env python3
"""
Assignment Solutions Runner
Run all assignment problems or specific ones
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from assignments import assignment1_problem1
from assignments import assignment1_problem2
from assignments import assignment1_problem3
from assignments import assignment1_problem4


def main():
    print("\n" + "="*70)
    print("  STP 604E - COMPOSITE MATERIALS")
    print("  ASSIGNMENT SOLUTIONS")
    print("="*70)

    if len(sys.argv) > 1:
        # Run specific problem
        problem_num = sys.argv[1]
        run_problem(problem_num)
    else:
        # Interactive menu
        show_menu()


def show_menu():
    """Display interactive menu"""
    while True:
        print("\n" + "-"*70)
        print("Select an option:")
        print("  1 - Problem 1: Quasi-Isotropic Laminate Analysis")
        print("  2 - Problem 2: Micromechanics Analysis")
        print("  3 - Problem 3: Zero Shear Strain Constraint")
        print("  4 - Problem 4: Stiffness Matrix Comparison")
        print("  5 - Run ALL problems")
        print("  0 - Exit")
        print("-"*70)

        choice = input("\nEnter your choice: ").strip()

        if choice == '0':
            print("\nExiting...")
            break
        elif choice == '1':
            run_problem('1')
        elif choice == '2':
            run_problem('2')
        elif choice == '3':
            run_problem('3')
        elif choice == '4':
            run_problem('4')
        elif choice == '5':
            run_all_problems()
        else:
            print("\nInvalid choice. Please try again.")

        input("\nPress Enter to continue...")


def run_problem(problem_num):
    """Run specific problem"""
    try:
        if problem_num == '1':
            assignment1_problem1.solve_problem1()
        elif problem_num == '2':
            assignment1_problem2.solve_problem2()
        elif problem_num == '3':
            assignment1_problem3.solve_problem3()
        elif problem_num == '4':
            assignment1_problem4.solve_problem4()
        else:
            print(f"\nUnknown problem number: {problem_num}")
    except Exception as e:
        print(f"\nError running problem {problem_num}: {e}")
        import traceback
        traceback.print_exc()


def run_all_problems():
    """Run all assignment problems"""
    print("\n" + "="*70)
    print("  RUNNING ALL ASSIGNMENT PROBLEMS")
    print("="*70)

    problems = ['1', '2', '3', '4']

    for prob in problems:
        try:
            run_problem(prob)
        except Exception as e:
            print(f"\n!!! Error in Problem {prob}: {e}")
            continue

    print("\n" + "="*70)
    print("  ALL PROBLEMS COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()
