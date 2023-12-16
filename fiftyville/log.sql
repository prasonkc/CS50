-- Keep a log of any SQL queries you execute as you solve the mystery.

--Start with looking at the table of crime report
--Look for crime scene report at 28 July 2021 that took place at Humphrey Street
SELECT id,description FROM crime_scene_reports WHERE year = 2021 AND month = 07 AND day = 28 AND street = 'Humphrey Street';

--Now we know
--Theft of the CS50 duck took place at '10:15am' at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

--Since the witnesses mention bakery, we look at the interview that mentions bakery.
SELECT id,name,transcript FROM interviews WHERE year = 2021 AND month = 07 AND day = 28 AND transcript LIKE "%bakery%";

-- 161|Ruth|Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

--162|Eugene|I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

--163|Raymond|As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


--The thief whitdrew some money from atm.When he left the bakery, he called someone for less than a minute and asked them to purchase a flight ticket. He got into a car in the parking lot after 10 minutes of theft, thats beofre 10:25.

 SELECT hour, minute,activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 07 AND day = 28 AND hour = 10;

--There was no record at exactly 10:25 so, we look at the closest record to 10:25
--We get 2 lisence plate at exit at 10:23
--  10|23|exit|322W7JE
--  10|23|exit|0NTHK55

--We don't know which one is the thief's car. So, We extract information about bank account number using both lisence key and match the time of atm transaction.

SELECT bank_accounts.account_number FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE people.license_plate = '322W7JE'; 

--26013199

SELECT bank_accounts.account_number FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE people.license_plate = '0NTHK55';

--We don't get any results which means we assume that this person doesn't have a registered bank account. 

--Lets check the transaction time of our culprit with bank account no = 26013199
SELECT year, month, day FROM atm_transactions WHERE account_number = 26013199;

-- 2021|7|26
-- 2021|7|28
-- We can see, the transaction was performed at 2021,7,28 which means we found our culprit. Lets extract his information

--We know the liscence plate and bank account number, so we use that to extract name, phone_number, passport_number from people table

SELECT name, phone_number, passport_number FROM people WHERE license_plate = '322W7JE';
-- The thief was Diana, her phone number is(770) 555-1861 and her passport number is 3592750733

--Lets check her phone calls
SELECT receiver,duration FROM phone_calls WHERE caller = '(770) 555-1861';

--According to our witness, the phone call was less than a minute. So, the reciever is (725) 555-3243 whom she called for 49 seconds.

--Lets find out who is the reciever
SELECT name, passport_number FROM people WHERE phone_number = '(725) 555-3243';
--The other culprit who helped Diana book flight ticket was Philip. His passport number is 3391710505.

--Now we can see which airport he booked
SELECT airports.full_name, airports.city, flights.year,flights.month,flights.day,flights.hour FROM airports JOIN flights ON flights.destination_airport_id = airports.id JOIN passengers ON passengers.flight_id = flights.id WHERE passengers.passport_number = 3592750733;
--She flew to Boston