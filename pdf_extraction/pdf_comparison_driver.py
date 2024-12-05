

if __name__ == '__main__':
    # Begin Input Loop
    user_input = input('Enter file name (enter \'q\' to quit): ')
    while user_input.lower() != "q":
        file_path = f'../classification_model/loss_runs/input/{user_input}'
        print(file_path)
        
        # Continue input loop
        user_input = input('Enter file name (enter \'q\' to quit): ')
