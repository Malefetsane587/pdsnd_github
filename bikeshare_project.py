import time
import pandas as pd
import json

CITY_DATA = { 'chicago': '/home/malefetsa/Desktop/all-project-files/chicago.csv',
              'new york city': '/home/malefetsa/Desktop/all-project-files/new_york_city.csv',
              'washington': '/home/malefetsa/Desktop/all-project-files/washington.csv' }

CITIES = list(CITY_DATA)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWhich city do you want to explore? Chicago, Washington or New York City: ').lower()
        if city in CITIES:
            break
        else:
            print('\nThis is city is not catered for. Please enter appropriate city.')

    # get user input for month (all, january, february, ... , june)
    month = input('\nWhich month would you like to filter by? Or type \'all\' to apply no filter: ').lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nWhich day would you like to filter by? Or type \'all\' to apply no filter: ').lower()

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from Start Time to create month column
    df['month'] = df['Start Time'].dt.month
    
    
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()] 

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # First convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # TO DO: display the most common month
    # extract month from the Start Time column to create a new month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular month
    popular_month = df['month'].mode()[0]
    print("\nPopular month", popular_month)

    # TO DO: display the most common day of week    
    # extract day from the Start Time column to create day of the week column
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # find the most popular day of the week
    popular_day = df['day_of_week'].mode()[0]
    print("\nPopular day", popular_day)


    # display the most common start hour
    #extract hour from the start time column to create an hour column
    df["hour"] = df["Start Time"].dt.hour

    #find most common hour from 0 to 23
    popular_hour = df["hour"].mode()[0]
    print("\nPopular hour", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print("\nPopular Start Station: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print("\nPopular End Station: ",popular_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("\nThe most commonly used start station and end station : {}, {}"\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("The total travel time is: ",total_travel_time)

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("\nThe mean travel time is: ",mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df["User Type"].value_counts()
    print("Counts of user types:\n",user_types_count)

    if "Gender" in df.columns:
        count_of_gender = df["Gender"].value_counts()
        print("\nCounts of gender:\n",count_of_gender)        
    
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_year = df["Birth Year"].min()
        print("\nEarliest birth year: ",earliest_year)
    
        most_recent_year = df["Birth Year"].max()
        print("\nRecent birth year: ",most_recent_year)    
    
        most_common_year = df["Birth Year"].mode()[0]
        print("\nMost common birth year: ",most_common_year)     


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    #display raw data in five rows at a time
    for i in range(0, row_length, 5):
        
        user_input = input('\nWould you like to see the Bikeshare raw data? Type \'yes\' or \'no\'\n ')
        if user_input.lower() != 'yes':
            break
        
        # retrieve and convert data to json format
        # split each json row data 
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            #print the raw data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
