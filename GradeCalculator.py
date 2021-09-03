from bs4 import BeautifulSoup

# Grade calculator 
# Chris Durnan
# There could be a ~1% difference because of floating point shenanigans
def main():
    location = input("\nEnter html file path: ")
    print("Skip incomplete (0%) assignments?")
    skip_incomplete = input("Y or N: ")
    
    if skip_incomplete == "Y":
        skip_incomplete = True
    else:
        skip_incomplete = False

    # Reads the HTML page specified
    with open(location, "r") as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, "lxml")

        grade = 0
        weighting = 0
        final_grade = 0

        # Finds the table which contains the grades
        table_selection = soup.find_all("tbody")
        for table in table_selection:
            # List to store the required grade labels
            label_list = []

            # Removes the headers (which contain your overall grade for those assignments/tests)
            for tr in table.find_all('tr', 'd_ggl1'):
                tr.decompose()
            for td in table.find_all('td', 'fct_w'):
                td.decompose()

            # Selects the div's that contain the grades
            div_selection = table.find_all("div", class_="dco_c", style="display:inline;")
            
            # Retreives grades from the labels and adds them to the list above
            for found_div in div_selection:
                for grade_label in found_div:
                    label_list.append(grade_label.text)

            # Skips the points and letter grades which we do not need
            if len(label_list) % 3 == 0:
                for required_label in label_list[1::3]:
                    split_string = required_label.split(" / ")

                    # Adds up the required grades
                    # If they are zero and wish to be skipped, discard them.
                    if split_string[0] != "0" or not skip_incomplete:
                        grade += float(split_string[0])
                        weighting += float(split_string[1])

            # Same as above but covers a slightly different table layout
            else:
                for required_label in label_list[1:-3:3]:
                    split_string = required_label.split(" / ")
                    if split_string[0] != "0" or not skip_incomplete:
                        grade += float(split_string[0])
                        weighting += float(split_string[1])

        # Rounds the grades. D2L does this as well IIRC
        grade = round(grade - 0.5)
        weighting = round(weighting - 0.5)
        final_grade = int(grade / weighting * 100)

        # Your final grade
        print("Your final grade is: " + str(final_grade) + "%")

main()
