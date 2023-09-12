import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})


class Hotels:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        pass

    def bookHotel(self):
        """book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)
        pass

    def available(self):
        """check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False
        pass


class ReservationTickets:

    def __init__(self, customer_name, name_of_hotel):
        pass

    def generate(self):

        pass


print("List of hotels:")
print(df)
hotel_id = input("Enter the id of the hotel: ")

hotel = Hotels(hotel_id)

if hotel.available():
    hotel.bookHotel()
    name = input("Enter your name: ")

    reservation = ReservationTickets(name, hotel)
    reservation.generate()
else:
    print("Hotel is not available")
