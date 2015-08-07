E-Store
=================
DESCRIPTION

E-Store is a prototype E-commerce website which is created using Python as a server
side language, and utilizes the Flask framework, with back-end data stored in a MySQL
database. This prototype comprises of all archetypical features found in an ecommerce
website.

The following is a flow that a user goes through, right from the time she lands on the
webpage, to the time she completes a checkout

● Ability to register and store new user information – As soon as a new user
comes in, she would be given the option to register, and gets to fill in a form.

● Existing user sign-in and validation - Once submitted, the user can use
the same credentials when he comes back to the website again. Else the user would
be prompted to fill it in, until he gets it right

● Ability to view all the inventory having non-zero quantity - Once done
registering/Logging in to the flow, the users are taken to the Inventory page,
where each item (having non-zero quantity) is sequentially shown to the users

● Selecting Size and Color - After honing into item of choice, the user now has an
option of selecting their size – Only after size has been selected, would all the
available colors be shown

● Adding items of interest to cart – Now the user is ready to add items to the
cart, and does so by clicking on the ‘Add to Cart’ button. Asynchronously the cart
image (top right hand corner of webpage) displays the number of items available
in the cart. At this time, the user can continue to shop and add as many items as he
wishes into his cart.

● Checkout all items in the cart – Right after the fun part, the not-so-fun part of
opening your wallet happens. By clicking on the cart image, the user is taken to
the checkout page where they see a summary of items added to cart and ready to
checkout

● Receipt generation – Once checked out, a receipt is generated (with a unique
receipt/order ID) indicating the total amount paid, and date of purchase
