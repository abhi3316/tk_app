//load_get_time.c
//This code is to store the ETA time from the tk_app and this engine will 
//run in the background and compute and the timer keep on ticking and 
//notify the user when the time up happens.
//
//
//tk_app --> socket --> load_get_time() --> timer --> socket --> tk_app()

#include <stdio.h>
//#include <socket.h>
#include <string.h>
#include <unistd.h>


#define TASK_NAME_CNT (50) /*tk_app also should be aware of this */

//Task status to communicate with the tk_app.
typedef enum {
	TASK_EXPIRED, /* Expired task, timer run out */
	TASK_RUNNING, /* Task is running */
	TASK_NOT_BEGINED, /*Task not started by the tk_app */
	TASK_DETACHED /* Task not monitored by hte tk_app */
} t_status;

typedef enum {
	Tk_create_task, /* Create Task structure  (Link list memory assign) */
	Tk_send_task_details, /* Task details in the payload */
	Tk_start_timer, /* Start the timer */
	Tk_check_timer_status, /* Check the timer status at any point of time */
	Tk_check_timer_expiry, /* Check for the timer expiry */
	Tk_check_run_status, /* Check the running status of the task */
	Tk_delete_task   /* Delete the task from the memory */
} tk_cmd;

struct time {
	unsigned int hour:8; /* hours */
	unsigned int min:8;  /* mins */
	unsigned int sec:8;  /* secs */

};

//Task status ds for the tk_app to monitor the task status
struct task_status {
	char *t_name; /* Task name */
	unsigned int t_id; /* Task id */
	unsigned int completion; /* Task Completion Status */
	t_status status; /* Task status */		
};

//Struct to hold the start time, end time and the current time.
struct task_timer {
	struct time st_time; /* Start time */
	struct time end_time; /* End time (ETA for Tk_app) */
	struct time cur_time; /* Curr time */
	

};

/* tk_app to the engine */
struct tk_app_eng {
	char name[TASK_NAME_CNT]; /* should match with the tk_app task_name_cnt */
	struct task_timer timer; /* Need the time */
	
};
	

//Struct the tk_app gives this engine 
struct tk_app_payload {
	unsigned int req_id:8; /* will repeat after 255 */
	tk_cmd cmd;
	/* Struct for the tk_app to the communicate with the engine */
	/* Struct for the engine to talk with the tk_app */
	
};

int log_val = 255;

#define print_fn(x)\
	if (log_val < 4) \
		printf(x);

int main(int argc, char **argv) {
	int opt = 0;	
	while ((opt = getopt(argc, argv, "l")) != -1) {
		switch(opt) {
			case 'l':
				log_val = 1;
				printf("log set value\n");
				break;	

		}

	}

	print_fn("The Code is completed\n");
	return 0;

}
		
