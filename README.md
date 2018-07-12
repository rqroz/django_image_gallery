# django_image_gallery

This is a web application written in Django used to serve as a basis for a collaborative wedding album web app.

## Getting Started

Go ahead and clone this repo in order to get the content.

```
$ git clone https://github.com/rqroz/django_image_gallery.git
```


### Prerequisites

- python3
- pip3

### Installing

Before starting the server, you'll need to install all the dependencies and preconfigure your environment variables.

1. Installing Dependencies

   To install the project dependencies, move to the project folder and run:
   ```
   $ pip3 install -r requirements.txt
   ```

2. Environment Variables

   This project contains an example of environment file named '.env.example', go ahead and change the values to the ones matching your needs, then change its name to '.env' (the project won't run if you skip this step).

3. Applying Migrations

   After configuring your environment variables, go ahead and apply the migrations to your database.
   ```
   $ ./manage.py makemigrations
   $ ./manage.py migrate
   ```

4. Starting the development server

   Now that you've done all the pre-configuration needed, go ahead and run the command bellow from the folder containing the manage.py file:
   ```
   $ ./manage.py runserver
   ```

After following the steps above, you should see the screen bellow on your localhost (http://127.0.0.1:8000/):

![landing page](/example-files/imgs/landing.png)

## Website Start Configuration

Now that your app is up and running, stop the development server and let's start configuring the manager users (the users representing the couple who just married).

1. Create a superuser

   If you haven't done so yet, go ahead and create a superuser so you can have access to the admin section.
   ```
   $ ./manage.py createsuperuser
   ```

2. Create the manager group & users
   - Now that you have created a superuser, start the development server again and log into the admin section (localhost:8000/admin). Once logged in, click the "+add" button under the AUTHENTICATION AND AUTHORIZATION container in order to create a new Group. Give it the name 'manager' (without the quotes, all lowercase) and leave the rest as it is, then save.

   - Now let's create the managers. Go ahead and create two new users from the admin interface. Once created,
   go and edit each of them to make sure the following is true:
     * The user's username and email must be the same
     * The user should have the First Name & Last Name fields set
     * The user should be assigned to the manager group

After these steps, your application should be ready for use. The users you just created (managers) represent the married couple: they can approve/refuse photos uploaded by other users and accept/deny new users requests.


## Website Behavior

### New Users (Friends)

  Friends from the couple can request access by clicking button next to the login button in the landing page. Once requested, it will be unactive (meaning they can't log in) until a decision is taken by the managers.

  **Managers**: To accept/deny a new user, click on your name (right side of the navbar), then click the Approve Users button to be taken to the users approval section.

  **Note**: When someone requests access, there is a message saying that an email will be sent if the managers accept their request. That is NOT implemented. That is for you to implement ([UserApprovalView](/image_gallery/website/views/user_views.py)) based on your preferred SMTP module. Bellow is a link to the django docs.
  - [Django SMTP](https://docs.djangoproject.com/en/2.0/topics/email/)

  <div style="dislpay:--webkit-inline-box;" align="center">
    <img height="220" alt="User Request" src="/example-files/imgs/user-request.png">
    <img height="220" alt="User Approval" src="/example-files/imgs/user-approval.png">
  </div>

### Search (Manager's only)

  Managers can search their friends (other users) by their names to see which photos they uploaded. The search bar is located in the navbar so they can search from all pages.

### Uploads

  All users can upload images under the section My Uploads.

  If the upload is made by a manager, the image status will automatically be set to Accepted (meaning it can be view under the Gallery section). Otherwise, the image status will be set to Pending and is up to the managers if they will accept or refuse it.

  **Note**: All the photos are kept, even the ones refused. That is so the managers can accept a previously refused photo if they have a change of heart.

  **Managers**: To change the status of an image, click on your name (right side of the navbar), then click the Approve Photos button to be taken to the photo approval section. There, you will be able to change the status of all uploaded photos.

  <div style="dislpay:--webkit-inline-box;">
    <img height="246" alt="User Uploads" src="/example-files/imgs/user-uploads.png">
    <img height="246" alt="Photo Approval" src="/example-files/imgs/gallery-approval.png">
  </div>

### Gallery

  The Gallery is the main section: all users have access to it and it shows all the approved photos.

  - Users can like images here (hovering over an image will show the options to like and view in original size).
  - Users can sort the images either by number of likes or by date taken. It is also possible to change the ordering (ascending/descending).

  **LARGE DATA SIMULATION**: You might notice a little red button on the right side of the gallery page with the initials SLG (Simulate Large Data). That button is for development only, its purpose is to show how the gallery will behave with 100x the data it contains in the first page (if you uploaded 2 images and click this button, the first page of the gallery will show 200 images, 100 of each).

  ![gallery page](/example-files/imgs/gallery.png)

### Profile

  Finally, there is a basic profile section that allows the users to change their personal data and password.

  ![profile page](/example-files/imgs/user-profile.png)

## Built With

* [Django](https://www.djangoproject.com/)

## Authors

* **Rodolfo Queiroz** - [DjangoImageGallery](https://github.com/rqroz/django_image_gallery)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
