import customtkinter
from customtkinter import *
from tkcalendar import Calendar
import datetime

class MyWindow:
    def __init__(self):
        self.root = CTk()
        self.root.title("Organizer")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        set_appearance_mode("dark")


        self.date_label = CTkLabel(self.root, text="Select Date: ",font=("Arial", 20), corner_radius=5, width=15, height=2)
        self.date_label.pack(padx=10, pady=10)

        self.calender()
        self.frame_button()
        self.input()
        self.save_button()
        self.del_button()


    def see_date(self, event=None):
        self.date = self.cal.get_date()
        self.date_label.configure(text="Selected Date: " + self.date)

    def calender(self):
        self.cal = Calendar(self.root, font="Arial 15", selectmode="day", locale="en_US", mindate=datetime.date.today(),
                            showweeknumbers=False, firstweekday="sunday")
        self.cal.configure(background="#1e1f1d", bordercolor="#1e1f1d", selectbackground="#2176ed", selectforeground="white",
                           headersbackground="#1e1f1d",headersforeground="white", cursor="hand2")
        #self.cal.pack(padx=10, pady=10)
        self.cal.pack(padx=10, pady=10, fill="both", expand=True)
        self.cal.bind("<<CalendarSelected>>", self.see_date)


    def frame_button(self):
        self.frame = CTkFrame(self.root)
        self.frame.pack(padx=10, pady=10,)


    def save_button(self):
        self.button = customtkinter.CTkButton(master=self.frame, text="Save Note", command=self.save_note)
        self.button.configure(width=160, font=("Arial", 15), hover_color="#1045e3", fg_color="#2176ed")
        self.button.pack(padx=10, pady=10, side=customtkinter.RIGHT)

    def del_button(self):
        self.button = customtkinter.CTkButton(master=self.frame, text="Delete Note", command=self.delete_note)
        self.button.configure(width=160, font=("Arial", 15), hover_color="#1045e3", fg_color="#2176ed")
        self.button.pack(padx=10, pady=10, side="left")

    def delete_note(self):

        with open("C:\\Users\\domin\\Desktop\\notes.txt.txt", "r") as file:
            lines = file.readlines()

        lines = [line for line in lines if self.date not in line]

        with open("C:\\Users\\domin\\Desktop\\notes.txt.txt", "w") as file:
            file.writelines(lines)
            print("Note deleted")


    def save_note(self):
        if not self.date:
            print("No date selected")
            return
        if not self.entry.get("1.0", customtkinter.END).strip():
            print("No text to save")
            return
        for lines in open("C:\\Users\\domin\\Desktop\\notes.txt.txt", "r").readlines():
            print(f"Checking line: {lines}")
            if self.date in lines:
                print("Date found in line")
                self.entry.delete("1.0", customtkinter.END)
                break
        else:
            print("Date not found in any line, writing to file")
            with open("C:\\Users\\domin\\Desktop\\notes.txt.txt", "a") as file:
                text_to_retrieve = self.entry.get("1.0", customtkinter.END).strip()
                text_to_write = f"{text_to_retrieve} - {self.date}"
                print(f"Writing text: {text_to_write}")
                file.write(text_to_write + '\n')

    def input(self):
        self.entry = CTkTextbox(master=self.frame, font=("Arial", 15), border_color="#2176ed", border_width=2, width=350, height=100, )
        self.entry.pack(padx=5, pady=5)

window = MyWindow()
window.root.mainloop()
