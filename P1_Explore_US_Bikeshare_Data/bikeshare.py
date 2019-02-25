import datetime
import pandas as pd
import calendar
from tkinter import *
import sys
from sys import executable
import os
import runpy
from subprocess import Popen, CREATE_NEW_CONSOLE

def restart_program():
    #Upon restart, the function opens in a console, so that all variables are flushed and input can be given anew.
    Popen([executable, 'bikeshare.py'], creationflags = CREATE_NEW_CONSOLE)

#initiate tkinter window
root = Tk()

#Creating Drop-Down Menu1
Option1 = [
"Chicago",
"New York",
"Washington"]

#Create Drop-Down Menu2
Option2 = [
"Month",
"Day",
"all"
]

ment = StringVar(root)
ment.set(Option1[0])
ment2 = StringVar(root)
ment2.set(Option2[0])

def m_hello(var):
    global root
    root.destroy()
    mtext=ment.get()
    mtext2=ment2.get()
    #printing the options, which have been chosen in tkinter window to console
    print('You have chosen ' + ment.get() + ' as City. Your results will be shown in a CSV.')
    print('You have chosen ' + ment2.get() + ' as time range. Your results will be shown in a CSV.')

#define content of tkinter window
root.title('Bikeshare Data Exploration')
label=Label(root,text='\nHello, let\'s explore some US Bikeshare data!\n'
        'Would you like to see data for Chicago, New York or Washington?\n').pack()
w = OptionMenu(root, ment, *Option1)
w.pack()
label2=Label(root,text='\nWould you like to filter the data by month, day or do you want to see all data.\n'
'Please type month for filtering on\'').pack()
w2 = OptionMenu(root, ment2, *Option2)
w2.pack()
mbutton=Button(root, text='Go!', command=lambda: m_hello(ment)).pack()
#define placement and size of tkinter window.
root.geometry('500x250+180+180')
#do not display x button of tkinter window.
root.overrideredirect(True)
root.mainloop()

def get_city():
    '''This def takes the input which is given via the tkinter gui and returns the matching filename.'''
    city = ''
    while city.lower() not in ['chicago','new york','washington']:
        city = ment.get()
        if city.lower() == 'chicago':
            return 'chicago.csv'
        elif city.lower() == 'new york':
            return 'new_york_city.csv'
        elif city.lower() == 'washington':
            return 'washington.csv'
        else:
            print('\n Sorry, i couldn\'t understand your input. Please type in eather Chicago, New York or Washington')

def get_time_period():
    '''This def takes the input which is given via the tkinter gui and returns the matching filter.'''
    time_period = ''
    while time_period.lower() not in ['month','day','all']:
        time_period = ment2.get()
        if time_period.lower() == 'month':
            return ['month', get_month()]
        if time_period.lower() == 'day':
            return ['day', get_day()]
        if time_period.lower() == 'all':
            return ['all','no filter']
        else:
            print('\nI\'m sorry, I\'m not sure which time period you\'re trying to filter by. Let\'s try again.')

def get_month():
    '''This function asks the user to choose a month and returns it.'''
    month = ''
    while month.lower() not in ['january','february','march','april','may','june']:
        month = input('\nWhich month? January, February, March, April, May, or June?\n'
        'Your results will be printed to a CSV.\n').title()
        if month.lower() == 'january':
            return '01'
        elif month.lower() == 'february':
            return '02'
        elif month.lower() == 'march':
            return '03'
        elif month.lower() == 'april':
            return '04'
        elif month.lower() == 'may':
            return '05'
        elif month.lower() == 'june':
            return '06'
        else:
            print("\nI'm sorry, I'm not sure which month you're trying to filter by. Let's try again.\n")

def get_day():
    '''This function asks the user to choose a day of week and returns it.'''
    day_of_week = ''
    while day_of_week.lower() not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        day_of_week = input('\nWhich day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n'
        'Your results will be printed to a CSV.\n')
    if day_of_week.lower() == 'monday':
        return 0
    elif day_of_week.lower() == 'tuesday':
        return 1
    elif day_of_week.lower() == 'wednesday':
        return 2
    elif day_of_week.lower() == 'thursday':
        return 3
    elif day_of_week.lower() == 'friday':
        return 4
    elif day_of_week.lower() == 'saturday':
        return 5
    elif day_of_week.lower() == 'sunday':
        return 6
    else:
        print('\nI\'m sorry, I\'m not sure which day of the week you\'re trying to filter by. Let\'s try again.\n')

def popular_month(df):
    '''This function returns the most common month by start time.'''
    trips_per_month = df.groupby('Month')['Start Time'].count()
    return "Most common month by start time: " + calendar.month_name[int(trips_per_month.sort_values(ascending=False).index[0])]


def popular_day(df):
    '''This function returns the most common day by start time.
    '''
    trips_per_day = df.groupby('Day of Week')['Start Time'].count()
    return "Most common day of the week: " + calendar.day_name[int(trips_per_day.sort_values(ascending=False).index[0])]


def popular_hour(df):
    '''This function returns the most common hour by start time.
    '''
    trips_per_hour = df.groupby('Hour of Day')['Start Time'].count()
    most_com_hour = trips_per_hour.sort_values(ascending=False).index[0]
    d = datetime.datetime.strptime(most_com_hour, "%H")
    return "Most common start hour: " + d.strftime("%I %p")

def trip_duration(df):
    '''This function returns the total and the average travel time.'''
    total_trip_duration = df['Trip Duration'].sum()
    avg_trip_duration = df['Trip Duration'].mean()
    m, s = divmod(total_trip_duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    total_trip_duration = "\nTotal travel time: %d years %02d days %02d hours %02d minutes %02d seconds" % (y, d, h, m, s)
    m, s = divmod(avg_trip_duration, 60)
    h, m = divmod(m, 60)
    avg_trip_duration = "Average travel time: %d hours %02d minutes %02d seconds" % (h, m, s)
    return [total_trip_duration, avg_trip_duration]

def popular_stations(df):
    '''This function retunrs the most common start and end station.'''
    start_station_counts = df.groupby('Start Station')['Start Station'].count()
    end_station_counts = df.groupby('End Station')['End Station'].count()
    sorted_start_stations = start_station_counts.sort_values(ascending=False)
    sorted_end_stations = end_station_counts.sort_values(ascending=False)
    total_trips = df['Start Station'].count()
    most_popular_start_station = "\nMost common start station: " + sorted_start_stations.index[0] + " (" + str(sorted_start_stations[0]) + " trips, " + '{0:.2f}%'.format(((sorted_start_stations[0]/total_trips) * 100)) + " of trips)"
    most_popular_end_station = "Most common end station: " + sorted_end_stations.index[0] + " (" + str(sorted_end_stations[0]) + " trips, " + '{0:.2f}%'.format(((sorted_end_stations[0]/total_trips) * 100)) + " of trips)"
    return [most_popular_start_station, most_popular_end_station]


def popular_trip(df):
    '''This function returns the most common trip, meaning the most common combination of start station and end station.'''
    trip_counts = df.groupby(['Start Station', 'End Station'])['Start Time'].count()
    sorted_trip_stations = trip_counts.sort_values(ascending=False)
    total_trips = df['Start Station'].count()
    return "Most common trip: " + "\n  Start station: " + str(sorted_trip_stations.index[0][0]) + "\n  End station: " + str(sorted_trip_stations.index[0][1]) + "\n  (" + str(sorted_trip_stations[0]) +  " trips, " + '{0:.2f}%'.format(((sorted_trip_stations[0]/total_trips) * 100)) + " of trips)"


def users(df):
    '''This function retunrs the number of trips by user type.'''
    user_type = df.groupby('User Type')['User Type'].count()
    return user_type

def most_popular_user(df):
    '''This function returns the most common user type and calculates data for it.'''
    user_counts = df.groupby('User Type')['User Type'].count()
    sorted_user_counts = user_counts.sort_values(ascending=False)
    total_users = df['User Type'].count()
    most_common_user = "\nMost common user type: " + sorted_user_counts.index[0] + " (" + str(sorted_user_counts[0]) + " trips, " + '{0:.2f}%'.format(((sorted_user_counts[0]/total_users) * 100)) + " of trips)"
    return [most_common_user]

def most_popular_gender(df):
    '''This function returns the most common user type and calculates data for it.'''
    gender_counts = df.groupby('Gender')['Gender'].count()
    sorted_gender_counts = gender_counts.sort_values(ascending=False)
    total_genders = df['Gender'].count()
    most_common_gender = "\nMost common gender: " + sorted_gender_counts.index[0] + " (" + str(sorted_gender_counts[0]) + " trips, " + '{0:.2f}%'.format(((sorted_gender_counts[0]/total_genders) * 100)) + " of trips)"
    return [most_common_gender]

def gender(df):
    '''This function returns the number of trips by gender.'''
    count_gender = df.groupby('Gender')['Gender'].count()
    return count_gender


def birth_years(df):
    '''This function returns the the oldest, the youngest and the most common birth year.'''
    earliest_birth_year = "Earliest birth year: " + str(int(df['Birth Year'].min()))
    most_recent_birth_year = "Most recent birth year: " + str(int(df['Birth Year'].max()))
    birth_year_counts = df.groupby('Birth Year')['Birth Year'].count()
    sorted_birth_years = birth_year_counts.sort_values(ascending=False)
    total_trips = df['Birth Year'].count()
    most_common_birth_year = "Most common birth year: " + str(int(sorted_birth_years.index[0])) + " (" + str(sorted_birth_years.iloc[0]) + " trips, " + '{0:.2f}%'.format(((sorted_birth_years.iloc[0]/total_trips) * 100)) + " of trips)"
    return [earliest_birth_year, most_recent_birth_year, most_common_birth_year]


def display_data(df, current_line):
    '''This function asks the user, if he would like to see 20 more lines of data. If the users choose yes, it will display 20 new lines of data and then ask anew, if he would like to see more. If not, it will jump back the function returns and the user will be ask to choose what city he wants to see data for.'''
    display = input('\nWould you like to dive deeper and see more data?'
                    ' If so, please type \'yes\' or \'no\'.\n'
                    'Please note that this data is not printed to your CSV but to the console.\n')
    display = display.lower()
    if display == 'yes' or display == 'y':
        print(df.iloc[current_line:current_line+20])
        current_line += 20
        return display_data(df, current_line)
    if display == 'no' or display == 'n':
        return
    else:
        print('\nI\'m sorry. I didn\'t understand your input. If you would like to see more, please type yes, if not, please type no\n')
        return display_data(df, current_line)


def statistics():
    '''The functions listed below are responsible for calculating and printing statistic about the city, time period and user, depending an the users input'''

    '''Depending on the users input, this functions filts the data by city (Chicago, New York, Washington)'''
    city = get_city()
    city_df = pd.read_csv(city)

    def get_day_of_week(str_date):
        '''This function is used for parsing the dates and at the end, returning integer values for a week day.'''
        date_obj = datetime.date(int(str_date[0:4]), int(str_date[5:7]), int(str_date[8:10]))
        return date_obj.weekday()
    city_df['Day of Week'] = city_df['Start Time'].apply(get_day_of_week)
    city_df['Month'] = city_df['Start Time'].str[5:7]
    city_df['Hour of Day'] = city_df['Start Time'].str[11:13]

    '''This function is used to filter the data by the time period the user has specified.'''
    time_period = get_time_period()
    filter_period = time_period[0]
    filter_period_value = time_period[1]
    filter_period_label = 'No filter'

    if filter_period == 'all':
        filtered_df = city_df
    elif filter_period == 'month':
        filtered_df = city_df.loc[city_df['Month'] == filter_period_value]
        filter_period_label = calendar.month_name[int(filter_period_value)]
    elif filter_period == 'day':
        filtered_df = city_df.loc[city_df['Day of Week'] == filter_period_value]
        filter_period_label = calendar.day_name[int(filter_period_value)]

# This fd function is responsible for passing the defined data to a CSV file, which will be stored in the same folder as the python script.
    fd = open(city[:-4].lower().replace("_", "-") + '-' + filter_period_label.lower()+".csv",'w')
    old_stdout = sys.stdout
    sys.stdout = fd
    #print header information
    print('\n')
    print(city[:-4].upper().replace("_", " ") + ' - ' + filter_period_label.upper())
    print('-----------')
    print('-----------')
    print('This data is calculated based on your input:\n')

    print('Total trips: ' + "{:,}".format(filtered_df['Start Time'].count()))

    if filter_period == 'none' or filter_period == 'day':
        print(popular_month(filtered_df))

    if filter_period == 'none' or filter_period == 'month':
        print(popular_day(filtered_df))

    #print popular hour
    print(popular_hour(filtered_df))

    #print trip duration
    trip_duration_stats = trip_duration(filtered_df)
    print(trip_duration_stats[0])
    print(trip_duration_stats[1])

    #print most popular stations.
    most_popular_stations = popular_stations(filtered_df)
    print(most_popular_stations[0])
    print(most_popular_stations[1])

    #print most popular trips
    print(popular_trip(filtered_df))

    #print data for the most popular user type. Definite numbers and %.
    most_popular_users = most_popular_user(filtered_df)
    print(most_popular_users[0])
    print('')
    print(users(filtered_df))

    #only print the following data if source is Chicago or New York CSV, as this data is missing for washington.
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        #print data for the most popular user type. Definite numbers and %.
        most_popular_genders = most_popular_gender(filtered_df)
        print(most_popular_genders[0])
        print('')
        print(gender(filtered_df))

        birth_years_data = birth_years(filtered_df)
        print('')
        print(birth_years_data[0])
        print(birth_years_data[1])
        print(birth_years_data[2])
    #finish printing data to csv with the next three lines
    sys.stdout = old_stdout
    fd.close()
    display_data(filtered_df, 0)

    def restart_question():
        '''Conditionally restarts the program based on the user's input
        Args:
            none.
        Returns:
        '''
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'. Upon typing no the program will be canceled.)\n'
        'If you choose \'yes\' a you will be able to start anew.\n')
        if restart.lower() == 'yes':
            restart_program()
        elif restart.lower() == 'no':
            return
        else:
            print('\nSorry, i wasn\'t able to understand your input. Please type \'yes\' or \'no\n')
        return restart_question()

    restart_question()
if __name__ == "__main__":
    statistics()
