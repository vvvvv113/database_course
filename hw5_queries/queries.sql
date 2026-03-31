-- 1)How many containers of antibiotics are currently available? 
SELECT SUM(quantityOnHand) AS totalContainers
FROM item
WHERE itemDescription LIKE '%antibiotics%';
-- 2)  Which volunteer(s), if any, have phone numbers that do not start with the number 2 and 
-- whose last name is not Jones.  Query should retrieve names rather than ids. 
SELECT volunteerName FROM volunteer WHERE volunteerTelephone NOT LIKE '2%' AND volunteerName NOT LIKE '%Jones';
-- 3)  Which volunteer(s) are working on transporting tasks?  Query should retrieve names 
-- rather than ids. 
SELECT DISTINCT volunteerName FROM volunteer AS v 
JOIN assignment AS a 
ON v.volunteerId = a.volunteerId 
JOIN task AS t 
ON a.taskCode = t.taskCode 
JOIN task_type AS tp 
ON t.taskTypeId = tp.taskTypeId 
WHERE taskTypeName = 'transporting';
-- 4)  Which task(s) have yet to be assigned to any volunteers (provide task descriptions, not 
-- the codes? 
SELECT taskDescription FROM task AS t 
LEFT JOIN assignment AS a 
ON t.taskCode = a.taskCode 
WHERE volunteerId IS null;
-- 5)  Which type(s) of package contain some kind of bottle?   
SELECT DISTINCT packageTypeName FROM package_type AS pt 
JOIN package AS p
ON pt.packageTypeId = p.packageTypeId 
JOIN package_contents AS pc 
ON pc.packageId = p.packageId
JOIN item AS i
ON pc.itemId = i.itemId
WHERE itemDescription LIKE '%bottle%';

-- 6)  Which items, if any, are not in any packages?  Answer should be item descriptions. 
SELECT itemDescription FROM item AS i
LEFT JOIN package_contents AS pc
ON i.itemId = pc.itemId
WHERE pc.packageId IS null;
-- 7)  Which task(s) are assigned to volunteer(s) that live in New Jersey (NJ)?  Answer should 
-- have the task description and not the task ids. 
SELECT DISTINCT t.taskDescription FROM task AS t
JOIN assignment AS a
ON t.taskCode = a.taskCode
JOIN volunteer AS v
ON a.volunteerId = v.volunteerId
WHERE v.volunteerAddress LIKE '%NJ%';

-- 8)  Which volunteers began their assignments in the first half of 2021?  Answer should have 
-- the volunteer names and not their ids. 
SELECT DISTINCT volunteerName FROM volunteer AS v
JOIN assignment AS a
ON v.volunteerId = a.volunteerId
WHERE a.startDateTime >= '2021-01-01' AND a.startDateTime < '2021-07-01';
-- 9)  Which volunteers have been assigned to tasks that include packing spam?  Answer 
-- should have the volunteer names and not their ids.
SELECT DISTINCT v.volunteerName FROM volunteer AS v
JOIN assignment AS a
ON v.volunteerId = a.volunteerId
JOIN package AS p
ON a.taskCode = p.taskCode
JOIN package_contents AS pc
ON p.packageId = pc.packageId
JOIN item AS i
ON pc.itemId = i.itemId
WHERE i.itemDescription LIKE '%spam%';

-- 10) Which item(s) (if any) have a total value of exactly $100 in one package?  Answer should 
-- be item descriptions. 
SELECT DISTINCT i.itemDescription FROM item AS i
JOIN package_contents AS pc
ON i.itemId = pc.itemId
WHERE i.itemValue * pc.itemQuantity = 100;

-- 11) How many volunteers are assigned to tasks with each different status?   The answer 
-- should show each different status and the number of volunteers sorted from highest to 
-- lowest) 
SELECT ts.taskStatusName, COUNT(DISTINCT a.volunteerId) AS volnum
FROM assignment AS a
JOIN task AS t
ON a.taskCode = t.taskCode
JOIN task_status AS ts 
ON t.taskStatusId = ts.taskStatusId
GROUP BY ts.taskStatusId,ts.taskStatusName
ORDER BY volnum DESC;
-- 12) Which task creates the heaviest set of packages and what is the weight?  Show both the 
-- taskCode and the weight (You should be able to do this without using any sub-queries). 
SELECT taskCode, SUM(p.packageWeight) AS totalWeight FROM package AS p
GROUP BY p.taskCode
ORDER BY totalWeight DESC
LIMIT 1;
-- 13) How many tasks are there that do not have a type of “packing”? 
SELECT COUNT(*) AS taskCount FROM task AS t -- count the number of rows
JOIN task_type AS tp 
ON t.taskTypeId = tp.taskTypeId
WHERE tp.taskTypeName != 'packing';
-- 14) Of those items that have been packed, which item (or items) were touched by fewer 
-- than 3 volunteers?  Answer should be item descriptions. 
SELECT itemDescription FROM item AS i
JOIN package_contents AS pc 
ON i.itemId = pc.itemId
JOIN package AS p
ON p.packageId = pc.packageId
JOIN assignment AS a
ON p.taskCode = a.taskCode
GROUP BY i.itemId, itemDescription
Having COUNT(DISTINCT a.volunteerId) < 3;
-- 15) Which packages have a total value of more than 100?  Show the packageIds and their 
-- value sorted from lowest to highest.
SELECT pc.packageId, SUM(i.itemValue * pc.itemQuantity) AS totalValue
FROM package_contents AS pc 
JOIN item AS i
ON pc.itemId = i.itemId
GROUP BY pc.packageId
Having SUM(i.itemValue * pc.itemQuantity) > 100
ORDER BY totalValue ASC;
