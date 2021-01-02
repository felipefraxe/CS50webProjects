# CS50 SHOP
#### Video Demo:  <https://youtu.be/vnEauSsHW0U>
#### Description:
It´s a simple store web application that allows people to buy stuff.
There features available: Register, Login, Log out, Cart, Add funds and Buy.

Flask:
    "/register", "/login", "/logout":
        They work almost as identical as in Finance problem set, but now it requires an e-mail, which the user will need to login.
    User´s passwords are hash in the database as well, ensuring their privice. ´Cash´ field now starts with default value of 0.00.

    "/":
        It works showing all the products inside the database where the ´amount´ filed is greater than 0 (you can see this feature in the video).
    It shows products ´name´, ´price´, ´type´, ´in stock´ as well as the ´add to cart´ button. I´ve changed the ´layout´ code to fit the proposal better, including
    user´s name on "Hello, Felipe", for exemple (Got the inspiration on Amazon.com)

    "/funds"
        It shows people names adn how much money they have in the plataform. It also contains a field in which they can add funds in order to buy stuff

    "/cart"
        Shows user´s cart selection, allowing them to put as many products as they like (if available in stock). The program automatically calculates the price
    (multiplying ´amount´ x ´price´) in each row of products.
        In order for this to work, I´ve created a new table in the database called ´cart´ associating user´s id with products´ id.

    "/buy"
        Can only acess via "post" method and it basically calculates user´s total price and subtracts from user´s cash while adjust all products ´amount´ field.
    Once ´amount´ field goes to 0, that specific product disappear from index page.

Templates:
    ´apology´:
        Used the same as Finance, really liked the cat

    ´cart´:
        Informs user of the products they have selected, including the amount of times. Made basically with loops and showing
    some information on the database

    ´funds´:
        Made with 1 row table, showing user´s name and how much cash does it has in the web app, and 1 submitt, containing a text
    allowing users to inform how much cash they would like to add, and a button, to effectively add the amount in the databse.

    ´index´:
        The homepage of the site, showing all products available. Made essentially with loops and products id in a hidden field, to allow
    change information with the databse.

    ´layout´, ´login´, ´logout´:
        Used basically the same as Finance problem set, with some minor changes.