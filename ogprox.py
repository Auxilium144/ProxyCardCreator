from PIL import Image
import os

def resize_image(image_path, target_size):
    image = Image.open(image_path)
    image = image.resize(target_size, Image.LANCZOS)
    return image

def main(input_directory, output_directory, margin=80, dpi=1200):
    # Constants for card dimensions in millimeters
    card_width_mm = 66
    card_height_mm = 92

    # Convert millimeters to inches
    card_width_inches = card_width_mm / 25.4
    card_height_inches = card_height_mm / 25.4

    # Calculate the dimensions of a single Magic card in pixels based on the DPI
    card_width_pixels = int(card_width_inches * dpi)
    card_height_pixels = int(card_height_inches * dpi)
    target_size = (card_width_pixels, card_height_pixels)

    images = []
    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_directory, filename)
            images.append(resize_image(image_path, target_size))

    if not images:
        print("No image files found in the input directory.")
        return None

    # Calculate the dimensions of the paper in pixels based on the DPI
    paper_width_inches = 8.5
    paper_height_inches = 11
    paper_width_pixels = int(paper_width_inches * dpi)
    paper_height_pixels = int(paper_height_inches * dpi)

    # Calculate the total width and height of the group of 9 cards including margins
    total_width_cards = 3
    total_height_cards = 3
    total_width_pixels = total_width_cards * (card_width_pixels + margin) - margin
    total_height_pixels = total_height_cards * (card_height_pixels + margin) - margin

    # Calculate the left and top offset to center the group of cards on the paper
    left_offset = (paper_width_pixels - total_width_pixels) // 2
    top_offset = (paper_height_pixels - total_height_pixels) // 2

    # Initialize canvas and page
    current_page = 0
    current_row = 0
    current_col = 0
    canvas = Image.new("RGB", (paper_width_pixels, paper_height_pixels), color="white")

    for image in images:
        # Check if adding the current image would exceed the width of the paper
        if current_col + 1 > 3:
            current_row += 1
            current_col = 0

        if current_row + 1 > 3:
            current_page += 1
            current_row = 0
            current_col = 0
            output_file_path = os.path.join(output_directory, f"output_page_{current_page}.jpg")
            canvas.save(output_file_path, format="JPEG", dpi=(dpi, dpi))
            canvas = Image.new("RGB", (paper_width_pixels, paper_height_pixels), color="white")

        # Calculate the position to paste the image onto the canvas
        x_offset = left_offset + current_col * (card_width_pixels + margin)
        y_offset = top_offset + current_row * (card_height_pixels + margin)
        canvas.paste(image, (x_offset, y_offset))

        # Update the position for the next image
        current_col += 1

    # Save the last page
    output_file_path = os.path.join(output_directory, f"output_page_{current_page + 1}.jpg")
    canvas.save(output_file_path, format="JPEG", dpi=(dpi, dpi))

if __name__ == "__main__":
    input_directory = r"D:\Images\ai art\Magic\Proxy Templates and Scripts\Generator\Singles"
    output_directory = r"D:\Images\ai art\Magic\Proxy Templates and Scripts\Generator\Sheets"
    main(input_directory, output_directory)