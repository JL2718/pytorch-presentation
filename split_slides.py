import re

def split_slides(file_path, output_dir):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content by headings
    slides = re.split(r'\n--- \*\*', content)

    # Remove the first element which is empty or contains the title slide
    slides = slides[1:]

    # Save each slide as a separate file
    for i, slide in enumerate(slides):
        slide_number = i + 1
        slide_file_path = f"{output_dir}/slide_{slide_number}.md"
        with open(slide_file_path, 'w') as slide_file:
            slide_file.write(slide)
        print(f"Saved slide {slide_number} to {slide_file_path}")

if __name__ == "__main__":
    file_path = "outline_citations.md"
    output_dir = "slides"
    split_slides(file_path, output_dir)
