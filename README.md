# Django Ecommerce
This Django e-commerce project is a robust web application designed to facilitate online shopping experiences. It offers a user-friendly interface for customers to browse through a wide range of products, add items to their cart, and securely complete their purchases. The platform includes features for product categorization, user authentication, and order management.

Key Features:
- User-friendly product catalog with detailed descriptions and images.
- User authentication and account management for personalized shopping experiences.
- Shopping cart functionality for adding, modifying, and removing items.
- Secure checkout process with payment integration.
- Order history and tracking for customers.
- Admin interface for managing products, orders, and user accounts.
- Responsive design for seamless browsing on various devices.

This project serves as an excellent foundation for building a fully functional e-commerce website. It incorporates best practices in Django development to ensure scalability, security, and maintainability. Feel free to explore, modify, and enhance this project to meet specific business requirements and create a thriving online store.

## Running the Application

1. Clone the repository and navigate to the working directory:
    ```bash
    git clone https://github.com/realsanjeev/django-ecommerce.git
    cd django-ecommerce
    ```

2. Create a virtual environment and install the requirements:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Or If you have Docker installed on your machine, you can use the provided Dockerfile to run the project**

   First, build the Docker image:
    ```bash
    docker build -t django-ecommerce .
    ```

   Then, run the Docker container:
    ```bash
    docker run -p 8000:8000 --name django-ecommerce-container django-ecommerce
    ```

This will start the Django e-commerce application and make it accessible at `http://localhost:8000` on your local machine.

You can try to access supperuser or login to the app using admin name `admin@admin.com` and password for it is `admin`

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to submit a pull request.

## Contact Me

<table>
  <tr>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/instagram.png" alt="Instagram" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/twitter.png" alt="Twitter" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/github.png" alt="GitHub" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/linkedin-logo.png" alt="LinkedIn" width="50" height="50"></td>
  </tr>
</table>
