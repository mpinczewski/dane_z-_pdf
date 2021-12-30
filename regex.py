import pdfplumber

path = "test2.pdf"


with pdfplumber.open(path) as pdf:
    text = str("")
    for page in pdf.pages:
        text = text + "\n" + page.extract_text()


text_partition = text.partition("Kampanie")
header = text_partition[0] + text_partition[1]
rest_of_text = text_partition[2]

text_partition = rest_of_text.partition("Ziemia Inwestycje Spółka")
text_data = text_partition[0]
footer = text_partition[1] + text_partition[2]

lines = text_data.splitlines()


cleaned_lines = []

for line in lines:
    line = line.replace("zł", "")
    line = line.replace(",", ".")
    cleaned_lines.append(line)
    if line == "":
        cleaned_lines.remove(line)


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
    cleaned_amount_data.append(line)


print(f"zbiory są zgodne: {len(name_lines)==len(amount_lines)}")

var = list(zip(name_lines, amount_lines))
for elem in var:
    print(elem)
