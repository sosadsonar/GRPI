import os
import sys
import csv
import random
import datetime
import xlsxwriter


# Personal information
Personal_Informations = []

# Personal identities in id
Personal_IDs = []

# Personal identities in name
Provinces_Name = []
Sexes = []
Birth_Years = []
Phone_Numbers = []

# Name
Surname = []
Middle_Name = []
First_Name = []
Full_Name = []


# Input the quantity of random number to be generated
def handle_quantity_of_number():
    while True:
        try:
            global quantity
            quantity = int(input("Số thông tin cá nhân ngẫu nhiên cần tạo: "))
            if quantity <= 0:
                print("Vui lòng nhập số nguyên dương.")
                continue
            break
        except ValueError:
            print("Vui lòng nhập số nguyên dương.")     
        else:
            continue
    
    handle_path()


def handle_path():
    global csv_path
    global xlsx_path
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        path = sys._MEIPASS
        xlsx_path = os.path.join(os.path.dirname(sys.executable), "Thông Tin Cá Nhân Ngẫu Nhiên.xlsx")
    else:
        path = os.path.dirname(os.path.abspath(__file__))
        xlsx_path = os.path.join(os.path.dirname(__file__), "Thông Tin Cá Nhân Ngẫu Nhiên.xlsx")
        
    csv_path = os.path.join(path, "Thông Tin Cá Nhân.csv")
    
    read_csv_to_dict()


def read_csv_to_dict():
    """
    Reads a CSV file and adds it to a dictionary with the key as the first column and the value as the second column.
    Skip the first row
    """
    location = {}
    global male_sex_and_birthdate
    male_sex_and_birthdate = {}
    female_sex_and_birthdate = {}
    
    # Name
    global surname
    global new_surname_prob
    global new_male_middle_name
    global new_female_middle_name
    global male_first_name
    global new_male_first_name_prob
    global female_first_name
    global new_female_first_name_prob   
    
    surname = []
    surname_prob = []
    new_surname_prob = []
    male_middle_name = []
    female_middle_name = []
    male_first_name = []
    male_first_name_prob = []
    female_first_name = []
    female_first_name_prob = []

    # Get personal identities
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # Get location
            area_code = row[0]
            area = row[1]
            location[area_code] = area
            
            # Get male sex and first two number of birthdate
            male_birthdate_code = row[3]
            male_birthdate = row[4]
            male_sex_and_birthdate[male_birthdate_code] = male_birthdate
        
            # Get female sex and first two number of birthdate
            female_birthdate_code = row[5]
            female_birthdate = row[6]
            female_sex_and_birthdate[female_birthdate_code] = female_birthdate
            
            # Get last name
            surname.append(row[8])
            surname_prob.append(row[9])
            
            # Get middle name
            male_middle_name.append(row[11])
            female_middle_name.append(row[12])
            
            # Get first name
            male_first_name.append(row[14])
            male_first_name_prob.append(row[15])
            
            female_first_name.append(row[17])
            female_first_name_prob.append(row[18])
      
        # Remove an empty key-pair value at the end of dictionary
        male_sex_and_birthdate.popitem()
        female_sex_and_birthdate.popitem() 
        sex_and_birthdate = [male_sex_and_birthdate, female_sex_and_birthdate]
        
        # Convert string to float in prob
        new_surname_prob = [float(i) for i in surname_prob]
        new_male_first_name_prob = [float(i) for i in male_first_name_prob]
        new_female_first_name_prob = [float(i) for i in female_first_name_prob]
     
        # Remove empty value from name
        new_male_middle_name = list(filter(None, male_middle_name))
        new_female_middle_name = list(filter(None, female_middle_name))
    
    handle_year(location, sex_and_birthdate)


def handle_year(location, sex_and_birthdate):
    # Get current year
    today = datetime.date.today()
    cur_year = today.year
    
    # Get min year
    while True:
        try:
            min_year = int(input(f"Năm sinh thấp nhất để tạo ngẫu nhiên (lớn hơn hoặc bằng 1900)(mặc định {cur_year-35}): "))
            if min_year <= 1900 or min_year > cur_year:
                print(f"Vui lòng nhập số nguyên dương lớn hơn hoặc bằng 1900 và nhỏ hơn hoặc bằng {cur_year}.")
                continue
            break
        except ValueError:
            print(f"Giá trị không hợp lệ, tự động nhập năm sinh thấp nhất: {cur_year-35}.") 
            min_year = cur_year-35
            break
    
    # Get max year
    while True:
        try:
            max_year = int(input(f"Năm sinh cao nhất để tạo ngẫu nhiên (lớn hơn hoặc bằng {min_year})(mặc định {cur_year-18}): "))
            if max_year <= 1900 or min_year > max_year or max_year > cur_year:
                print(f"Vui lòng nhập số nguyên dương lớn hơn hoặc bằng {min_year} và nhỏ hơn hoặc bằng {cur_year}.")
                continue
            break
        except ValueError:
            print(f"Giá trị không hợp lệ, tự động nhập năm sinh cao nhất: {cur_year-18}.") 
            if cur_year-18 < min_year:
                print(f"Năm sinh thấp nhất cao hơn năm sinh cao nhất. Thoát chương trình!")
                return
            else:
                max_year = cur_year-18
                break  

    generate_personal_id(location, sex_and_birthdate, min_year, max_year)


def generate_personal_id(location, sex_and_birthdate, min_year, max_year):
    for i in range(quantity): 
        # Get random year
        year = str(random.randint(min_year, max_year))
        
        # Get random area code and name
        provinces_ids = random.choice(list(location.keys()))
        Provinces_Name.append(random.choice(list(location.values())))
        
        # Get random sex and name
        random_sex_and_birthdate = random.choice(sex_and_birthdate)
        sexes = next((key for key in random_sex_and_birthdate if random_sex_and_birthdate[key] == year[:2]), None)
        if sexes in male_sex_and_birthdate:
            Sexes.append("Nam")
            Middle_Name.append(random.choice(new_male_middle_name))
            First_Name = random.choices(male_first_name, new_male_first_name_prob, k = quantity)
        else:
            Sexes.append("Nữ")
            Middle_Name.append(random.choice(new_female_middle_name))
            First_Name = random.choices(female_first_name, new_female_first_name_prob, k = quantity)
            
        # Get random birthdate
        Birth_Years.append(year)
        birth_years = year[-2:]
        
        # Generate random 8 digit
        random_integer = random.randint(0, 99999999)
        # Convert the random integer to a string.
        random_integer_str = str(random_integer)
        # Pad the string with leading zeros, if necessary.
        random_integer_str = random_integer_str.zfill(8)
        
        # Get random phone number
        Phone_Numbers.append("0" + str(random.randint(100, 999)) + " " + (str(random.randint(0, 999))).zfill(3) + " " + (str(random.randint(0, 999))).zfill(3))
        
        # Get name
        Surname = random.choices(surname, new_surname_prob, k = quantity)
        Full_Name.append(Surname[i] + " " + Middle_Name[i] + " " + First_Name[i])
        
        # Get personal IDs
        Personal_IDs.append(provinces_ids + sexes + birth_years + random_integer_str)
    
    export_to_xlsx_file()
    
    
def export_to_xlsx_file():
    # Create an XlsxWriter workbook
    with xlsxwriter.Workbook(xlsx_path) as workbook:
        # Set the encoding to UTF-8
        workbook.encoding = "utf-8"
        worksheet = workbook.add_worksheet()
        
        # Format text to center aligned
        header_format = workbook.add_format()
        header_format.set_align("center")
        header_format.set_align("vcenter")   
        header_format.set_bg_color("#ff7b59")
        
        
        cell_format = workbook.add_format()
        cell_format.set_align("center")
        cell_format.set_align("vcenter")       
        
        # Write Headers
        worksheet.write("A1", "Họ và tên", header_format)
        worksheet.write("B1", "Căn cước công dân", header_format)
        worksheet.write("C1", "Tỉnh", header_format)
        worksheet.write("D1", "Giới tính", header_format)
        worksheet.write("E1", "Năm sinh", header_format)
        worksheet.write("F1", "Số điện thoại", header_format)
        
        for i in range(quantity):
            worksheet.write("A" + str(i + 2), Full_Name[i], cell_format)
            worksheet.write("B" + str(i + 2), Personal_IDs[i], cell_format)
            worksheet.write("C" + str(i + 2), Provinces_Name[i], cell_format)
            worksheet.write("D" + str(i + 2), Sexes[i], cell_format)
            worksheet.write("E" + str(i + 2), Birth_Years[i], cell_format)
            worksheet.write("F" + str(i + 2), Phone_Numbers[i], cell_format)
        
        # Autofit the worksheet.
        worksheet.autofit()

            
if __name__ == "__main__":
    handle_quantity_of_number()
    
