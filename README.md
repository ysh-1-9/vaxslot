# VaxSlot
Vaccine availability notification bot - notifies you when a vaccination slot opens up near you.

Built on Flask, and deployed on Heroku using gunicorn.

There's a sqlite database that stores vaccine availability information and user information.

On startup, all data from sqlite is loaded to a variable (dict) called db_data which we use in various places. Whenever db_data is modified, the sqlite db is also changed accordingly. The initialize function does this.

The flask route adds new user registrations to db_data.
The updateDB function fetches vaccine availability data for one particular district and stores the update in db_data.
The notify function notifies everyone in one particular vaccine about vaccine availability. All information can be passed to it as arguments, so it doesn't need to access db_data.

The scheduling needs to run initialize once at startup, and the updateDB and notify functions as often as possible.

db_data could potentially be split into 2 variables, one for vaccine availability information and another for user information, so that you won't need to lock updateDB. Once this is done, only initialize needs a lock.
