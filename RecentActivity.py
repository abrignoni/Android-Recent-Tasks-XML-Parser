import xml.etree.ElementTree as ET  
import glob, os, sqlite3, os, sys, re, json

#Create sqlite databases
db = sqlite3.connect('RecentAct.db')

cursor = db.cursor()

#Create table recent.

cursor.execute('''

    CREATE TABLE recent(task_id TEXT, effective_uid TEXT, affinity TEXT, real_activity TEXT, first_active_time TEXT, last_active_time TEXT,

					  last_time_moved TEXT, calling_package TEXT, user_id TEXT, action TEXT, component TEXT, snap TEXT, 
					  
					  recimg TXT, fullat1 TEXT, fullat2 TEXT)

''')

db.commit()

err = 0
print ()
print ('Android Recent Activity Parser')
print ('By: @AlexisBrignoni')
print ('Web: abrignoni.com')
print ()
print ('Files processed: ')

script_dir = os.path.dirname(__file__)
for filename in glob.iglob(script_dir+r'\recent_tasks\**', recursive=True):
	if os.path.isfile(filename): # filter dirs
		file_name = os.path.basename(filename)
		#print(filename)
		#print(file_name)
		#numid = file_name.split('_')[0]
		
		#Test if xml is well formed
		try:
			ET.parse(filename)
		except ET.ParseError:
			print('Parse error - Non XML file? at: '+filename)
			err = 1
			#print(filename)
			
		if err == 1:
			err = 0
			continue
		else:
			tree = ET.parse(filename)
			root = tree.getroot()
			print('Processed: '+filename)
			for child in root:
				#All attributes. Get them in using json dump thing
				fullat1 = json.dumps(root.attrib)
				task_id = (root.attrib.get('task_id'))
				effective_uid = (root.attrib.get('effective_uid'))
				affinity = (root.attrib.get('affinity'))
				real_activity = (root.attrib.get('real_activity'))
				first_active_time = (root.attrib.get('first_active_time'))
				last_active_time = (root.attrib.get('last_active_time'))
				last_time_moved = (root.attrib.get('last_time_moved'))
				calling_package = (root.attrib.get('calling_package'))
				user_id = (root.attrib.get('user_id'))
				#print(root.attrib.get('task_description_icon_filename'))
				
				#All attributes. Get them in using json dump thing
				fullat2 = json.dumps(child.attrib)
				action = (child.attrib.get('action'))
				component = (child.attrib.get('component'))
				icon_image_path = (root.attrib.get('task_description_icon_filename'))
				
				#Snapshot section picture
				snapshot = task_id + '.jpg'
				#print(snapshot)
				
				#check for image in directories
				check1 = script_dir + '\\snapshots\\' + snapshot
				isit1 = os.path.isfile(check1)
				if isit1:
					snap = r'./snapshots/' + snapshot
				else:
					snap = 'NO IMAGE'
				#Recent_images section
				if icon_image_path is not None:
					recent_image = os.path.basename(icon_image_path)
					check2 = script_dir + '\\recent_images\\' + recent_image
					isit2 = os.path.isfile(check2)
					if isit2:
						recimg = r'./recent_images/' + recent_image
					else:
						recimg = 'NO IMAGE'
				else:
					recimg = 'NO IMAGE'
				#insert all items in database
				cursor = db.cursor()
				datainsert = (task_id, effective_uid, affinity, real_activity, first_active_time, last_active_time, last_time_moved, calling_package, user_id, action, component, snap, recimg, fullat1, fullat2,)
				cursor.execute('INSERT INTO recent (task_id, effective_uid, affinity, real_activity, first_active_time, last_active_time, last_time_moved, calling_package, user_id, action, component, snap, recimg, fullat1, fullat2)  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', datainsert)
				db.commit()
				
#Create html file for report
f1=open('./Recent_Activity.html', 'w+')

print('')
print('Generated: RecentAct.db')
#HTML header
f1.write('<html><body>')
f1.write('<h2> Android Recent Tasks Report </h2>')
f1.write ('<style> table, th, td {border: 1px solid black; border-collapse: collapse;} img {width: 180px; height: 370px; object-fit: cover;}</style>')


#Query to create report
db = sqlite3.connect('RecentAct.db')
cursor = db.cursor()

#Query to create report
cursor.execute('''
SELECT 
	task_id as Tak_ID, 
	effective_uid as Effective_UID, 
	affinity as Affinity, 
	real_activity as Real_Activity, 
	datetime(first_active_time/1000, 'UNIXEPOCH', 'LOCALTIME') as First_Active_Time, 
	datetime(last_active_time/1000, 'UNIXEPOCH', 'LOCALTIME') as Last_Active_Time,
	datetime(last_time_moved/1000, 'UNIXEPOCH', 'LOCALTIME') as Last_Time_Moved,
	calling_package as Calling_Package, 
	user_id as User_ID, 
	action as Action, 
	component as Component, 
	snap as Snapshot_Image, 
	recimg as Recent_Image
FROM recent
''')
all_rows = cursor.fetchall()
colnames = cursor.description

for row in all_rows:
	if row[2] is None:
		row2 = 'NO DATA'
	else:
		row2 = row[2]
	appName = '<h3> Application: ' + row2 + '<h3>'
	f1.write(appName)
	f1.write('<table> <tr><th>Key</th><th>Values</th></tr>')
	
	#do loop for headers
	
	for x in range(0, 13):
		
		if row[x] is None:
			dbCol = 'NO DATA'
			f1.write('<tr>')
			f1.write('<td align="left">')
			f1.write(colnames[x][0])
			f1.write('</td>')
		
			f1.write('<td align="left">')
			f1.write(dbCol)
			f1.write('</td>')
			f1.write('</tr>')
			#f1.write('</br>')
			
			
		else:
			f1.write('<tr>')
			f1.write('<td align="left">')
			f1.write(colnames[x][0])
			f1.write('</td>')
			
			f1.write('<td align="left">')
			f1.write(row[x])
			f1.write('</td>')
			f1.write('</tr>')
			
			#f1.write('</br>')
	f1.write('</table></p>')	
	f1.write('<table> <tr><th>Snapshot_Images</th><th>Recent_Image</th></tr>')
	f1.write('<tr>')
	for x in range(11, 13):
			if row[x] == 'NO IMAGE':
					
				
				f1.write('<td align="left">')
				f1.write('<img src="noimg.jpg" alt="Smiley face">')
				f1.write('</td>')
				
			else:
				
			#f1.write('</tr>')
				#f1.write('<tr>')
				f1.write('<td align="left">')
				f1.write('<a href="')
				f1.write(row[x])
				f1.write('"><img src="')
				f1.write(row[x])
				f1.write('" alt="Smiley face">')
				f1.write('</a>')
				f1.write('</td>')
				#f1.write('</tr>')
	f1.write('</tr>')
	f1.write('</table></p>')
f1.write('Code by:' + '</br>')
f1.write('@AlexisBrignoni' + '</br>')
f1.write('abrignoni.com' + '</br>')
print('Generated: Recent_Activity.html')
