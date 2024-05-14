from collections import UserDict

class PhoneValidateError(Exception):
     pass

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):

    def __init__(self, phone):
         self.validate_phone(phone)
         super().__init__(phone)

    def validate_phone(self, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise PhoneValidateError("Number should be 10 digits")
               
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number: str):
        phones_list_str = [str(phone) for phone in self.phones]

        if phone_number in phones_list_str:
            raise ValueError("Phone is alredy in the list")
        
        self.phones.append(Phone(phone_number))

    def edit_phone(self, old_number: str, new_number: str):
        try:
             Phone(new_number)
        except PhoneValidateError:
            raise PhoneValidateError("This number is not valid")
        
        for number in self.phones:
            if number.value == old_number:
                number.value = new_number
                break
               
    def find_phone(self, phone:str):

        for number in self.phones:
            if number.value == phone:
                return phone
        
        return f"Phone {phone} is not in the list"

    def remove_phone(self, phone: str) -> None:
        self.phones.remove(self.find_phone(phone))

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, user_record: Record):
        user_name = user_record.name.value

        if user_name in self.data:
             raise ValueError("User is alredy in the list")

        self.data[user_name] = user_record

    def find(self, name:str) -> Record:
        if name not in self.data:
            raise ValueError("User not found")
        
        return self.data[name]

    def delete(self, name:str) -> None:
        if name not in self.data:
            raise ValueError("User not found")
        
        del self.data[name]

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("tr34567890") # PhoneValidateError: Number should be 10 digits
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

#після видалення перевіряємо які контакти залишились
for name, record in book.data.items():
     print(record)
