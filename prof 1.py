import requests
import csv
from bs4 import BeautifulSoup


def get_professor_info(professor_contact_link):
    soup1 = BeautifulSoup(professor_contact_link_response.text, 'lxml')
    proffessor_business_card = soup1.find('div', class_='b_rte').p.text
    try:
        table_row_values = soup1.find('div', class_='b_table').find_all('tr')
    except Exception as e:
        print(professor_contact_link)
        print('error ', e)
        professor_information = None

    else:
        try:
            professor_information = ([each_row.text.strip().replace('\n', ' ') for each_row in table_row_values])
        except:
            print('error finding professor intfo')
        else:
            professor_information = None
    try:
        image_link = base_url + (soup1.find('picture').img['src'])
    except Exception as e:
        image_link = None

    return proffessor_business_card, professor_information, image_link


all_link = ['https://www.srh-hochschule-heidelberg.de/en/bachelor/business-engineering/',
                   'https://www.srh-hochschule-heidelberg.de/en/bachelor/study-international-business/international-business/',
                   'https://www.srh-hochschule-heidelberg.de/en/bachelor/study-international-business/international-business/',
                   'https://www.srh-hochschule-heidelberg.de/en/bachelor/electrical-engineering/','https://www.srh-hochschule-heidelberg.de/en/master/global-business-and-leadership/','https://www.srh-hochschule-heidelberg.de/en/master/international-management-and-leadership/','https://www.srh-hochschule-heidelberg.de/en/master/information-technology/','https://www.srh-hochschule-heidelberg.de/en/master/international-business-and-engineering/','https://www.srh-hochschule-heidelberg.de/en/master/water-technology/','https://www.srh-hochschule-heidelberg.de/en/master/blockchain-technology/','https://www.srh-hochschule-heidelberg.de/en/master/artificial-intelligence/','https://www.srh-hochschule-heidelberg.de/en/master/architecture/','https://www.srh-hochschule-heidelberg.de/en/master/applied-computer-science/','https://www.srh-hochschule-heidelberg.de/en/master/applied-data-science-and-analytics/','https://www.srh-hochschule-heidelberg.de/en/master/music-therapy/','https://www.srh-hochschule-heidelberg.de/en/master/dance-movement-therapy/']
# all_link = ['https://www.srh-hochschule-heidelberg.de/en/master/global-business-and-leadership/','https://www.srh-hochschule-heidelberg.de/en/master/international-management-and-leadership/','https://www.srh-hochschule-heidelberg.de/en/master/information-technology/','']
# with open('./data/prof.csv', 'a',newline='',encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['professor_name','professor_role','professor_business_card', 'professor_info', 'image_link',])
#     for link in all_link:
#         response = requests.get(link)
#         soup = BeautifulSoup(response.text,'lxml')
#
#         professors_blocks = soup.find_all('article',class_='b_card')
#         base_url = 'https://www.srh-hochschule-heidelberg.de'
#
#         for professor_block in professors_blocks:
#             role = professor_block.span.text.strip()
#             professor = professor_block.header.text.strip()
#             professor_contact_link = professor_block.a['href']
#             try:
#                 professor_contact_link_response = requests.get(base_url+professor_contact_link)
#             except Exception as e:
#                     print(f'error as {e}')
#             else:
#                 proffessor_business_card, professor_info, image_link  = get_professor_info(professor_contact_link)
#                 writer.writerow([professor,role,proffessor_business_card,professor_info])
#                 print([professor,role,proffessor_business_card,professor_info])

import pandas as pd
from reportlab.pdfgen import canvas

def create_pdf_from_csv(csv_file, pdf_file):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Create a PDF document
    pdf = canvas.Canvas(pdf_file)

    # Set font and size
    pdf.setFont("Helvetica", 8)

    # Get column names and data from DataFrame
    column_names = list(df.columns)
    data = df.values.tolist()

    # Set column widths based on the length of column names
    col_widths = [pdf.stringWidth(col, "Helvetica", 8) + 10 for col in column_names]

    # Set the initial position for drawing the table
    y_position = 750
    row_height = 20

    # Draw the column names
    for i, col in enumerate(column_names):
        pdf.drawString(100 + sum(col_widths[:i]), y_position, col)

    # Draw the data
    for row in data:
        for i, value in enumerate(row):
            pdf.drawString(100 + sum(col_widths[:i]), y_position - row_height, str(value))

        # Move to the next row
        y_position -= row_height

    # Save the PDF
    pdf.save()

# Specify the path to your CSV file and the desired PDF output file
csv_file_path = '../srhscraping/data/prof.csv'
pdf_output_path = 'output.pdf'

# Create the PDF from the CSV data
# create_pdf_from_csv(csv_file_path, pdf_output_path)

print(f"PDF created from CSV data and saved in: {pdf_output_path}")

import pandas as pd
from reportlab.lib import pagesizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# Step 1: Read CSV File
# csv_file = 'your_file.csv'  # Replace with your CSV file path
data_frame = pd.read_csv(csv_file_path)

# Convert DataFrame to a list of lists for ReportLab
data = [data_frame.columns.to_list()] + data_frame.values.tolist()

# Step 2: Create a PDF file
pdf_file = 'output.pdf'  # Output PDF file name
pdf = SimpleDocTemplate(pdf_file, pagesize=pagesizes.letter)

# Create a Table with the data
table = Table(data)

# Add style to the table
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), (0.7, 0.7, 0.7)),
    ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), (0.95, 0.95, 0.95)),
])
table.setStyle(style)

# Add the table to the PDF
elements = [table]
pdf.build(elements)

print(f"PDF created: {pdf_file}")
