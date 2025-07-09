
--create database DevDB2024_leoanik;

CREATE TABLE departments (
    department_id serial primary key,
    name varchar(100) NOT NULL,
    parent_department_id integer references departments(department_id) ON DELETE SET NULL,
    manager_id integer references employees(employee_id) ON DELETE SET NULL,
    opening_date date NOT NULL,
    close_date date,
   	creation_order_id integer references orders(order_id) NOT null,
    close_order_id integer references orders(order_id) ON DELETE SET NULL
);

CREATE TABLE employees(
    employee_id serial primary key,
    full_name varchar(100) NOT NULL,
    birth_date date NOT NULL,
    registration_address varchar(200) NOT NULL,
    phone varchar(20),
    email varchar(100),
    hire_date date NOT NULL,
    terminate_date date,
    creation_order_id integer references orders(order_id) NOT null,
    close_order_id integer references orders(order_id) ON DELETE SET NULL
    
);

CREATE TABLE positions(
    position_id serial primary key,
    title varchar(100) NOT NULL,
    min_salary integer NOT NULL,
    max_salary integer NOT null
 );



CREATE TABLE staff_assignments (
    assignment_id serial primary key,
    employee_id integer references employees(employee_id) on delete cascade,
    department_id integer references departments(department_id) on delete cascade,
    position_id integer references positions(position_id) on delete cascade,
    employment_rate float8 NOT NULL,
    salary integer NOT NULL,
    assignment_date date NOT NULL,
    removal_date date,
  	assignment_order_id integer references orders(order_id) on delete cascade,
    close_order_id integer references orders(order_id) ON DELETE SET null
);


CREATE TABLE orders (
    order_id serial primary key,
    title varchar(30) NOT NULL, 
    order_date date NOT NULL,
    order_number integer NOT NULL,
    signer_id integer 
);

alter table orders add constraint fk_signer foreign key (signer_id) references employees(employee_id) on delete cascade;

--alter table staff_assignments alter column employment_rate TYPE float8;
--alter table employees add column terminate_date date;
--alter table departments add column close_date date;
--alter table staff_assignments add column removal_date date;



--Представления:

--1 Инфо о сотруднике

select e.full_name, p.title, name, salary
from public.employees as e
join public.staff_assignments as sa on e.employee_id = sa.employee_id
join public.positions as p on sa.position_id = p.position_id
join public.departments as d on sa.department_id = d.department_id;

--2 Инфо о приказах 

select o.title, o.order_date, o.order_number, e.full_name
from public.orders as o
join public.employees as e on o.signer_id = e.employee_id;



