import smtplib
import random
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from random import randint
from numpy.random import choice
 

"""We will create a rando generator to fill in our RUN LOG, which then emails the log to my phy ed teacher. This script will be scheduled to run every Sunday between 9 and 10:30. I do enough running, (probably more than required by this class) but I do it for fun and relaxation, and having to keep track of it all saps the fun from it."""

def rungen(): #This function is the meat and potatoes of the program. All this generated info will later be inserted into the email function, so we can send it to my senile Phy Ed coach, because let's face it -- why are college students forced to participate in Phy Ed anyway! rungen stands for running-log generator ;) This program also has a few little quirks to randomise stuff to hide the fact that the running logs are being generated by a script, like send-time and mileage time, etc. This file was scheduled using cron to execute every Sunday, when the logs were due.  
	#We need to randomly pick 5 different distances for 5 different days of the week, each of which needs to be between 1.5 and 4 miles (with around 2-3 miles favored). The total mileage needs to be between 10 and twenty miles (roughly). We also want to make sure the days are sorted!



#########################################################################
	"""This section picks 5 random days of the week and sorts them"""
#########################################################################
	day1 = "Sunday"
	day2 = "Monday"
	day3 = "Tuesday"
	day4 = "Wednesday"
	day5 = "Thursday"
	day6 = "Friday"
	day7 = "Saturday"
	days_list = [day1,day2,day3,day4,day5,day6,day7]
	chosen_days = [] #a list that will eventually hold our chosen, sorted days
	rando_list = [] #This will become our list of random values, which will become random days of the week
	counter = 1
	while counter <6:
		rando = randint(1,7) #Pick a random day of the week, corresponding to its number - Sunday is 1!
		if rando in rando_list:
			counter = counter
		else:
			rando_list.append(rando)
			counter +=1
	rando_list.sort(key=int)
	#print rando_list 
	for i in rando_list:
		chosen_days.append(days_list[i-1])
	print chosen_days



########################################################################################################################################################################
	"""This section picks running distances, ensuring theyre between 1.5 and 4 miles, favoring around 2 miles, and that the total is between 10 and 22 miles"""
########################################################################################################################################################################
	distances = [1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0,4.1,4.2,4.3,4.4] #length = 30
	d_weights =   [.005,.007,.008,.03,.05,.05,.08,.11,.07,.03,.03,.03,.03,.03,.03,.025,.025,.025,.025,.025,.025,.025,.025,.025,.025,.025,.025,.03,.03,.05] # weights for entries in distances, sum = 1.0
	#print sum(d_weights) #To ensure the sum of the p-weights is 1
	distances_list = []
	for i in chosen_days:
		distances_list.append(choice(distances, p=d_weights))
	print distances_list
	total_distance = round(sum(distances_list),3)
	#print total_distance


	#print(choice(distances, p=weights)) #This command picks a random distance value, using the weights to ensure feasability
	

###############################################################
	"""This section comes up with an intensity and time"""
###############################################################
	intensities = ["mild", "medium", "vigorous"] #a list that holds intensity ratings for each exercise. This will be used to calculate how long the run took.
	i_weights = [.2,.35,.45] #Weighted values for how hard we want to run and how often
	intensities_list = [] #a list that will hold the intensities for each day
	time_list = [] #a list that will calculate how long each run took
	for i in distances_list:
		intensity = choice(intensities, p=i_weights)
		intensities_list.append(intensity)
		loc = distances_list.index(i)
		#print loc
		if  intensities_list[loc]== "mild":
			time = random.uniform(6.9,7.7) * i
			time = str(round(time,2))
			tsplit = time.split('.')
			time = '%.2f' % float(tsplit[0] + '.' + str(int(float(tsplit[1]) * .6 )))
			time_list.append(time)
		elif intensities_list[loc] == "medium":
			time = random.uniform(6.2,7) * i
			time = str(round(time,2))
			tsplit = time.split('.')
			time = '%.2f' % float(tsplit[0] + '.' + str(int(float(tsplit[1]) * .6 )))
			time_list.append(time)
		elif intensities_list[loc] == "vigorous":
			time = random.uniform(5.8,6.3) *i
			time = str(round(time,2))
			tsplit = time.split('.')
			time = '%.2f' % float(tsplit[0] + '.' + str(int(float(tsplit[1]) * .6 )))
			time_list.append(time)	
	print intensities_list
	print time_list
	

######################################################################################################################
	"""This next section packages all the info up and returns it as a usable string to be inserted in our email"""
######################################################################################################################
	final_list = []
	intro = "Hello, here is my log for the last week. Thanks! \n \n"
	outro = "\n\nTotal distance = " + str(total_distance) + " miles."
	for i in range(0,5):
		final_list.append(str(chosen_days[i] + ': distance = ' + str(distances_list[i]) + " miles at " + intensities_list[i] + " intensity. Total time was " + str(time_list[i])))
	print final_list
	final_string = intro + "\n".join(final_list) + outro
	print final_string
	return final_string

		
####################################################################################################################
y = rungen()	#run the function and name its output, final_string, y

delay = randint(0,5400) #setup a delay time
print str(delay) + " second delay" #to tell us how much delay there will be!
time.sleep(delay) #Delays the email so it's not always sent at the exact same time.




fromaddr = "You wish you could get this email"
toaddr = "Who do you want to send this to?"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Running Log for the past week"
 
body = y
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "You wish you knew my password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

