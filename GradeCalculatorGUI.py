from tkinter import *
from tkinter import filedialog, font, ttk
from bs4 import BeautifulSoup

def main():
    def open_file():
        global grades_file
        window.filename = filedialog.askopenfilename(
            title="Open File", filetypes=[("HTML Web Page", "*.htm;*.html")])
        grades_file = window.filename

        try:
            with open(grades_file, "r") as html_file:
                content = html_file.read()
                page_file = BeautifulSoup(content, 'lxml')

                course_title = ""
                grade = 0
                weighting = 0
                final_grade = 0

                title_selection = page_file.find_all(
                    'div', class_='d2l-navigation-s-title-container')
                course_title = title_selection[0].text

                # Finds the table which contains the grades
                table_selection = page_file.find_all('tbody')
                for table in table_selection:
                    # List to store the required grade labels
                    label_list = []

                    # Removes the headers (which contain your overall grade for those assignments/tests)
                    for tr in table.find_all('tr', 'd_ggl1'):
                        tr.decompose()
                    for td in table.find_all('td', 'fct_w'):
                        td.decompose()

                    # Selects the div's that contain the grades
                    div_selection = table.find_all(
                        'div', class_='dco_c', style="display:inline;")

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
                            if split_string[0] != "0" or skip_incomplete.get() == 0:
                                grade += float(split_string[0])
                                weighting += float(split_string[1])

                    # Same as above but covers a slightly different table layout
                    else:
                        for required_label in label_list[1:-3:3]:
                            split_string = required_label.split(" / ")
                            if split_string[0] != "0" or skip_incomplete.get() == 0:
                                grade += float(split_string[0])
                                weighting += float(split_string[1])

                # Rounds the grades. D2L does this as well IIRC
                grade = round(grade - 0.5)
                weighting = round(weighting - 0.5)
                final_grade = int(grade / weighting * 100)

                # Your final grade
                class_var.set(course_title)
                grade_var.set("is " + str(final_grade) + "%")
        except (FileNotFoundError, ZeroDivisionError):
            class_var.set("An improper file was selected.")

    # Main Window
    window = Tk()
    window.title("D2L Grade Calculator")

    # Header/Description
    upper_frame = Frame(window)
    upper_frame.grid(row=0, column=0, padx=10, pady=10)
    text_font = "Calibri 14"

    title = Label(upper_frame, text="Grade Calculator", font="Calibri 24")
    description = Label(upper_frame, text="Calculates your current grade in a course using the D2L/Brightspace" +
                        " grades page.", font=text_font)
    how_to = Label(
        upper_frame, text="Go to D2L -> Course -> Assessments -> Grades and download the page.", font=text_font)
    how_to_two = Label(
        upper_frame, text="Open the downloaded HTML page to view your grade.", font=text_font)

    title.grid(row=0, column=0, sticky='w')
    description.grid(row=1, column=0, sticky='w')
    how_to.grid(row=2, column=0, sticky='w')
    how_to_two.grid(row=3, column=0, sticky='w')

    # Middle Frame
    middle_frame = Frame(window, padx=15, pady=10)
    middle_frame.config(bd=1, relief=SOLID)
    middle_frame.grid(row=1, column=0)

    skip_incomplete = IntVar()
    check = Checkbutton(middle_frame, text="Skip incomplete (0%) assignments?",
                        variable=skip_incomplete, font=text_font, padx=10, pady=10)
    check.grid(row=4, column=0)

    open_button = Button(middle_frame, text="Open File",
                         font=text_font, command=open_file)
    open_button.grid(row=4, column=2)

    # Lower Frame
    lower_frame = Frame(window)
    lower_frame.grid(row=2, column=0, padx=10, pady=10)

    grade_desc = Label(lower_frame, text="Your grade in: ", font=text_font)

    class_var = StringVar()
    class_label = Label(lower_frame, textvariable=class_var, font=text_font)

    grade_var = StringVar()
    grade_label = Label(lower_frame, textvariable=grade_var, font=text_font)

    grade_desc.grid(row=0, column=0)
    class_label.grid(row=1, column=0)
    grade_label.grid(row=2, column=0)

    window.mainloop()


if __name__ == "__main__":
    main()
