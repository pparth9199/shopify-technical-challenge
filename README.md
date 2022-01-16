# Shopify Backend Developer Intern Challenge - Summer 2022

I built an inventory tracking web application with basic CRUD functionality
along with the additional feature of filtering by certain attributes.

For the tech stack, I used [Fast-API](https://fastapi.tiangolo.com/) and SQLite3.

## Installation

I highly recommend using conda for your development environment. Once it's
installed, run the following commands to setup the environment and install the
dependencies.

```bash
conda create -n inventory_backend python=3 -y
conda activate inventory_backend
pip install -r requirements.txt
```

## Running

Run the following in the project directory to start the API with hot-reloading.

```bash
uvicorn api.main:app --reload
```

The focus was on the backend so I skipped the frontend as all the logic can be triggered via the Swagger Docs. When trying it out you can also visit http://127.0.0.1:8000/get-inventory to see how the database is changing.

## Documentation

To view the auto-generated documentation for the, please visit the documentation page at http://127.0.0.1:8000/docs. URL may vary but the path is the same. This page is also a great place to try the endpoints just like you would in Postman or other RESTful API testing tools.

## Endpoint Explanation

**Get Inventory** - GET Request which will return all the items in the inventory.

**Get Filtered Inventory** - GET Request which will return items in the inventory that
match the given filters (in_stock, cost, weight). Note that the stock filter will show only items in stock if set to True and all items if set to False.

**Get Item** - GET Request which will return information about a specific item in the inventory if it exists.

**Add Item** - PUT Request which will add a new item to the inventory if no item with
the same Product ID exists.

**Update Inventory** - PUT Request which will overwrite the item with the same Product ID if it exists.

**Remove Item** - DELETE Request which will remove an item from the inventory if it exists.

## Additional Thoughts on Design

I built an API because it'll make it easy to add more features later down the line. For example, when adding a new feature, the frontend dev only needs to interact with API endpoints with the actual logic abstracted away. It also makes testing easier.

To speak on testing and formatting, the tests are like integration tests, where I create a test database and run the endpoints against it. All the code has been formatted with black and isort. Also enforcing flake8 standards and a pylint score of 9.38. All of these are enforced with pre-commit hooks.

The tests have 100% line coverage. To run the tests, run the following command in the project directory.

`pytest --cov-report term-missing --cov=api tests`

One thing I was considering was to combine the add and update functions into one function that would update an item if it exists, or add a new item if it doesn't. I decided against this because I just wanted to be explicit with the functionality for the sake of the challenge.

I also made sure to use prepared statements to prevent SQL injection attacks.

In general, I've been enjoying FastAPI as opposed to Flask, which I've used in the past. The auto-generated documentation is very useful and I'm glad I used it. It also makes testing and dealing with data types much easier.
