
hunter_green = (13,143,50)
black =        (20,20,20)
light_gray =   (75,75,75)
lighter_gray = (224, 223, 215)
popcorn =      (219, 206, 131)
brown =        (89,46,12)
safe_blue =    (15, 65, 150)
yellow =       (255, 213, 0)

# TODO refactor functions to be `get_something()`
def dark_gray(time_of_day=None):
    if time_of_day == None:
        return dark_gray_morning
    elif time_of_day == "morning":
        return dark_gray_morning
    elif time_of_day == "afternoon":
        return dark_gray_afternoon
    elif time_of_day == "evening":
        return dark_gray_evening
    elif time_of_day == "night":
        return dark_gray_night
    else:
        raise("no color for time of day {}".format(time_of_day))

def white(time_of_day=None):
    if time_of_day == None:
        return white_morning
    elif time_of_day == "morning":
        return white_morning
    elif time_of_day == "afternoon":
        return white_afternoon
    elif time_of_day == "evening":
        return white_evening
    elif time_of_day == "night":
        return white_night
    else:
        raise("no color for time of day {}".format(time_of_day))

def red(time_of_day=None):
    if time_of_day == None:
        return red_morning
    if time_of_day == "morning":
        return red_morning
    elif time_of_day == "afternoon":
        return red_afternoon
    elif time_of_day == "evening":
        return red_evening
    elif time_of_day == "night":
        return red_night
    else:
        raise("no color for time of day {}".format(time_of_day))

def blue(time_of_day=None):
    if time_of_day == None:
        return blue_morning
    elif time_of_day == "morning":
        return blue_morning
    elif time_of_day == "afternoon":
        return blue_afternoon
    elif time_of_day == "evening":
        return blue_evening
    elif time_of_day == "night":
        return blue_night
    else:
        raise("no color for time of day {}".format(time_of_day))

def green(time_of_day=None):
    if time_of_day == None:
        return green_morning
    elif time_of_day == "morning":
        return green_morning
    elif time_of_day == "afternoon":
        return green_afternoon
    elif time_of_day == "evening":
        return green_evening
    elif time_of_day == "night":
        return green_night
    else:
        raise("no color for time of day {}".format(time_of_day))

def dark_green(time_of_day=None):
    if time_of_day == None:
        return dark_green_morning
    elif time_of_day == "morning":
        return dark_green_morning
    elif time_of_day == "afternoon":
        return dark_green_afternoon
    elif time_of_day == "evening":
        return dark_green_evening
    elif time_of_day == "night":
        return dark_green_night
    else:
        raise("no color for time of day {}".format(time_of_day))
        
def orange(time_of_day=None):
    if time_of_day == None:
        return orange_morning
    elif time_of_day == "morning":
        return orange_morning
    elif time_of_day == "afternoon":
        return orange_afternoon
    elif time_of_day == "evening":
        return orange_evening
    elif time_of_day == "night":
        return orange_night
    else:
        raise("no color for time of day {}".format(time_of_day))


dark_gray_morning = (31,31,31)
white_morning = (224, 223, 215)
red_morning = (248, 37, 103)
blue_morning = (164, 118, 255)
green_morning = (156, 222, 41)
dark_green_morning = (31, 57, 31)
orange_morning = (253, 140, 29)

dark_gray_night = (28,32,51)
white_night = (188,204,204)
red_night = (116,83,147)
blue_night = (111,115,155)
green_night = (160,189,160)
orange_night = (139,131,117)
dark_green_night = (42,51,59)

dark_gray_afternoon = (31,25,13)
white_afternoon = (255,252,200)
red_afternoon = (255,0,70)
blue_afternoon = (188,112,212)
green_afternoon = (171,222,0)
orange_afternoon = (255,132,0)
dark_green_afternoon = (29,54,5)

dark_gray_evening = (50,27,5)
white_evening = (255,231,97)
red_evening = (255,76,39)
blue_evening = (228,114,85)
green_evening = (252,196,45)
orange_evening = (255,137,37)
dark_green_evening = (61,49,8)
