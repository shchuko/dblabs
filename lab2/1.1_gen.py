from faker import Faker
import random
import hashlib
import re

from pathlib import Path
from datetime import datetime as dt
from datetime import timedelta

fake = Faker()

# Users generator

users_total = 15
users = []
for i in range(users_total):
  name = fake.name()
  phone = fake.phone_number()
  email = fake.email()
  pass_hash = hashlib.sha256(str(random.randint(-10000000,100000000)).encode()).hexdigest()

  result = f"{i};{name};{phone};{email};{pass_hash};"
  users.append(result)


# Addresses generator
addresses = []
for i in range(0, users_total):
  userid = i % users_total
  name = fake.last_name()
  zip = fake.postcode()
  country = fake.country()
  city = fake.city()
  street = fake.street_name()
  building = fake.building_number()
  room = fake.building_number()
  notes = name + " address notes"
  result = f"{i};{userid};{name};{zip};{country};{city};{street};{building};{room};{notes}"
  addresses.append(result)

# Restaurants generator
restaurants_cnt = 10
restaurants = []
for i in range(0, restaurants_cnt):
  name = fake.last_name()
  phone = fake.phone_number()
  country = fake.country()
  city = fake.city()
  street = fake.street_name()
  building = fake.building_number()
  description = fake.job()

  result = f"{i};{name};{phone};{country};{city};{street};{building};{description}"
  restaurants.append(result)

# Menus generator
menu_cnt = restaurants_cnt * 3
menus = []
for i in range(0, menu_cnt):
    name = fake.last_name_female() + " Menu"
    description = name + " Description"
    rest_id = i % restaurants_cnt
    result = f"{i};{rest_id};{name};{description}"
    menus.append(result)

# Meals generator
meals_cnt = menu_cnt * 2
meals = []
for i in range(0, 20):
    name = fake.first_name() + " Meal"
    description = name + " Description"

    result = f"{i};{name};{description}"
    meals.append(result)

# MenuMeal generator
menu_meal = []
for i in range(0, 20):
    menu_id = i % menu_cnt
    meal_id = i % meals_cnt
    price = random.randint(100, 5000)

    result = f"{menu_id};{meal_id};{price}"
    menu_meal.append(result)

# Orders generator
orders_cnt = users_total * 2
orders = []
for i in range(0, orders_cnt):
  order_id = i
  user_id = i % users_total
  address_id = list(filter(lambda address: address.split(';')[1] == str(user_id), addresses))[0].split(';')[0]
  restaurant_id = i % restaurants_cnt
  status_id = 2 if i < (orders_cnt / 2) else 1
  creation_date = timestamp=(dt.now() - timedelta(days=100) + timedelta(days=(i * 2))).strftime('%Y-%m-%d %H:%M:%S.%f0')
  total_price = 0
  notes = 'foo bar'

  result = f"{order_id};{user_id};{address_id};{restaurant_id};{status_id};{creation_date};{total_price};{notes}"
  orders.append(result)

# Order entries generator
order_entries = []
for i in range(0, orders_cnt):
  order_id = i % orders_cnt
  accepted_menus = list(filter(lambda menu : menu.split(';')[1] == orders[order_id].split(';')[3], menus))
  accepted_meals = []
  for menu in accepted_menus:
    accepted_meals += list(filter(lambda menu_meal: menu_meal.split(';')[0] == menu.split(';')[0], menu_meal))

  for j in range(0, random.randint(1, len(accepted_meals))):
    meal = accepted_meals[j]
    meal_id = meal.split(';')[0]
    price = meal.split(';')[2]
    result = f"{order_id};{meal_id};{price}"
    order_entries.append(result)

# Restaurant <-> kitechen type generator

kitchen_first_id = 1
kitchen_types_len = 3
restaurant_kitchen = []
for i in range(restaurants_cnt):
  restaurant_id = restaurants[i].split(';')[0]
  for j in range(0, random.randint(1, kitchen_types_len)):
    kitchen_type_id = j + kitchen_first_id
    result = f"{restaurant_id};{kitchen_type_id}"
    restaurant_kitchen.append(result)

# Create dir
Path("csvs").mkdir(parents=True, exist_ok=True)

# Write generated values
with open('csvs/1_users.csv', 'w') as users_file:
  print('id;name;phone;email;password_hash;favourite_address', file=users_file)
  for user in users:
    print(user, file=users_file)

with open('csvs/2_addresses.csv', 'w') as addresses_file:
  print('id;user_id;name;zip_code;country;city;street;building;room;notes', file=addresses_file)
  for address in addresses:
    print(address, file=addresses_file)


with open('csvs/3_restaurants.csv', 'w') as restaurants_file:
  print('id;name;phone;country;city;street;building;description', file=restaurants_file)
  for restaurant in restaurants:
    print(restaurant, file=restaurants_file)

with open('csvs/4_menus.csv', 'w') as menus_file:
  print('id;name;description', file=menus_file)
  for menu in menus:
    print(menu, file=menus_file)

with open('csvs/5_meals.csv', 'w') as meals_file:
  print('id;name;description', file=meals_file)
  for meal in meals:
    print(meal, file=meals_file)

with open('csvs/6_menu_meal.csv', 'w') as menu_meal_file:
  print('menu_id;meal_id;price', file=menu_meal_file)
  for it in menu_meal:
    print(it, file=menu_meal_file)


with open('csvs/7_restaurant_kitchen.csv', 'w') as restaurant_kitchen_file:
  print('restaurant_id;kitchen_id', file=restaurant_kitchen_file)
  for en in restaurant_kitchen:
    print(en, file=restaurant_kitchen_file)

with open('csvs/8_orders.csv', 'w') as orders_file:
  print('id;user_id;address_id;restaurant_id;status_id;creation_date;total_price;notes', file=orders_file)
  for order in orders:
    print(order, file=orders_file)

with open('csvs/9_order_entries.csv', 'w') as order_entries_file:
  print('order_id;meal_id;price', file=order_entries_file)
  for en in order_entries:
    print(en, file=order_entries_file)
