from PIL import Image, ImageFont, ImageDraw
from  PIL.ImageOps import fit
from math import ceil, floor
from os import remove


icon_size = 32
achievement_path = 'image_generation/achievement.png'
font_path = 'image_generation/minecraft.ttf'
items_path = 'image_generation/items.png'
all_items_path = 'image_generation/all_items.png'
user_image_path = 'image_generation/user_image.png'


def get_font(size: int):
    return ImageFont.truetype(font_path, size)


def get_size_of_image(top_text: str, bottom_text: str):
    size = {'x': 320,
            'y': 64}

    while True:
        img = Image.new('RGBA', (size['x'], size['y']), color='white')
        imgdraw = ImageDraw.Draw(img)
        font = get_font(16)
        imgdraw.text((60, 14), top_text, font=font, fill=(0, 0, 0))
        imgdraw.text((60, 36), bottom_text, font=font, fill=(0, 0, 0))

        checking_range = 16
        pixels = []

        for x in range(checking_range):
            for y in range(14, 28):
                pixel_color = img.getpixel((size['x']-1-x, y))
                pixels.append(pixel_color)
            for y in range(36, 51):
                pixel_color = img.getpixel((size['x']-1-x, y))
                pixels.append(pixel_color)

        if (0, 0, 0, 255) in pixels:
            size['x'] += 6
        else:
            return size


def draw_rectangles(imagedraw: ImageDraw, image_size: dict, cords: list, color):
    for x, y in cords:
        imagedraw.rectangle((x, y, image_size['x'] - x - 1, image_size['y'] - y - 1), fill=color)


def create_image(top_text: str, bottom_text: str, icon: Image):
    image_size = get_size_of_image(top_text, bottom_text)

    # Image
    image = Image.new('RGBA', (image_size['x'], image_size['y']), color=(0, 0, 0, 0))
    imagedraw = ImageDraw.Draw(image)

    # Background
    black_bg_cords = [[6, 0], [0, 6], [4, 2], [2, 4]]
    draw_rectangles(imagedraw, image_size, black_bg_cords, 'black')
    light_gray_bg_cords = [[6, 2], [2, 6], [4, 4]]
    draw_rectangles(imagedraw, image_size, light_gray_bg_cords, (85, 85, 85))
    dark_gray_bg_cords = [[8, 6], [6, 8]]
    draw_rectangles(imagedraw, image_size, dark_gray_bg_cords, (33, 33, 33))

    # Text
    font = get_font(16)
    imagedraw.text((60, 14), top_text, font=font, fill=(255, 255, 0))
    imagedraw.text((60, 36), bottom_text, font=font, fill=(255, 255, 255))

    # Icon
    icon = fit(icon, (icon_size, icon_size), Image.ANTIALIAS)
    try:
        image.paste(icon, (15, 16), mask=icon)
    except ValueError:
        image.paste(icon, (15, 16))

    return image


def increase_image_size(image: Image, multiplier: float):
    return image.resize((image.size[0] * multiplier, image.size[1] * multiplier))


def create_all_items_image():
    icons = get_icons(path=items_path)
    increase_image_size(create_numbered_grid(icons), 2).save(all_items_path, 'PNG')


def delete_image(image_path):
    remove(image_path)


def get_icons(path='items.png'):
    image = Image.open(path)
    items = split_image_with_grid(image)
    return items


def split_image_with_grid(image: Image):
    items = []
    x_items_count = int(image.size[0] / icon_size)
    y_items_count = int(image.size[1] / icon_size)

    for y_item_count in range(y_items_count):
        for x_item_count in range(x_items_count):
            x1_cord = x_item_count * icon_size
            y1_cord = y_item_count * icon_size
            x2_cord = x1_cord + icon_size
            y2_cord = y1_cord + icon_size

            item = image.crop((x1_cord, y1_cord, x2_cord, y2_cord))
            items.append(item)

    return items


def create_numbered_grid(items: list, items_in_a_row=20, space_for_text=20, font_size=10, bg_color='white'):
    items_in_a_column = ceil(len(items) / items_in_a_row)

    width = items_in_a_row * icon_size
    height = items_in_a_column * icon_size + items_in_a_column * space_for_text

    image = Image.new('RGBA', (width, height), color=bg_color)
    imagedraw = ImageDraw.Draw(image)

    for i in range(len(items)):
        item = items[i]

        row_number = floor(i / items_in_a_row)
        x_cord_item = icon_size * (i - items_in_a_row * row_number)
        y_cord_item = row_number * 32 + space_for_text * row_number
        image.paste(item, (x_cord_item, y_cord_item), mask=item)

        x_cord_text = (x_cord_item + icon_size / 2) - (font_size / 2) - 2
        y_cord_text = y_cord_item + icon_size + ((space_for_text - font_size) / 2)
        font = get_font(font_size)
        imagedraw.text((x_cord_text, y_cord_text), str(i+1), font=font, fill='black')

    return image


def create_achievement_icon(upper_text, bottom_text, icon_id):
    icons = get_icons(path=items_path)
    create_image(upper_text, bottom_text, icons[icon_id+1]).save(achievement_path, 'PNG')


def create_achievement_user_image(upper_text, bottom_text):
    image = Image.open(user_image_path)
    create_image(upper_text, bottom_text, image).save(achievement_path, 'PNG')
    remove(user_image_path)


def start():
    top_text = input("Введите верхний текст: ")
    bottom_text = input("Введите нижний текст: ")
    icons = get_icons()
    increase_image_size(create_numbered_grid(icons), 2).show()

    icon_number = int(input('Номер иконки: ')) - 1
    create_image(top_text, bottom_text, icons[icon_number]).show()
    create_image(top_text, bottom_text, icons[icon_number]).save('Template', 'PNG')
    # increase_image_size(Image.open('items.png'), 8)


if __name__ == '__main__':
    start()