from datetime import date, timedelta

# Define the formatted date string
formatted_date_str = date.today().strftime("%Y-%m-%d")  # "2024-03-20" (assuming today's date)

# Parse the formatted string into a date object
date_obj = date.fromisoformat(formatted_date_str)

# Use timedelta to add one month
one_month_delta = timedelta(days = 31)  # Adjust for months with less than 31 days if needed

# Calculate the date one month ahead (considering potential adjustments)
next_month_date = date_obj + one_month_delta

# Handle cases where the next month might have less days than the current month's day
if next_month_date.day > date_obj.day:
  # Set the day to the last day of the next month
  next_month_date = next_month_date.replace(day=28)  # Start with 28 to handle February
  while next_month_date.month == date_obj.month + 1:  # Loop until it's actually next month
    next_month_date = next_month_date.replace(day=next_month_date.day - 1)

# Format the resulting date object back to the desired string
new_formatted_date_str = next_month_date.strftime("%Y-%m-%d")

# Print the new formatted date string
print(new_formatted_date_str)