# Web Scraper (Zbieracz Opinii)

Welcome to **Web Scraper**, an application designed to extract and analyze product reviews from [Ceneo.pl](https://www.ceneo.pl/). This project is an easy-to-use tool that allows users to gather and manage product reviews, view statistics, and export data in popular formats.

---

## **Purpose of the Application**

The main goal of the application is to:
- Simplify access to product reviews.
- Provide useful insights through statistics and visualizations.
- Help users manage and analyze reviews in a structured and intuitive way.

---

## **How the Application Works**

The application allows users to retrieve product reviews from Ceneo.pl using a unique product ID. It collects the following information for each review:
- Reviewer information (e.g., username).
- Recommendations (positive/negative).
- Star ratings.
- Review content, advantages, and disadvantages.
- Purchase verification status.
- Review submission and purchase dates.
- Feedback details (e.g., helpful or non-helpful votes).

Once the reviews are extracted, they are saved in a manageable structure (e.g., JSON, CSV, or XLSX). Users can then view the reviews along with statistical data and graphical visualizations of collected metrics, such as:
- The distribution of star ratings (bar charts).
- The proportion of recommendations (pie charts).

The interface is built using **Flask**, with HTML, CSS, and essential JavaScript for a smooth user experience. All functionality has been designed with error handling, ensuring stability during use.

---

## **About the Author**

Hello! My name is **Maksym Shablovskyy**, student ID **237161**, and I’m the developer behind this project.  
This application is my first completed project, and I’m incredibly proud of it. It was a great challenge – one that helped me learn and work with various new technologies. Despite encountering difficulties, I successfully handled everything and greatly enjoyed the experience.

### **Inspirations and Learning**
While working on the project, I aimed to not only complete an assignment but also build something meaningful that could help users. The experience taught me:
- Advanced programming practices.
- How to handle real-world data processing tasks.
- Web development using Flask and integration with JavaScript, HTML, and CSS for an optimized interface.
- Proper error handling to provide a reliable user experience.

---

## **Potential Use Cases**

Here are a few ways this application can be used:  
- **Helping consumers**: Easily compare reviews and ratings before purchasing a product.  
- **For marketing analysts**: Analyze customer feedback to better understand product strengths and weaknesses.  
- **Data handling**: Export reviews in `.json`, `.csv`, or `.xlsx` format for further external processing.  
- **Content generation**: Use collected data to create reports, graphs, and visualizations for business needs.  

---

## **Potential Problems & Errors**

While this application is designed specifically to scrape user comments from **ceneo.pl**, there are some inherent limitations and potential issues to be aware of:

1. **Website Security Measures**  
   Although the app is tailored for ceneo.pl, the site's security mechanisms—such as rate limiting, bot detection, or Captchas—may occasionally interfere with the scraping process. As a result, issues can arise, particularly when attempting to scrape pages from a server environment.

2. **Server vs. Local Machine Execution**  
   Running the `page.py` script directly from your **own computer (local machine)** is much more reliable and will almost certainly load and scrape the first page successfully. However, running the same script from a **server environment** may lead to less reliable results due to the server's IP being flagged by ceneo.pl's security systems or other unforeseen factors.

3. **Limitations on Scraping Multiple Pages**  
   While the app is capable of accessing comments across multiple pages of a product, there is no **100% guarantee** that it will successfully scrape more than one page in all cases. Issues such as connection interruptions, site-specific limitations, or security measures may prevent this feature from always working as intended.

4. **Confidence in the First Page**  
   If the app is run from your local machine, scraping the **first page of comments** should always succeed. However, when running the app on a remote server, I cannot promise the same reliability for even the first page due to the aforementioned security-related constraints.

If you encounter recurring problems or see room for improvement, please feel free to open an issue or contribute to the repository.

---

## **Acknowledgments**

I’d like to express my gratitude to my teachers and everyone else who helped along the way:
- **To my teachers:** Thank you for your knowledge, guidance, and valuable advice during this project.  

---

## **GitHub Repository**

You can check out the source code and learn more about the project on its [GitHub repository](https://github.com/mshablovskyy/WebScraping).  

---

## **Technologies Used**

- **BeautifulSoup4**: Parsing HTML and XML for extracting product opinions.  
- **Flask**: Backend framework used for building the web application.  
- **Jinja2**: Templating engine for rendering dynamic web pages.  
- **Matplotlib**: Used for generating visualizations from opinion data (charts and graphs).  
- **Requests**: Library for sending HTTP requests to fetch data from Ceneo.pl.  
- **XlsxWriter**: Exporting data to Excel `.xlsx` files.  
- **JSON** and **CSV modules**: For storing and exporting review data.  
- **datetime**: Managing timestamps and dates.  
- **threading (Lock)**: Synchronizing certain operations to avoid issues in multi-threaded contexts.  
- **HTML, CSS, and JavaScript**: For building a responsive and interactive user interface.

---

Feel free to reach out if you have feedback or suggestions for the project!