from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = '8dfaeb61-7a53-45e7-bd2f-f3939f172446' # Putting all together
task2_id = 'c6c2c356-c83f-4a01-896f-739eec6a05bc' # Count down
task3_id = '3891db35-2f65-43bd-849c-cde77ac0cb56' # Repeat until a player gets three victories
task4_id = '39061c7d-6221-49ca-b269-3f6495166b6e' # Take it even further! (Optional)
task5_id = '90885a05-24f5-43a2-b4fe-962a2baaddb4' # Update your documentation

    
# test_camera_rps_presence
# test_presence_readme

if 'milestone_4_p1.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_4_p1.txt')


    # If there are no errors, mark everything as complete
    if 'test_presence_readme' in errors:
        mark_incomplete(task5_id)
        print(errors['test_presence_readme'])
    else:
        mark_complete(task5_id)
    # Check if keras_model.h5 is in the repo
    if 'test_camera_rps_presence' in errors:
        # mark_incomplete(task2_id, message=errors['test_model_presence'])
        mark_incomplete(task1_id)
        mark_incomplete(task2_id)
        mark_incomplete(task3_id)
        mark_incomplete(task4_id)
        print(errors['test_camera_rps_presence'])

else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
    mark_incomplete(task3_id)
    mark_incomplete(task4_id)
    mark_incomplete(task5_id)
