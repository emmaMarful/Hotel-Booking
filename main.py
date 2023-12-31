import pandas as pd
from fpdf import FPDF
from datetime import datetime

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_card = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("card_security.csv", dtype=str)

class Hotels:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.id = df.loc[df["id"] == self.hotel_id, "id"].squeeze()
        self.hotel_name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.city = df.loc[df["id"] == self.hotel_id, "city"].squeeze()
        self.cap = df.loc[df["id"] == self.hotel_id, "capacity"].squeeze()

    def bookHotel(self):
        """book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False
        pass


class ReservationTickets:

    def __init__(self, customer_name, hotel_obj):
        self.customer_name = customer_name
        self.hotel_obj = hotel_obj
        hotelRev = hotel_obj

    def generate(self):
        # generate a pdf as a receipt
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Arial", style="B", size=14)
        pdf.cell(w=0, h=24, txt="Receipt for EM's Booking", align="L")

        date = datetime.now().strftime("%d-%m-%Y")
        timee = datetime.now().strftime("%I:%M:%S")

        pdf.set_font(family="Times", style="I", size=15)
        pdf.cell(w=0, h=24, txt=f'Date: {date}', align="R")
        pdf.cell(w=0, h=39, txt=f'Time: {timee}', align="R", ln=1)

        # name
        pdf.set_font(family="Arial", style="B", size=13)
        pdf.cell(w=0, h=24, txt=f'Name: {self.customer_name}', align="L", ln=1)

        # add a header
        col = df.columns
        col = [i.title() for i in col]

        pdf.set_font(family="Arial", style="", size=13)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=25, h=12, txt=col[0], align="C", border=1)
        pdf.cell(w=70, h=12, txt=col[1], align="C", border=1)
        pdf.cell(w=60, h=12, txt=col[2], align="C", border=1)
        pdf.cell(w=25, h=12, txt=col[3], align="C", border=1, ln=1)

        pdf.set_text_color(0, 0, 0)
        pdf.cell(w=25, h=12, txt=self.hotel_obj.id, align="C", border=1)
        pdf.cell(w=70, h=12, txt=self.hotel_obj.hotel_name, align="C", border=1)
        pdf.cell(w=60, h=12, txt=self.hotel_obj.city, align="C", border=1)
        pdf.cell(w=25, h=12, txt=str(self.hotel_obj.cap), align="C", border=1, ln=1)

        pdf.set_font(family="Arial", style="I", size=13)
        pdf.cell(w=0, h=20, txt="Thank you for choosing us!", align="L")
        pdf.output("receipt.pdf")

        print("Hotel has been booked")


class CreditCard:
    def __init__(self, number):
        self.number = number

    def credit_validate(self, exp, cvc, holder):
        card_data = {"number": self.number, "expiration": exp, "holder": holder, "cvc": cvc}
        if card_data in df_card:
            return True


class creditCardSecurity(CreditCard):
    def authenticate(self, ent_pass):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if ent_pass == password:
            return True
        else:
            return False





print("List of hotels:")
print(df)
hot_id = [i for i in df["id"]]
hotel_id = input("Enter the id of the hotel: ")

hotel = Hotels(hotel_id)

if hotel_id in hot_id:
    # book a hotel if available
    if hotel.available():
        # credit card validation
        credit_card = creditCardSecurity(number="1234567890123456")
        if credit_card.credit_validate(exp="12/26", holder="JOHN SMITH", cvc="123"):
            if credit_card.authenticate(ent_pass="mypass"):
                hotel.bookHotel()
                name = input("Enter your name: ")

                reservation = ReservationTickets(name, hotel)
                reservation.generate()

            else:
                print("Validation failed")
        else:
            print("Enter a correct card")
    else:
        print("Hotel is not available")

else:
    print("Select an available hotel")
