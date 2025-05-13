import abc
import json
from datetime import datetime
from typing import Dict, List, Type, Union


class ProductException(Exception):
    """Base exception for product-related errors"""
    pass


class OutOfStockError(ProductException):
    """Raised when trying to sell more than available stock"""
    pass


class DuplicateProductError(ProductException):
    """Raised when adding a product with a duplicate ID"""
    pass


class InvalidProductDataError(ProductException):
    """Raised when loading invalid product data from file"""
    pass


class Product(abc.ABC):
    """Abstract base class for all products"""
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock
    
    @property
    def product_id(self) -> str:
        return self._product_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            raise ValueError("Price must be positive")
        self._price = new_price
    
    @property
    def quantity_in_stock(self) -> int:
        return self._quantity_in_stock
    
    def restock(self, amount: int):
        """Add more items to inventory"""
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        self._quantity_in_stock += amount
    
    def sell(self, quantity: int):
        """Sell items from inventory"""
        if quantity <= 0:
            raise ValueError("Sale quantity must be positive")
        if quantity > self._quantity_in_stock:
            raise OutOfStockError(f"Not enough stock. Available: {self._quantity_in_stock}, Requested: {quantity}")
        self._quantity_in_stock -= quantity
    
    def get_total_value(self) -> float:
        """Calculate total inventory value for this product"""
        return self._price * self._quantity_in_stock
    
    @abc.abstractmethod
    def __str__(self) -> str:
        """Abstract method for product information"""
        pass
    
    def to_dict(self) -> dict:
        """Convert product to dictionary for serialization"""
        return {
            'type': self.__class__.__name__,
            'product_id': self._product_id,
            'name': self._name,
            'price': self._price,
            'quantity_in_stock': self._quantity_in_stock
        }


class Electronics(Product):
    """Electronic product with warranty and brand"""
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, 
                 warranty_years: int, brand: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._warranty_years = warranty_years
        self._brand = brand
    
    @property
    def warranty_years(self) -> int:
        return self._warranty_years
    
    @property
    def brand(self) -> str:
        return self._brand
    
    def __str__(self) -> str:
        return (f"Electronics - ID: {self._product_id}, Name: {self._name}, "
                f"Brand: {self._brand}, Price: ${self._price:.2f}, "
                f"Warranty: {self._warranty_years} years, "
                f"Stock: {self._quantity_in_stock}")
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            'warranty_years': self._warranty_years,
            'brand': self._brand
        })
        return base_dict


class Grocery(Product):
    """Grocery product with expiry date"""
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, 
                 expiry_date: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._expiry_date = expiry_date
    
    @property
    def expiry_date(self) -> str:
        return self._expiry_date
    
    def is_expired(self) -> bool:
        """Check if the product has expired"""
        today = datetime.now().date()
        expiry = datetime.strptime(self._expiry_date, "%Y-%m-%d").date()
        return today > expiry
    
    def __str__(self) -> str:
        expired = " (EXPIRED)" if self.is_expired() else ""
        return (f"Grocery - ID: {self._product_id}, Name: {self._name}, "
                f"Price: ${self._price:.2f}, Expiry: {self._expiry_date}{expired}, "
                f"Stock: {self._quantity_in_stock}")
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            'expiry_date': self._expiry_date
        })
        return base_dict


class Clothing(Product):
    """Clothing product with size and material"""
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, 
                 size: str, material: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._size = size
        self._material = material
    
    @property
    def size(self) -> str:
        return self._size
    
    @property
    def material(self) -> str:
        return self._material
    
    def __str__(self) -> str:
        return (f"Clothing - ID: {self._product_id}, Name: {self._name}, "
                f"Size: {self._size}, Material: {self._material}, "
                f"Price: ${self._price:.2f}, Stock: {self._quantity_in_stock}")
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            'size': self._size,
            'material': self._material
        })
        return base_dict


class Inventory:
    """Manages a collection of products"""
    
    def __init__(self):
        self._products: Dict[str, Product] = {}
    
    def add_product(self, product: Product):
        """Add a new product to inventory"""
        if product.product_id in self._products:
            raise DuplicateProductError(f"Product ID {product.product_id} already exists")
        self._products[product.product_id] = product
    
    def remove_product(self, product_id: str):
        """Remove a product from inventory"""
        if product_id not in self._products:
            raise KeyError(f"Product ID {product_id} not found")
        del self._products[product_id]
    
    def search_by_name(self, name: str) -> List[Product]:
        """Search products by name (case-insensitive partial match)"""
        return [product for product in self._products.values() 
                if name.lower() in product.name.lower()]
    
    def search_by_type(self, product_type: Type[Product]) -> List[Product]:
        """Search products by type (class)"""
        return [product for product in self._products.values() 
                if isinstance(product, product_type)]
    
    def list_all_products(self) -> List[Product]:
        """Get all products in inventory"""
        return list(self._products.values())
    
    def sell_product(self, product_id: str, quantity: int):
        """Sell a specific product"""
        if product_id not in self._products:
            raise KeyError(f"Product ID {product_id} not found")
        self._products[product_id].sell(quantity)
    
    def restock_product(self, product_id: str, quantity: int):
        """Restock a specific product"""
        if product_id not in self._products:
            raise KeyError(f"Product ID {product_id} not found")
        self._products[product_id].restock(quantity)
    
    def total_inventory_value(self) -> float:
        """Calculate total value of all inventory"""
        return sum(product.get_total_value() for product in self._products.values())
    
    def remove_expired_products(self) -> List[str]:
        """Remove all expired grocery products and return their IDs"""
        expired_ids = []
        for product_id, product in list(self._products.items()):
            if isinstance(product, Grocery) and product.is_expired():
                expired_ids.append(product_id)
                del self._products[product_id]
        return expired_ids
    
    def save_to_file(self, filename: str):
        """Save inventory to JSON file"""
        data = {
            'products': [product.to_dict() for product in self._products.values()]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename: str):
        """Load inventory from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self._products.clear()
        
        for product_data in data['products']:
            try:
                product_type = product_data.pop('type')
                if product_type == 'Electronics':
                    product = Electronics(**product_data)
                elif product_type == 'Grocery':
                    product = Grocery(**product_data)
                elif product_type == 'Clothing':
                    product = Clothing(**product_data)
                else:
                    raise InvalidProductDataError(f"Unknown product type: {product_type}")
                
                self.add_product(product)
            except (KeyError, TypeError) as e:
                raise InvalidProductDataError(f"Invalid product data: {e}")


def display_menu():
    """Display the CLI menu options"""
    print("\nInventory Management System")
    print("1. Add Product")
    print("2. Sell Product")
    print("3. Restock Product")
    print("4. Search Products")
    print("5. List All Products")
    print("6. Remove Expired Groceries")
    print("7. Save Inventory to File")
    print("8. Load Inventory from File")
    print("9. Exit")


def get_product_details() -> dict:
    """Get common product details from user"""
    details = {
        'product_id': input("Enter product ID: "),
        'name': input("Enter product name: "),
        'price': float(input("Enter product price: ")),
        'quantity_in_stock': int(input("Enter initial stock quantity: "))
    }
    return details


def add_product(inventory: Inventory):
    print("\nAdd New Product")
    print("1. Electronics")
    print("2. Grocery")
    print("3. Clothing")
    choice = input("Select product type: ")
    
    common_details = get_product_details()
    
    try:
        if choice == '1':
            # Electronics
            warranty = int(input("Enter warranty years: "))
            brand = input("Enter brand: ")
            product = Electronics(
                **common_details,
                warranty_years=warranty,
                brand=brand
            )
        elif choice == '2':
            # Grocery
            expiry = input("Enter expiry date (DD-MM-YYYY): ")
            product = Grocery(
                **common_details,
                expiry_date=expiry
            )
        elif choice == '3':
            # Clothing
            size = input("Enter size: ")
            material = input("Enter material: ")
            product = Clothing(
                **common_details,
                size=size,
                material=material
            )
        else:
            print("Invalid choice")
            return
        
        inventory.add_product(product)
        print("Product added successfully!")
        print(product)
    except ValueError as e:
        print(f"Error: {e}")
    except DuplicateProductError as e:
        print(f"Error: {e}")


def sell_product(inventory: Inventory):
    product_id = input("Enter product ID to sell: ")
    quantity = int(input("Enter quantity to sell: "))
    
    try:
        inventory.sell_product(product_id, quantity)
        print(f"Successfully sold {quantity} of product {product_id}")
    except (KeyError, OutOfStockError, ValueError) as e:
        print(f"Error: {e}")


def restock_product(inventory: Inventory):
    product_id = input("Enter product ID to restock: ")
    quantity = int(input("Enter quantity to add: "))
    
    try:
        inventory.restock_product(product_id, quantity)
        print(f"Successfully restocked {quantity} to product {product_id}")
    except (KeyError, ValueError) as e:
        print(f"Error: {e}")


def search_products(inventory: Inventory):
    print("\nSearch Options:")
    print("1. By Name")
    print("2. By Type")
    choice = input("Select search method: ")
    
    if choice == '1':
        name = input("Enter product name to search: ")
        results = inventory.search_by_name(name)
    elif choice == '2':
        print("\nProduct Types:")
        print("1. Electronics")
        print("2. Grocery")
        print("3. Clothing")
        type_choice = input("Select product type: ")
        
        if type_choice == '1':
            results = inventory.search_by_type(Electronics)
        elif type_choice == '2':
            results = inventory.search_by_type(Grocery)
        elif type_choice == '3':
            results = inventory.search_by_type(Clothing)
        else:
            print("Invalid choice")
            return
    else:
        print("Invalid choice")
        return
    
    if results:
        print("\nSearch Results:")
        for product in results:
            print(product)
    else:
        print("No products found")


def list_products(inventory: Inventory):
    products = inventory.list_all_products()
    if products:
        print("\nAll Products:")
        for product in products:
            print(product)
        print(f"\nTotal Inventory Value: ${inventory.total_inventory_value():.2f}")
    else:
        print("No products in inventory")


def remove_expired(inventory: Inventory):
    expired_ids = inventory.remove_expired_products()
    if expired_ids:
        print("Removed expired products with IDs:", ", ".join(expired_ids))
    else:
        print("No expired products found")


def save_inventory(inventory: Inventory):
    filename = input("Enter filename to save: ")
    try:
        inventory.save_to_file(filename)
        print(f"Inventory saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")


def load_inventory(inventory: Inventory):
    filename = input("Enter filename to load: ")
    try:
        inventory.load_from_file(filename)
        print(f"Inventory loaded from {filename}")
    except FileNotFoundError:
        print("File not found")
    except (json.JSONDecodeError, InvalidProductDataError) as e:
        print(f"Error loading file: {e}")


def main():
    inventory = Inventory()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_product(inventory)
        elif choice == '2':
            sell_product(inventory)
        elif choice == '3':
            restock_product(inventory)
        elif choice == '4':
            search_products(inventory)
        elif choice == '5':
            list_products(inventory)
        elif choice == '6':
            remove_expired(inventory)
        elif choice == '7':
            save_inventory(inventory)
        elif choice == '8':
            load_inventory(inventory)
        elif choice == '9':
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
    cli = Inventory()
    cli.run()