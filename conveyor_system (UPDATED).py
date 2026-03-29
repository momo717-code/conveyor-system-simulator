import time     # Used to pause the program for one second to simulate each hour of production time 
import os       # Used to check if the production data file already exists on the computer

# Must assume constants in the following variables:
data_file = 'productivity_data.txt'     # Name of the text file that stores all production data
maintenance_threshold = 35.0            # Number of operating hours after which a maintence inspection is required
optimised_rate = 1.5                    # Items produced per minute for when optimised mode option is selected 
full_rate = 2.0                         # Items produced per minute for when full production mode option is selected 

# Function 1: This part handles loading data into a split format
def load_data():
    # This will read comma-sperated hours and items from file at start of the program
    try:
        if not os.path.exists(data_file):
            save_data(0.0, 0.0) # creates the file with all values at zero if missing
        with open(data_file, 'r') as f:
            data = f.read().strip().split(',')
            return float(data[0]), float(data[1])
    except (FileNotFoundError, ValueError, PermissionError):
        print('Data error, starting new loading data......') # displays error message when file cannot be read
        return 0.0, 0.0

# Function 2: This part will handle saving data
def save_data(hours, items):
    # This will write the current total hours and total items to the text file so they are saved between run cycles
    try:
        with open(data_file, 'w') as f:
            f.write(f'{hours},{items}')
    except IOError:
        print('Save has failed')

# Function 3: This part handles running the production and handles maintenance checks before starting production cycle 
def run_production(total_hours, total_items):
    # this will simulate the full day of the production and checks for maintencance
    # need to also check that maintenance is already needed before actually starting the production cycle
    if total_hours >= maintenance_threshold:
        print('\nMaintenance Inspection Required !')
        print(f'Total Hours: {total_hours:>8.1f}\nTotal Items: {total_items:>8.1f}')
        while True: # this is a validation loop - checks if maintance is already required and that it must be done before continuing production cycles
            confirm = input('Confirm maintenance has been completed ? (yes/no): ').lower().strip()
            if confirm in ['yes', 'y']:
                total_hours = 0.0
                total_items = 0.0
                save_data(total_hours, total_items)
                print('Data has been reset after conveyor maintenance')
                return total_hours, total_items
            elif confirm in ['no', 'n']:
                print('Maintenance not confirmed. Production will not start until maintenance is completed')
                return total_hours, total_items
            else:
                print('This is an invalid input. Please only type "yes" or "no"')
    # This is now the normal daily production cycle that only runs if below threshold hours
    while True: # mode selection loop
        mode = input('Please select a mode (1:Optimised Mode, 2:Full Mode): ')
        try:
            mode = int(mode)
            if mode in [1,2]: 
                break
        except ValueError:
            pass
        print('Sorry you have entered a wrong value, please try again...')

    rate = [optimised_rate, full_rate][mode-1] # this confirms the list for the available rates to choose from

    daily_hours = 0.0   # Tracks how many hours have been simulated on the current shift 
    daily_items = 0.0   # Tracks how many items have been produced on the current shift

    while daily_hours < 10 and total_hours < maintenance_threshold:
        time.sleep(1) # delay as recommended in brief - 1 second represents 1 hour of production time
        daily_hours += 1
        items_per_hour = rate * 60
        daily_items += items_per_hour
        total_hours += 1
        total_items += items_per_hour
        print(f'Hour {int(daily_hours)}: +{items_per_hour:.1f} items') # Should display current daily hours and the hourly rate for items being made for each hour gone by

        if total_hours >= maintenance_threshold:
            print('\n Maintence Inspection Required !')
            print(f'Total Hours: {total_hours:>8.1f}\nTotal Items: {total_items:>8.1f}')

            # Apply the same yes/no check for maintenance
            while True:
                confirm = input('Confirm maintenance has been completed ? (yes/no): ').lower().strip()
                if confirm in ['yes', 'y']:
                    total_hours = 0.0
                    total_items = 0.0
                    save_data(total_hours, total_items)
                    print('Data has been reset after maintenance')
                    break
                elif confirm in ['no', 'n']:
                    print('Maintence not confirmed. Production will not start until maintenance is completed')
                    break
                else:
                    print('This is an invalid input. Please type "yes" or "no" ')
            break

     #saves at the end of the work day       
    save_data(total_hours, total_items)    
    return total_hours, total_items

# function 4: Main menu loop for operator to make a selection 1 - 4 and call the correct function to whatever the operator picks
def main():
    print('Welcome to Main Menu !')
    total_hours, total_items = load_data()
    while True:
        # the main menu list available to the operator
        menu_options = ['1: Start Production', '2: View Production Records', '3: Confirm Maintenance Inspection', '4: Exit Main Menu']
        print('\n'.join(menu_options))
        operator_choice = input('Select: ')
        if operator_choice == '1':
            #Starts a full day of production which simualtes 10 hours or until maintenance is needed 
            total_hours, total_items = run_production(total_hours, total_items)
        elif operator_choice == '2':
            # Shows the current total hours and total items produced since last maintenance
            print(f'Current totals and Hours: {total_hours:.1f} | Items: {total_items:.1f}')
        elif operator_choice == '3':
            # Allows the operator to manually confirms that the maintenance has been completed and reset the data
            # now need to call the same reset
            if total_hours >= maintenance_threshold:
                print('\nMaintenance Inspection Required !')
                print(f'Total Hours: {total_hours:>8.1f}\nTotal Items: {total_items:.1f}')
                while True:
                    confirm = input('Confirm maintence has been completed ? (yes/no): ').lower().strip()
                    if confirm in ['yes', 'y']:
                        total_hours = 0.0
                        total_items = 0.0
                        save_data(total_hours, total_items)
                        print('Data has been reset')
                        break
                    elif confirm in ['no', 'n']:
                        print('maintenance not yet confirmed')
                        break
                    else:
                        print('Invalid input. Please type "yes" or "no" ')
            else:
                print('No Maintenance need just yet please continue production')
        elif operator_choice == '4':
            # Exits the program and ends the session 
            print('Goodbye !')
            break
        else:
            print('This choice was invalid, please try again')
            # Handles any invalid menu choice entered by the user
    
if __name__ == '__main__': # wasn't properly indented (Self reflect)
        main()




