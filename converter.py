import fitz
import os
import sys
import argparse

def pdf_to_jpg(pdf_path: str, output_folder: str = 'output', prefix_name: str = "output_"):
    if not os.path.isdir(output_folder):
        print("Creating output file")
        os.mkdir(output_folder)
    if not os.path.isfile(pdf_path):
        print("File could not be found")
        sys.exit(1)
    output_content = os.listdir(output_folder)
    if len(output_content) > 0:
        response = input(f"Output directory has content: {output_content}\nDo you want to delete[Y/n]: ")
        if response.lower() == 'y':
            for file in output_content:
                print(f"Removing file: {file}")
                os.remove(os.path.join(output_folder, file))
        else:
            print("Not recognize: {response}... Exitting")
            sys.exit(2)

    doc = fitz.open(pdf_path)
    print("Document open")

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix = mat)
        output_path = os.path.join(output_folder, f"{prefix_name}{page_num + 1}.jpg")
        pix.save(output_path, jpg_quality = 90)
        print(f"Saved image: {output_path}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Convert PDF files images into jpg files")
    parser.add_argument('filename')
    parser.add_argument('-o', '--output-folder', help = 'output directory to store the jpg files')
    parser.add_argument('-p', '--prefix-name', help = 'set a prefix to all images name')

    args = parser.parse_args()

    if not args.filename:
        print("PDF files not found")
        parser.print_help()
        sys.exit(0)
    


    if args.output_folder and args.prefix_name:
        pdf_to_jpg(pdf_path = args.filename, output_folder = args.output_folder, prefix_name = args.prefix_name)
        sys.exit(0)
    if args.output_folder:
        pdf_to_jpg(pdf_path = args.filename, output_folder = args.output_folder)
        sys.exit(0)
    if args.prefix_name:
        pdf_to_jpg(pdf_path = args.filename, prefix_name = args.prefix_name)
        sys.exit(0)
        
    pdf_to_jpg(pdf_path = args.filename)

