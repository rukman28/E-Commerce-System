# AI Commerce Automation

Welcome to the AI Commerce Automation repository! 🚀

## About

AI Commerce Automation leverages emerging technologies to revolutionize ecommerce operations. By harnessing the power of artificial intelligence, this application automates various tasks, streamlines processes, and enhances the overall efficiency of your online store.

## Features

### Search By Image

#### Client-Side (JavaScript):

1. **User Input:** The user selects an image file from their device using an HTML file input element.
2. **Image Processing:** JavaScript reads the image file and converts it into a Base64 encoded string, which is a text format suitable for sending through an HTTP request.
3. **AJAX Request:** The JavaScript code sends an AJAX request to the server endpoint `/search-by-image/`, carrying the Base64 encoded image data in the request body.

#### Server-Side (Django):

1. **Receive Image Data:** The Django view function receives the AJAX request containing the Base64 encoded image data.
2. **Process Image:** The image is processed using a model hosted on the Replicate computing platform, which extracts a caption from the image using machine learning.
3. **Search for Similar Products:** The extracted text data is used to search for visually similar products in the database.
4. **Return Search Results:** The view function sends a JSON response with details of the matching products, including titles, prices, and potentially image URLs.

#### Client-Side (Response Handling):

1. **Receive Response:** The JavaScript code receives the JSON response from the server.
2. **Parse Results:** The response data is parsed to extract information about the matching products.
3. **Display Results:** The JavaScript dynamically generates HTML content to display the retrieved products, creating product cards with titles, images, and prices. If no matching products are found, an appropriate message is displayed.

#### Benefits:

- **Simplified Product Search:** Users can find similar products without manually entering text descriptions.
- **Improved User Experience:** Provides a more intuitive way to search for visual items.
- **Accessibility:** Helps users who have difficulty describing products in words.

### Product Description Generation Using AI

#### Admin-Side (Django Admin Interface):

1. **Add Product:** When an admin adds a new product, they upload an image of the product along with other necessary details like the title and price.
2. **Generate Caption:** Upon saving the product, the application automatically calls a machine learning model to generate a caption from the product image.
3. **Generate Description:** The generated caption is then passed to the Langchain and Gemini Large Language Models (LLMs) to create a customer-centric product description.
4. **Save Description:** The generated product description is saved in the database, providing a rich and engaging product description for potential customers.

#### Benefits:

- **Enhanced Product Descriptions:** Automatically generates detailed and attractive product descriptions to improve customer engagement.
- **Time Efficiency:** Saves time for admins by automating the product description creation process.
- **Consistency:** Ensures consistent and high-quality product descriptions across the online store.

## Getting Started

To use AI Commerce Automation, follow these steps:

1. **Clone the Repository:** Clone this repository to your local machine using:

   ```sh
   git clone https://github.com/isuru0x01/AI-Driven-Ecommerce.git
   ```

2. **Configure Settings:** Rename the `sample.env` file to `.env` and add the required API keys and configurations.

3. **Run the Application:** Start the application by running:

   ```sh
   docker compose up --build
   ```

   Access the application via your web browser at the appropriate URL.

4. **Explore and Customize:** Explore the features of AI Commerce Automation and customize them to suit your specific needs. Feel free to experiment and innovate!

## Contributing

We welcome contributions from the community to further enhance AI Commerce Automation. Whether it's adding new features, fixing bugs, or improving documentation, your contributions are invaluable.

## Support

If you encounter any issues or have any questions, feel free to reach out to us or open an issue in the repository.

## License

This project is licensed under the [MIT License].
