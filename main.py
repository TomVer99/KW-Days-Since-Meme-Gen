import datetime
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from typing import Union

SAVE_FILE = "save.txt"
KIOWA_WARRIOR_FIRST_FLIGHT = "1983-10-06"

def read_from_save_file() -> Union[datetime.date, int]:
    """
    Read the last date and record days from the save file.

    Returns:
        Union[datetime.date, int]: the date this program was last run, the record number of days
    """
    last_date = None
    record_days = None

    # Check if the file exists.
    try:
        # Read the last date and record days from the file.
        with open(SAVE_FILE, "r") as f:
            last_date = f.readline()
            last_date = last_date[:-1]
            record_days = f.readline()

        # Check if the file is empty.
        # If it is, use the date of the first flight of the Kiowa Warrior.
        if last_date == "":
            last_date = KIOWA_WARRIOR_FIRST_FLIGHT
        if record_days == "":
            record_days = 0
    except FileNotFoundError:
        with open(SAVE_FILE, "w") as f:
            f.write(KIOWA_WARRIOR_FIRST_FLIGHT + "\n")
            last_date = KIOWA_WARRIOR_FIRST_FLIGHT
            f.write("0")
            record_days = 0

    # Check if the date is valid.
    try:
        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format in the file. Please use YYYY-MM-DD.")
        print("The file will be cleared. If there is no date in the file,")
        print("the program will use the date of the first flight of the Kiowa Warrior.")
        with open(SAVE_FILE, "w") as f:
            f.write("")
        os._exit(1)

    return last_date, int(record_days)

def write_to_save_file(last_date: datetime.date, record_days: int):
    """
    Write the last date and record days to the save file.

    Args:
        last_date (datetime.date): The date this program was last run.
        record_days (int): The record number of days.
    """
    with open(SAVE_FILE, "w") as f:
        f.write(last_date.strftime("%Y-%m-%d") + "\n")
        f.write(f"{record_days}")

def calculate_days_since_date(last_date: datetime.date) -> int:
    """
    Calculate the number of days since the last date compared to the current date.

    Args:
        last_date (datetime.date): The date this program was last run.

    Returns:
        int: The number of days since the last date.
    """
    today = datetime.date.today()
    days_since = today - last_date
    return days_since.days

def draw_outline(draw, x, y, offset, text, font, outline_color):
    """
    Draw an outline around text.

    Args:
        draw (_type_): The ImageDraw object.
        x (_type_): The x coordinate of the text (assumes left align).
        y (_type_): The y coordinate of the text (assumes left align).
        offset (_type_): The offset/thickness of the outline.
        text (_type_): The text to draw.
        font (_type_): The font to use.
        outline_color (_type_): The color of the outline.
    """
    draw.text((x + offset, y), text, font=font, fill=outline_color, align="left")
    draw.text((x - offset, y), text, font=font, fill=outline_color, align="left")
    draw.text((x, y - offset), text, font=font, fill=outline_color, align="left")
    draw.text((x, y + offset), text, font=font, fill=outline_color, align="left")

def draw_image_and_save_to_image_file(days_since:int, days_record:int):
    """
    Draw the image and save it to a image file.
    Uses the base image "base.png".
    Exported image is "output.png".

    Args:
        days_since (int): The number of days since the last date.
        days_record (int): The record number of days.
    """
    base_image = Image.open("base.png")
    new_image = Image.new("RGB", base_image.size)
    Image.Image.paste(new_image, base_image, (0, 0))

    base_font_size = 65

    old_days_x = 250
    old_days_y = 160

    new_days_x = 260
    new_days_y = 60

    font = 'FreeMonoBold.ttf'

    text_color = (0, 0, 0)
    text_outline_color = (255, 255, 255)

    temp_days_since = days_since
    div_by = 1
    while temp_days_since > 9:
        temp_days_since = int(temp_days_since / 10)
        div_by += 1

    base_font_size = int(base_font_size / div_by)

    old_days_y += ((65 - base_font_size) / 2)

    old_days_font = ImageFont.truetype(font, base_font_size)
    new_days_font = ImageFont.truetype(font, 65)
    
    draw = ImageDraw.Draw(new_image)

    draw.text((old_days_x, old_days_y), f"{days_since}", font=old_days_font, fill=text_color, align="center")
    draw.text((new_days_x, new_days_y), "0", font=new_days_font, fill=text_color, align="center")

    record_days_font = ImageFont.truetype(font, 50)
    draw_outline(draw, 1, 392, 2, f"Record: {days_record} days", record_days_font, text_outline_color)
    draw.text((1, 392), f"Record: {days_record} days", font=record_days_font, fill=text_color, align="left")

    new_image.save("output.png")

def main():
    last_date, record_days = read_from_save_file()
    days_since = calculate_days_since_date(last_date)
    if days_since > record_days:
        record_days = days_since
    write_to_save_file(datetime.date.today(), record_days)
    draw_image_and_save_to_image_file(days_since, record_days)

if __name__ == '__main__':
    print("Kiowa Warrior Days Since Meme Generator")
    print("======================================")
    print("Made by: Tom")
    print("======================================")
    print("")
    main()
    os._exit(0)
