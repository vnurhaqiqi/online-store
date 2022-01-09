-- auto-generated definition
create table alembic_version
(
    version_num varchar(32) not null
        primary key
);


-- auto-generated definition
create table products
(
    id             int auto_increment
        primary key,
    name           varchar(200) not null,
    quantity       int          not null,
    price          float        not null,
    status         tinyint(1)   null,
    most_lead_time int          null,
    lead_time      int          null
)

-- auto-generated definition
create table order_details
(
    id           int auto_increment
        primary key,
    order_id     int       not null,
    quantity     int       null,
    created_date timestamp null,
    updated_date timestamp null,
    product_id   int       not null,
    price        float     null,
    constraint order_details_ibfk_1
        foreign key (order_id) references orders (id),
    constraint order_details_ibfk_2
        foreign key (product_id) references products (id)
);

create index order_id
    on order_details (order_id);

create index product_id
    on order_details (product_id);

-- auto-generated definition
create table orders
(
    id           int auto_increment
        primary key,
    order_date   timestamp    null,
    status       varchar(120) null,
    created_date timestamp    null,
    updated_date timestamp    null
);

-- auto-generated definition
create table payments
(
    id           int auto_increment
        primary key,
    order_id     int          not null,
    order_date   timestamp    null,
    status       varchar(120) not null,
    payment_date timestamp    null,
    amount       float        not null,
    created_date timestamp    null,
    updated_date timestamp    null,
    constraint payments_ibfk_1
        foreign key (order_id) references orders (id)
);

create index order_id
    on payments (order_id);



