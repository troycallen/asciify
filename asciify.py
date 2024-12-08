import argparse
import sys
import os
import logging
from PIL import Image

# Define the ASCII characters to use, ordered from dark to light
ASCII_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

# Configure logging
logging.basicConfig(
    filename='asciiartify.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def resize_image(image, new_width=100):
    """Resizes the image while maintaining aspect ratio."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for font aspect ratio
    resized_image = image.resize((new_width, new_height))
    logging.debug(f"Image resized to {new_width}x{new_height}")
    return resized_image

def grayscale_image(image):
    """Converts the image to grayscale."""
    grayscale = image.convert("L")
    logging.debug("Image converted to grayscale")
    return grayscale

def map_pixels_to_ascii(image, range_width=25):
    """Maps each pixel to an ASCII character based on brightness."""
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value // range_width]
    logging.debug("Pixels mapped to ASCII characters")
    return ascii_str

def convert_image_to_ascii(image_path, output_file=None, width=100):
    """Converts an image to ASCII art."""
    try:
        logging.info(f"Starting conversion for {image_path}")
        image = Image.open(image_path)
    except Exception as e:
        logging.error(f"Unable to open image file {image_path}. Error: {e}")
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
            logging.info(f"ASCII art successfully written to {output_file}")
            print(f"ASCII art successfully written to '{output_file}'")
        except Exception as e:
            logging.error(f"Failed to write ASCII art to {output_file}. Error: {e}")
            print(f"Failed to write ASCII art to '{output_file}'.")
            print(e)
    else:
        print(ascii_art)

def convert_directory(input_dir, output_dir, width):
    """Converts all images in a directory to ASCII art."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")
    else:
        logging.info(f"Using existing output directory: {output_dir}")

    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_extensions):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '.txt'
            output_path = os.path.join(output_dir, output_filename)
            convert_image_to_ascii(input_path, output_path, width)
        else:
            logging.warning(f"Skipped unsupported file: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Convert images to ASCII art.")
    parser.add_argument('input', help='Path to the input image file or directory.')
    parser.add_argument('-o', '--output', help='Path to the output text file or directory.')
    parser.add_argument('-w', '--width', type=int, default=100, help='Width of the ASCII art. Default is 100.')

    args = parser.parse_args()

    if os.path.isdir(args.input):
        output_dir = args.output if args.output else 'output_ascii'
        convert_directory(args.input, output_dir, args.width)
    elif os.path.isfile(args.input):
        convert_image_to_ascii(args.input, args.output, args.width)
    else:
        logging.error("Invalid input path provided.")
        print("Invalid input path. Please provide a valid file or directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
