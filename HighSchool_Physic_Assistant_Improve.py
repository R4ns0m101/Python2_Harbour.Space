import math
import os
import json
from typing import Union, Dict, List
from datetime import datetime
from abc import ABC, abstractmethod

class Constant:
    """all physics constants"""
    GRAVITY_FORCE = 9.8  



class CalculationHistory:
    """
    context manager to save a history
    """
    def __init__(self, filename: str = "physics_history.json"):
        self.filename = filename
        self.history: List[Dict] = []
        self.load_history()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.save_history()
        if exc_type is not None:
            print(f"Error occured: {exc_value}")
        return False

    def add_calculation(self, topic: str, inputs: Dict, results: Dict):
        """Add a calculation to history"""
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": topic,
            "inputs": inputs,
            "results": results
        }
        self.history.append(entry)

    def save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError as error:
            print(f"Warning: Could not save history: {error}")

    def load_history(self):
        """Load history from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.history = json.load(f)
        except (IOError, json.JSONDecodeError) as error:
            print(f"Warning: Could not load history: {error}")
            self.history = []
            
    def display_history(self, limit: int = 10):
        """Display recent calculation history"""
        if not self.history:
            print("No calculation history")
            return
        
        print(f"CALCULATION HISTORY (Last {min(limit, len(self.history))} entries)")
        
        for entry in self.history[-limit:]:
            print(f"{entry['timestamp']} - {entry['topic']}")
            print(f"Inputs: {entry['inputs']}")
            print(f"Results: {entry['results']}")

    def clear_history(self):
        """Clear all history"""
        self.history = []
        self.save_history()
        print("History clear successfull!")

    


def get_float_input(prompt: str) -> Union[float, None]:
    """Get float input from user"""
    while True:
        try:
            value = input(prompt).strip()
            if value == "":
                return None
            return float(value)
        except ValueError:
            print("Invalid input! Please enter a number or press Enter to skip.")


def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Get integer input with validation"""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


"""
program function
- Motion
    1.Basic Motion
    2.Equation of Motion
    3.Free Fall
"""

class PhysicCalcution(ABC):
    """Abstract base class for all physics calculators"""
    
    def __init__(self, history: CalculationHistory):
        self.history = history
        self.inputs: Dict = {}
        self.results: Dict = {}
    
    @abstractmethod
    def get_inputs(self):
        """Get inputs from user"""
        pass
    
    @abstractmethod
    def calculate(self):
        """Perform calculations"""
        pass
    
    @abstractmethod
    def display_results(self):
        """Display calculation results"""
        pass
    
    def run(self):
        """Run the complete calculation workflow"""
        try:
            self.get_inputs()
            self.calculate()
            self.display_results()
            self.history.add_calculation(
                topic=self.__class__.__name__,
                inputs=self.inputs,
                results=self.results
            )
        except Exception as e:
            print(f"Calculation Error: {e}")



class Motion(PhysicCalcution):
    """ Calculate basic motion variables (v = s / t)"""
    
    def get_inputs(self):
        print("====== BASIC MOTION ======")
        print("Enter known values (if you don't know press Enter to skip)")
        print("Formula is v = s / t")
        
        self.inputs = {
            "speed": get_float_input("Speed (m/s): "),
            "time": get_float_input("Time (s): "),
            "distance": get_float_input("Distance (m): ")  
        }

    def calculate(self):
        speed = self.inputs["speed"]
        time = self.inputs["time"]
        distance = self.inputs["distance"]

        # Check if exactly 2 values provided
        none_count = sum(val is None for val in [speed, time, distance])
        if none_count != 1:
            raise ValueError("You must provide exactly 2 values!")

        try:
            if speed is None:
                if time == 0:
                    raise ValueError("Time cannot be zero!")
                self.results["speed"] = distance / time
            elif distance is None:
                self.results["distance"] = speed * time
            elif time is None:
                if speed == 0:
                    raise ValueError("Speed cannot be zero!")
                self.results["time"] = distance / speed
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero!")

    def display_results(self):
        print("====== Calculating ======")

        for key, value in self.results.items():
            print(f"{key.capitalize()}: {value:.2f}")



class EquationOfMotion(PhysicCalcution):
    def get_inputs(self):
        """ Calculate equations of motion variable"""
        print("====== EQUATIONS OF MOTION ======")
        print("Enter known values (if you don't know press Enter to skip)")
        print("we can calculate the problems that can use 3 formula show below")
        print("v = u + at")
        print("s = ut + 0.5at²")
        print("v² = u² + 2as")

    
        self.inputs = {
                "initial_velocity": get_float_input("Initial velocity u (m/s): "),
                "final_velocity": get_float_input("Final velocity v (m/s): "),
                "acceleration": get_float_input("Acceleration a (m/s²): "),
                "time": get_float_input("Time t (s): "),
                "distance": get_float_input("Distance s (m): ")
            }

    def calculate(self):
        initial_velocity = self.inputs["initial_velocity"]
        final_velocity = self.inputs["final_velocity"]
        acceleration = self.inputs["acceleration"]
        time = self.inputs["time"]
        distance = self.inputs["distance"]

        try:
            # v = u + at
            # find v
            if final_velocity is None and initial_velocity is not None and acceleration is not None and time is not None:
                self.results["final_velocity"] = initial_velocity + (acceleration * time)
                self.results["formula"] = "v = u + at"
            # find u
            elif final_velocity is not None and initial_velocity is None and acceleration is not None and time is not None:
                self.results["initial_velocity"] = final_velocity - (acceleration * time)
                self.results["formula"] = "v = u + at"
            # find a
            elif final_velocity is not None and initial_velocity is not None and acceleration is None and time is not None:
                if time == 0:
                    raise ValueError("Time cannot be zero!")
                self.results["acceleration"] = (final_velocity - initial_velocity) / time
                self.results["formula"] = "v = u + at"
            # find t
            elif final_velocity is not None and initial_velocity is not None and acceleration is not None and time is None:
                if acceleration == 0:
                    raise ValueError("Acceleration cannot be zero!")
                self.results["time"] = (final_velocity - initial_velocity) / acceleration
                self.results["formula"] = "v = u + at"

            # s = ut + 0.5at²
            # find s
            elif distance is None and initial_velocity is not None and time is not None and acceleration is not None:  # เปลี่ยนเป็น elif
                self.results["distance"] = (initial_velocity * time) + \
                    (0.5 * (acceleration * (time ** 2)))
                self.results["formula"] = "s = ut + 0.5at²"
            # find u
            elif distance is not None and initial_velocity is None and time is not None and acceleration is not None:
                if time == 0:
                    raise ValueError("Time cannot be zero!")
                self.results["initial_velocity"] = (distance - 0.5 * acceleration * (time ** 2)) / time  # ลบ "initial_velocity =" ซ้ำออก
                self.results["formula"] = "s = ut + 0.5at²"
            # find a
            elif distance is not None and initial_velocity is not None and time is not None and acceleration is None:
                if time == 0:
                    raise ValueError("Time cannot be zero!")
                self.results["acceleration"] =  2 * (distance - initial_velocity * time) / (time ** 2)
                self.results["formula"] = "s = ut + 0.5at²"
        

            # v² = u² + 2as
            # find v
            elif final_velocity is None and initial_velocity is not None and acceleration is not None and distance is not None:  # เปลี่ยนเป็น elif
                velocity_squared = (initial_velocity ** 2) + \
                    (2 * acceleration * distance)  # แก้ชื่อตัวแปรเป็น velocity_squared
                if velocity_squared < 0:
                    raise ValueError("Cannot calculate square root of negative number!")
                self.results["final_velocity"] = math.sqrt(velocity_squared)  # ใช้ชื่อตัวแปรที่ถูกต้อง
                self.results["formula"] = "v² = u² + 2as"
            # find u
            elif final_velocity is not None and initial_velocity is None and acceleration is not None and distance is not None:
                initial_velocity_squared = (
                    final_velocity ** 2) - (2 * acceleration * distance)  # เปลี่ยนชื่อให้สอดคล้อง
                if initial_velocity_squared < 0:
                    raise ValueError("Cannot calculate square root of negative number!")
                self.results["initial_velocity"] = math.sqrt(initial_velocity_squared)
                self.results["formula"] = "v² = u² + 2as"
            # find a
            elif final_velocity is not None and initial_velocity is not None and acceleration is None and distance is not None:
                if distance == 0:
                    raise ValueError("Distance cannot be zero!")
                self.results["acceleration"] = ((final_velocity ** 2) - (initial_velocity ** 2)) / (2 * distance)
                self.results["formula"] = "v² = u² + 2as"
            # find s
            elif final_velocity is not None and initial_velocity is not None and acceleration is not None and distance is None:
                if acceleration == 0:
                    raise ValueError("Acceleration cannot be zero!")
                self.results["distance"] = ((final_velocity ** 2) -
                            (initial_velocity ** 2)) / (2 * acceleration)
                self.results["formula"] = "v² = u² + 2as"
            
            else:
                raise ValueError("Insufficient data or invalid combination of inputs!")
            
        except ZeroDivisionError:
            raise ValueError("Division by zero error!")
    
    def display_results(self):
        print("CALCULATION RESULTS")
        print(f"Formula used: {self.results.get('formula', 'Unknown')}")
        
        for key, value in self.results.items():
            if key != "formula":
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")
    



class FreeFall(PhysicCalcution):
    """ Calculate Free fall variables"""
    def get_inputs(self):
        
        print("====== FREE FALL ======")
        print("Enter known values (if you don't know press Enter to skip)")

        self.inputs = {
            "final_velocity": get_float_input("Final velocity (m/s): "),
            "height": get_float_input("Height (m): "),
            "time": get_float_input("Time (s): ")
        }


    def calculate(self):  

        final_velocity = self.inputs["final_velocity"]
        height = self.inputs["height"] 
        time = self.inputs["time"]
        gravity = Constant.GRAVITY_FORCE 

        # Check if exactly 2 values provided
        none_count = sum(val is None for val in [final_velocity, height, time])
        if none_count != 1:
            raise ValueError("You must provide exactly 2 values!")

        # v = gt
        # find v
        try:
            if final_velocity is None and time is not None:
                self.results["final_velocity"] = gravity * time
                self.results["formula"] = "v = gt"

        # find t
            elif time is None and final_velocity is not None:
                self.results["time"] = final_velocity / gravity
                self.results["formula"] = "v = gt"

            # v² = 2gh
            # find v
            elif final_velocity is None and height is not None:  
                self.results["final_velocity"] = math.sqrt(2 * gravity * height)
                self.results["formula"] = "v² = 2gh"

            # find h
            elif height is None and final_velocity is not None:
                self.results["height"] = (final_velocity ** 2) / (2 * gravity)
                self.results["formula"] = "v² = 2gh"

            # h = 0.5gt²
            # find h
            elif height is None and time is not None: 
                self.results["height"] = 0.5 * gravity * (time ** 2)  
                self.results["formula"] = "h = 0.5gt²"

            # find t
            elif time is None and height is not None:
                self.results["time"] = math.sqrt(2 * height / gravity)
                self.results["formula"] = "h = 0.5gt²"
            
            else:
                raise ValueError("Insufficient data or invalid combination of inputs!")        
        
        except ZeroDivisionError:
            raise ValueError("Division by zero error!")

    def display_results(self):
        print("CALCULATION RESULTS")
        print(f"Formula used: {self.results.get('formula', 'Unknown')}")
        
        for key, value in self.results.items():
            if key != "formula":
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")




class PhysicsAssistant:

    banner = """
  _____  _               _                         _     _              _    
 |  __ \| |             (_)          /\           (_)   | |            | |   
 | |__) | |__  _   _ ___ _  ___     /  \   ___ ___ _ ___| |_ __ _ _ __ | |_  
 |  ___/| '_ \| | | / __| |/ __|   / /\ \ / __/ __| / __| __/ _` | '_ \| __| 
 | |    | | | | |_| \__ \ | (__   / ____ \\__ \__ \ \__ \ || (_| | | | | |_  
 |_|    |_| |_|\__, |___/_|\___| /_/    \_\___/___/_|___/\__\__,_|_| |_|\__| 
                __/ |                                                        
   __          |___/____               _        __  ___                      
  / _|            / ____|             | |      /_ |/ _ \                     
 | |_ ___  _ __  | |  __ _ __ __ _  __| | ___   | | | | |                    
 |  _/ _ \| '__| | | |_ | '__/ _` |/ _` |/ _ \  | | | | |                    
 | || (_) | |    | |__| | | | (_| | (_| |  __/  | | |_| |                    
 |_| \___/|_|     \_____|_|  \__,_|\__,_|\___|  |_|\___/                     
                                                                             
                                                                             
"""

    def __init__(self):
        self.history = None
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def show_banner(self):
        self.clear_screen()
        print(self.banner)

    def show_main_menu(self) -> int: 
        print("====== Main Menu ======")
        print("1. Motion Calculations")
        print("2. Show Calculations History")
        print("3. Clear History")
        print("0. Exit")
        
        return get_int_input("Enter your choice: ", 0, 3)  

    def show_motion_menu(self):
        print("====== Motion Menu ======")
        print("1. Basic Motion")
        print("2. Equation of Motion")
        print("3. Free Fall")

        choice = get_int_input("Enter your choice: ", 1, 3) 
        
        calculators = {
            1: Motion,
            2: EquationOfMotion,
            3: FreeFall
        }

        calculator = calculators[choice](self.history)
        calculator.run()

    def run(self):
        """ Main loop function"""
        self.show_banner()
        
        with CalculationHistory() as history:
            self.history = history
        
            while True:  
                try:
                    choice = self.show_main_menu() 
                    
                    if choice == 0:  
                        print("Thank you for using Physics Assistant")
                        print("Your calculation history has been saved")
                        break
                    elif choice == 1:  
                        self.show_motion_menu()
                    elif choice == 2:  
                        history.display_history()
                    elif choice == 3:
                        confirm = input("Are you sure you want to clear history? (yes/no): ")
                        if confirm.lower() == 'yes':
                            history.clear_history()
                    
                    input("Press Enter to continue...")
                
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    input("Press Enter to continue...")

if __name__ == "__main__":
    app = PhysicsAssistant()
    app.run()