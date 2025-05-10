1. Application Description
The Flea Market is a full-featured web application that enables users to buy and sell second-hand items. Built using Django framework, it's designed to provide a user-friendly platform for online marketplace transactions.

User Communities:

Regular Users: Can browse products, create their own listings, add items to cart, place orders, and manage their profile information
Administrative Users: Manage product listings, user accounts, orders, and the overall system

2. Authentication and Authorization Scheme
The application implements Django's built-in authentication system with custom user models. Authorization is handled through session-based authentication, with different permissions based on user roles.
All non-logged in users are redirected to the login page or the about page, depending on which page they are trying to access. Authentication is required for all features except viewing the about page.
User Groups and Permissions:
Username/Group | Password    | Active | Staff | Superuser | Regular User | Seller | Admin
---------------|-------------|--------|-------|-----------|--------------|--------|-------
tester         | {iSchoolUI} |   X    |   X   |     X     |              |        |   X
sysadmin       | {iSchoolUI} |   X    |   X   |     X     |              |        |   X
regular_user   | {iSchoolUI} |   X    |       |           |      X       |        |
seller_user    | {iSchoolUI} |   X    |       |           |      X       |   X    |
buyer_user     | {iSchoolUI} |   X    |       |           |      X       |        |

3. Testing Instructions
Setup

Create a new project in PyCharm and open the project directory
Run migrations: python manage.py migrate
Run the server: python manage.py runserver
Access the application at http://127.0.0.1:8000/

Testing User Authentication

Access the home page without logging in to be redirected to the About page
Click on "Login" in the upper right corner
Use the provided user credentials to test different user roles

Testing Product Browsing

After logging in, access the Products page from the navigation menu
Use the search bar to search for specific products
Sort products by price or popularity using the options at the top
View product details by clicking on a product

Testing Shopping Cart

Add a product to the cart by clicking "Add to Cart" on a product detail page
Navigate to the Shopping Cart page from the navigation menu
Modify quantities or remove items from the cart
Proceed to checkout

Testing Order Placement

From the shopping cart, click "Proceed to Checkout"
Review shipping information and order summary
Complete the order process
View order confirmation and check the Orders page for order history

Testing User Profile Management

Navigate to the User Center from the navigation menu
Update shipping address information
View order history

Testing Product Management (for seller accounts)

Log in as a seller account (seller_user)
Add a new product by clicking "Add Product" on the Products page
Edit or delete one of your existing products
View your products in the product listings

Testing Administrative Functions

Log in as a superuser (tester or sysadmin)
Access the Django admin interface at http://127.0.0.1:8000/admin/
Manage users, products, orders, and other data through the admin interface

5. Other Relevant Information
Features Implemented:

User authentication and authorization
Product listing and categorization
Shopping cart functionality
Order processing system
User profile management
Seller dashboard for product management
Search and filtering capabilities

Technology Stack:

Django 4.1
SQLite database
JavaScript for dynamic frontend interactions
Bootstrap-inspired custom CSS
jQuery for AJAX requests

Project Structure
The project follows Django's recommended structure with separate apps for different functionality:

fm_user: User authentication and profile management
fm_goods: Product listings and management
fm_cart: Shopping cart functionality
fm_order: Order processing and history