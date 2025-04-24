//load_get_time.c
//This code is to store the ETA time from the tk_app and this engine will 
//run in the background and compute and the timer keep on ticking and 
//notify the user when the time up happens.
//
//
//tk_app --> socket --> load_get_time() --> timer --> socket --> tk_app()

#include <stdio.h>
#include <sys/un.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>
#include <string.h>

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


//Struct to hold the start time, end time and the current time.
struct task_timer {
	struct time st_time; /* Start time */
	struct time end_time; /* End time (ETA for Tk_app) */
	struct time cur_time; /* Curr time */
	

};

//Task status ds for the tk_app to monitor the task status
struct task_status {
	char *t_name; /* Task name */
	unsigned int t_id; /* Task id */
	unsigned int completion; /* Task Completion Status */
	t_status status; /* Task status */		
    struct task_timer timer_val; /* stores all the time */
};

//Link list of the task node.
struct task_node {
    unsigned int tnode; /*index of the task node */
    struct task_status tstaus;
};

/* tk_app to the engine */
struct tk_app_to_eng {
	char name[TASK_NAME_CNT]; /* should match with the tk_app task_name_cnt */
	struct task_timer timer; /* Need the time */
	void *prv_data; /* Start the development with void * and add on the members based on req */ 
};
	

//Struct the tk_app gives this engine 
struct tk_app_payload {
	unsigned int req_id:8; /* will repeat after 255 */
	tk_cmd cmd;
	struct tk_app_to_eng tk_to_eng; /* Struct for the tk_app to the communicate with the engine */
	/* Struct for the engine to talk with the tk_app */
	
};

int log_val = 255;

#define print_fn(val, x)\
	if (val < 4) \
		printf(x);\
    printf("\n");

#define p_e(x)\
    print_fn(0, x);

#define p_i(x)\
    print_fn(5, x);

typedef struct {
    unsigned int sockfd; /* Sockfd to store the unix socket */
    /* add mutex lock to the task_timer*/
}app_data;

#define UPATH "/tmp/unix_socket_example"

int create_socket(app_data *adata) {
    if(!adata) {
        p_e("app data null");
        return -1;
    
    }
    
    int success = 0;
    int server_sock = 0;
    struct sockaddr_un addr;
    /* Create a socket */
    
    server_sock = socket(AF_UNIX, SOCK_STREAM, 0);
    
    if(server_sock == -1) {
        p_e("Error in creating socket");
        return -1;
        
    }

    memset(&addr, 0, sizeof(struct sockaddr_un));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, UPATH, sizeof(addr.sun_path) - 1);
    unlink(UPATH); // Remove previous socket if it exists
    if (bind(server_sock, (struct sockaddr *)&addr, sizeof(struct sockaddr_un)) == -1) {
        p_e("bind failed");
        return -1;
    
    }

    return success;
}

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

	return 0;

}
		
