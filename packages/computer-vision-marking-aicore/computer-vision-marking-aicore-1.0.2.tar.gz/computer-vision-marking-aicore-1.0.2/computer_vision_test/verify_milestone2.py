from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = '1ef920ef-7e5f-4078-9e28-eb8e08946319' # Create a new virtual environment
task2_id = 'bbbdf8bf-d35b-4473-857f-dc81d16edac4' # Run the model in your local machine
task3_id = 'c41ad504-5f65-4348-9f4c-5cf9b752e477' # Get familiar with the code

# test_requirements_presence
# test_can_import_opencv
# test_can_import_numpy
# test_can_import_keras

if 'milesone_2.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_2.txt')

    # If there are no errors, mark everything as complete
    if len(errors) == 0:
        mark_complete(task1_id)
        mark_complete(task2_id)
    # Check if keras_model.h5 is in the repo
    if 'test_requirements_presence' in errors:
        # mark_incomplete(task2_id, message=errors['test_model_presence'])
        mark_incomplete(task1_id)
        print(errors['test_requirements_presence'])
    else:
        mark_complete(task1_id)

        
    if 'test_can_import_numpy' in errors:
        mark_incomplete(task2_id)
        print(errors['test_can_import_numpy'])
    
    elif 'test_can_import_opencv' in errors:
        mark_incomplete(task2_id)
        print(errors['test_can_import_opencv'])

    elif 'test_can_import_keras' in errors:
        mark_incomplete(task2_id)
        print(errors['test_can_import_keras'])
    
    else:
        mark_complete(task2_id)

else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)

## TODO: Add verification to tick off task 3 in case the user has gone through the following lessons:

# cbd4ec1b-8781-4dcd-9278-ca75febc2974 Python Environment
# 25d1757b-66ee-4c5d-8489-adcc923fec0e Arithmetic Operations
# 96a873c0-3f66-455d-b672-41c29ca73f0d Lists and sets
# 6556d991-bdd0-4e97-bfb1-c9355f34a868 Dictionaries, tuples and operators
# 34f017d8-c4c0-468c-bd43-bb2f1ed17683 Control Flow
