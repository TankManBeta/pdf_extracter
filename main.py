from tqdm import tqdm
from utils import extract_pdf_two_columns, get_all_filename


if __name__ == "__main__":
    filenames = get_all_filename()
    for filename in tqdm(filenames):
        extract_pdf_two_columns(filename, "./paper/", "./picture/", 5, 5, 0)
