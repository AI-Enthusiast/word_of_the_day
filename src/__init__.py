from .scraper import create_image as create_wotd_image


def display_wotd(inky_display, display_color):
    print("Displaying word of the day")
    return create_wotd_image(inky_display, display_color)