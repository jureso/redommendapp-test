#!/usr/bin/env bash
psql recommend_app_test << EOF
copy users(user_id,first_name,last_name)
from '/Users/jureso/Projects/FarisTest/recommend_app/data/users.csv' delimiter ',' CSV HEADER;
copy places(place_id,place_name)
from '/Users/jureso/Projects/FarisTest/recommend_app/data/places.csv' delimiter ',' CSV HEADER;
copy friends(user_id,friend_user_id)
from '/Users/jureso/Projects/FarisTest/recommend_app/data/friends.csv' delimiter ',' CSV HEADER;
copy ratings(user_id,place_id,rating)
from '/Users/jureso/Projects/FarisTest/recommend_app/data/ratings.csv' delimiter ',' CSV HEADER;
EOF
