# Neuro_check-main
 
Neurocheck is a Flask application designed to predict whether a person is at risk of having a stroke. Leveraging the power of machine learning, Neurocheck utilizes a gradient boosting model to analyze various medical markers and provide accurate predictions with a 94 percent accuracy rate. This project showcases the potential of AI in healthcare and aims to assist in early detection and prevention of strokes, ultimately saving lives.

Machine Learning Model: The core of Neurocheck relies on a machine learning model called gradient boosting. This model works by combining multiple weak predictive models, known as decision trees, into a strong predictive model. The gradient boosting algorithm trains the model to learn from a training dataset, improving its predictive capabilities over time. By leveraging this model, Neurocheck can accurately assess the risk of stroke based on various medical indicators. Deployment on AWS EC2: Neurocheck is deployed using an AWS EC2 instance, which provides a scalable and secure infrastructure for hosting the application. The EC2 instance makes use of the powerful computing resources provided by AWS, ensuring high performance and availability. This deployment method allows users to access Neurocheck remotely, making it accessible to healthcare professionals and individuals seeking to assess their stroke risk.

Server Configuration with Nginx To handle HTTP requests and ensure smooth communication between the user and the Neurocheck application, the deployment on the AWS EC2 instance utilizes two key technologies: Nginx and Gunicorn.

Nginx acts as a reverse proxy server, directing incoming requests to the appropriate backend server. It provides load balancing and caching features, enhancing the performance and scalability of the application. Nginx also adds an extra layer of security by protecting against common web vulnerabilities.

Gunicorn, short for Green Unicorn, serves as the interface between the application and the web server. It acts as a Python web server gateway interface (WSGI) HTTP server, running multiple worker processes to handle incoming requests efficiently. Gunicorn ensures that the Neurocheck Flask application is seamlessly connected to Nginx, providing a smooth user experience.
