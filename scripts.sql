1.	number of registered users by country 
select country_code,
       count(*) 
  from user
 group by country_code

2.	% of users, who made their first payment in 3 days after registration by country 
select u.country_code,
       count(distinct p.user_id)/count(distinct u.id)
  from user u left join payment p on u.id = p.user_id 
                        and days(p.created_at – u.date_joined)<=3
 group by u.country_code

3.	% of users, who made their first payment in 3 days after registration and had 2 
confirmed lessons in 7 days after registration by country 
WITH 
three_days_reg AS
(
select distinct u.id
  from user u inner join payment p on u.id = p.user_id 
                                      and days(p.created_at – u.date_joined)<=3
)
two_lessons_week AS
(
select u.id
  from user u inner join lesson l on u.id = l.user_id 
                                     and days(l.created_at – u.date_joined)<=7
                                     and l.status = 'CONFIRMED'
 group by u.id
having count(*)>=2
)
select u.country_code,
       count(distinct t.id)/count(distinct u.id)
  from user u 
       left join 
       (
       	select tdg.id 
       	  from three_days_reg tdg inner join two_lessons_week tlw on tdg.id=tlw.id
       	) t 
       on u.id = t.id
 group by u.country_code

4.	% of weekly new users that never have done a payment 
select count(distinct (case when p.id is NULL then u.id end))/count(distinct u.id)
  from user u left join payment p on u.id = p.user_id 
 where u.created_at >= trunc(sysdate)-7


5.	Advanced level (Extra point): Write the SQL that returns how many hours of confirmed 
lessons a specific user (for example user_id=1) has taken between payments. 
-- Calculation w/o taking into account that lessons may overlap with payments
WITH user_pauments_min_max AS
(
select user_id,
       min(created_at) first_payment,
       max(created_at) last_payment
  from payment 
 group by user_id
)
select u.user_id,
       sum(l.hours)
  from user_pauments_min_max u inner join lesson l on u.user_id = l.user_id
                                                      and l.status = 'CONFIRMED'
                                                      and l.created_at > u.first_payment
                                                      and l.created_at < u.last_payment
 where u.user_id = some_specific_user_id
 group by user_id

-- Calculation with taking into account that lessons may overlap with payments
WITH user_pauments_min_max AS
(
select user_id,
       min(created_at) first_payment,
       max(created_at) last_payment
  from payment 
 group by user_id
)
select u.user_id,
       sum(case when (l.created_at > u.first_payment) 
       	             and (l.created_at+l.hours/24 < u.last_payment) then l.hours
       	        when (l.created_at < u.first_payment) 
       	             and (l.created_at+l.hours/24 < u.last_payment) then l.hours - hours(u.first_payment-l.created_at)
       	        when (l.created_at > u.first_payment) 
       	             and (l.created_at+l.hours/24 > u.last_payment) then hours(u.last_payment-l.created_at)
       	        when (l.created_at < u.first_payment) 
       	             and (l.created_at+l.hours/24 > u.last_payment) then hours(u.last_payment-u.first_payment)
       	    end)
  from user_pauments_min_max u inner join lesson l on u.user_id = l.user_id
                                                      and l.status = 'CONFIRMED'
                                                      and l.created_at+l.hours/24 > u.first_payment
                                                      and l.created_at < u.last_payment
 where u.user_id = some_specific_user_id
 group by user_id
 /*
 one may check "case" statement by using the following picture:
-------------------------
 -----  -------   -------
***P*****************P***
where "*" stand for the timeline with "P" as payment
"-" stands for lesson cases duration
 */































