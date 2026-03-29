import time     # Needed for simulation delay - time delay - to simualte each hour of production time
import os       # Needed for file existence checks to see if production data file already exists on computer 

# Must assume constants in the following variables:
data_file = 'productivity_data.txt' # this is going to be the file name that stores all production data
maintenance_threshold = 35.0        # Number of hours before maintenance inspection is required
                                    # mode optimised_rate no longer needed for requirement 8 
                                    # mode full_rate no longer need for requirement 8 
belt_rates = [0.5, 1.0, 1.5, 2.0]   # List of different production rate for the 4 conveyor belts - Requirement 8
number_of_belts = 4                 # Number of conveyor belts running at the same time - Requirement 8 

# Function 1: This part handles loading data into a split format
def load_data():
    # This function loads the data to account for the 4 conveyor and individual item totals for all 4 belts from the text file
    try:
        if not os.path.exists(data_file):
            save_data(0.0, [0.0, 0.0, 0.0, 0.0]) # Creates if missing - updated to now account for 4 belts 
        with open(data_file, 'r') as f:
            data = f.read().strip().split(',')
            if len(data) < 5:
                raise ValueError('File format is incorrect')
            hours = float(data[0])
            belt_items = [float(data[1]), float(data[2]), float(data[3]), float(data[4]),]
            return hours, belt_items
    except (FileNotFoundError, ValueError, PermissionError):
        print('Data error, starting new loading data....') # displays error message when either of those 3 errors are found
        return 0.0, [0.0, 0.0, 0.0, 0.0] # Now returns a list of 4 zeros to mark the beggening of each reset after a maintenance 

# Function 2: This part will handle saving data
def save_data(hours, belt_items):
    # This will write the total hours and items totals for all 4 belts to the text file
    try:
        with open(data_file, 'w') as f:
            f.write(f'{hours},{belt_items[0]},{belt_items[1]},{belt_items[2]},{belt_items[3]}')     # have to update to show each item produced per belt
    except IOError:
        print('Save has failed')

# Function 3: This part handles running the production and does early maintenance checks and simulates one full day of production for all 4 belts
def run_production(total_hours, belt_items):
    # Need to also check that maintenance is already needed before production begins
    if total_hours >= maintenance_threshold:
        print('\nMaintenance Inspection Required !')
        print(f'Total Hours (all belts): {total_hours:.1f}')

        for i in range(4):
            print(f'Belt {i+1}: {belt_items[i]:.1f} items')

        while True:     # This is a validation loop - checks if maintance is already required and that it must be done before continuing production cycles
            confirm = input('Confirm maintenance has been completed ? (yes/no): ').lower().strip()
            if confirm in ['yes', 'y']:
                total_hours = 0.0
                belt_items = [0.0] * 4
                save_data(total_hours, belt_items)
                print('Data has been reset after conveyor maintenance')
                return total_hours, belt_items
            elif confirm in ['no', 'n']:
                print('Maintenance not confirmed. Production will not start until maintenance is completed')
                return total_hours, belt_items
            else:
                print('This is an invalid input. Please only type "yes" or "no"')

    # Normal daily production cycle for all 4 belts
    daily_hours = 0.0               # Tracks how many hours have passed on current shift
    daily_belt_items = [0.0] * 4    # Tracks items produced by each belt on the current shift

    while daily_hours < 10 and total_hours < maintenance_threshold:
        time.sleep(1)   # Delay as recommended in brief - 1 sec = 1 hours real time
        daily_hours += 1
        total_hours += 1

        print(f'Hour {int(daily_hours)}: ', end='')     # Starts the line

        for i in range(4):
            items_per_hour = belt_rates[i] * 60
            daily_belt_items[i] += items_per_hour
            belt_items[i] += items_per_hour     # belt_items comes from load data function
        
            print(f'Belt{i+1} +{items_per_hour:.1f} ', end='')
        
        print()     # move to the next line after printing all 4 belts
            
        # Check if maintenance is now required
        if total_hours >= maintenance_threshold:
            print('\n Maintence Inspection Required !')
            print(f'Total Hours (all belts): {total_hours:.1f}')

            for i in range(4):
                print(f'Belt {i+1}: {belt_items[i]:.1f} items')     

            # Apply the same yes/no check for maintenance
            while True:
                confirm = input('Confirm maintenance has been completed ? (yes/no): ').lower().strip()
                if confirm in ['yes', 'y']:
                    total_hours = 0.0
                    belt_items = [0.0] * 4
                    save_data(total_hours, belt_items)
                    print('Data for all belts has been reset after maintenance')
                    return total_hours, belt_items
                elif confirm in ['no', 'n']:
                    print('Maintence not confirmed. Production will not start until maintenance is completed')
                    return total_hours, belt_items
                else:
                    print('This is an invalid input. Please type "yes" or "no" ')
            break

     #saves at the end of the work day       
    save_data(total_hours, belt_items)    
    return total_hours, belt_items

# function 4: Main menu loop for opertor to view and confirm menu options - calls correct function based on user choice
def main():
    print('Welcome to Main Menu !')
    total_hours, belt_items = load_data()
    while True:
        # The main menu list for operator to view and select
        menu_options = ['1: Start Production', '2: View Production Records', '3: Confirm Maintenance Inspection', '4: Exit Main Menu']
        print('\n'.join(menu_options))
        operator_choice = input('Select: ')
        if operator_choice == '1':
            # Starts a full day of production for all 4 conveyor belts at the same time 
            total_hours, belt_items = run_production(total_hours, belt_items)   # needed to change total_items to belt_items
        elif operator_choice == '2':
            # Displays the current total hours and individual item totals for each of the 4 belts
            print(f'Total Hours: {total_hours:.1f}')
            for i in range(4):
                print(f'Belt {i+1}: {belt_items[i]:.1f} items')
        elif operator_choice == '3':
            # Allows the operator to confirm that maintenance has been completed and resets all 4 conveyor belts
            # now need to call the same reset
            if total_hours >= maintenance_threshold:
                print('\nMaintenance Inspection Required !')
                print(f'Total Hours (all belts): {belt_items[i]:.1f} items')

                while True:
                    confirm = input('Confirm maintence has been completed ? (yes/no): ').lower().strip()
                    if confirm in ['yes', 'y']:
                        total_hours = 0.0
                        belt_items = [0.0] * 4
                        save_data(total_hours, belt_items)
                        print('Data has been reset for all belts')
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
            # Handles any invalid menu choice entered by the user 
            print('This choice was invalid, please try again')

    
if __name__ == '__main__': # wasn't properly indented (Self reflect)
        main()




