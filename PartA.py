

class Pet:
    def __init__(self, name, age, sex, petID, owner_name):
        self.name = name
        self.age = age
        self.sex = sex
        self.petID = petID
        self.owner_name = owner_name

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}, Sex: {self.sex}, Pet ID: {self.petID}, Owner: {self.owner_name}")

        def update_attribute(self, attribute, value):
            valid_types = {
                "name": str, "age": int, "sex": str, "petID": str, "owner_name": str
            }
            if attribute in valid_types and isinstance(value, valid_types[attribute]):
                setattr(self, attribute, value)
            else:
                print(f"Invalid type for {attribute}.")

    def display_info(self):
        pass

    def update_attribute(self, attribute, value):
        pass


class Dog(Pet):
    def __init__(self, name, age, sex, petID, owner_name, breed, energy_level):
        super().__init__(name, age, sex, petID, owner_name)
        self.breed = breed
        self.energy_level = energy_level

        def display_info(self):
            return f"{super().display_info()}, Breed: {self.breed}, Energy Level: {self.energy_level}"

        def update_attribute(self, attribute, value):
            valid_types = {
                "breed": str, "energy_level": int
            }
            if attribute in valid_types and isinstance(value, valid_types[attribute]):
                setattr(self, attribute, value)
            else:
                super().update_attribute(attribute, value)

# Creating instances
pet1 = Pet("Milo", 4, "Female","201","Emma")
dog1 = Dog("Rex", 6, "Male", 202, "Jake", "Husky", 8)

# Displaying initial info
print(pet1.display_info())
print(dog1.display_info())

#Updating attributes
pet1.update_attribute("name", "Bella")
pet1.update_attribute("age", 5)
dog1.update_attribute("breed", "German Shepherd")
dog1.update_attribute("energy_level", 9)

# Displaying updated info
print(pet1.display())
print(dog1.display())


