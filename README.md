# Wellness Journal
This project is a wellness journal to create and track daily entries regarding various aspects of physical and mental 
health, such as fitness, hydration, sleep, and mindfulness reflection. It was built using Python
and a MySQL database, giving the users the oppurtinity to create, read, delete, and update 
various entriees in their journal.

## Instructions and Technical Specifications
To run this application on a local machine, follow these steps
1. Connect to a MySQL server (MySQL Workbench used during development)
2. Import the wellness_journal_db.sql SQL dump file into a MySQL database.
3. Ensure the following dependencies are installed:
-            Python 3.6 or above
-            pip install pymysql
-            pip install prettytable
4. Within "MySQL Server User Login Information," view or modify the b_username and db password 
variables to match MySQL username and password.
5. Run and execute the Application.py script.

## Conceptual Design
![Alt Text](/Users/laurenphan/Downloads/WellnessJournal/ProposalUML.png)

## Logical Schema Design
![Alt Text](/Users/laurenphan/Downloads/WellnessJournal/Schema.png)

## Final User Flow
![Alt Text](/Users/laurenphan/Downloads/WellnessJournal/ProposalActivityDiagram.png)

The user interacts with the system using a CLI interaction. The user starts by entering their
username and viewing their current entries. Then, they are prompted to select a date. If they date exists,
they have the option to edit, read, or delete the entry, as well as its smaller components. If the 
entry did not exist, one was created. The user has various options to backtrack and exit the 
programming during its duration.

## Lessons Learned
This project taught as a multitude of technical and behavioral skills. Technically, we learned how to expand upon our
previous python knowledge by connecting it to a database server, giving us a more efficient way to store and
interact with large amounts of data. Conceptually, we learned how to better work in a team for a large-scale project, 
including proper time management and communication. We approached the project wanting to take it one step at a time,
but we realized that designing a large program is easier when envisioning the final product and breaking it down 
step by step, as opposed to working chronologically and trying to figure things out on the way. Another design we 
considered was having the entry table contain all components, to allow the user to view an entire entry in one 
view. We also contemplated having users be able to have friends and view their entries, too. However, we decided 
upon this design because we believe is has the simplest segregation of information while maintaining third normal form.

## Future Work
As busy college students, we intend to use this program to track and hold ourselves more accountable for maintaining 
our physical and emotional health. By logging this information more frequently, we hope to increase our self awareness 
mindfulness. In the future, we hope to expand by implementing a fully interactive GUI as well as
implementing a weekly and/or monthly view.