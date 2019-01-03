from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import sys
import time
import imp
import xlsxwriter

profile = webdriver.FirefoxProfile() 
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 8132)
profile.update_preferences() 
driver = webdriver.Firefox(firefox_profile=profile)

#function to get server detail and userid and password from text file
def getVarFromFile(filename):
    f = open(filename)
    global data
    data = imp.load_source('data', '', f)
    f.close()

getVarFromFile('server_input.txt')
print data.server
print data.Userid
#print data.Password
servername=data.server
Username=data.Userid
Pass=data.Password

#get and open servername
driver.get("%s" %servername)

userElem=driver.find_element_by_id('accountname')
userElem.send_keys('%s' %Username)
passwordElem = driver.find_element_by_id('accountpassword')
passwordElem.send_keys('%s' %Pass)
passwordElem.submit()

driver.get("%s" %servername)

#driver.implicitly_wait(5)


#driver.close()

#locating 1st Custom Filter and clicking    ##here it is taking time
try:
#    element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//button[@id='ext-gen2208']")))
    element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//button[@id='ext-gen71']")))
    element.click()
#    print "1st Custom Filter found and clicked"
except:
    print "issue in finding 1st custom filter"
#    driver.quit() 



#locating 2nd Custom Filter and clicking.    ## here it is taking time
try:
#   element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//button[@id='ext-gen2208']")))
	element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.LINK_TEXT, "Custom Filter")))
	element.click()
#    print "2nd Custom Filter found and clicked"
except:
    print "issue in finding 2nd custom filter"
#    driver.quit()




# locating text field and inserting Workflow value.
try:
	element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//input[@class='ext-mb-input']")))
	# element.click()
	# element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME, "ext-mb-fix-cursor")))
#	print "Text area located"
	element.send_keys('id=%s' %sys.argv[1])
	
except:
    print "issue in locating text field and inserting workflow value"
#    driver.quit()


#locating OK and clicking it.

#version_1 works fine but has limitation of dependency on id=ext-gen215 which is not fixed in html.

#version_2 works fine.
try:
	WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='x-btn-text' and contains(text(),'OK')]")))
	while EC.element_to_be_clickable((By.XPATH, "//button[@class='x-btn-text' and contains(text(),'OK')]")):
	##	driver.find_element_by_xpath("//button[@class='x-btn-text']").click()
   		if driver.find_element_by_xpath("//button[@class='x-btn-text' and contains(text(),'OK')]").is_enabled():
#   			print "click enabled "
   			element=driver.find_element_by_xpath("//button[@class='x-btn-text' and contains(text(),'OK')]")
   			element.click()
#   			print "submitted"
   		break
    	#WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='x-btn-text']")))
except:
	print "issue in locating OK and clicking it"

#new page open and click the shown job id.  ## here it is taking time
#version_2
try:
    element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='x-grid3-cell-inner x-grid3-col-id' and contains(text(),'%s')]" %sys.argv[1])))

    element.click()
#    print "new page open and job id clicked"
except:
    print "issue in new page open and click the shown job id"
    
    

#create function to work in each hive query
def hive_func(i,o_list1,hiveid):    
#new page opened and click on Consol URl     
	try:
		element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.TAG_NAME, "img")))
#		print "COnsole URL located"
		element=driver.find_element_by_css_selector(".x-form-trigger.x-form-search-trigger")
		element.click()
#		print "Consol URL clicked"
	finally:
		print "finally out"
#	print "Login window sholud open now"
	#skip apple login and jump directly to 
	if i==0:
		#toggle between two windows
		first_window=driver.current_window_handle
#		print first_window.title
	
		driver.implicitly_wait(40)
		driver.switch_to_window(driver.window_handles[1]) # this line takes control to new login window.
		second_window=driver.current_window_handle
#		print second_window.title
		#driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + Keys.TAB)	
#		print "control came to new window"
	
		#Login to Apple again

		#version_3
		element = WebDriverWait(driver,40).until(EC.element_to_be_clickable((By.CLASS_NAME, "logo")))
#		print "account password located"
		#userElem=driver.find_element_by_id('accountname')
		#userElem.send_keys('asharma26')
		passwordElem = driver.find_element_by_id('accountpassword')
		passwordElem.send_keys('%s' %Pass)
		passwordElem.submit()

		# goes back to original oozie window.
		driver.switch_to_window(driver.window_handles[0]) 

		# Came back to oozie and click on Consol URl again 
		try:
			element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".x-form-trigger.x-form-search-trigger")))
			element.click()
#			print "Consol URL clicked again"
		finally:
			print "finally out"

	# go to new 3rd window having Time stats # also need to check if the correct page opens or not.# also take time stats
	driver.implicitly_wait(40)
#	print len(driver.window_handles)
	driver.switch_to_window(driver.window_handles[i+2])
	print "came to time stats window"

	lists=driver.find_elements_by_tag_name('body')

	with open('amit.txt','w') as f:
		for line in lists:
			#print line.text
			f.write(line.text)
	#	print htmltextfile.csv
	Tags = ['Launched At', 'Finished At', 'Status', 'Started at', 'Finished at', 'Finished in']

	counter=0
	with open('amit.txt','r') as ff:
		for line in ff:
			#print line.strip()
			for element in Tags:
				if line.startswith(element):
					counter=1
					#print line.strip()
					data=line.strip()
					atpos=data.find('t:') #or data.find('n:')
					if atpos != -1:
						if element=='Launched At':
							host1=data[atpos+3:atpos+23]
							print host1
							o_list1.append(host1)
						elif element == 'Finished At':
							host2=data[atpos+3:atpos+23]
							print host2
							o_list1.append(host2)
							host3=data[atpos+24:]
							print host3
							o_list1.append(host3)
						elif element== 'Started at':
							host1=data[atpos+3:atpos+23]
							print host1
							o_list1.append(host1)
						elif element == 'Finished at':
							host1=data[atpos+3:atpos+23]
							print host1
							o_list1.append(host1)
					#	elif element == 'Finished in':
					#		host1=data[atpos+3:atpos+14]
					#		print host1
					#	else:
					#		print data
					elif element == 'Finished in':
						atpos=data.find('n:')
						host1=data[atpos+3:]
						print host1
						o_list1.append(host1)
					else:
						print data
						o_list1.append(data)
	if counter==0:
		print "No Time sats found on page"		
	#print "looking for Starting Job function"
	#Log file calculation function definition
	def main():
		f=open('tlog.txt','r')
		for line in f:
			if line.startswith("Total MapReduce jobs"):
				print line
                        

		f.close()
	
	def Starting_Job():
#		global o_tuple2
		global o_tupleJobid
		o_tupleJobid=()
		global o_tupleJobmr
		o_tupleJobmr=()
		f=open('tlog.txt','r')
#		o_list2=[]
		global op
		for item in f:
			checkpoint=0   
			o_listjobid=[]
			o_listmr=[]
			if item.startswith("Starting Job"):
				checkpoint=1
				atpos=item.find('Starting Job')
				host1=item[atpos+15:atpos+38]
				print host1
				o_list2.append(host1)
				o_listjobid.append(hiveid)
				o_listjobid.append(host1)
#				print re.findall(r'^Starting Job = (\S+)[^,]',item)
#				o_list2.append(re.findall(r'^Starting Job = (\S+)[^,]',item))
               
                
				start= item.find("Tracking URL")
				host2=item[start+15:].strip()				
				print host2
				o_list2.append(host2)
				o_listjobid.append(host2)
#				start= item.index("Tracking URL")
#				print re.findall(r'^Tracking URL = (\S+)',item[start:])
#				o_list2.append(re.findall(r'^Tracking URL = (\S+)',item[start:]))
				
				o_tupleJobid=o_tupleJobid+(o_listjobid,)				
			if "number of mappers" in item:
				checkpoint=1
				if item.startswith('Hadoop'):
					start= item.index("number of mappers")
					#print item[start:]
					op=re.findall('[0-9]+',item[start:])[0]
					o_list2.append(op)
					o_listmr.append(hiveid)
					o_listmr.append(op)
					op=re.findall('[0-9]+',item[start:])[1]
					#print op
					o_list2.append(op)
					o_listmr.append(op)
					o_tupleJobmr=o_tupleJobmr+(o_listmr,)
#			if checkpoint==1:
#				o_tuple3=o_tuple3+(o_list2,)		

#			o_list2=o_list2+op

#		o_tuple2=(o_list2,)	
		for each in o_tupleJobid:
			print "o_tuplejobid's",each			
		for each in o_tupleJobmr:
			print "o_tuplemr's",each
	
		
		
		
        #return o_tuple2
        f.close()

	'''	def Tracking():
		f=open('tlog.txt','r')
		for item in f: 
			if "Tracking URL" in item:
				start= item.index("Tracking URL")
				#print item[start:]
				print re.findall(r'^Tracking URL = (\S+)',item[start:])	
		f.close()	
	'''
	
	'''	def mapred():
		f=open('tlog.txt','r')
		for item in f: 
			if "number of mappers" in item:
				if item.startswith('Hadoop'):
					start= item.index("number of mappers")
					#print item[start:]
					op=re.findall('[0-9]+',item[start:])
					print op
	
		f.close()
	'''
	def tablename():
		f=open('tlog.txt','r')
		for item in f:
			if "Loading data to table" in item:
				splitted= item.split(".")
				tableline=splitted[1]			
				doublesplit=tableline.split()			
				tablename=doublesplit[0]
				print tablename
			
		f.close()	


	#Check for Tab "Analysis This Job" present or not and crawl to Log file to get map reduce stats
	#print "came to check analyse job"
	try:
		element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.LINK_TEXT, "Analyse This Job")))
		element=driver.find_element_by_link_text('Analyse This Job')
		#print " found analyse job"
		element.click()
		#print "analyse job clicked"

		# came to Task Id page. Find Task id and click
		element=driver.find_element_by_partial_link_text('task_')
		element.click()

		# came to All Task Logs page. Click All link.
		element=driver.find_element_by_partial_link_text('All')
		element.click()

		#Check if Task Log file page comes.
		try:
			element = WebDriverWait(driver,30).until(EC.title_contains("Task Logs"))
			if EC.title_contains("Task Logs"):
				print "In side Task log "
				lists=driver.find_elements_by_tag_name('html')
				with open('tlog.txt','w') as f:
					for line in lists:
						#print line.text
						f.write(line.text)
			#	main()
				Starting_Job()
		
			#	Tracking()
			#	mapred()
			#	tablename()
		finally:
			if EC.title_contains("Error"):
				print "No Log file"
			#    o_list2.append("No Log File")    
	

	finally:
		print "no Analyse Job link found"
	 #   o_list2.append("No 'Analyse Job' link found")

#new page opens and click on 1st hive query    ## here it is taking time and too much time as comapred   # need to loop thru for all hive queries here

try:
	#with open('input_jobid.txt', 'r') as f:
	'''	jobid=['%s@IBNP_Hive_Query_1_1' %sys.argv[1],'%s@IBNP_Hive_Query_1_2' %sys.argv[1],'%s@IBNP_Hive_Query_1_3' %sys.argv[1],'%s@IBNP_Hive_Query_1_4' %sys.argv[1],'%s@IBNP_Hive_Query_1_5' %sys.argv[1],'%s@IBNP_Hive_Query_1_6' %sys.argv[1],'%s@IBNP_Hive_Query_1_7' %sys.argv[1],'%s@IBNP_Hive_Query_1_8' %sys.argv[1],
	'%s@IBNP_Hive_Query_2_1' %sys.argv[1],'%s@IBNP_Hive_Query_2_2' %sys.argv[1],'%s@IBNP_Hive_Query_2_3' %sys.argv[1],'%s@IBNP_Hive_Query_2_4' %sys.argv[1],'%s@IBNP_Hive_Query_2_5' %sys.argv[1],'%s@IBNP_Hive_Query_2_6' %sys.argv[1],'%s@IBNP_Hive_Query_2_7' %sys.argv[1],'%s@IBNP_Hive_Query_2_8' %sys.argv[1],
	'%s@IBNP_Hive_Query_3_1' %sys.argv[1],'%s@IBNP_Hive_Query_3_1_1' %sys.argv[1],'%s@IBNP_Hive_Query_3_2' %sys.argv[1],'%s@IBNP_Hive_Query_3_3' %sys.argv[1],'%s@IBNP_Hive_Query_3_4' %sys.argv[1],'%s@IBNP_Hive_Query_3_5' %sys.argv[1],
	'%s@IBNP_Hive_Query_4_1' %sys.argv[1],'%s@IBNP_Hive_Query_4_2' %sys.argv[1],'%s@IBNP_Hive_Query_4_3' %sys.argv[1],'%s@IBNP_Hive_Query_4_4' %sys.argv[1],'%s@IBNP_Hive_Query_4_5' %sys.argv[1],'%s@IBNP_Hive_Query_4_6' %sys.argv[1],'%s@IBNP_Hive_Query_4_7' %sys.argv[1],'%s@IBNP_Hive_Query_4_8' %sys.argv[1],
	'%s@IBNP_Hive_Query_5_1_1' %sys.argv[1],'%s@IBNP_Hive_Query_5_1_2' %sys.argv[1],'%s@IBNP_Hive_Query_5_2' %sys.argv[1]]
	'''
	
	element1 = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='x-grid3-cell-inner x-grid3-col-id' and contains(text(),'Hive_Query')]")))
	element2=driver.find_elements_by_xpath(".//div[@class='x-grid3-cell-inner x-grid3-col-id' and contains(text(),'Hive_Query')]")
	#	a=re.search('0035391-151017222341994-oozie-oozi-W@(\S+)_Hive_Query_(\S+)')
	#'%s@(\S+)_Hive_Query_(\S+)'
	#print element1
	for each in element2:
		print each.text
	#element1.click() 
#	while EC.presence_of_element_located((By.XPATH, "//div[@class='x-grid3-cell-inner x-grid3-col-id' and contains(text(),'%s@(\S+)_Hive_Query_(\S+)')]" %sys.argv[1])):
	iteration=0
#	print iteration
 
	o_tuple1=() # output tuple to contain o_list1.
	o_tuple2=()
	for id in element2:
		o_list1=[]        #output list of time stats calculation intitated here for each hive query
		
		o_list2=[]        # output list of Jobid,URL,Mapper reducer intitated here for each hive query.update-it has been declared in Stating_job function
#		o_tuple2=()			# declare tuple here so that it get initiated afresh for each hive query. it conatains o_list2. 
		print id.text
		hiveid=id.text
		o_list1.append(id.text) #list started getting data from here.
		#print "//div[@class='x-grid3-cell-inner x-grid3-col-id' and contains(text(),'%s')]" %id.text
		element1 = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='x-grid3-cell-inner x-grid3-col-id' and contains(text(),'%s')]" %id.text)))

		element1.click()
	#	print iteration
		hive_func(iteration,o_list1,hiveid)
#		o_tuple1=(o_list1,)+o_tuple2
		
		o_tuple1=o_tuple1+(o_list1,)
		
		o_tuple2=o_tuple2+o_tupleJobid+o_tupleJobmr
		
		## goes back to original oozie window.
		driver.switch_to_window(driver.window_handles[0])
		iteration+=1
		time.sleep(5)
			
finally:
	print "finally out"


	
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Stats_calculation.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
#o_tuple1
#o_tuple2
# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

#for each in o_tuple1:
#	print each
for each in o_tuple2:
	print each
#tuple3=(o_list2[2],)
#for each in tuple3:
#	print "tuple3's", each

# Iterate over the data and write it out row by row.
for query,Start_date,End_date,Total_time,status in (o_tuple1):
    worksheet.write(row, col,     query)
    worksheet.write(row, col + 1, Start_date)
    worksheet.write(row, col + 2, End_date)
    worksheet.write(row, col + 3, Total_time)
    worksheet.write(row, col + 4, status)   
    row += 1
row = 0
for hiveid,JobId,URL in (o_tuple2):

    worksheet.write(row, col + 5, hiveid)
    worksheet.write(row, col + 6, JobId)
    worksheet.write(row, col + 7, URL)
#    worksheet.write(row, col + 8, RE)
    row += 1
# Write a total using a formula.
#worksheet.write(row, 0, 'Total')
#worksheet.write(row, 1, '=SUM(B1:B4)')

workbook.close()
				