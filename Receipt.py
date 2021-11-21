import enum
# Using enum class create enumerations
class Unit(enum.Enum):
   Gramm = 1
   Stueck = 2
   Packung = 3
   Milliliter = 4

class Receipt:
  def __init__(self, name, ingridients):
    self.name = name
    self.ingridients = ingridients

  def ToString(self):
    string = ""
    string += self.name + "\n"
    for r in self.ingridients:
        temp = f"{r[0]} {r[1]} {r[2].name}"
        string += f"{temp}\n"
    return string 
    

