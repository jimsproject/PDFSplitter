import fitz  # PyMuPDF

# Define A4 and A3 dimensions in points (1 inch = 72 points)
A4_WIDTH = 595  # ~210 mm
A4_HEIGHT = 842  # ~297 mm
A3_WIDTH = 1190  # ~420 mm (Landscape orientation width)
A3_HEIGHT = 842  # ~297 mm (Landscape orientation height)

# Open the input PDF
input_pdf = fitz.open("input.pdf")

# Create a new PDF to save the split A4 pages
output_pdf = fitz.open()

# Iterate over each page in the original PDF
for page_num in range(len(input_pdf)):
    page = input_pdf.load_page(page_num)

    # Get the page size (in points)
    width, height = page.rect.width, page.rect.height

    print(f"Processing page {page_num + 1} with size: {width}x{height}")

    # Check if the page is already A4 (Portrait or Landscape)
    if (abs(width - A4_WIDTH) < 10 and abs(height - A4_HEIGHT) < 10) or \
            (abs(width - A4_HEIGHT) < 10 and abs(height - A4_WIDTH) < 10):
        # Page is A4, copy it directly to the output PDF
        print(f"Page {page_num + 1} is A4, copying directly.")
        output_pdf.new_page(width=width, height=height)
        output_pdf[-1].show_pdf_page(page.rect, input_pdf, page_num)

    # Otherwise, assume the page is A3 (Landscape), split it into two A4 pages
    elif (abs(width - A3_WIDTH) < 10 and abs(height - A3_HEIGHT) < 10):
        print(f"Page {page_num + 1} is A3, splitting into two A4 pages.")

        # Left half (first A4 page)
        rect_left = fitz.Rect(0, 0, width / 2, height)  # Taking left half of the A3 page
        left_page = output_pdf.new_page(width=A4_WIDTH, height=A4_HEIGHT)  # Output as A4 size
        left_page.show_pdf_page(fitz.Rect(0, 0, A4_WIDTH, A4_HEIGHT), input_pdf, page_num, clip=rect_left)

        # Right half (second A4 page)
        rect_right = fitz.Rect(width / 2, 0, width, height)  # Taking right half of the A3 page
        right_page = output_pdf.new_page(width=A4_WIDTH, height=A4_HEIGHT)  # Output as A4 size
        right_page.show_pdf_page(fitz.Rect(0, 0, A4_WIDTH, A4_HEIGHT), input_pdf, page_num, clip=rect_right)

# Save the new PDF with A4 pages
output_pdf.save("output.pdf")
output_pdf.close()
input_pdf.close()