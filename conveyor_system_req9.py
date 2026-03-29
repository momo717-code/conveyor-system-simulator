import time # Needed for simulation delay - time delay - to simualte each hour of production time
import os # Needed for file existence checks to see if production data file already exists on computer 

# Must assume constants in the following variables:
data_file = 'productivity_data.txt'     # This constant is going to be the file name that stores all production data 
maintenance_threshold = 35.0            # This constant will define the number of hours after which maintenance is required 
optimised_rate = 1.5                    # This constant is the production rate for optimised mode
full_rate = 2.0                         # This constant is the production rate for the full production mode
operator_names = ['Scott', 'Andrew', 'Nicole', 'Joan']  # This list stores the 4 operator names for requirement 9

# Function 1: This part handles loading data into a split format
def load_data():
    # This function will load total hours, total items, and 4 operator items totals from the text file
    try:
        if not os.path.exists(data_file):
            save_data(0.0, 0.0, [0.0, 0.0, 0.0, 0.0])   # creates file with zero values if missing
        with open(data_file, 'r') as f:
            data = f.read().strip().split(',')
            if len(data) < 6:
                raise ValueError('File format incorrect')
            hours = float(data[0])
            total_items = float(data[1])
            operator_items = [float(data[2]), float(data[3]), float(data[4]), float(data[5])]
            return hours, total_items, operator_items
    except (FileNotFoundError, ValueError, PermissionError):
        print('Data error, starting new loading data......') # displays error message when either of those 3 errors are found
        return 0.0, 0.0, [0.0, 0.0, 0.0, 0.0]

# Function 2: This part will handle saving data
def save_data(hours, total_items, operator_items):
    # This function will now write the total hours, total items and the 4 operator totals to the text file
    try:
        with open(data_file, 'w') as f:
            f.write(f'{hours},{total_items},{operator_items[0]},{operator_items[1]},{operator_items[2]},{operator_items[3]}')
    except IOError:
        print('Save has failed')

# Function 3: This part handles running the production and does mode checks and checks if maintenance inspection is need
def run_production(total_hours, total_items, operator_items):
    # This function will simulate one full work day of production, handles mode selection, operator choice, and maintenance checks
    # Need to also check that maintenance is already needed at the start of production 
    if total_hours >= maintenance_threshold:
        print('\nMaintenance Inspection Required !')
        print(f'Total Hours: {total_hours:>8.1f}\nTotal Items: {total_items:>8.1f}')
        while True:     # this is a validation loop - checks if maintance is already required and that it must be done before continuing production cycles
            confirm = input('Confirm maintenance has been completed ? (yes/no): ').lower().strip()
            if confirm in ['yes', 'y']:
                total_hours = 0.0
                total_items = 0.0 # was missing for some reason 
                operator_items = [0.0, 0.0, 0.0, 0.0] # should now reset the 4 operators items after 35 hrs 
                save_data(total_hours, total_items, operator_items)
                print('Data has been reset after conveyor maintenance')
                return total_hours, total_items, operator_items
            elif confirm in ['no', 'n']:
                print('Maintenance not confirmed. Production will not start until maintenance is completed')
                return total_hours, total_items, operator_items
            else:
                print('This is an invalid input. Please only type "yes" or "no"')
    
    # Now need to ask which operator is running production today - Requirement 9
    print('\nWhich operator is starting the production for this shift today ?')
    for i in range(4):
        print(f'{i+1}: {operator_names[i]}')    # had to also add [i] so it list names as a list not the whole list 1 - 4
    
    while True:
        try:
            operator_choice = int(input('Please enter assigned operator number (select 1 - 4): ')) - 1
            if 0 <= operator_choice <= 3:
                selected_operator = operator_choice
                break
        except ValueError:
            pass
        print('Sorry that is an invalid choice, please enter 1 - 4')

    # This is now the normal daily production cycle that only runs if below threshold hours
    while True:     # mode selection
        mode = input('Please select a mode (1:Optimised Mode, 2:Full Mode): ')
        try:
            mode = int(mode)
            if mode in [1,2]: 
                break
        except ValueError:
            pass
        print('Sorry you have entered a wrong value, please try again...')

    rate = [optimised_rate, full_rate][mode-1]     # This selects the correct production rate based on user choice 

    daily_hours = 0.0   # This tracks hours passed on current shift
    daily_items = 0.0   # This tracks items produced on current shift 

    # hourly loop 
    while daily_hours < 10 and total_hours < maintenance_threshold:
        time.sleep(1) # delay as recommended in brief - 1 second sec = 1 hour real time
        daily_hours += 1
        items_per_hour = rate * 60
        daily_items += items_per_hour
        total_hours += 1
        total_items += items_per_hour   # had to add this to fix missing total item each time a production has ran through a cycle
        operator_items[selected_operator] += items_per_hour     # now adds to the chosen opeterator for requirement 9 
        print(f'Hour {int(daily_hours)}: +{items_per_hour:.1f} items')  # Should display current daily hours and the hourly rate for items being made

        if total_hours >= maintenance_threshold:
            print('\n Maintence Inspection Required !')
            print(f'Total Hours: {total_hours:>8.1f}\nTotal Items: {total_items:>8.1f}')

            #show each operator's total
            print('Individual operator totals: ')
            for i in range(4):
                print(f' {operator_names[i]}: {operator_items[i]:.1f} items')

            # Apply the same yes/no check for maintenance
            while True:
                confirm = input('Confirm maintenance has been completed ? (yes/no): ').lower().strip()
                if confirm in ['yes', 'y']:
                    total_hours = 0.0
                    total_items = 0.0
                    operator_items = [0.0, 0.0, 0.0, 0.0] # should reset all operator item counts
                    save_data(total_hours, total_items, operator_items)
                    print('Data has been reset after maintenance')
                    break
                elif confirm in ['no', 'n']:
                    print('Maintence not confirmed. Production will not start until maintenance is completed')
                    break
                else:
                    print('This is an invalid input. Please type "yes" or "no" ')
            break

     #saves at the end of the work day       
    save_data(total_hours, total_items, operator_items)    
    return total_hours, total_items, operator_items

# function 4: Main menu loop for opertor to view and confirm menu options based on user choice
def main():
    print('Welcome to Main Menu !')
    total_hours, total_items, operator_items = load_data()
    while True:
        # the main menu list available to operator
        menu_options = ['1: Start Production', '2: View Production Records', '3: Confirm Maintenance Inspection', '4: Exit Main Menu']
        print('\n'.join(menu_options))
        operator_choice = input('Select: ')
        if operator_choice == '1':
        # starts a full day of production, and asks which operator is working this current shift, and runs until end of work day or maintenance required
            total_hours, total_items, operator_items = run_production(total_hours, total_items, operator_items)
        elif operator_choice == '2':
            # Displays the current total hours, total items and individual totals for all 4 operators since last maintenance
            print(f'Current totals and Hours: {total_hours:.1f} | Total Items: {total_items:.1f}')
            print('Operator production since this period')
            for i in range(4):
                print(f' {operator_names[i]}: {operator_items[i]:.1f} items')
        elif operator_choice == '3':
            # Allows the operator to confirm that maintenance has been completed and resets all data if confirmed 
            # now need to call the same reset
            if total_hours >= maintenance_threshold:
                print('\nMaintenance Inspection Required !')
                print(f'Total Hours: {total_hours:>8.1f}\nTotal Items: {total_items:.1f}') 
                while True:
                    confirm = input('Confirm maintence has been completed ? (yes/no): ').lower().strip()
                    if confirm in ['yes', 'y']:
                        total_hours = 0.0
                        total_items = 0.0
                        operator_items = [0.0, 0.0, 0.0, 0.0]   # resets all operator item counts
                        save_data(total_hours, total_items, operator_items)
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
            #Handles any invalid menu choice entered by the user
            print('This choice was invalid, please try again')

    
if __name__ == '__main__':  # wasn't properly indented (Self reflect)
        main()




