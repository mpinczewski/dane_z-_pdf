import pdfplumber

path = "test.pdf"
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
for line in lines:
    if line == "":
        lines.remove(line)

for line in lines:
    if "Od" in line:
        lines.remove(line)


import re

cleaned_data = []

for elem in lines:
    elem = elem.replace("zł", "")
    elem = elem.replace(",", ".")

    pattern_with_numbers = re.findall(r"(\d+)[^\d]+Wyświetlenia", elem)
    if len(pattern_with_numbers) > 0:
        number_to_delete = pattern_with_numbers[0]
        string_to_delete = number_to_delete + " " + "Wyświetlenia"
        elem = elem.replace(string_to_delete, "")

    pattern_to_split = re.findall(r"\d+.\d+", elem)
    if len(pattern_to_split) > 0:
        amount = pattern_to_split[0]
        elem = elem.replace(amount, "," + amount + ",")

    cleaned_data.append(elem)

str1 = "".join(cleaned_data)

str2 = str1.split(",")

final_data = []

for elem in str2:
    if len(elem) < 2:
        str2.remove(elem)
    elem = elem.rstrip()
    elem = elem.lstrip()
    if len(elem) > 0:
        final_data.append(elem)


# print(final_data)

names = []
amount = []

for elem in final_data:
    try:
        elem = float(elem)
        amount.append(elem)
    except:
        names.append(elem)

# print(names)
# print(amount)

var = list(zip(names, amount))
for elem in var:
    print(elem)

# print(str2)
# print(cleaned_data)
