# Cryptracker-web

### Setup
```
./manage.py seed
```

Creates the database and seeds it with dev data. Warning: creates an insecure admin account. :)


### Running the Application

```sh
$ python manage.py runserver -p 9000
```

So access the application at the address [http://localhost:9000/](http://localhost:9000/)

### Testing

With coverage:

```sh
$ python manage.py cov
```
