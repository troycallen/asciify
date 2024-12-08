import argparse
import sys
import os
from PIL import Image

# Define the ASCII characters to use, ordered from dark to light
ASCII_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

def resize_image(image, new_width=100):
    """Resizes the image while maintaining aspect ratio."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for font aspect ratio
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale_image(image):
    """Converts the image to grayscale."""
    return image.convert("L")

def map_pixels_to_ascii(image, range_width=25):
    """Maps each pixel to an ASCII character based on brightness."""
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value // range_width]
    return ascii_str

def convert_image_to_ascii(image_path, output_file=None, width=100):
    """Converts an image to ASCII art."""
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}.")
        print(e)
        return

    # Process the image
    image = resize_image(image, new_width=width)
    grayscale = grayscale_image(image)

    # Convert pixels to ASCII
    ascii_str = map_pixels_to_ascii(grayscale)
    img_width = grayscale.width
    ascii_lines = [ascii_str[index: index + img_width] for index in range(0, len(ascii_str), img_width)]
    ascii_art = "\n".join(ascii_lines)

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(ascii_art)
            print(f"ASCII art successfully written to {output_file}")
        except Exception as e:
            print(f"Failed to write ASCII art to {output_file}")
            print(e)
    else:
        print(ascii_art)

def main():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument('input_image', help='Path to the input image file.')
    parser.add_argument('-o', '--output', help='Path to the output text file. If not specified, ASCII art is printed to the console.')
    parser.add_argument('-w', '--width', type=int, default=100, help='Width of the ASCII art. Default is 100.')

    args = parser.parse_args()

    if not os.path.isfile(args.input_image):
        print(f"Input file '{args.input_image}' does not exist.")
        sys.exit(1)

    convert_image_to_ascii(args.input_image, args.output, args.width)

if __name__ == "__main__":
    main()
