TODO:
	* generate an empty table with a v-for
	* after you did that ^, do the same with the content from a list generated from a db query
	

db orarEtti:

 - Necessary tables:
	* ROOMS
		- room_name 		STRING
		- room_id 			INT
		- capacity			INT
		- building			STRING
		- floor				INT
		- has_projector 	BOOL
		- has_wifi			BOOL
	
	* CLASSES
		- class_id 			INT
		- start_time		DATE
		- end_time			DATE
		- room_id			INT
		- prof_id			INT
		- class_type		STRING (curs/seminar/lab)
		- course_id			INT
		
	* COURSES
		- course_id			INT
		- name				STRING
		- prof_id			INT		-> PROF_ACCOUNT
		- course_type		STRING (curs/seminar/lab)
		- language			STRING
		- description		STRING
		
	* PROF_ACCOUNTS (will be stored after creation)
		- prof_id			INT
		- name				STRING
		- email				STRING
		- passwd			STRING
		- teached_courses	STRING
		- bio				STRING
		
	* GROUPS
		- group_id
		- name
		- sef_grupa
		- nr_telefon
		- mail
		- size
	
	* SERIES
		- id
		- name
		
	* GROUP_CLASSES (intermediary table)
		- group_id
		- class_id

 - Notes:
  * we need to update the site each time the db is updated from ANYWHERE, not just from the current session.
  * there must be 2 views:
    - the current schedule with all the days and hour intervals.
    - the schedule for each room for current week.
  * option to announce if a course will not be held in order to announce other profs for a potential re-schedule.
  * option to quickly find a room for a re-schedule with desired hour and day as input.
    - usage: reschedule [-t time] [-r fav_room]
  * regarding students: account registration would be too much. better, opt to announce via mail or sms potential changes/updates of a selected group!
  * option to export selected group to Google Calendar, .csv etc.
  * option to acces api for given groups.
  
