#include "phylib.h"

//This function will create a new still ball, given its number and position
phylib_object *phylib_new_still_ball( unsigned char number,
phylib_coord *pos ){
    phylib_object * still_ball = malloc(sizeof(phylib_object)); //allocate memory
    if(still_ball == NULL){      
        return NULL;          //if malloc failed, return NULL
    }
    still_ball->type = PHYLIB_STILL_BALL;
    still_ball->obj.still_ball.number = number;
    still_ball->obj.still_ball.pos = (*pos);
    return still_ball;
}

/*This function will create new rolling ball on table given its
number, position, velocity and acceleration*/
phylib_object *phylib_new_rolling_ball( unsigned char number,
phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){
    phylib_object * rolling_ball = malloc(sizeof(phylib_object)); //allocate memory
    if(rolling_ball == NULL){ 
        return NULL;          //if malloc failed, return NULL
    }
    rolling_ball->type = PHYLIB_ROLLING_BALL;
    rolling_ball->obj.rolling_ball.number = number;
    rolling_ball->obj.rolling_ball.pos = (*pos);
    rolling_ball->obj.rolling_ball.vel = (*vel);
    rolling_ball->obj.rolling_ball.acc = (*acc);

    return rolling_ball;
}

//This function will create a new hole on the table given position
phylib_object *phylib_new_hole( phylib_coord *pos ){
    phylib_object * new_hole = malloc(sizeof(phylib_object));  //allocate memory
    if(new_hole == NULL){
        return NULL;       //if malloc failed, return NULL
    }
    new_hole->type = PHYLIB_HOLE;
    new_hole->obj.hole.pos = (*pos);

    return new_hole;
}

//This function will create a new horizontal cushion that stretches all the way
phylib_object *phylib_new_hcushion( double y ){
    phylib_object * new_hcushion = malloc(sizeof(phylib_object));  //allocate memory
    if(new_hcushion == NULL){
        return NULL;         //if malloc failed, return NULL
    }
    new_hcushion->type = PHYLIB_HCUSHION;
    new_hcushion->obj.hcushion.y = y;

    return new_hcushion;
}

//This function will create a new vertical cushion that stretches
phylib_object *phylib_new_vcushion( double x ){
    phylib_object * new_vcushion = malloc(sizeof(phylib_object));   //allocate memory
    if(new_vcushion == NULL){
        return NULL;         //if malloc failed, return NULL
    }
    new_vcushion->type = PHYLIB_VCUSHION;
    new_vcushion->obj.vcushion.x = x;

    return new_vcushion;
}

// phylib_coord * phylib_coord_new(double x, double y){
//     phylib_coord * temp = malloc(sizeof(phylib_coord));
//     if(temp == NULL){
//         return NULL;
//     }
//   //  phylib_object * temp =malloc(sizeof(phylib_object));
//     // temp->obj.hole.pos.x = x;
//     // temp->obj.hole.pos.y = y;
//     temp->x = x;
//     temp->y = y;
//   //  phylib_new_hole(temp);
//     return temp;
// }

//This function sets up the table
phylib_table *phylib_new_table( void ){
    phylib_table * new_table = malloc(sizeof(phylib_table));  //allocate memory
    if(new_table == NULL){
        return NULL;
    }
    
    new_table->time = 0.0;     //set time to 0
    //new_table->object = phylib_new_hcushion(0.0);
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        new_table->object[i]=NULL;           //initialize all to NULL
    }
    //set 4 cushions
    new_table->object[0]=phylib_new_hcushion(0.0);
    new_table->object[1]=phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2]=phylib_new_vcushion(0.0);
    new_table->object[3]=phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    //set 6 holes
    new_table->object[4] = phylib_new_hole( &(phylib_coord){0,0});
    new_table->object[5]= phylib_new_hole(&(phylib_coord){0,PHYLIB_TABLE_WIDTH});
    new_table->object[6]= phylib_new_hole(&(phylib_coord){0,PHYLIB_TABLE_LENGTH});
    new_table->object[7]= phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0});
    new_table->object[8]= phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH/2});
    new_table->object[9]= phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});

    return new_table;
}

//This function will copy a phylib_object
void phylib_copy_object( phylib_object **dest, phylib_object **src ){
    if(*src == NULL){
        *dest = NULL;
    }
    else{
        phylib_object *copy = malloc(sizeof(phylib_object));   //allocate memory
        if(copy == NULL){
            return;
        }
        memcpy(copy, (*src), sizeof(phylib_object));    //memcpy the contents
        (*dest) = copy; 
    }
}

//This function will copy a phylib_table
phylib_table *phylib_copy_table( phylib_table *table ){
    
    phylib_table * copy_table = malloc(sizeof(phylib_table));  //allocate memory
    if(copy_table == NULL){
        return NULL;
    }
    copy_table->time = table->time;   //set time
    if(copy_table == NULL){
        return NULL;
    }
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] == NULL){
            copy_table->object[i] = NULL;  
        }
        else{
            phylib_copy_object(&(copy_table->object[i]), &(table->object[i]));
            //call copy object function for each phylib_object
        }
    }

    return copy_table;
}

//This function will add a phylib_object to the phylib_table
void phylib_add_object( phylib_table *table, phylib_object *object ){
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i]==NULL){          //if spot is NULL/empty
            table->object[i] = object;
            break;
        }
    }
}

//This function will free the memory allocated by table
void phylib_free_table( phylib_table *table ){
    if(table == NULL){
        return;
    }
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] != NULL){
            free(table->object[i]);         //free the object, set to NULL
            table->object[i] = NULL;
        }
    }
    free(table);                        //free the table
}

//This function will perform the subtraction of 2 phylib_coordinates
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    phylib_coord pos;    //create new phylib_coord
    pos.x = c1.x - c2.x;
    pos.y = c1.y - c2.y;
    return pos; 
}

//This function will return the length of a coordinate by pythagorean theorem
double phylib_length( phylib_coord c ){
    double vector = sqrt((c.x * c.x) + (c.y * c.y)); //sqrt (a^2 + b^2)
    return vector;
}

//This function will return the dot product of two coordinates
double phylib_dot_product( phylib_coord a, phylib_coord b ){
    double x = a.x * b.x;   //x value
    double y = a.y * b.y;   //y value
    return (x+y);
}

//This function will return the distance of a rolling ball and another object
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){
    if(obj1->type != PHYLIB_ROLLING_BALL){   //obj1 has to be rolling ball
        return -1.0;
    }
    double distance;
    if(obj2->type == PHYLIB_STILL_BALL){  //if obj2 still ball
        phylib_coord coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
        distance = phylib_length(coord) - PHYLIB_BALL_DIAMETER;

    }else if(obj2->type == PHYLIB_ROLLING_BALL){  //if obj2 rolling ball
        phylib_coord coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
        distance = phylib_length(coord) - PHYLIB_BALL_DIAMETER;
    
    }else if(obj2->type == PHYLIB_HOLE){    //if obj2 is a hole
        phylib_coord coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
        distance = phylib_length(coord) - PHYLIB_HOLE_RADIUS;
    
    }else if(obj2->type == PHYLIB_HCUSHION ){   //if obj2 is a hCushion
        distance = ((obj1->obj.rolling_ball.pos.y) - obj2->obj.hcushion.y);
        distance = fabs(distance);              //absolute value
        distance = distance -PHYLIB_BALL_RADIUS;
   
    }else if(obj2->type == PHYLIB_VCUSHION){    //if obj2 is vCushion
        distance = ((obj1->obj.rolling_ball.pos.x) - obj2->obj.vcushion.x);
        distance = fabs(distance) - PHYLIB_BALL_RADIUS;

    }else {
        return -1.0;   //if not a valid type, return -1.0
    }
    return distance;   //return the distance calculated
}

//This function will roll a rolling ball for a certain period of time
void phylib_roll( phylib_object *new, phylib_object *old, double time ){

    if(new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL){
        //calculate the position
        new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x*time) + 
        (0.5 * old->obj.rolling_ball.acc.x * (time*time));
        new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y*time) +
        (0.5 * old->obj.rolling_ball.acc.y * (time*time));

        //calculate the velocity
        new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
        new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);
    
        //If velocity changed signs, velocity and acceleration is set to 0
        if((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0.0){
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;
        }
        if((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0.0){
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;
        }
    }
}

//This function will check if any rolling ball has stopped moving 
unsigned char phylib_stopped( phylib_object *object ){
    if(object->type == PHYLIB_ROLLING_BALL){
        double speed = phylib_length(object->obj.rolling_ball.vel);  //get speed of ball
        if(speed < PHYLIB_VEL_EPSILON){
            object->type = PHYLIB_STILL_BALL;   //convert type
            object->obj.still_ball.number = object->obj.rolling_ball.number;  //set number
            object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;    //set position
            object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
    
            return 1;   //return 1 for converted
        }
    }
    return 0;   //return 0 for not converted
}

//This is a helper function for case 5 of bounce, when it is rolling ball
void bounce_helper(phylib_object **a, phylib_object **b){
    //calculate the normal vector
    phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
    phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
    phylib_coord n;
    n.x = r_ab.x / fabs(phylib_length(r_ab));
    n.y = r_ab.y / fabs(phylib_length(r_ab));
    double v_rel_n = phylib_dot_product(v_rel, n);

    //set the velocity
    (*a)->obj.rolling_ball.vel.x -= (v_rel_n * n.x);
    (*a)->obj.rolling_ball.vel.y -= (v_rel_n * n.y);

    (*b)->obj.rolling_ball.vel.x += (v_rel_n * n.x);
    (*b)->obj.rolling_ball.vel.y += (v_rel_n * n.y);

    //calculate speed of the balls
    double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
    double speed_b = phylib_length((*b)->obj.rolling_ball.vel);
    
    if(speed_a > PHYLIB_VEL_EPSILON){
        (*a)->obj.rolling_ball.acc.x = ((*a)->obj.rolling_ball.vel.x * -1.0) / (speed_a) * PHYLIB_DRAG;
        (*a)->obj.rolling_ball.acc.y = ((*a)->obj.rolling_ball.vel.y * -1.0) / (speed_a) * PHYLIB_DRAG;
    }

    if(speed_b > PHYLIB_VEL_EPSILON){
        (*b)->obj.rolling_ball.acc.x = ((*b)->obj.rolling_ball.vel.x * -1.0) / (speed_b) * PHYLIB_DRAG;
        (*b)->obj.rolling_ball.acc.y = ((*b)->obj.rolling_ball.vel.y * -1.0) / (speed_b) * PHYLIB_DRAG;
    }
}

//This function will bounce two objects once they have collided
void phylib_bounce( phylib_object **a, phylib_object **b ){
    if((*b)->type == PHYLIB_HCUSHION){   //if b is hCushion
        //calculate new velocity and acceleration
        (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * -1.0;
        (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * -1.0;

    }else if((*b)->type == PHYLIB_VCUSHION){   //if b is vCushion
        //calculate new velocity and acceleration
        (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * -1.0;
        (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * -1.0;

    }else if((*b)->type == PHYLIB_HOLE){    //if b is a hole
        free(*a);                       //free a since it has fallen in hole
        *a = NULL;                      //set to NULL
        
    }else if((*b)->type == PHYLIB_STILL_BALL){   //if b is still ball
        (*b)->type = PHYLIB_ROLLING_BALL;        //b converts to a rolling ball
        
        //initialize velocity and acceleration to 0
        (*b)->obj.rolling_ball.vel.x = 0.0;
        (*b)->obj.rolling_ball.vel.y = 0.0;
        (*b)->obj.rolling_ball.acc.x = 0.0;
        (*b)->obj.rolling_ball.acc.y = 0.0;

        bounce_helper(a,b);    //go to case 5, b is rolling ball
    }

    else if((*b)->type == PHYLIB_ROLLING_BALL){   //if b is rolling ball
        bounce_helper(a,b);    //go to helper function
    }
}

//This function will return the number of total rolling balls on table
unsigned char phylib_rolling( phylib_table *t ){
    int total = 0;
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){    //loop through table objects
        if(t->object[i] != NULL){
            if(t->object[i]->type == PHYLIB_ROLLING_BALL){  //if type is rolling ball
                total++;                                    //increment
            }
        }
    }
    return total;
}

/*This function will loop through gameplay, until a collision
occurs, max_time is reached, or a rolling ball has
stopped
*/
phylib_table *phylib_segment( phylib_table *table ){
    double num = 1.0;
    double i = PHYLIB_SIM_RATE;  //set loop counter to sim rate
    phylib_table * copy;

    if(phylib_rolling(table)==0){  //if no rolling balls return null
        return NULL;
    }

    phylib_table * new_table = phylib_copy_table(table);  //get copy of table
    while(i < PHYLIB_MAX_TIME){
        new_table->time += PHYLIB_SIM_RATE;   //time increase by sim rate
    
        for(int j=0; j<PHYLIB_MAX_OBJECTS; j++){
            if((new_table->object[j] != NULL) && (new_table->object[j]->type == PHYLIB_ROLLING_BALL)){
                phylib_roll(new_table->object[j], table->object[j], i);  //roll the ball
            }
        }
        for(int l = 10; l<PHYLIB_MAX_OBJECTS; l++){
            for(int k=0; k<PHYLIB_MAX_OBJECTS; k++){
                if(((new_table->object[l] != NULL) && (new_table->object[k] != NULL)) && (k != l)){
                    num = phylib_distance(new_table->object[l], new_table->object[k]);

                        //check for collisions
                    if((num != -1.0) && (num <= 0.0)){
                        //    printf("\n %f goes in here diatnce collidded in here k%d j%d wadeakhkaw\n", num, k, j);
                        phylib_bounce(&(new_table->object[l]), &(new_table->object[k]));  //call bounce
                        copy = phylib_copy_table(new_table);  //copy new table
                        phylib_free_table(new_table);         //free new table
                        return copy;                          //return copy
                    }
                }
            }
                //Check if rolling ball has stopped
            if((new_table->object[l] != NULL) && phylib_stopped(new_table->object[l]) == 1){
                copy = phylib_copy_table(new_table);        //get copy of new table
                phylib_free_table(new_table);               //free new table
                return copy; 
            }
        }
        i = i+PHYLIB_SIM_RATE;    //increment loop time counter
    }
  
    copy = phylib_copy_table(new_table);  //copy new table
    phylib_free_table(new_table);         //free new table
    return copy;                          //return copy
}


char *phylib_object_string( phylib_object *object ){
    static char string[80];
    if (object==NULL){
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
            break;
    }
    return string;
}

