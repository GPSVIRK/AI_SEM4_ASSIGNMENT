# ============================================================
# AI TRAVEL PLANNER
# ============================================================
# Features:
# 1. Destination Knowledge Base
# 2. Food Recommendation System
# 3. Hotel Recommendation System
# 4. Personalized Itinerary Generation
# 5. Cost Assessment
# ============================================================

from dataclasses import dataclass


# KB

DESTINATIONS = {
    "Goa": {
        "places": [
            "Calangute Beach",
            "Baga Beach",
            "Fort Aguada",
            "Dudhsagar Falls"
        ],
        "foods": [
            "Goan Fish Curry",
            "Prawn Balchao",
            "Bebinca"
        ],
        "hotels": [
            ("Budget Inn Goa", 2000),
            ("Sea View Resort", 5000),
            ("Luxury Beach Palace", 10000)
        ]
    },

    "Jaipur": {
        "places": [
            "Amber Fort",
            "Hawa Mahal",
            "City Palace",
            "Jantar Mantar"
        ],
        "foods": [
            "Dal Baati Churma",
            "Laal Maas",
            "Ghewar"
        ],
        "hotels": [
            ("Pink City Lodge", 1800),
            ("Royal Heritage Hotel", 4500),
            ("Maharaja Palace Resort", 9000)
        ]
    },

    "Kerala": {
        "places": [
            "Munnar",
            "Alleppey Backwaters",
            "Wayanad",
            "Kovalam Beach"
        ],
        "foods": [
            "Appam",
            "Kerala Fish Curry",
            "Puttu"
        ],
        "hotels": [
            ("Green Valley Stay", 2500),
            ("Backwater Resort", 6000),
            ("Luxury Lake Palace", 12000)
        ]
    }
}


# user profile

@dataclass
class UserProfile:
    name: str
    destination: str
    days: int
    budget: int
    food_preference: str
    hotel_type: str


# hotel reccomendation

def recommend_hotel(destination, hotel_type):

    hotels = DESTINATIONS[destination]["hotels"]

    if hotel_type.lower() == "budget":
        return hotels[0]

    elif hotel_type.lower() == "standard":
        return hotels[1]

    else:
        return hotels[2]


# food recommendation

def recommend_food(destination):

    return DESTINATIONS[destination]["foods"]


# tourplan gen

def generate_itinerary(destination, days):

    attractions = DESTINATIONS[destination]["places"]

    itinerary = {}

    index = 0

    for day in range(1, days + 1):

        day_places = []

        for _ in range(2):

            if index < len(attractions):
                day_places.append(attractions[index])
                index += 1

        itinerary[f"Day {day}"] = day_places

    return itinerary


# cost estimation

def estimate_cost(destination, days, hotel_type):

    hotel_name, hotel_cost = recommend_hotel(
        destination,
        hotel_type
    )

    accommodation_cost = hotel_cost * days

    food_cost = 1000 * days

    local_transport = 500 * days

    sightseeing = 700 * days

    total = (
        accommodation_cost
        + food_cost
        + local_transport
        + sightseeing
    )

    return total


# main travel planner

def create_travel_plan(profile):

    destination = profile.destination

    print("\n==============================")
    print(" AI TRAVEL PLAN ")
    print("==============================")

    print(f"\nTraveller: {profile.name}")
    print(f"Destination: {destination}")
    print(f"Trip Duration: {profile.days} Days")
    print(f"Budget: ₹{profile.budget}")

    # Hotel Recommendation

    hotel_name, hotel_cost = recommend_hotel(
        destination,
        profile.hotel_type
    )

    print("\nRecommended Hotel:")
    print(f"  {hotel_name}")
    print(f"  ₹{hotel_cost}/night")

    # Food Recommendation

    foods = recommend_food(destination)

    print("\nRecommended Local Foods:")

    for food in foods:
        print(f"  - {food}")

    # Itinerary

    itinerary = generate_itinerary(
        destination,
        profile.days
    )

    print("\nSuggested Itinerary:")

    for day, places in itinerary.items():

        print(day)

        for place in places:
            print(f"   • {place}")

    # Cost Estimation

    total_cost = estimate_cost(
        destination,
        profile.days,
        profile.hotel_type
    )

    print("\nEstimated Trip Cost:")
    print(f"₹{total_cost}")

    if total_cost <= profile.budget:
        print("Trip is within budget.")
    else:
        print("Trip exceeds budget.")

    print("\n==============================\n")


# TEST CASES

def test_case_1():

    user = UserProfile(
        name="Rahul",
        destination="Goa",
        days=3,
        budget=25000,
        food_preference="Seafood",
        hotel_type="Standard"
    )

    create_travel_plan(user)


def test_case_2():

    user = UserProfile(
        name="Priya",
        destination="Jaipur",
        days=2,
        budget=15000,
        food_preference="Vegetarian",
        hotel_type="Budget"
    )

    create_travel_plan(user)


def test_case_3():

    user = UserProfile(
        name="Arjun",
        destination="Kerala",
        days=5,
        budget=70000,
        food_preference="Mixed",
        hotel_type="Luxury"
    )

    create_travel_plan(user)


# ============================================================
# DRIVER
# ============================================================

if __name__ == "__main__":

    print("Running Test Case 1")
    test_case_1()

    print("Running Test Case 2")
    test_case_2()

    print("Running Test Case 3")
    test_case_3()# ============================================================
# AI TRAVEL PLANNER
# ============================================================
# Features:
# 1. Destination Knowledge Base
# 2. Food Recommendation System
# 3. Hotel Recommendation System
# 4. Personalized Itinerary Generation
# 5. Cost Assessment
# ============================================================

from dataclasses import dataclass
from typing import List


# ============================================================
# KNOWLEDGE BASE
# ============================================================

DESTINATIONS = {
    "Goa": {
        "places": [
            "Calangute Beach",
            "Baga Beach",
            "Fort Aguada",
            "Dudhsagar Falls"
        ],
        "foods": [
            "Goan Fish Curry",
            "Prawn Balchao",
            "Bebinca"
        ],
        "hotels": [
            ("Budget Inn Goa", 2000),
            ("Sea View Resort", 5000),
            ("Luxury Beach Palace", 10000)
        ]
    },

    "Jaipur": {
        "places": [
            "Amber Fort",
            "Hawa Mahal",
            "City Palace",
            "Jantar Mantar"
        ],
        "foods": [
            "Dal Baati Churma",
            "Laal Maas",
            "Ghewar"
        ],
        "hotels": [
            ("Pink City Lodge", 1800),
            ("Royal Heritage Hotel", 4500),
            ("Maharaja Palace Resort", 9000)
        ]
    },

    "Kerala": {
        "places": [
            "Munnar",
            "Alleppey Backwaters",
            "Wayanad",
            "Kovalam Beach"
        ],
        "foods": [
            "Appam",
            "Kerala Fish Curry",
            "Puttu"
        ],
        "hotels": [
            ("Green Valley Stay", 2500),
            ("Backwater Resort", 6000),
            ("Luxury Lake Palace", 12000)
        ]
    }
}


# ============================================================
# USER PROFILE
# ============================================================

@dataclass
class UserProfile:
    name: str
    destination: str
    days: int
    budget: int
    food_preference: str
    hotel_type: str


# ============================================================
# HOTEL RECOMMENDATION
# ============================================================

def recommend_hotel(destination, hotel_type):

    hotels = DESTINATIONS[destination]["hotels"]

    if hotel_type.lower() == "budget":
        return hotels[0]

    elif hotel_type.lower() == "standard":
        return hotels[1]

    else:
        return hotels[2]


# ============================================================
# FOOD RECOMMENDATION
# ============================================================

def recommend_food(destination):

    return DESTINATIONS[destination]["foods"]


# ============================================================
# TOUR PLAN GENERATION
# ============================================================

def generate_itinerary(destination, days):

    attractions = DESTINATIONS[destination]["places"]

    itinerary = {}

    index = 0

    for day in range(1, days + 1):

        day_places = []

        for _ in range(2):

            if index < len(attractions):
                day_places.append(attractions[index])
                index += 1

        itinerary[f"Day {day}"] = day_places

    return itinerary


# ============================================================
# COST ESTIMATION
# ============================================================

def estimate_cost(destination, days, hotel_type):

    hotel_name, hotel_cost = recommend_hotel(
        destination,
        hotel_type
    )

    accommodation_cost = hotel_cost * days

    food_cost = 1000 * days

    local_transport = 500 * days

    sightseeing = 700 * days

    total = (
        accommodation_cost
        + food_cost
        + local_transport
        + sightseeing
    )

    return total


# ============================================================
# MAIN TRAVEL PLANNER
# ============================================================

def create_travel_plan(profile):

    destination = profile.destination

    print("\n==============================")
    print(" AI TRAVEL PLAN ")
    print("==============================")

    print(f"\nTraveller: {profile.name}")
    print(f"Destination: {destination}")
    print(f"Trip Duration: {profile.days} Days")
    print(f"Budget: ₹{profile.budget}")

    # Hotel Recommendation

    hotel_name, hotel_cost = recommend_hotel(
        destination,
        profile.hotel_type
    )

    print("\nRecommended Hotel:")
    print(f"  {hotel_name}")
    print(f"  ₹{hotel_cost}/night")

    # Food Recommendation

    foods = recommend_food(destination)

    print("\nRecommended Local Foods:")

    for food in foods:
        print(f"  - {food}")

    # Itinerary

    itinerary = generate_itinerary(
        destination,
        profile.days
    )

    print("\nSuggested Itinerary:")

    for day, places in itinerary.items():

        print(day)

        for place in places:
            print(f"   • {place}")

    # Cost Estimation

    total_cost = estimate_cost(
        destination,
        profile.days,
        profile.hotel_type
    )

    print("\nEstimated Trip Cost:")
    print(f"₹{total_cost}")

    if total_cost <= profile.budget:
        print("Trip is within budget.")
    else:
        print("Trip exceeds budget.")

    print("\n==============================\n")


# ============================================================
# TEST CASES
# ============================================================

def test_case_1():

    user = UserProfile(
        name="Rahul",
        destination="Goa",
        days=3,
        budget=25000,
        food_preference="Seafood",
        hotel_type="Standard"
    )

    create_travel_plan(user)


def test_case_2():

    user = UserProfile(
        name="Priya",
        destination="Jaipur",
        days=2,
        budget=15000,
        food_preference="Vegetarian",
        hotel_type="Budget"
    )

    create_travel_plan(user)


def test_case_3():

    user = UserProfile(
        name="Arjun",
        destination="Kerala",
        days=5,
        budget=70000,
        food_preference="Mixed",
        hotel_type="Luxury"
    )

    create_travel_plan(user)


# ============================================================
# DRIVER
# ============================================================

if __name__ == "__main__":

    print("Running Test Case 1")
    test_case_1()

    print("Running Test Case 2")
    test_case_2()

    print("Running Test Case 3")
    test_case_3()
