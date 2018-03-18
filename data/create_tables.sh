#!/usr/bin/env bash
psql recommend_app_test << EOF
create table users(
    user_id int NOT NULL,
    first_name varchar(20) NOT NULL,
    last_name varchar(20) NOT NULL,
    PRIMARY KEY(user_id)
);
create table places(
    place_id int NOT NULL,
    place_name varchar(20) NOT NULL,
    PRIMARY KEY(place_id)
);
create table friends(
    user_id int NOT NULL,
    friend_user_id int NOT NULL
);
create table ratings(
    user_id int NOT NULL,
    place_id int NOT NULL,
    rating int NOT NULL
);
EOF