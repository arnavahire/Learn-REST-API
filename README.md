# Learn to create REST APIs with Flask - Python

In this project we create 4 models that are associated with a store.
1. Store 
Stores a store info. Every store has it's own unique id that starts from 1,2,3.. and so on. It also has a name, associated items that are in the store and the tags associated with the items in the store. A store can have multiple tags. However a tag cannot have multiple stores. So Stores -> tags is a 1:many relationship.

2. Items
Stoes item info. It has id, name, description tags, store id associated with every item. Each item can have multiple tags associated with it. Also every tag can have multiple items associated with it. Hence Item <-> tags is a many:many relationship.

3. Tags
Stoes tag info. It has id, name, store id as primary attributes with store and items as the property attributes. Each item can have multiple tags associated with it. Also every tag can have multiple items associated with it. Hence Item <-> tags is a many:many relationship.

4. Items Tags
Stores the many:many relationship shared between items and tags.

4. User
Stoes user info. Every user has an id, email, username and password. For every user to access the Stores REST API, he first has to register using the /register endpoint. Once registration is complete he has to use the /login endpoint which then generates an access token for the user. This generated access token needs to be used as an authroization header to access stores, items and tags.

To understand what are the required headers/attributes that a request must have you can either use

<domain_url>/swagger-ui

or if you are working locally you can refer the below url to see how the endpoints have been created and what are the requirements to hit them.

http://localhost:5000/swagger-ui

## Where to find the REST API endpoints ?
The entire Insomnia collection that has all of the Stores REST API endpoints are present in the Stores_REST_API_insmonia_collection.json file.

## How to run the project locally or using a domain ?

The steps for setting up project locally or using a domain, please refer CONTRIBUTING.md file for details.