from PIL import Image, ImageDraw, ImageFont
import random
import sys


def resize_and_place_on_a4(img):
    a4_width, a4_height = 2100, 2970
    img_aspect_ratio = img.width / img.height

    if img_aspect_ratio > (a4_width / a4_height):
        new_width = a4_width
        new_height = int(a4_width / img_aspect_ratio)
    else:
        new_width = int(a4_height * img_aspect_ratio)
        new_height = a4_height

    resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    a4_img = Image.new("RGB", (a4_width, a4_height), (128, 128, 128))
    offset_x = (a4_width - new_width) // 2
    offset_y = (a4_height - new_height) // 2
    a4_img.paste(resized_img, (offset_x, offset_y))

    return a4_img


def split_image(img, rows, columns):
    width, height = img.size
    block_width = width // columns
    block_height = height // rows
    return [
        img.crop(
            (
                j * block_width,
                i * block_height,
                (j + 1) * block_width,
                (i + 1) * block_height,
            )
        )
        for i in range(rows)
        for j in range(columns)
    ]


def add_watermark(img, text):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Helvetica.ttc", 86)
    text_width, text_height = draw.textsize(text, font=font)
    padding = 10

    # Draw a semi-transparent rectangle behind the text
    rectangle_x0, rectangle_y0 = 10 - padding, 10 - padding
    rectangle_x1, rectangle_y1 = 10 + text_width + \
        padding, 10 + text_height + padding
    draw.rectangle([rectangle_x0, rectangle_y0, rectangle_x1,
                   rectangle_y1], fill=(128, 128, 128, 128))

    # Draw the text on top of the rectangle
    draw.text((10, 10), text, font=font, fill=(255, 255, 255, 128))

    return img


def add_frame(img, frame_width, frame_color):
    framed_img = Image.new(
        "RGB",
        (img.width + 2 * frame_width, img.height + 2 * frame_width),
        frame_color,
    )
    framed_img.paste(img, (frame_width, frame_width))
    return framed_img


def assemble_image(blocks, rows, columns, shuffle=False):
    a4_width, a4_height = 2100, 2970
    output_img = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))

    if shuffle:
        blocks = random.sample(blocks, len(blocks))

    for i, block in enumerate(blocks):
        row = i // columns
        column = i % columns
        output_img.paste(block, (column * block.width, row * block.height))

    return output_img


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python image_randomizer.py input_image shuffled_output_image unshuffled_output_image [--frame]")
        sys.exit(1)

    input_image = sys.argv[1]
    shuffled_output_image = sys.argv[2]
    unshuffled_output_image = sys.argv[3]
    use_frame = '--frame' in sys.argv

    img = Image.open(input_image)
    a4_img = resize_and_place_on_a4(img)

    rows = 9
    columns = 3
    blocks = split_image(a4_img, rows, columns)

    if use_frame:
        frame_width = 2
        frame_color = (0, 0, 0)  # Gray frame
        framed_blocks = [add_frame(block, frame_width, frame_color)
                         for block in blocks]
        watermarked_blocks = [
            add_watermark(block, str(i + 1)) for i, block in enumerate(framed_blocks)
        ]
    else:
        watermarked_blocks = [
            add_watermark(block, str(i + 1)) for i, block in enumerate(blocks)
        ]

    shuffled_assembled_img = assemble_image(
        watermarked_blocks, rows, columns, shuffle=True)
    shuffled_assembled_img.save(shuffled_output_image)

    unshuffled_assembled_img = assemble_image(
        watermarked_blocks, rows, columns, shuffle=False)
    unshuffled_assembled_img.save(unshuffled_output_image)
