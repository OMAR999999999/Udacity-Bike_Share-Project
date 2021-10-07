import time
import pandas as pd
import datetime

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US BikeShare data!')
    # getting user input for city (chicago, new york city, washington)
    while True:
        city = input("\nType the City name? (Chicago , New York or Washington)\n").title()
        if city not in CITY_DATA:
            print("It sounds like you've chosen an invalid City-Name or made a spelling mistake, Please Try Again!")
        else:
            break

    # getting user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month?(January, February, March, April, May, June, or 'All'\n").title()
        if month not in ["January", "February", "March", "April", "May", "June", "All"]:
            print("It sounds like you've chosen an invalid Month-Name or made a spelling mistake, Please Try Again!")
        else:
            break
    # getting user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day? (Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or All)\n").title()
        if day not in ("Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "All"):
            print("It sounds like you've chosen an invalid Day-Name or made a spelling mistake, Please Try Again!")
        else:
            break

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
    # loading Data-File into a Data-Frame
    df = pd.read_csv(CITY_DATA[city])
    # converting "Start Time" column to a "data time"
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extracting data from "Start Time" column to make new columns(month, weekday, hour)
    df["month"] = df["Start Time"].dt.month
    df["day"] = df["Start Time"].dt.day_name()
    df["hour"] = df["Start Time"].dt.hour

    # filtering applicable month & day
    if month != "All":
        months_list = ["January", "February", "March", "April", "May", "June"]
        month = months_list.index(month)+1
        df = df[df["month"] == month]

    if day != "All":
        df = df[df["day"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extracting the most common month
    common_mon = df["month"].mode()[0]
    common_months_list = ["January", "February", "March", "April", "May", "June"]
    common_month_name = common_months_list[common_mon - 1]
    print("The most common month is : ", common_mon, "(", common_month_name, ")")

    # extracting the most common day of week
    common_day = df["day"].mode()[0]
    print("The most common day of week is : ", common_day)

    # extracting the most common start hour
    common_hour = df["hour"].mode()[0]
    print("the most common start hour is : ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    start_station = df["Start Station"].mode()[0]
    start_station_count = df["Start Station"].value_counts()
    print("most commonly used start station is : ", start_station, "\n", start_station_count)

    # most commonly used end station
    end_station = df["End Station"].mode()[0]
    end_station_counts = df["End Station"].value_counts()
    print("\nmost commonly used end station is : ", end_station, "\n", end_station_counts)

    # most frequent combination of start station and end station trip
    common_journey = (df["Start Station"] + df["End Station"]).mode()[0]
    print("most frequent combination of start station and end station trip is : ", common_journey)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    total_travel_time_sec = df["Trip Duration"].sum()
    total_travel_time = str(datetime.timedelta(seconds=int(total_travel_time_sec)))
    print("total travel time is : ", total_travel_time)
    print("total travel time in seconds is : ", total_travel_time_sec, " Seconds", "\n")

    # mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("mean travel time is (Sec): ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on BikeShare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # counts of user types
    print("User Types : ")
    user_types = df["User Type"].value_counts()
    print(user_types)

    try:
        # counts of gender
        gender_count = df["Gender"].value_counts()
        print("Gender Stats : ")
        print(gender_count)

        # earliest, most recent, and most common year of birth
        oldest_birth = df["Birth Year"].min()
        youngest_birth = df["Birth Year"].max()
        common_birth = df["Birth Year"].mode()[0]
        print("\nDate Of Birth Of Oldest Users : ", int(oldest_birth))
        print("Date Of Birth Of Youngest Users : ", int(youngest_birth))
        print("Most Common Year Of Birth : ", int(common_birth))
    except KeyError:  # washington
        print("No Data For : Gender/Birth")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
