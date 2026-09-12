#!/usr/bin/env bash


#Variables
LOG_FILE="../docs/secure_network_check.log"
TARGET_DOMAIN_ARR=("example.com" "google.com" "chasacademy.instructure.com")
TARGET_PORT=8080
TEST_SERVER="python3 -m http.server $TARGET_PORT --bind 127.0.0.1"
PID_TEST_SERVER=0
declare -A NINF=()

#-----------------------------------------------------------#

# Function to format log messages with timestamp
log_message() {
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    STATUS=$1
    MESSAGE=$2
    echo "[$TIMESTAMP] [$STATUS] $MESSAGE" | tee -a "$LOG_FILE"
}

#-----------------------------------------------------------#

cleanup(){
    log_message INFO "Checking if test server is running"
    if  pgrep -f "$TEST_SERVER" > /dev/null; then
        log_message INFO "Shutting down test server"
        pkill -f "python3 -m http.server $TARGET_PORT"
        log_message OK "Test server stopped"
    else
        log_message OK "No test server running";
    fi


}
#-----------------------------------------------------------#

startTestServer()
{
	log_message INFO Starting Test server
	python3 -m http.server $TARGET_PORT --bind 127.0.0.1 &
	PID_TEST_SERVER=$(pgrep -f "$TEST_SERVER")
	
	sleep 1
	log_message INFO "fetching HTTP from localhost"
	echo "#/////////////////////////////////////////////////#"
	if curl localhost:8080; then
		 echo "#/////////////////////////////////////////////////#"

		log_message OK "Succesfully fetch http from localhost"
	else
		log_message FAIL "Could not curl towards localhost"
	fi
}

#-----------------------------------------------------------#

dnsCheck()
{
    if [ -z "$TARGET_DOMAIN_ARR" ]; then
        log_message WARN "No domains provided"
    else
	    for domain in "${TARGET_DOMAIN_ARR[@]}"
	    do
		if getent hosts "$domain" >/dev/null; then
			log_message OK "$domain is reachable"
		else
			log_message FAIL "$domain is not reachable"
		fi
		done
    fi
}

directoryExists()
{
echo Hello
}

openPorts()
{
	log_message INFO "Fetching listening ports"
	echo "#/////////////////////////////////////////////////#"	
	ss -tuln 
	echo "#/////////////////////////////////////////////////#"

}

routing()
{
	declare -A NINF=()

	for iface in /sys/class/net/*; do
       		NINF[$(basename "$iface")]=$(<"$iface/carrier");
	done

	for i in "${!NINF[@]}"; do
        	echo "${i}: ${NINF[$i]}";
	done



	interfaceCount="$(ip -br a | wc -l)";
	
	#if wired/wireless connection up
		# log connection is wired/wireless
	#else if
		# log warning no wired/wireless connection
	
	#else 
		#log OK Connected via (show type of connection)
		# show address information 
}



main() {
    log_message INFO "Starting secure network check"
   
    dnsCheck
    startTestServer
    cleanup
    openPorts
    log_message INFO "Secure network check completed"
}


main


