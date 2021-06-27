## 10 hourLabs Test
> Python schedule logger

## Setting up the project.
- To run the api and setup completely simply run the commands below in a sequencial order.
```sh
docker-compoe -p flask_api build web db #this builds the flask app and it's database environment
```
Next run 
```sh
docker-compose -p flask_api up -d web db
```

Using the frontend, you can connect to this api and perform operations on the connection.
### Seeding the database
to seed the db, run the following commands.
```
docker-compose -p flask_api exec web sh
```

this would take you into the virtual environement of the python app, then run the following.
```sh
python seed.py
```

This would seed te data from the seed.py file. You can edit this file to add more service seeders