from django.shortcuts import render
import random


def room(request, slug):
    datapoints = []
    datapoints2 = []
    count, y = 24, 5

    for i in range(count):
        y += round(5 + random.uniform(-5, 5))
        datapoints.append({"x": i, "y": y})
        datapoints2.append({"x": i+2, "y": y-3})


    return render(request, 'rooms/room.html', context={"datapoints": datapoints, "datapoints2": datapoints2})
