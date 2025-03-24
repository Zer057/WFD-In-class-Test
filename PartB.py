import unittest

class Pet:
    def __init__(self, name, age, sex, petID, owner_name):
        self.name = name
        self.age = age
        self.sex = sex
        self.petID = petID
        self.owner_name = owner_name

    def display_info(self):
        return f"Pet - Name: {self.name}, Age: {self.age}, Sex: {self.sex}, ID: {self.petID}, Owner: {self.owner_name}"

    def update_attribute(self, attribute, value):
        valid_types = {
            "name": str, "age": int, "sex": str, "petID": str, "owner_name": str
        }
        if attribute in valid_types and isinstance(value, valid_types[attribute]):
            setattr(self, attribute, value)
        else:
            print(f"Invalid type for {attribute}.")

        class Dog(Pet):
            def _init__(self, name, age, sex, petID, owner_name, breed, energy_level):
                super().__init__(name, sex, petID, owner_name)
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

            # Unit Testing
            class TestPetClasses(unittest.TestCase):
                def setUp(self):
                    self.pet1 = Pet("Milo", 4, "Female", 201, "Emma")
                    self.dog1 = Dog("Rex", 6, "Male", 202, "Jake", "Husky", 8)
                    self.dog2 = self.dog1

                def test_instance_of_pet(self):
                    self.assertIsInstance(self.pet1, Pet)
                    self.assertIsInstance(self.dog1, Pet)

                def test_not_instance_of_dog(self):
                    self.assertNotIsInstance(self.pet1, Dog)

                def test_identical_objects(self):
                    self.assertIs(self.dog1, self.dog2)

                def test_update_attribute(self):
                    self.pet1.update_attribute("name", "Bella")
                    self.assertEqual(self.pet1.name, "Bella")

                    self.pet1.update_attribute("age", 5)
                    self.assertEqual(self.pet1.age, 5)

                    self.dog1.update_attribute("breed", "German Shepherd")
                    self.assertEqual(self.dog1.breed, "German Shepherd")

                    self.dog1.update_attribute("energy_level", 9)
                    self.assertEqual(self.dog1.energy_level, 9)

            if __name__ == "__main__":
                unittest.main()
