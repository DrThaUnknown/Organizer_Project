import customtkinter
from customtkinter import *
from tkcalendar import *
from tkinter import *
import datetime


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Notes")
        self.resizable(True, True)
        self.notes_frame()
        self.notes_label()
        self.notes_text()
        self.read_notes()
    def notes_frame(self):
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack()
    def notes_label(self):
        self.label = customtkinter.CTkLabel(master=self.frame, text="Notes", font=("Arial", 20))
        self.label.pack(padx=10, pady=10)
    def notes_text(self):
        self.text = customtkinter.CTkTextbox(master=self.frame, font=("Arial", 15), border_color="#2176ed",
                                             border_width=2, width=350, height=100, wrap="word")
        self.text.pack(padx=5, pady=5)
    def read_notes(self):
        with open(r"C:\Users\domin\PycharmProjects\Organizer Project\Notes.txt", 'r') as file:
            for line in file:
                self.text.insert(customtkinter.END, line)
        self.text.configure(state="disabled")




class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = CTk()
        self.root.title("Organizer")
        self.root.geometry("600x510")
        self.root.resizable(True, True)

        self.tap()
        self.option_menu()
        self.frame_option()
        self.calender()
        self.frame_button()
        self.input()
        self.save_button()
        self.del_button()

        # Read the mode from a file
        try:
            with open(r"C:\Users\domin\PycharmProjects\Organizer Project\apperance_mode.txt", 'r') as file:
                apperance_mode = file.read().strip()
        except FileNotFoundError:
            apperance_mode = "Dark"

        self.set_apperance_mode(apperance_mode)

        self.date_label = CTkLabel(master=self.frame_label, text="Selected Date: ", font=("Arial", 20))
        self.date_label.pack(padx=10, pady=10)

        self.toplevel_button()
        self.notes_window = None

    def tap(self):
        self.tap_frame = CTkFrame(self.root)
        self.tap_frame.pack(padx=10, pady=10, fill="y", side="left")
    def toplevel_button(self):
        self.button = customtkinter.CTkButton(master=self.tap_frame, text="Notes", command=self.open_toplevel)
        self.button.configure(width=70, font=("Arial", 15), hover_color="#1045e3", fg_color="#2176ed")
        self.button.pack(side="top", padx=10, pady=10)

    def open_toplevel(self):
        if self.notes_window is None or not self.notes_window.winfo_exists():
            self.notes_window = ToplevelWindow(self.root)
        else:
            self.notes_window.focus()
        self.tap_frame.focus_set()

    def option_menu(self):
        self.option = CTkOptionMenu(master=self.tap_frame, values=["Dark", "Light"], command=self.set_apperance_mode)
        self.option.configure(width=5, font=("Arial", 15), fg_color="#2176ed")
        self.option.pack(padx=10, pady=10)

    def set_apperance_mode(self, mode):
        apperance_mode = mode
        if apperance_mode == "Dark":
            set_appearance_mode("Dark")
            self.cal.configure(background="#1e1f1d", bordercolor="#1e1f1d", selectbackground="#2176ed",
                               selectforeground="white",
                               headersbackground="#1e1f1d", headersforeground="white", cursor="hand2",
                               foreground="white")
            apperance_mode = "Dark"
        elif apperance_mode == "Light":
            set_appearance_mode("Light")
            self.cal.configure(background="#d1cfcf", bordercolor="#d1cfcf", selectbackground="#2176ed",
                               selectforeground="white",
                               headersbackground="#d1cfcf", headersforeground="black", cursor="hand2",
                               foreground="black")
            apperance_mode = "Light"


        with open(r"C:\Users\domin\PycharmProjects\Organizer Project\apperance_mode.txt", 'w') as file:
            file.write(apperance_mode)

    def see_date(self, event=None):
        self.date = self.cal.get_date()
        self.date_label.configure(text="Selected Date: " + self.date)

    def calender(self):
        self.cal = Calendar(self.root, font="Arial 15", selectmode="day", locale="en_US", mindate=datetime.date.today(),
                            showweeknumbers=False, firstweekday="sunday")
        self.cal.pack(padx=10, pady=10, ipadx=10, ipady=10)
        self.cal.bind("<<CalendarSelected>>", self.see_date)


    def frame_button(self):
        self.frame = CTkFrame(self.root)
        self.frame.pack()

    def frame_option(self):
        self.frame_label = CTkFrame(self.root)
        self.frame_label.pack()

    def save_button(self):
        self.button = customtkinter.CTkButton(master=self.frame, text="Save Note", command=self.save_note)
        self.button.configure(width=160, font=("Arial", 15), hover_color="#1045e3", fg_color="#2176ed")
        self.button.pack(padx=10, pady=10, side=customtkinter.RIGHT)

    def del_button(self):
        self.button = customtkinter.CTkButton(master=self.frame, text="Delete Note", command=self.delete_note)
        self.button.configure(width=160, font=("Arial", 15), hover_color="#1045e3", fg_color="#2176ed")
        self.button.pack(padx=10, pady=10, side="left")
    def delete_note(self):

        with open(r"C:\Users\domin\PycharmProjects\Organizer Project\Notes.txt", 'r') as file:
            lines = file.readlines()

        lines = [line for line in lines if self.date not in line]

        with open(r"C:\Users\domin\PycharmProjects\Organizer Project\Notes.txt", 'w') as file:
            file.writelines(lines)
            print("Note deleted")


    def save_note(self):
        print(f"Date: {self.date}")
        print(f"Note: {self.entry.get('1.0', customtkinter.END).strip()}")
        if not self.cal.selection_get():
            print("No date selected")
            return
        if not self.entry.get("1.0", customtkinter.END).strip():
            print("No text to save")
            return

        if self.check_if_in_file():
            print("Date found in line")
            self.entry.delete("1.0", customtkinter.END)

        elif not self.check_if_in_file():
            print("Date not found in any line, writing to file")
            with open(r"C:\Users\domin\PycharmProjects\Organizer Project\Notes.txt", 'a') as file:
                text_to_retrieve = self.entry.get("1.0", customtkinter.END).strip()
                text_to_write = f"{text_to_retrieve} - {self.date}"
                print(f"Writing text: {text_to_write}")
                file.write(text_to_write + '\n')
                self.entry.delete("1.0", customtkinter.END)
    def check_if_in_file(self):
        with open(r"C:\Users\domin\PycharmProjects\Organizer Project\Notes.txt", 'r') as file:
            for line in file:
                if self.date in line:
                    return True
    def input(self):
        self.entry = CTkTextbox(master=self.frame, font=("Arial", 15), border_color="#2176ed", border_width=2, width=350, height=100, )
        self.entry.pack(padx=5, pady=5)

if __name__ == "__main__":
    app = App()
    app.root.mainloop()
