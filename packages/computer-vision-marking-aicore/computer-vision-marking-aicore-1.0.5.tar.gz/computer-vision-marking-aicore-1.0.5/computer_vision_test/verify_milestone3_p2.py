from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = '2ca4b14e-76dc-44a3-bfcd-052cf78615ef' # Store the user's and the computer's choices
task2_id = 'ae562b8c-bb0f-4861-a9d3-f8695953918b' # Figure out who won
task3_id = 'c1dfcdc5-97a4-4780-ab07-a0c4b785fcd2' # Create a function to simulate the game
task4_id = 'bd6076ef-ac2e-45a1-b38c-b5b1d733f63c' # Update your documentation

# def test_computer_choice_presence
# def test_user_choice_presence
# def test_user_choice_input

# def test_get_winner_presence
# def test_get_winner_args
# def test_get_winner_logic

# def test_play_presence
# def test_play_logic

if 'milestone_3_p2.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_3_p2.txt')


    # If there are no errors, mark everything as complete
    if len(errors) == 0:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_complete(task3_id)

    if ('test_computer_choice_presence' in errors) or ('test_user_choice_presence' in errors) or ('test_user_choice_input' in errors):
        # mark_incomplete(task2_id, message=errors['test_model_presence'])
        mark_incomplete(task1_id)
        mark_incomplete(task2_id)
        mark_incomplete(task3_id)
        if 'test_computer_choice_presence' in errors:
            print(errors['test_computer_choice_presence'])
        if 'test_user_choice_presence' in errors:
            print(errors['test_user_choice_presence'])
        if 'test_user_choice_input' in errors:
            print(errors['test_user_choice_input'])
    
    else:
        mark_complete(task1_id)

    if ('test_get_winner_presence' in errors) or ('test_get_winner_args' in errors) or ('test_get_winner_logic' in errors):
        mark_incomplete(task2_id)
        mark_incomplete(task3_id)
        if 'test_get_winner_presence' in errors:
            print(errors['test_get_winner_presence'])
        if 'test_get_winner_args' in errors:
            print(errors['test_get_winner_args'])
        if 'test_get_winner_logic' in errors:
            print(errors['test_get_winner_logic'])

    else:
        mark_complete(task2_id)

    if ('test_play_presence' in errors) or ('test_play_logic' in errors):
        mark_incomplete(task3_id)
        if 'test_play_presence' in errors:
            print(errors['test_play_presence'])
        if 'test_play_logic' in errors:
            print(errors['test_play_logic'])

    else:
        mark_complete(task3_id)

else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
    mark_incomplete(task3_id)
