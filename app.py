import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, 
    QMessageBox, QTabWidget, QGridLayout, QListWidgetItem, QRadioButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

class RecipeWindow(QWidget):
    def __init__(self, ingredients, recipes, urls):
        super().__init__()
        self.initUI(ingredients, recipes, urls)

    def initUI(self, ingredients, recipes, urls):
        self.setWindowTitle("Found Recipes")

        layout = QVBoxLayout()
        
        # Apply dark mode stylesheet
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        
        # Display selected ingredients
        ingredients_label = QLabel(f"Selected Ingredients: {', '.join(ingredients)}")
        layout.addWidget(ingredients_label)
        
        # Display found recipes
        results_label = QLabel("Found Recipes:")
        layout.addWidget(results_label)
        
        self.results_list = QListWidget()
        self.results_list.setStyleSheet("background-color: #444; color: white;")
        for recipe, url in zip(recipes, urls):
            item = QListWidgetItem(recipe)
            item.setData(Qt.ToolTipRole, url)  # Store URL in tooltip
            self.results_list.addItem(item)
        
        self.results_list.itemClicked.connect(self.open_recipe_url)  # Connect click event
        layout.addWidget(self.results_list)
        
        self.setLayout(layout)

    def open_recipe_url(self, item):
        url = item.data(Qt.ToolTipRole)
        if url:
            QDesktopServices.openUrl(QUrl(url))

class SettingsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.resize(300, 200)  # Increase the size of the settings window
        
        layout = QVBoxLayout()
        
        self.light_theme_radio = QRadioButton("Light Theme")
        self.dark_theme_radio = QRadioButton("Dark Theme")
        
        layout.addWidget(self.light_theme_radio)
        layout.addWidget(self.dark_theme_radio)
        
        self.apply_button = QPushButton("Save and Apply")
        self.apply_button.clicked.connect(self.save_settings)
        layout.addWidget(self.apply_button)
        
        self.setLayout(layout)

    def save_settings(self):
        if self.light_theme_radio.isChecked():
            self.main_window.setStyleSheet("background-color: white; color: black;")
            if self.main_window.recipe_window:  # Check if recipe_window exists
                self.main_window.recipe_window.setStyleSheet("background-color: white; color: black;")
            self.main_window.tab_widget.setStyleSheet("QTabWidget::pane { border: 1px solid #ccc; } QTabBar::tab { background: #f0f0f0; color: black; }")
        elif self.dark_theme_radio.isChecked():
            self.main_window.setStyleSheet("background-color: #2E2E2E; color: white;")
            if self.main_window.recipe_window:  # Check if recipe_window exists
                self.main_window.recipe_window.setStyleSheet("background-color: #2E2E2E; color: white;")
            self.main_window.tab_widget.setStyleSheet("QTabWidget::pane { border: 1px solid #444; } QTabBar::tab { background: #333; color: white; }")
        self.close()

class FlavorFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_ingredients = []
        self.recipe_window = None  # Initialize recipe_window attribute
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Flavor Finder")
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Select ingredients:")
        self.layout.addWidget(self.label)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabWidget::pane { border: 1px solid #ccc; } QTabBar::tab { background: #f0f0f0; color: black; }")
        
        ingredient_categories = {
            "Fruits": ["Apple", "Apricot", "Avocado", "Banana", "Blueberry", "Cherry", "Grapes", "Lemon", "Mango", "Orange", "Peach", "Pear", "Pineapple", "Strawberry"],
            "Vegetables": ["Carrot", "Cauliflower", "Cucumber", "Eggplant", "Garlic", "Onion", "Pepper", "Potato", "Spinach", "Tomato", "Zucchini"],
            "Proteins": ["Chicken", "Beef", "Fish", "Pork", "Salmon", "Tofu", "Turkey"],
            "Grains": ["Rice", "Quinoa", "Pasta", "Bread", "Oats", "Flour", "Barley", "Cornmeal"],
            "Dairy": ["Cheese", "Milk", "Yogurt", "Cream", "Butter"],
            "Legumes": ["Chickpeas", "Lentils", "Peas", "Beans"],
            "Condiments": ["Salt", "Pepper", "Sugar", "Honey", "Vinegar", "Soy Sauce", "Olive Oil", "Mustard", "Ketchup"],
            "Spices": ["Cinnamon", "Cumin", "Paprika", "Turmeric", "Oregano", "Basil", "Thyme", "Ginger"],
            "Nuts & Seeds": ["Almonds", "Walnuts", "Peanuts", "Chia Seeds", "Flaxseeds", "Pumpkin Seeds"]
        }
        
        for category, ingredients in ingredient_categories.items():
            tab = QWidget()
            tab_layout = QVBoxLayout()
            grid_layout = QGridLayout()
            # Create buttons for each ingredient and place them in a grid layout
            for index, ingredient in enumerate(ingredients):
                button = QPushButton(ingredient)
                button.clicked.connect(lambda checked, ing=ingredient: self.add_ingredient(ing))
                grid_layout.addWidget(button, index // 3, index % 3)  # Place in rows of 3
            
            tab_layout.addLayout(grid_layout)
            tab.setLayout(tab_layout)
            self.tab_widget.addTab(tab, category)

        self.layout.addWidget(self.tab_widget)
        
        self.selected_label = QLabel("Selected ingredients:")
        self.layout.addWidget(self.selected_label)
        
        self.selected_list = QListWidget()
        self.layout.addWidget(self.selected_list)
        
        self.remove_button = QPushButton("Remove Selected Ingredient")
        self.remove_button.clicked.connect(self.remove_ingredient)
        self.layout.addWidget(self.remove_button)

        self.search_button = QPushButton("Find Recipes")
        self.search_button.clicked.connect(self.find_recipes)
        self.layout.addWidget(self.search_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        self.layout.addWidget(self.settings_button)

        self.setLayout(self.layout)
        
    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
        
    def add_ingredient(self, ingredient):
        if ingredient not in self.selected_ingredients:
            self.selected_ingredients.append(ingredient)
            self.selected_list.addItem(ingredient)
        
    def remove_ingredient(self):
        selected_items = self.selected_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select an ingredient to remove.")
            return
        
        for item in selected_items:
            self.selected_ingredients.remove(item.text())
            self.selected_list.takeItem(self.selected_list.row(item))
        
    def find_recipes(self):
        if not self.selected_ingredients:
            QMessageBox.warning(self, "Input Error", "Please select at least one ingredient.")
            return
        
        ingredients = ','.join(self.selected_ingredients)
        app_id = 'f48c8fe6'
        app_key = '63d93afaa6febc6a7ba83576c6cef2d6'
        url = f"https://api.edamam.com/search?q={ingredients}&app_id={app_id}&app_key={app_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            recipes = []
            recipe_urls = []
            recipe_hits = data.get('hits', [])
            if recipe_hits:
                for recipe in recipe_hits:
                    recipe_title = recipe['recipe']['label']
                    recipe_url = recipe['recipe']['url']
                    recipes.append(recipe_title)
                    recipe_urls.append(recipe_url)  # Corrected line
            else:
                QMessageBox.information(self, "No Results", "No recipes found for the selected ingredients.")
                return
            
            self.recipe_window = RecipeWindow(self.selected_ingredients, recipes, recipe_urls)
            self.recipe_window.show()
        else:
            QMessageBox.critical(self, "API Error", "Failed to retrieve recipes. Please try again later.")

def main():
    app = QApplication(sys.argv)
    finder = FlavorFinder()
    finder.resize(600, 400)
    finder.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
