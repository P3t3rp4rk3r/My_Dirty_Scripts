#!/bin/bash -u
#
# Tools: NMAP, NDIFF, PRIPS and Slackcli
# SLACKTOKEN from here https://api.slack.com/web
# PRIPS : Parellel processing 
# NDIFF latest version


NETWORKS="192.168.0.0/24"
TARGETS=$(for NETWORK in ${NETWORKS}; do prips $NETWORK; done)
INTERVAL="1800"
SLACKTOKEN="Get This From https://api.slack.com/web"
OPTIONS='-T4 --open --exclude-ports 25'


cd  ~/scan
LAST_RUN_FILE='.lastrun'

while true; do

    # If the last run file exists, we should only sleep for the time
    # specified minus the time that's already elapsed.
    if [ -e "${LAST_RUN_FILE}" ]; then
        LAST_RUN_TS=$(date -r ${LAST_RUN_FILE} +%s)
        NOW_TS=$(date +%s)
        LAST_RUN_SECS=$(expr ${NOW_TS} - ${LAST_RUN_TS})
        SLEEP=$(expr ${INTERVAL} - ${LAST_RUN_SECS})
        if [ ${SLEEP} -gt 0 ]; then
            UNTIL_SECS=$(expr ${NOW_TS} + ${SLEEP})
            echo $(date) "- sleeping until" $(date --date="@${UNTIL_SECS}") "(${SLEEP}) seconds"
            sleep ${SLEEP}
        fi
    fi

    START_TIME=$(date +%s)
    echo '' 
    echo '=================='
    echo '' 


    DATE=`date +%Y-%m-%d_%H-%M-%S`
    for TARGET in ${TARGETS}; do
        CUR_LOG=scan-${TARGET/\//-}-${DATE}
        PREV_LOG=scan-${TARGET/\//-}-prev
        DIFF_LOG=scan-${TARGET/\//-}-diff

	echo ''        
	echo $(date) "- starting ${TARGET}"
	

        # Scan the target
        nmap ${OPTIONS} ${TARGET} -oX ${CUR_LOG} >/dev/null

        # If there's a previous log, diff it
        if [ -e ${PREV_LOG} ]; then

            # Exclude the Nmap version and current date - the date always changes
            ndiff ${PREV_LOG} ${CUR_LOG} | egrep -v '^(\+|-)N' > ${DIFF_LOG}
            if [ -s ${DIFF_LOG} ]; then
			printf "Changes Detected, Sending to Slack."
			nmap -sV ${TARGET} | grep open | grep -v "#" > openports.txt
			slackcli -t $SLACKTOKEN -h nmap -m "Changes were detected on ${TARGET}. The following ports are now open: " 
			sleep 1
			cat openports.txt | slackcli -t $SLACKTOKEN -h nmap -c 
			rm openports.txt
                # Set the current nmap log file to reflect the last date changed
                ln -sf ${CUR_LOG} ${PREV_LOG}
            else
                # No changes so remove our current log
		printf "No Changes Detected."
                rm ${CUR_LOG}
            fi
            rm ${DIFF_LOG}
        else
            # Create the previous scan log
            ln -sf ${CUR_LOG} ${PREV_LOG}
        fi
    done

    touch ${LAST_RUN_FILE}
    END_TIME=$(date +%s)
    echo
    echo $(date) "- finished all targets in" $(expr ${END_TIME} - ${START_TIME}) "second(s)"
done