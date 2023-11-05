from django.shortcuts import render
import random


def room(request, slug):
    datapoints = []
    count, y = 24, 5

    for i in range(count):
        y += round(5 + random.uniform(-5, 5))
        datapoints.append({"x": i, "y": y})

    print(datapoints)

    return render(request, 'rooms/room.html', context={"datapoints": datapoints})
