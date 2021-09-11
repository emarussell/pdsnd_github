import time
import datetime
import pandas as pd
import numpy as np

class colour:
   blue = '\033[94m'
   yellow = '\033[93m'
   red = '\033[91m'
   bold = '\033[1m'
   end = '\033[0m'


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city they want to analyse, followed by if they want to filter by month and day or return data for all days and months.

    Returns:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) day_month_filter - 'y' or 'n' depending on if user wants to specify a filter for month and day
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Enter the name of the city you want to view data for (Chicago, New York City or Washington): ")
            # Check if user input matches one of the three available cities. If it doesn't, ask the user to try again.
            if city.title() == 'Chicago' or city.title() == 'New York City' or city.title() == 'Washington':
                break
            else:
                print("Looks like that input wasn't one of the three cities, let's try again!")
        except:
            continue

    city = city.title()

    while True:
        try:    # Ask the user if they want to filter by month and day
            day_month_filter = input("\nWould you like to filter by month and day (y/n): ")

            # If user wants to filter month and day - ask them to provide a month or enter 'all' for all months
            if day_month_filter.lower() == 'y':

                # TO DO: get user input for month (all, january, february, ... , june)
                months = ['January','February','March','April','May','June','All']
                month = input("\nEnter the month you want to view (January to June), or enter 'All' to view data for all 6 months: ")

                # Check if user input is a valid month, if not, ask them to enter it again
                while  month.title() not in months:
                    month = input("Sorry, looks like that input wasn't quite right. Please enter a month from January to June, or enter 'All': ")

                month = month.title()

                # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
                days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
                day = input("\nEnter the day of the week you want to view, or enter 'All' to view data for all days: ")

                # Check if user input is a valid day, if not, ask them to enter it again
                while day.title() not in days:
                    day = input("Sorry, looks like that wasn't a valid input. Please enter a day of the week you want to view, or enter 'All': ")

                day = day.title()
                break

            # If user doesn't want to filter month and day - set month and day values to 'All'
            elif day_month_filter.lower() == 'n':
                month = 'All'
                day = 'All'
                break

            else: # Filter value wasn't valid, go back and ask to input again
                day_month_filter = print("Ooops, that didn't work. Let's try again!")
        except:
            continue

    # Set values based on validated user inputs
    month = month.title()
    day = day.title()
    day_month_filter = day_month_filter.lower()

    # Print a summary of the data to be analysed based on user inputs
    print('\n' + colour.blue + '-'*80 + colour.end)

    # User specified a month and day
    if day_month_filter == 'y' and month != 'All' and day != 'All':
        print("Thanks! Data displayed will be for "+ colour.red + "{}".format(city) + colour.end + " on " + colour.red + "{}'s".format(day) + colour.end + " during the month of " + colour.red + "{}".format(month) + colour.end + ".")

    # User selected all months and specified a day
    elif day_month_filter == 'y' and month == 'All' and day != 'All':
        print("Thanks, data displayed will be for " + colour.red + "{}".format(city) + colour.end + " on " + colour.red + "{}'s".format(day) + colour.end + " from " + colour.red + "January to June" + colour.end + ".")

    # User select a month and all days
    elif day_month_filter =='y' and month != 'All' and day == 'All':
        print("Thanks, data displayed will be for " + colour.red + "{}".format(city) + colour.end + " for " + colour.red + "all days" + colour.end + " during the month of " + colour.red + "{}".format(month) + colour.end + ".")

    # User chose not to filter, or selected all months and all days
    else:
        print("Thanks, data displayed will be for " + colour.red + "{}".format(city) + colour.end + " for " + colour.red + "all days" + colour.end + " from " + colour.red + "January to June" + colour.end + ".")

    print(colour.blue + '-'*80 + colour.end)

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
    # Select csv file based on city specified by user
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create additional columns for month, weekday name, hour and journey(start station to end station)
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    df['journey'] = df['Start Station'] + ' to ' + df['End Station']

    # Apply month filter if specified
    if month != 'All':
        months = ['January','February','March','April','May','June']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # Apply day filter if specified
    if day != 'All':

        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Returns:
        (float) time_stats_time_calculation - length of time taken to calculate time stats in seconds
    """

    print(colour.yellow + '\nMost Frequent Times of Travel Summary\n' + colour.end)

    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    # Convert month from interger to string
    months = ['January','February','March','April','May','June']
    popular_month_str = months[popular_month-1]

    print('Most Popular Month: ', popular_month_str)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Weekday: ', popular_day)

    # TO DO: display the most common start hour
    popular_hour = int(df['start_hour'].mode()[0])

    # Take 24 hour start hour and convert to 12 hour am/pm
    if popular_hour < 13:
        print("Most Popular Start Hour: {}am".format(popular_hour))
    else:
        print("Most Popular Start Hour: {}pm".format(popular_hour - 12))

    time_stats_calc_time = time.time() - start_time

    print('\n' + colour.blue + '-'*40 + colour.end)

    return time_stats_calc_time



def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Returns:
        (float) station_stats_time_calculation - length of time taken to calculate station stats in seconds
    """

    print(colour.yellow + '\nThe Most Popular Stations and Trips Summary\n' + colour.end)
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().index[0]
    popular_start_station_trips = df['Start Station'].value_counts().values[0]
    print('Most Popular Start Station: {} ({} journeys started from here)'.format(popular_start_station, popular_start_station_trips))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].value_counts().index[0]
    popular_end_station_trips = df['End Station'].value_counts().values[0]
    print('Most Popular End Station: {} ({} journeys ended here)'.format(popular_end_station, popular_end_station_trips))

    # TO DO: display most frequent combination of start station and end station trip
    popular_journey = df['journey'].value_counts().index[0]
    popular_journey_count = df['journey'].value_counts().values[0]
    print('Most Popular Journey: {} (it was made {} times)'.format(popular_journey, popular_journey_count))

    station_stats_calc_time = time.time() - start_time

    print('\n' + colour.blue + '-'*40 + colour.end)

    return station_stats_calc_time



def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Returns:
        (float) trip_stats_time_calculation - length of time taken to calculate trip duration stats in seconds
    """

    print(colour.yellow + '\nTrip Duration Summary\n' + colour.end)
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time_seconds = df['Trip Duration'].sum()
    # Convert total travel time in seconds to days, hours and minutes
    total_travel_time_days = int(total_travel_time_seconds // 86400)
    total_travel_time_hours = int((total_travel_time_seconds % 86400) // 3600)
    total_travel_time_minutes = int(((total_travel_time_seconds % 86400) % 3600) // 60)

    print('Total travel time is {} days, {} hours and {} minutes'.format(total_travel_time_days, total_travel_time_hours, total_travel_time_minutes))

    # TO DO: display mean travel time
    mean_travel_time_seconds = df['Trip Duration'].mean()
    # Convert mean travel time in seconds to minutes and seconds
    mean_travel_time_minutes = int(mean_travel_time_seconds // 60)
    mean_travel_time_seconds_r = int(mean_travel_time_seconds % 60)

    print('Average travel time is {} minutes and {} seconds'.format(mean_travel_time_minutes, mean_travel_time_seconds_r))

    # Get the average trip time by for each journey
    avg_journey_time = df.groupby(['journey'])['Trip Duration'].mean()
    dict_avg_journey_time = avg_journey_time.to_dict()

    # Sort the dictionary on value size, from shortest average trip time to longest
    sorted_avg_journey_time = sorted(dict_avg_journey_time.values())
    # Find quickest journey time and longest journeytime
    quickest_avg_journey_time = sorted_avg_journey_time[0]
    longest_avg_journey_time = sorted_avg_journey_time[-1]
    # Find the journeys with the quickest and longest times
    quickest_avg_journeys = [ dir for dir, avg_journey_time in dict_avg_journey_time.items() if avg_journey_time == quickest_avg_journey_time]
    longest_avg_journeys = [dir for dir, avg_journey_time in dict_avg_journey_time.items() if avg_journey_time == longest_avg_journey_time]

    # Print quickest average journey and convert time from seconds to minutes and seconds
    print("\nThe quickest average journey time is {} minute(s) and {} seconds, between the following stations:".format(int(quickest_avg_journey_time // 60), int(quickest_avg_journey_time % 60)))

    for quickest_avg_journey in quickest_avg_journeys:
        print(quickest_avg_journey)

    # Print longest average journey and convert time from seconds to hours, minutes and seconds
    print("\nThe longest average journey time is {} hour(s) {} minutes and {} seconds between the following stations:".format(int(longest_avg_journey_time // 3600), int((longest_avg_journey_time % 3600) // 60), int((longest_avg_journey_time % 3600) % 60)))

    for longest_avg_journey in longest_avg_journeys:
        print(longest_avg_journey)

    trip_stats_calc_time = time.time() - start_time

    print('\n' + colour.blue + '-'*40 + colour.end)

    return trip_stats_calc_time



def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Returns:
        (float) user_stats_time_calculation - length of time taken to calculate user stats in seconds
    """

    print(colour.yellow + '\nUsers Summary\n' + colour.end)
    start_time = time.time()

    # If city is Washington let user know user stats aren't available
    if city.title() == 'Washington':
        print ("Sorry User Stats aren't available for Washington")

    else:
        # TO DO: Display counts of user types
        print(colour.bold + "Count of Users by Type" + colour.end)
        user_types = df['User Type'].value_counts()
        dict_user_types = user_types.to_dict()
        for key, value in dict_user_types.items():
            print("{}: {}".format(key,value))

        # TO DO: Display counts of gender
        print(colour.bold + "\nCount of Users by Gender" + colour.end)
        gender = df['Gender'].value_counts()
        dict_gender = gender.to_dict()
        for key, value in dict_gender.items():
            print("{}: {}".format(key, value))

        # TO DO: Display earliest, most recent, and most common year of birth
        min_birth = int(df['Birth Year'].min())
        max_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])

        #Get current year to calculate age of users
        current_date = datetime.date.today()
        current_year = current_date.year

        oldest_user = current_year - min_birth
        youngest_user = current_year - max_birth
        common_user = current_year - common_birth

        print("\nEarliest Birth Year is: {} (making the oldest user {} years old)".format(min_birth, oldest_user))

        if youngest_user == 0:
            print("Most recent Birth Year is: {} (making the youngest user less than a year old)".format(max_birth))
        else:
            print("Most Recent Birth Year is: {} (making the youngest user {} years old)".format(max_birth, youngest_user))

        print("Most common year of birth is: {} (making {} the most common age of users)".format(common_birth, common_user))

    user_stats_calc_time =  time.time() - start_time

    print('\n' + colour.blue + '-'*40 + colour.end)

    return user_stats_calc_time



def calculation_times(time_stats_calc_time, station_stats_calc_time, trip_stats_calc_time, user_stats_calc_time):
    """Displays calculation times for each summary block

       Args:
        (float) time_stats_calc_time - time taken in seconds to calculate travel times summary
        (float) station_stats_calc_time - time taken in seconds to calculate station and trips summary
        (float) trip_stats_calc_time - time taken in seconds to calculate trip duration summary
        (float) user_stats_calc_time - time taken in seconds to calculate users summary
        (float) gender_stats_calc_time - time taken in seconds to calculate users summary
    """

    print(colour.yellow + "\nThis is how long it took to calculate each summary\n" + colour.end)

    # Print the calculation time for each section
    print("Travel times summary: {} seconds".format(round(time_stats_calc_time,3)))
    print("Station and Trips summary: {} seconds".format(round(station_stats_calc_time,3)))
    print("Trip Duration summary: {} seconds".format(round(trip_stats_calc_time,3)))
    print("Users summary: {} seconds".format(round(user_stats_calc_time,3)))

    print('\n' + colour.blue + '-'*40 + colour.end)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats_calc_time = time_stats(df)
        station_stats_calc_time = station_stats(df)
        trip_stats_calc_time = trip_duration_stats(df)
        user_stats_calc_time = user_stats(df,city)

        calculation_times(time_stats_calc_time, station_stats_calc_time, trip_stats_calc_time, user_stats_calc_time)

        answers = ['yes','no']
        # Ask if user wants to view a sample set of the data. If yes, then print top 5 rows
        view_sample = input('\nWould you like to view a sample set of data? Enter yes or no.\n')
        while view_sample.lower() not in answers:
            view_sample = input('Sorry, not sure what you meant with that response, please enter either yes or no.\n')

        view_sample = view_sample.lower()

        # Get the number of rows in the data frame and set the start and end index
        rows = len(df)
        row_start = 0
        row_end = 5

        # If user asked to see data, display 5 rows of data and increase start and end index by 5
        while view_sample.lower() == 'yes':
            print(df.iloc[row_start:row_end])
            row_start += 5
            row_end += 5

            #Check if reached the end of the df, if so let user know
            if row_start > rows:
                print(colour.red + '\nSorry there\'s no more data to display!'+ colour.end)
                break

            # Ask user if they want to view more data
            view_sample = input('\nWould you like to view another 5 rows of data? Enter yes or no.\n')
            # Validate user input, should be yes or now
            while view_sample.lower() not in answers:
                view_sample = input ('Sorry, not sure what you meant with that response, please enter either yes or no.\n')

            view_sample = view_sample.lower()
            # If user entered yes, restart loop and display another 5 rows of data, if no then exit
            if view_sample == 'no':
               break


        # Ask if user wants to restart, and either exit or restart based on response
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in answers:
            restart = input('Sorry, not sure what you meant with that response, please enter either yes or no.\n')

        restart = restart.lower()

        if restart == 'no':
            break
        else:
            print('\nGreat - let\'s look at some more data\n')
            print(colour.blue + '-'*40 + colour.end)


if __name__ == "__main__":
	main()
