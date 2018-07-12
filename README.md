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

## Website Configuration

Now that your app is up and running, stop the development server and let's start configuring the manager users (the users representing the couple who just married).

1. Create a superuser

   If you haven't done so yet, go ahead and create a superuser so you can have access to the admin section.
   ```
   $ ./manage.py createsuperuser
   ```

2. Create the manager group & users
   - Now that you have created a superuser, start the development server again and log in into the admin section (localhost/admin). Once logged in, click the "+add" button under the AUTHENTICATION AND AUTHORIZATION container in order to create a new Group. Give it the name 'manager' (without the quotes, all lowercase) and leave the rest as it is, then save.

   - Now let's create the managers. Go ahead and create two new users from the admin interface. Once created,
   go and edit each of them to make sure the following is true:
     * The user's username and email must be the same
     * The user should have the First Name & Last Name fields set
     * The user should be assigned to the manager group

After these steps, your application should be ready for use. The users you just created (managers) represent the married couple: they can approve/refuse photos uploaded and accept/deny new users requests.


### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
