## ECS162 Homework 3 – Jaden Yang

### Github link: https://github.com/jadenzy/ECS162_HW2.git

### Running Instructions

- **Run Docker and localhost the frontend**  
  ```bash
  docker-compose -f docker-compose.dev.yml up --build 
  http://localhost:5173
  ```
- **Test backend:**  
  ```bash
  cd backend && pytest
  ```
---

## Important info: 
  - The login functions works as the following: 
    1. Redirect to dex 
    2. Vertify the info, and save the user info to the database 
    3. Redirect to frontend localhost 
    4. The frontend will call /api/user to check if any user has been save in the Database session, if so then render the username and logout 

  - The comment functions contains: 
    - Post: post will allow nested replies 
    - Delete: Each user can only delete its own commends, but if username == **'moderator'**, then can delete any comments. If delete a comment with replies, then the entier reply tree will be deleted at that level 
    - Get: get the comments for a artlie based on its own id 
    - Patch: Only the **moderator** can do this, which it to make a comment as █

  - There are 3 preset users in config/dex: 
    1. username: admin
      - email: admin@hw3.com
      - password = "password"
      
     
    2. username: moderator , **moderator** is set as this one 
      - email: moderator@hw3.com
      - password = "mpassword" 
     
    3. username: user
      - email: user@hw3.com
      - password = "upassword"
      
## Frontend Structure

### `/src`
- **`app.css`**
  - Carries over CSS files from Homework 2

- **`App.svelte`**
  - Add comments 
  - Add login 

- **`CommentItem.svelte`**
  - The main componments to render the comments for each articles 
  - Allow nested replies, but if deleting 

## Backend Structure

### `app.py`
  - Add all the needed functions for MangoDB 
  - Add login functions by using dex 
  - Add GET, POST, DELETE, PATCH apis for the comments 
  - Everything will save to the database including the articles and their corresponding articles 
  - Comment is an object contains    
    - "article_id"
    - "text"
    - "user": the user name 
    - "redacted_text": if the moderator do it or not 
    - "parent_id": if it contains a parent reply 
  - Move the fetch articles to flask instead of frontend 

### `/test`

- **`test_app.py`**
  - Tests a `GET` request to `/api/key`
    - Checks for **status code 200** and **JSON format**
  - Mocks `fake.txt` with `app.send_from_directory()`:
    - Verifies the path exists
    - Sends a `GET` request to `fake.txt`
    - Checks if **status code 200** is returned
    

