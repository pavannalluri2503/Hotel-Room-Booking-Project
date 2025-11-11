#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt


# In[2]:


rooms = {
    "standard": {"total": 10, "price": 1400.0, "available": 10},
    "deluxe": {"total": 5, "price": 2000.0, "available": 5},
    "suite":  {"total": 2, "price": 5000.0, "available": 2},
}

bookings = []


# In[3]:


def show_rooms(rooms_data):
    """Function shows the room data available."""
    print("\n<----- Available Rooms ----->")
    for room, info in rooms_data.items():
        print(f"Room Type: {room.title()}\n\tPrice/night: Rs.{info["price"]:.2f}\n\tAvailable: {info["available"]}")
    print()


# In[4]:


def check_availabilty(rooms_data, room_type):
    """Function checks whether the selected room type is available or not."""
    if room_type not in rooms_data:
        return False
    return rooms_data[room_type]["available"] >= 1


# In[13]:


def generate_booking_id():
    """Function used to generate the booking id for new bookings."""
    id_no = str(dt.datetime.now()).replace('-','').replace(':','').replace(' ','')[:-7]
    return ('B'+id_no)    


# In[6]:


def book_room(rooms_data, bookings_list):
    """Function used to book a room using the information taken from user."""
    print("\n<----- Book a Room ----->")
    name = input("Please enter your name:").title()
    room_type = input("Please enter type of room:").lower()
    nights = int(input("Please enter number of nights of stay:"))

    if not check_availabilty(rooms, room_type):
        print(f"Sorry, no {room_type} rooms are available right now.")
        return

    confirm = input("Confirm booking? (y/n):").lower()
    if confirm != 'y':
        print("Booking cancelled.")
        return

    booking_id = generate_booking_id()
    price_per_night = rooms_data[room_type]['price']
    subtotal = price_per_night*nights
    taxes = subtotal * 0.12
    total = subtotal + taxes

    booking = {
        'id': booking_id,
        'name': name,
        'room_type': room_type,
        'nights': nights,
        'price_per_night': price_per_night,
        'subtotal': subtotal,
        'taxes': taxes,
        'total': total
    }

    rooms_data[room_type]["available"] -= 1
    bookings_list.append(booking)
    with open('booking_data.txt', 'a') as f:
        f.write(f"-> {booking}\n")

    print("\nBooking successful!")
    print(f"Booking ID: {booking_id}")
    print(f"Guest: {name}\nRoom : {room_type.title()}, Nights: {nights}")
    print(f"Total Bill (incl. taxes): Rs.{total:.2f}\n")


# In[7]:


def cancel_booking(rooms_data, bookings_list):
    """Function used to cancel a booking based on the booking id generated during booking a room."""
    print("\n<----- Cancel Booking ----->")
    if not bookings_list:
        print("No active bookings to cancel.")
        return

    bid = input("Enter Booking ID to cancel:").title()

    booking = False
    for b in bookings_list:
        if b['id'] == bid:
            booking = b
            break
    if not booking:
        print(f"No booking found with ID: {bid}.")
        return

    print("Booking found.")
    print(f"ID: {booking['id']}")
    print(f"Guest: {booking['name']}\nRoom: {booking['room_type'].title()}, Nights: {booking['nights']}")
    print(f"Total Bill: Rs.{booking['total']:.2f}\n")
    confirm = input("Confirm cancellation? (y/n):").lower()
    if confirm != 'y':
        print("Cancellation aborted.")
        return

    print(f"Cancellation is done. Amount of Rs.{booking['subtotal']} will be refunded.")
    rooms_data[booking['room_type']]['available'] += 1
    bookings_list.remove(booking)
    print(f"Booking {bid} is cancelled and details are updated.")
    print("Thank You! Visit Again!")


# In[8]:


def view_bookings(bookings_list):
    """Function used to view the active bookings in hotel."""
    print("\n<----- Active Bookings ----->")
    if not bookings_list:
        print("No active bookings.")
        return
    for b in bookings_list:
        print(f"Id: {b['id']}")
        print(f"Guest: {b['name']}\nRoom: {b['room_type']}, Nights: {b['nights']}")
        print(f"Total bill: {b['total']}\n\n")
    print()


# In[9]:


def previous_bookings():
    """Function used to print overall bookings done in the past."""
    with open('booking_data.txt', 'r') as f:
        data = f.read()
        print(data)
    return


# In[10]:


def main_menu():
    """Function used to initiate the work in booking a room in hotel."""
    print("\n=====Hotel Booking System=====")
    print("\n1. Show Rooms\n2. Book a Room\n3. Cancel Booking\n4. View Bookings\n5. View Overall Bookings\n6. Exit Menu")    
    while True:
        ch = int(input("\nEnter Your Choice (1-6):"))
        if ch == 1:
            show_rooms(rooms)
        elif ch == 2:
            book_room(rooms, bookings)
        elif ch == 3:
            cancel_booking(rooms, bookings)
        elif ch == 4:
            view_bookings(bookings)
        elif ch == 5:
            previous_bookings()
        elif ch == 6:
            print("\nThank You! Visit Again!")
            break
        else:
            print("\nEnter a valid input.")
        
