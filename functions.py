import pdfplumber
import re


def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = str("")
        for page in pdf.pages:
            text = text + "\n" + page.extract_text()

    split_text_to_groups(text)


def get_invocie_number(footer):
    lines = footer.splitlines()
    invocie_number_line = ""
    for line in lines:
        if "Faktura numer" in line:
            invocie_number_line = line
    last_part_of_line = invocie_number_line.split("numer")[1]
    invoice_number = last_part_of_line.lstrip()
    
    return invoice_number


def get_account_id(header):
    lines = header.splitlines()
    id_number_line = ""
    for line in lines:
        if "Identyfikator konta" in line:
            id_number_line = line
    id_number = re.findall(r"\d+.\d+", id_number_line)[0]
    
    return id_number


def split_text_to_groups(text):
    text_partition = text.partition("Kampanie")
    header = text_partition[0] + text_partition[1]
    rest_of_text = text_partition[2]
    text_partition = rest_of_text.partition("Ziemia Inwestycje Spółka")
    text_data = text_partition[0]
    footer = text_partition[1] + text_partition[2]

    id_number = get_account_id(header)
    invoice_number = get_invocie_number(footer)
    print(f"Numer konta: {id_number}")
    print(f"numer faktury: {invoice_number}")
    clean_text_data(text_data)


def clean_text_data(text_data):
    lines = text_data.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.replace("zł", "")
        line = line.replace(",", ".")
        cleaned_lines.append(line)
        if line == "":
            cleaned_lines.remove(line)

    data_mining(cleaned_lines)


def data_mining(cleaned_lines):
    amount_lines = []
    previous_line = ""
    for line in cleaned_lines:
        if "Od" in line:
            amount_lines.append(previous_line)
        previous_line = line
        
    name_lines = []
    for line in cleaned_lines:
        if line in amount_lines:
            name_lines.append(previous_line)
        previous_line = line

    cleaned_amount_data = []
    for line in amount_lines:
        line = line.replace("zł", "")
        line = line.replace(",", ".")
        cleaned_amount_data.append(float(line))

    zip_data_list(cleaned_amount_data, name_lines)


def zip_data_list(cleaned_amount_data, name_lines):
    print(f"Porównywane zbiory są zgodne: {len(name_lines)==len(cleaned_amount_data)}")
    print(f"Suma z pozycji w fakturze wynosi: {sum(cleaned_amount_data)}")
    var = list(zip(name_lines, cleaned_amount_data))
    for elem in var:
        print(elem)
    



extract_text_from_pdf("test.pdf")
