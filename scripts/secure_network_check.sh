#!/usr/bin/env bash


#Variables
EVIDENCE="../evidence/secure_network_check_log_extended.log"
LOG_FILE="../evidence/secure_network_check.log"
TARGET_DOMAIN_ARR=("example.com" "google.com" "chasacademy.instructure.com")
TARGET_PORT=8080
PID_TEST_SERVER=0
declare -a TOOLS=("curl" "ss" "getent" "pgrep" "pkill" "ip" "date" "tee" "python3" "sed")

SUCCESS=0
FAILED=0
#-----------------------------------------------------------#

# Function to format log messages with timestamp
log_message() {
    local TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    local STATUS=$1
    local MESSAGE=$2
    echo "[$TIMESTAMP] [$STATUS] $MESSAGE" | tee -a "$LOG_FILE"
	
	#Case-switch logic for summery of statuses
	case "$STATUS" in

	OK)
	((SUCCESS++))
	;;

	FAIL)
	((FAILED++))
	;;
	esac
	

}	
	

#-----------------------------------------------------------#

start()
{	
	#Start logic to determine if to wipe logs
	while true;
	do
		echo $'IF YOU CONTINUE THE PREVIOUS LOGS WILL BE WIPED!'
		echo $'\nCONTINUE?  y/n'
		# User input determines if to continue or not
		read -r input

		if [[ "$input" =~ ^[yY]+$ ]]; then
			clear
			echo "STARTING NETWORK CHECK ..."
			sleep 2
			#Program coninues normaly.
			break
		elif [[ "$input" =~ ^[nN]+$ ]]; then
			clear
			echo "EXITING ..."
			sleep 2
			exit 0; #Exiting normally, no error.
		else
			#User input wasnt valid so loop starts over
			clear
			echo "input invalid INPUT: $input"
			sleep 2
			clear
		fi
	done
}

#-----------------------------------------------------------#

#Determine if system has the required commands installed
validate_command()
{
	

	declare -a FAILED_TOOLS=()		

	#Appends missing command to array
	for command in "${TOOLS[@]}";do
		if ! command -v "$command" &> /dev/null; then
			FAILED_TOOLS+=("$command")
		fi
	done

	#If missing atleast one command the program is interupted with exit code 1
	if [ ${#FAILED_TOOLS[@]} -ne 0 ]; then
		log_message FAIL "The following required commands are missing: ${FAILED_TOOLS[*]}"
		exit 1
	else 
		log_message OK "All required commands are available."
	fi
}

#-----------------------------------------------------------#

#Stops test service, and sanitzes output
cleanup(){
	#Replace regexmatch with replacement string
	sed -Ei 's/127(\.[0-9]{1,3}\.){2}[1]{1,3}/[LOCALHOST]/g' $EVIDENCE
	sed -Ei 's/([0-9]{1,3}\.){3}[0-9]{1,3}/[REDACTED]/g' $EVIDENCE
	
	#Closes test server, if running
    log_message INFO "Checking if test server is running"

	
	if [ -z "$PID_TEST_SERVER" ]; then
		log_message FAIL "Cleanup failure, no server running or could not stop service"
    elif [ $PID_TEST_SERVER -gt 0 ] > /dev/null; then
        log_message INFO "Shutting down test server"
        kill "$PID_TEST_SERVER"
        log_message OK "Test server stopped"
    #Catch unexpected errors
	else	
		log_message WARN "Unexpected error during service cleanup"
	fi

	summery
	
}
#-----------------------------------------------------------#

startTestServer()
{

	echo "#////LOCAL TEST SERVER////" >> "$EVIDENCE"
	log_message INFO "Starting Test server";
	#Start a http server to serve http on localhost
	python3 -m http.server $TARGET_PORT --bind 127.0.0.1 &
	#save process id to variable
	PID_TEST_SERVER=$!
	jobs
	sleep 1
	log_message INFO "fetching HTTP from localhost"
	
	#Is http server serving http from localhost
	if curl localhost:"$TARGET_PORT" >> "$EVIDENCE" 2>&1; then
		log_message OK "Succesfully fetch http from localhost"
		log_message INFO "Test server info at $EVIDENCE"
	else
		log_message FAIL "Could not curl towards localhost:$TARGET_PORT"
	fi
}

#-----------------------------------------------------------#

dnsCheck()
{
	#Were domain names given to test
    if [ ${#TARGET_DOMAIN_ARR[@]} -eq 0 ]; then
        log_message WARN "No domains provided"
    else
		# Try to reslove each domain in array
	    for domain in "${TARGET_DOMAIN_ARR[@]}"
	    do
		if getent hosts "$domain" >/dev/null; then
			log_message OK "$domain was resolved successfully"
		else
			log_message FAIL "$domain could not be resolved"
		fi
		done
    fi
}

#-----------------------------------------------------------#

logsExists()
{
	declare -a LOGS=("$LOG_FILE" "$EVIDENCE")
	for log in "${LOGS[@]}";do
		if [ -e "$log" ]; then 
			log_message OK "$log Exists"
		else
			log_message INFO "$log doesnt exist, creating directory . . ."
			touch "$log"
			log_message OK "$log created"
		fi
	done
}

#-----------------------------------------------------------#

openPorts()
{
	log_message INFO "Fetching listening ports"
	echo "////LISTENING PORTS////" >> "$EVIDENCE"	
	#Lists currently listening ports
	ss -tuln | grep -e tcp -e udp | sed -E 's/:([0-9]{1,5})/:[PORT]/g' >> "$EVIDENCE"
	openPortCount="$(ss -tuln | grep -e tcp -e udp| wc -l)" 
	log_message INFO "Number of open ports: $openPortCount | More at evidence file"
}

#-----------------------------------------------------------#

routing()
{
	declare -A NINF=()
	


	for iface in /sys/class/net/*; do
		if [ -r "$iface/carrier" ]; then
       		NINF[$(basename "$iface")]=$(<"$iface/carrier");
		fi
	done

	echo "////NETWORK INTERFACES & ROUTE////" >> "$EVIDENCE"
	ip -br a  >> "$EVIDENCE"
	echo "" >> "$EVIDENCE"
	ip route show >> "$EVIDENCE"
	
	for i in "${!NINF[@]}"; do
			
			if [ "${NINF[$i]}" -ne 1 ]; then
			log_message WARN "${i} is not connected";
			else
			log_message OK "${i} is connected"
			fi 
	done
 


}

summery()
{

	echo
	echo "========== SUMMARY =========="
	echo "Successful checks : $SUCCESS"
	echo "Failed checks     : $FAILED"
	echo "Log file          : $LOG_FILE"
	echo "Evidence file     : $EVIDENCE"
	echo "============================="

}

#-----------------------------------------------------------#

main() {
	# Cleanup is done at end of program or if program is terminated early 
	trap cleanup EXIT INT TERM
	# Is user rooted?
	

		# Prepare network check
		start
		clear
		logsExists
		# Wipe logfiles
		> $LOG_FILE
		> $EVIDENCE

		# Start Network check
		log_message INFO "Starting secure network check"
		validate_command
		routing
    	dnsCheck
    	startTestServer
    	openPorts
    	log_message INFO "Secure network check completed"
		
	
}


main


