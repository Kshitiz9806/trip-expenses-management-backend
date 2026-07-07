# Trip Expenses Management System Backend

Ever been on a business trip with spend limits and wondered how much have you spent today.

Normal human reaction is to pull out a calculator, go through all the bills and find your spends all cateogries.

The computation nightmares scale exponentially when there are multiple people on a same trip.

And the old school way of noting everything down on a piece of paper where you forget why the heck did you write 4.90$ on a random corner without any furhter information.

Fear Not: WE ARE HERE TO HELP.

## Our Requirerment:

Just a simple one line solution: Some place I track my expenses, log them all and at a glance know how much can I afford to spend on food today.

Catered specificially to "special-shall-not-be-named-organization" as the rules are specifically applied to the organization. [DON'T WORRY, WE'LL SCALE]

## Down to the technical stuff [ENDPOINTS]:

 - POST   /users                              -> create user
 - POST   /trips                              -> create trip
 - GET    /trips/{trip_id}                    -> get trip details
 - PUT    /trips/{trip_id}/users/{user_id}    -> join user to trip
 - PUT    /trips/{trip_id}/limits             -> set/replace limits
 - POST   /trips/{trip_id}/expenses           -> add a trip expense
 - GET    /trips/{trip_id}/expenses           -> get all trip expenses
 - GET    /trips/{trip_id}/summary            -> get trip summary for today
 - POST   /trips/{trip_id}/suggest-payer      -> suggest who should pay acc to limits

## Steps to run the backend

1. Clone the repository and open a powershell / bash shell inside the repo.
2. Create a virtual environment and activate it
``` python -m venv ./venv && ./venv/Scripts/activate ```
3. Install requirements
``` pip install -r requirements.txt ```
4. Run the app
``` uvicorn app.main:app ```

PS: Head over to the hosted website at /docs to open the SWAGGER UI and test out the APIs yourselves.
