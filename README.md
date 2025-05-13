Inventory Management System: 
System in Python that can manage different types of products, handle stock operations, sales, and persist data applied OOP concepts, The code follows clean Python practices with strings, and encapsulation. The design is extensible for adding more product types or features in the future. This simplified version removes some advanced features like JSON persistence and custom exceptions to keep demonstrating all the core OOP concepts required. 


#Features: 

#Basic Inventory Management: 
1. Add/remove products. 
2. Sell and restock items. 
3. List all products. 
4. Remove expired groceries. 
5. Search by name or type. 
6. Calculate total inventory value.

#Key OOP Concepts: 
1. Inheritance (Product subclasses). 
2. Encapsulation (protected attributes with properties). 
3. Polymorphism (different string representations). 
4. Abstraction (ABC module).

#Product Subclasses: 
1. Electronics with warranty and brand. 
2. Grocery with expiry date checking. 
3. Clothing with size and material. 
4. Each with their specific attributes and string representation. 

#Persistence: 
1. Save to JSON file. 
2. Load from JSON file with proper reconstruction. 

#Error Handling: 
1. Custom exceptions enable to specific error messages.
2. Input validation throughout the data. 

#User_Interface: 
1. Command-line interface with menu system.
2. Clear feedback for all operations.
