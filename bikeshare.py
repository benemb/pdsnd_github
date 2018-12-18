# Tested on: Python 3.7.0
#            Pandas 0.23.4
#            Numpy 1.15.1


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('')
    with open('bike.txt', 'r') as f:
        file_data = f.read()
        print(file_data)
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = ['chicago','new york city','washington']
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    week_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()
            city_idx = cities.index(city)
            break
        except: ValueError
        print('Oops! Enter the correct city')

    print('Thank you, you selected {}'.format(city.title()))

    while True:
        try:
            options = ['month', 'day', 'both', 'none']
            option = input('Would you like to filter the data by month, day, both or not at all? Type \'none\' for no filters: ').lower()
            option_idx = options.index(option)
            break

        except: ValueError
        print('Oops!')

    if option == 'month':
        while True:
            try:
                # add 'all' in case user changes his/her mind without the need of restarting the code.
                month = input('Which month - January, February, March, April, May, June or \'all\'? ').lower()
                month_idx = months.index(month)
                day = 'all'
                break
            except: ValueError
            print('Oops! Enter a correct month ')

        print('Thank you, you selected {}'.format(month.title()))

    elif option == 'day':
        while True:
            try:
                # add 'all' in case user changes his/her mind without the need of restarting the code.
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or \'all\'? ').lower()
                days_idx = week_days.index(day)
                month = 'all'
                break
            except: ValueError
            print('Oops! Enter a correct day ')
        print('Thank you, you selected {}'.format(day.title()))

    elif option == 'both':
        while True:
            try:
                # add 'all' in case user changes his/her mind without the need of restarting the code.
                month = input('Which month - January, February, March, April, May, June or \'all\'? ').lower()
                month_idx = months.index(month)
                break
            except: ValueError
            print('Oops! Enter a correct month ')

        print('Thank you, you selected {}'.format(month.title()))

        while True:
            try:
                # add 'all' in case user changes his/her mind without the need of restarting the code.
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or \'all\'? ').lower()
                days_idx = week_days.index(day)
                break
            except: ValueError
            print('Oops! Enter a correct day ')
        print('Thank you, you selected {}'.format(day.title()))

    elif option == 'none':
        month = 'all'
        day = 'all'
        print('Ok, no filters for you')

    print('-'*40)

    question = input('City: {} \nMonth: {} \nDay: {} \nDo you confirm? y/n (press \'n\' to restart ) \n'.format(city.title(),month.title(),day.title())).lower()
    if question != 'y':
        print('Restarting.....')
        get_filters()


    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #  display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    most_common_month = df['month'].mode()[0]

    #  display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    most_common_dow = df['day'].mode()[0]

    #  display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]

    print('Most popular month: {}'.format(most_common_month))
    print('Most common day of week: {}'.format(most_common_dow))
    print('Most common start hour: {}'.format(most_common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station and count
    most_common_start_station = df['Start Station'].describe()['top']
    most_common_start_station_count = df['Start Station'].value_counts()[0]
    #  display most commonly used end station and count
    most_common_end_station = df['End Station'].describe()['top']
    most_common_end_station_count = df['End Station'].value_counts()[0]
    #  display most frequent combination of start station and end station trip and count
    df['common_station'] = df['Start Station'].astype(str) + ' to ' + df['End Station'].astype(str)
    most_common_combination = df['common_station'].describe()['top']
    most_common_combination_count = df['common_station'].value_counts()[0]

    print('The most commonly used start station is: {}. Count: {}'.format(most_common_start_station, most_common_start_station_count))
    print('The most commonly used end station is: {}. Count: {}'.format(most_common_end_station, most_common_end_station_count))
    print('The most frequent trip is: from {}. Count: {}'.format(most_common_combination, most_common_combination_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum( axis = 0 )

    # display mean travel time
    mean_travel_time = df['Trip Duration'].describe()['mean']

    # adapt the time visualization basing on its duration
    if total_travel_time > 86400:
        print('The total travel time is {} seconds or ~{} minutes or ~{} hours or ~{} days'.format(total_travel_time, int((total_travel_time // 60)), int((total_travel_time // 3600)), int((total_travel_time // 86400))))
    else:
        print('The total travel time is {} seconds or ~{} minutes or ~{} hours'.format(total_travel_time, int((total_travel_time // 60)), int((total_travel_time // 3600))))

    print('')

    if mean_travel_time > 3600:
        print('The mean travel time is {} seconds or ~{} minutes or ~{} hours'.format(mean_travel_time, int((mean_travel_time // 60)), int((mean_travel_time // 3600))))
    else:
        print('The mean travel time is {} seconds or ~{} minutes'.format(mean_travel_time, int((mean_travel_time // 60))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('User Types: \n{}'.format(user_type_counts))

    print('')

    while True:
        try:
    #  Display counts of gender and counts of NaN
            user_gender_count = df['Gender'].value_counts()
            nan_count_gender = df['Gender'].isnull().sum()
    #  Display earliest, most recent, and most common year of birth and counts of NaN
            earliest_yob = df['Birth Year'].describe()['min'].astype(int)
            most_recent_yob = df['Birth Year'].describe()['max'].astype(int)
            most_common_yob = df['Birth Year'].mode()[0].astype(int)
            nan_count_yob = df['Birth Year'].isnull().sum()
            print('User Genders: \n{} \nNote that you have {} missing data in the \'Gender\' column. \n\nThe earliest year of birth is: {} \nThe most recent year of birth is: {} \nThe most common year of birth is: {} \nNote that you have {} missing data in the \'Birth Year\' column.'.format(user_gender_count, nan_count_gender, earliest_yob, most_recent_yob, most_common_yob, nan_count_yob))
            break
        except: KeyError
        print('\nSorry, for this city \'Gender\' and \'Birth Year\' statistics are unavailable')
        break

    print('')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Asks the user to visualize the first five rows of data.
    Prompting and printing the next 5 rows at a time until the user chooses 'no'.
    """

    row_idx = 0
    question = input('Would you like to see the first five rows of data? y/n ').lower()
    while True:
        if question != 'y':
            break
        else:
            print(df.iloc[row_idx: row_idx + 5, 0:-5])
            row_idx = row_idx + 5
        question = input('\n Would you like to see five more rows of data? y/n ').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        print('-'*40)
        restart = input('\nWould you like to restart? y/n\n').lower()
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
