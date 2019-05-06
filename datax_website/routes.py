from datax_website import app
from flask import render_template, url_for, request, redirect, jsonify

rides_and_playgrounds = [
    "'It's a small world'",
    "A Pirate's Adventure - Treasures of the Seven Seas",
    "Astro Orbiter",
    "Big Thunder Mountain Railroad",
    "Buzz Lightyear's Space Ranger Spin",
    "Casey Jr. Splash 'N' Soak Station",
    "Cinderella Castle",
    "Country Bear Jamboree",
    "Dumbo the Flying Elephant",
    "Enchanted Tales with Belle",
    "Frontierland Shootin Arcade",
    "Haunted Mansion",
    "Jungle Cruise ",
    "Liberty Square Riverboat ",
    "Mad Tea Party ",
    "Main Street Vehicles ",
    "Mickey's PhilharMagic ",
    "Monsters, Inc Laugh Floor ",
    "Peter Pan's Flight ",
    "Pirate and Princess Adventures at Walt Disney World ",
    "Pirates at Walt Disney World ",
    "Pirates at Walt Disney World Resort ",
    "Pirates of the Caribbean ",
    "Play Disney Parks ",
    "Prince Charming Regal Carrousel ",
    "Seven Dwarfs Mine Train  ",
    "Sorcerers of the Magic Kingdom ",
    "Space Mountain ",
    "Splash Mountain ",
    "Swiss Family Treehouse ",
    "The Barnstormer ",
    "The Hall of Presidents ",
    "The Magic Carpets of Aladdin ",
    "The Many Adventures of Winnie the Pooh ",
    "Tom Sawyer Island ",
    "Tomorrowland Transit Authority PeopleMover ",
    "Under the Sea - Journey of The Little Mermaid ",
    "Walt Disney World Railroad - Fantasyland ",
    "Walt Disney World Railroad - Frontierland ",
    "Walt Disney World Railroad - Main Street U.S.A. ",
    "Walt Disney's Carousel of Progress ",
    "Walt Disney's Enchanted Tiki Room"
]

rides = [
    "A Pirate's Adventure - Treasures of the Seven Seas",
    "Astro Orbiter",
    "Big Thunder Mountain Railroad",
    "Buzz Lightyear's Space Ranger Spin",
    "Country Bear Jamboree",
    "Dumbo the Flying Elephant",
    "Enchanted Tales with Belle",
    "Haunted Mansion",
    "It's A Small World",
    "Jungle Cruise",
    "Liberty Square Riverboat",
    "Mad Tea Party",
    "Mickey's PhilharMagic",
    "Monsters, Inc. Laugh Floor",
    "Peter Pan's Flight",
    "Pirates of the Caribbean",
    "Prince Charming Regal Carrousel",
    "Seven Dwarfs Mine Train",
    "Space Mountain",
    "Splash Mountain",
    "The Barnstormer",
    "The Hall of Presidents",
    "The Magic Carpets of Aladdin",
    "The Many Adventures of Winnie the Pooh",
    "Tomorrowland Speedway",
    "Tomorrowland Transit Authority PeopleMover",
    "Under the Sea - Journey of The Little Mermaid",
    "Walt Disney's Carousel of Progress",
    "Walt Disney's Enchanted Tiki Room",
]


def query_api(datetime, ride, fastpass):
    import json
    import requests
    import pandas as pd
    import numpy as np
    from dateutil import parser
    import time

    header = {"Content-Type": "application/json", "Accept": "application/json"}

    # 42 Rides
    message_array = np.zeros(42, dtype=np.int)
    # Set one hot
    message_array[int(ride)] = 1
    # Insert WaltDisney Land
    message_array = np.insert(message_array, 0, 1)
    # Insert RideActive
    message_array = np.append(message_array, 1)
    # Insert FastPass+
    message_array = np.append(message_array, int(fastpass))

    dt = parser.parse(datetime)
    # Minute of day
    message_array = np.append(message_array, dt.minute)
    print(dt.minute)
    # Hour of day
    message_array = np.append(message_array, dt.hour)
    print(dt.hour)
    # Day of week
    message_array = np.append(message_array, dt.weekday())
    print(dt.weekday())
    # Day of month
    message_array = np.append(message_array, dt.day)
    print(dt.day)
    # Month of year
    message_array = np.append(message_array, dt.month)
    print(dt.month)
    # Unix time
    message_array = np.append(message_array, int(time.mktime(dt.timetuple())))
    print(int(time.mktime(dt.timetuple())))

    # 2 zeroes (federal and school holiday)
    message_array = np.append(message_array, 0)
    message_array = np.append(message_array, 0)

    # format the message
    print(message_array.reshape(1, -1).tolist())

    send_test = message_array.reshape(1, -1).tolist()
    json_file = "file.json"
    json_data = json.dumps(send_test)
    print(json_data)

    resp = requests.post("http://35.236.127.51:5000/", data=json_data, headers=header)

    return resp.json()


@app.route("/")
@app.route("/home")
def home():

    return render_template("home.html", data=rides)


@app.route("/schedule")
def schedule():

    return render_template("schedule.html", data=rides)


@app.route("/ride_statistics")
def ride_statistics():

    return render_template("ride_statistics.html", data=rides)

@app.route("/monthly_statistics")
def monthly_statistics():

    return render_template("monthly_statistics.html", data=rides)



@app.route("/query_wait_time", methods=["POST"])
def query_wait_time():
    print(
        "###############################################################################################"
    )
    print(request.method)
    print(request.get_json())
    datetime = request.get_json().get("datetime")
    ride = request.get_json().get("ride")
    fastpass = request.get_json().get("fastpass")

    query_response = str(query_api(datetime, ride, fastpass))
    print("Query Api Response: " + query_response)

    print(
        "###############################################################################################"
    )
    return query_response


@app.route("/query/<genre>")
def query(genre):
    if genre == "Interactive":
        return jsonify({"rides": ["26", "6", "0", "3"]})
    if genre == "Slow":
        return jsonify({"rides": ["15", "16", "24", "25", "27", "22", "23", "14", "10", "9", "1", "8", "5"]})
    if genre == "Thrill":
        return jsonify({"rides": ["17", "2", "18", "19", "7", "20", "11"]})
    if genre == "Show":
        return jsonify({"rides": ["28", "21", "4", "12", "13"]})

