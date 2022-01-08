import os
import csv

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.car_type = None
        self.brand = brand
        self.photo_file_name = photo_file_name
        try:
            self.carrying = float(carrying)
        except ValueError:
            self.carrying = None


    def get_photo_file_ext(self):
        ext = os.path.splitext(self.photo_file_name)
        return ext[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type='car'
        try:
            self.passenger_seats_count = int(passenger_seats_count)
        except ValueError:
            self.passenger_seats_count = None


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type='truck'
        try:
            self.body_whl=list(map(float, body_whl.split('x')))
            if len(self.body_whl)!=3:
                raise ValueError
            else:
                self.body_width=self.body_whl[1]
                self.body_height=self.body_whl[2]
                self.body_length=self.body_whl[0]
        except (ValueError, IndexError):
            self.body_width=float(0)
            self.body_height=float(0)
            self.body_length=float(0)


    def get_body_volume(self):
        return self.body_width*self.body_height*self.body_length

class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type='spec_machine'
        self.extra = extra


def get_car_list(csv_filename):
    ext=['.jpeg', '.png', '.jpg', '.gif']
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if len(row)!=7:
                continue
            if (isinstance(row[0],str) and len(row[0])>0):
                if row[0] == 'car':
                        el = Car(brand=row[1], passenger_seats_count=row[2], photo_file_name=row[3], carrying=row[5])
                        if isinstance(el.carrying, float) and isinstance(el.passenger_seats_count, int) and el.get_photo_file_ext() in ext and el.brand:
                            car_list.append(el)
                        else:
                            continue

                if row[0] =='truck':
                        el = Truck(brand=row[1], photo_file_name=row[3], body_whl=row[4], carrying=row[5])
                        if isinstance(el.carrying, float) and el.get_photo_file_ext() in ext and el.brand:
                            car_list.append(el)
                        else:
                            continue

                if row[0] == 'spec_machine':
                        el = SpecMachine(brand=row[1], photo_file_name=row[3], carrying=row[5], extra=row[6])
                        if isinstance(el.carrying, float) and el.get_photo_file_ext() in ext and el.brand and el.extra:
                            car_list.append(el)
                        else:
                            continue
            else:
                continue


    return car_list
