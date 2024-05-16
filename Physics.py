import phylib;
import random;
import os;
import sqlite3;
import math;

#import subprocess

#ffmpeg_cmd = ffmpeg_cmd = [
#    'ffmpeg', '-framerate', '100', '-i', './tables/table%04d.svg',
#    '-vf', '"crop=687.5:1362.5:12.5:12.5"', '-c:v', 'libvpx-vp9',
#    '-pix_fmt', 'yuv420p', '-s', '540x1080', '-b:v', '2M',
#    '-crf', '10', '-c:a', 'libvorbis', 'output.webm'
#]

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;

# add more here
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_RATE = 0.01

playerCur = -1

HEADER = """<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">    
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  </head>
                  <body><h1> <a href="http://localhost:55060/poolgame.html">Back</a></h1>
                            <p>Was NotGudd</p><br><br><div style="text-align: center;"><?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
    <svg width="280" height="550" viewBox="-25 -25 1400 2750" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<rect id="poolTable" width="1350" height="2700" x="0" y="0" fill="#C0D0C0"></rect>""";

FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """
    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """
        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    # add an svg method here returns svg string
    def get_stillBall(self):
        if (self.obj.still_ball.number == 0):
            return f"""<circle id="cue" cx="{self.obj.still_ball.pos.x}" cy="{self.obj.still_ball.pos.y}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.obj.still_ball.number]}" />\n"""
       # return """ <circle cx=,self.obj.still_ball.pos.x, cy="%d" r="%d" fill="%s" />\n"""
        return f""" <circle cx="{self.obj.still_ball.pos.x}" cy="{self.obj.still_ball.pos.y}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.obj.still_ball.number]}" />\n"""

################################################################################
class RollingBall( phylib.phylib_object ):
    def __init__(self, number, pos, vel, acc):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_ROLLING_BALL,
                                number, pos, vel, acc, 0.0, 0.0)
        self.__class__ = RollingBall
        
    # returns svg string
    def get_rollingBall(self):
        return f""" <circle cx="{self.obj.rolling_ball.pos.x}" cy="{self.obj.rolling_ball.pos.y}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.obj.rolling_ball.number]}" />\n"""

class Hole( phylib.phylib_object ):
    def __init__(self, pos):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HOLE, None, pos, 
                                None, None, None, None)
        self.__class__ = Hole

    # returns svg string
    def get_hole(self):
        return f""" <circle cx="{self.obj.hole.pos.x}" cy="{self.obj.hole.pos.y}" r="{HOLE_RADIUS}" fill="black" />\n"""

class HCushion( phylib.phylib_object ):
    def __init__(self, y):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HCUSHION, None, 
                                None, None, None, None, y)
        self.__class__ = HCushion

    # returns svg string
    def get_hcushion(self):
        return f""" <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen"></rect>\n <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" ></rect>\n"""

class VCushion( phylib.phylib_object ):
    def __init__(self, x):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_VCUSHION, None,
                                None, None, None, x, None)
        self.__class__ = VCushion

    # returns svg string
    def get_vcushion(self):
        return """ <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" ></rect>\n <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" ></rect>\n"""

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here, returns svg string
    def svg(self):
        sentence = ""
        sentence += HEADER
        for obj in self:
            if (isinstance (obj, StillBall)):
                sentence += obj.get_stillBall()
            elif (isinstance (obj, RollingBall)):
                sentence += obj.get_rollingBall()
            elif (isinstance (obj, Hole)):
                sentence += obj.get_hole()
            elif (isinstance (obj, VCushion)):
                sentence += obj.get_vcushion()
            #    print("jikik")
            elif (isinstance (obj, HCushion)):
                sentence += obj.get_hcushion()    
            #   print("hello") 
     #   sentence += StillBall.get_stillBall(StillBall)
      #  sentence += RollingBall.rollingBall( self )
        sentence += FOOTER
        return sentence

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
            # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                    Coordinate(0,0),
                    Coordinate(0,0),
                    Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                        Coordinate( ball.obj.still_ball.pos.x,
                        ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

#this method will return where cue ball is found on table
    def cueBall(self):
     #   print("3")
        for ball in self:
            if(isinstance(ball, StillBall)): # or (isinstance(obj, RollingBall))):
              #  print("went in still ball")
                if(ball.obj.still_ball.number == 0):
                  #  print("in cur ball ", self)
              #      print("went in still = 0")
                    output = ball
                  #  return ball
            if(isinstance(ball, RollingBall)):
               # print("went in rolling ball")
                if(ball.obj.rolling_ball.number == 0):
                #    print("in roll - 0")
                    output = ball
                  #  return ball
        return output

    def initialBoard(self):
        self.table = Table()
        pos = Coordinate(TABLE_WIDTH / 2.0,
                    TABLE_WIDTH / 2.0)
        sb = StillBall(1, pos)
        self.table += sb
        pos = Coordinate(
                    TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0,
                    TABLE_WIDTH/2.0 - 
                    math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0));
        sb = StillBall(2, pos)
        self.table += sb
        pos = Coordinate(
                    TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0,
                    TABLE_WIDTH/2.0 - 
                    math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0));
        sb = StillBall( 3, pos );
        self.table += sb;
        pos = Coordinate( TABLE_WIDTH/2.0,
                                TABLE_LENGTH - TABLE_WIDTH/2.0 );
        vel = Coordinate( 0.0, 0.0 );
        acc = Coordinate( 0.0, 0.0 );
        rb  = RollingBall( 0, pos, vel, acc );
        self.table += rb;
        pos = Coordinate(613, 567)
        sb = StillBall(4, pos);
        self.table +=sb
        pos = Coordinate(675,567)
        sb = StillBall(8, pos);
        self.table +=sb
        pos = Coordinate(737,567)
        sb = StillBall(5, pos);
        self.table +=sb
        pos = Coordinate(582,513)
        sb = StillBall(6, pos);
        self.table +=sb
        pos = Coordinate(644,513)
        sb = StillBall(7, pos);
        self.table +=sb
        pos = Coordinate(706,513)
        sb = StillBall(9, pos);
        self.table +=sb
        pos = Coordinate(768,513)
        sb = StillBall(10, pos);
        self.table +=sb
        pos = Coordinate(551,459)
        sb = StillBall(12, pos);
        self.table +=sb
        pos = Coordinate(613,459)
        sb = StillBall(13, pos);
        self.table +=sb
        pos = Coordinate(675,459)
        sb = StillBall(14, pos);
        self.table +=sb
        pos = Coordinate(737,459)
        sb = StillBall(15, pos);
        self.table +=sb
        pos = Coordinate(799,459)
        sb = StillBall(11, pos);
        self.table +=sb
     #   Game.shoot(table)
        return self.table;

    def getPlayerTurn(self):
        num = random.randint(1,2)
        self.setCurrentPlayer(num)
        playerCur = num
        return (num)
    
    def getPlayer(self, num):
        return(playerCur)

    def setCurrentPlayer(self, num):
        playerCur = num

class Database():

    def __init__(self, reset=False):

        # for testing only; remove this for real usage
        if reset:
            if os.path.exists( 'phylib.db' ):
                os.remove( 'phylib.db' );
        self.conn = sqlite3.connect( 'phylib.db' );
        self.cur = self.conn.cursor();
        #self. = cur

# if os.path.exists( 'a3.db' ):
#    os.remove( 'a3.db' );

# create database file if it doesn't exist and connect to it
#conn = sqlite3.connect( 'a3.db' );
   # def table_does_not_exists(name):
    #    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}';")
    #    result = cur.fetchone()
    #    if result:
    #        return False
    #    return True 

    def createDB( self ):
        #create tables if not found in database
        #data = self.cur.execute( """SELECT * FROM Ball;""" )
        #if data:
        #self.conn = sqlite3.connect( 'phylib.db' );
        #self.cur = self.conn.cursor();
        listOfTables = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='Ball'; """).fetchall()
        if listOfTables == []:
          #  print("in here")
      #  if table_does_not_exists(Ball, self):
            self.cur.execute( """CREATE TABLE Ball ( 
             		BALLID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             		BALLNO  INTEGER NOT NULL,
             		XPOS    FLOAT NOT NULL,
             		YPOS    FLOAT NOT NULL,
                    XVEL    FLOAT,
                    YVEL    FLOAT );""" );

       # if table_does_not_exists(TTable, self):
       # data = cur.execute( """SELECT * FROM TTable;""" )
       # if data:
        listOfTables = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='TTable'; """).fetchall()
        if listOfTables == []:
            self.cur.execute( """CREATE TABLE TTable ( 
                    TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    TIME    FLOAT NOT NULL);""" );

       # if table_does_not_exists(BallTable, self):
     #   data = cur.execute( """SELECT * FROM BallTable;""" )
     #   if data:
        listOfTables = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='BallTable'; """).fetchall()
        if listOfTables == []:
            self.cur.execute( """CREATE TABLE BallTable (
                    BALLID  INTEGER NOT NULL,
                    TABLEID INTEGER NOT NULL,
                    FOREIGN KEY (BALLID) REFERENCES Ball,
                    FOREIGN KEY (TABLEID) REFERENCES TTable  );""" );

       # if table_does_not_exists(Shot, self):
      #  data = cur.execute( """SELECT * FROM Shot;""" )
      #  if data:
        listOfTables = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='Shot'; """).fetchall()
        if listOfTables == []:
            self.cur.execute( """CREATE TABLE Shot ( 
             		SHOTID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             		PLAYERID    INTEGER NOT NULL,
             		GAMEID      INTEGER NOT NULL,
                    FOREIGN KEY (PLAYERID) REFERENCES Player,
                    FOREIGN KEY (GAMEID) REFERENCES Game  );""" );

        #if table_does_not_exists(TableShot, self):
        #data = cur.execute( """SELECT * FROM TableShot;""" )
        #if data:
        listOfTables = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='TableShot'; """).fetchall()
        if listOfTables == []:
            self.cur.execute( """CREATE TABLE TableShot ( 
             		TABLEID INTEGER NOT NULL,
             		SHOTID  INTEGER NOT NULL,
                    FOREIGN KEY (TABLEID) REFERENCES TTable,
                    FOREIGN KEY (SHOTID) REFERENCES Shot);""" );

        #if table_does_not_exists(Game, self):
       # data = cur.execute( """SELECT * FROM Game;""" )
       # if data:
        listOfTables = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='Game'; """).fetchall()
        if listOfTables == []:
            self.cur.execute( """CREATE TABLE Game ( 
                    GAMEID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    GAMENAME    VARCHAR(64) NOT NULL);""" );

        #if table_does_not_exists(Player, self):
     #   data = cur.execute( """SELECT * FROM Player;""" )
     #   if data:
        listOfTables = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='Player'; """).fetchall()
        if listOfTables == []:
            self.cur.execute( """CREATE TABLE Player ( 
                    PLAYERID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    GAMEID      FLOAT NOT NULL,
                    PLAYERNAME  VARCHAR(64) NOT NULL,
                    FOREIGN KEY (GAMEID) REFERENCES Game );""" );
        #cur.close();
        #conn.commit();
        #conn.close();
        self.cur.close();
        self.conn.commit();
         #self.close()

    def readTable(self, tableID):
       #given a tableID return a table that represents table in database
        # self.conn = sqlite3.connect( 'phylib.db' );
        self.cur = self.conn.cursor();
    #    print(tableID)

      #  self.table = Table()
        table = Table()
        time = self.cur.execute(f"SELECT TIME  FROM TTable WHERE TTable.TABLEID = {tableID+1}")
        time = time.fetchone()
        if time is not None:
         #   self.table.time = time[0]
            table.time = time[0]
         #   print("This is time ")
         #   print(time)

        self.cur.execute(f"""SELECT * 
            FROM Ball
            JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            WHERE BallTable.TABLEID = {tableID+1}""")
    
        rows = self.cur.fetchall()
     #   print(rows)
        # rowe = self.cur.fetchone()
        # print(rowe)
        if not rows:
          #  print("No rows re found")
            return None;

        for row in rows:
         #   print("At least rows re found")
         #   print(row)
            #get attributes of the ball
            ballId = row[0]
            ballNum = row[1]
            posx = row[2]
            posy = row[3]
            xvel = row[4]
            yvel = row[5]

            #calculate acceleration again
            if (xvel is not None) and (yvel is not None):
                speed = math.sqrt((xvel * xvel) + (yvel * yvel))
                if(speed > 0.01):
                    accx = (xvel * -1.0) / speed * 150.0
                    accy = (yvel * -1.0) / speed * 150.0
                else:
                    accx = 0.0
                    accy = 0.0

                rb = RollingBall(ballNum, Coordinate(posx, posy), Coordinate(xvel, yvel), Coordinate(accx, accy))
             #   self.table += rb
             #   print("Went n here ************")
                table += rb
             #   print("This also soemth")
            
            else:
                sb = StillBall(ballNum, Coordinate(posx, posy))
               # self.table += sb
             #   print("Went iin here ************")
                table += sb
            self.conn.commit();
            self.cur.close();

    #    time = self.cur.execute(f"SELECT TIME  FROM TTable WHERE TTable.TABLEID = {tableID+1}")
    #    time = time.fetchone()
    #    if time is not None:
    #     #   self.table.time = time[0]
    #        table.time = time[0]
    #        print("This is time ")
    #        print(time)

      
       # self.conn.commit();
     #   print("is this wrkingngng")
     #   print(table.__str__())
      #  return self.table
        return table

    def getTableId(self):
        self.cur = self.conn.cursor()
        tId = self.cur.execute("""SELECT * FROM TTABLLE""")
        tId = self.cur.lastrowid
        return tId

    def writeTable(self, table):
        #given a table, this will write to database 

        # self.conn = sqlite3.connect( 'phylib.db' );
        self.cur = self.conn.cursor();

        tId = self.cur.execute(f"""INSERT INTO TTable (TIME) VALUES ({table.time});""")
        tId = self.cur.lastrowid
       # print(table.time)


        for obj in table:
            if (isinstance (obj, StillBall)):
      #          print("something")
                
            #    print("ball.vel.x:", obj.obj.still_ball.vel.x)
            #    print("ball.vel.y:",obj.obj.still_ball.vel.y)
                self.cur.execute(f"""INSERT INTO Ball (BALLNO, XPOS, YPOS)
                    VALUES ({obj.obj.still_ball.number}, {obj.obj.still_ball.pos.x}, {obj.obj.still_ball.pos.y});""")
            #     bId = self.cur.execute(f"""SELECT BALLID FROM Ball WHERE Ball.BALLNO = {obj.obj.still_ball.number};""")
            #     bId = bId.fetchone()[0]
            #     print(bId)
           
            #   #  tId = self.cur.execute(f"""INSERT INTO TTable (TIME) VALUES ({table.time});""")
            #     tId = self.cur.execute(f"""SELECT TABLEID FROM TTable WHERE TTable.TIME = {table.time}; """)
            #     tId = tId.fetchone()[0]
            #     print("Table if")
            #     print(tId)
               # print(tId)
                self.cur.execute(f"""INSERT INTO BallTable(BALLID, TABLEID) SELECT (SELECT MAX(BALLID) FROM Ball), (SELECT MAX(TABLEID) FROM TTable)  ;""")
               # self.cur.execute(f"""INSERT INTO BallTable (BALLID, TABLEID) VALUES ({bId}, {tId}); """)
            #    self.cur.execute()
            #    tId = self.cur.execute(f"""SELECT TABLEID FROM TTable WHERE TTable.TIME = {table.time}; """)
            #    tId = tId.fetchone()[0]
            #    print(tId)
            #    self.cur.execute(f"""INSERT INTO BallTable (BALLID, TABLEID) VALUES ({bId}, {tId}); """)


            elif (isinstance (obj, RollingBall)):
       #         print("something else")
            #   print(obj.obj.rolling_ball.pos.x)
            #    print(tId)
                self.cur.execute(f"""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES ({obj.obj.rolling_ball.number}, {obj.obj.rolling_ball.pos.x}, {obj.obj.rolling_ball.pos.y}, {obj.obj.rolling_ball.vel.x}, {obj.obj.rolling_ball.vel.y});""")
                self.cur.execute(f"""INSERT INTO BallTable(BALLID, TABLEID) SELECT (SELECT MAX(BALLID) FROM Ball), (SELECT MAX(TABLEID) FROM TTable)  ;""")
             #   ex = self.cur.execute("""SELECT * FROM Ball""")
              #  print(ex.fetchall())
            #     bId = self.cur.execute(f"""SELECT BALLID FROM Ball 
            #     WHERE Ball.BALLNO = {obj.obj.rolling_ball.number};""")
            #     bId = bId.fetchone()[0]
            #     print(bId)

            # #    tId = self.cur.execute(f"""INSERT INTO TTable (TIME) VALUES ({table.time});""")
            #     tId = self.cur.execute(f"""SELECT TABLEID FROM TTable WHERE TTable.TIME = {table.time}; """)
            #     tId = tId.fetchone()[0]
            #     print("Table if")
            #     print(tId)
            #     self.cur.execute(f"""INSERT INTO BallTable (BALLID, TABLEID) VALUES ({bId}, {tId}); """)
            #     #tId = self.cur.execute(f"""SELECT TABLEID FROM TTable WHERE TTable.TIME = {table.time}; """)
               # if not 
                #tId = tId.fetchone()[0]
                #print(tId)
                #self.cur.execute(f"""INSERT INTO BallTable (BALLID, TABLEID) VALUES ({bId}, {tId}); """)


       # self.cur.execute(f"INSERT INTO BallTable (BALLID)
       #                     VALUES ({table.})")
      #  print("3")
      #  print(table.__str__())
       # ex = self.cur.execute("""SELECT * FROM Ball""")
       # print(ex.fetchall())
       # self.cur.execute(f"""INSERT INTO TTable (TIME) VALUES ({table.time});""")
        #tId = self.cur.execute(f"""SELECT TABLEID FROM TTable WHERE TTable.TIME = {table.time}; """)
       # tId = tId.fetchone()[0]
       #print(tId)
       # self.cur.execute(f"""INSERT INTO BallTable (BALLID, TABLEID) VALUES ({bId}, {tId}); """)


       # data = self.cur.execute("""SELECT * FROM  BallTable""")
        # data = self.cur.fetchall
       #for d in data:
       # print("bruhe soemthing pls")
       # print(data.fetchall())

      #  self.close()
        
       
      #  return self.cur.lastrowid
      #  tId = self.cur.execute(f"""SELECT TABLEID FROM TTable WHERE TTable.TIME = {table.time}; """)
      #  tId = tId.fetchone()[0]
        self.cur.close();
        self.conn.commit();
        return (tId-1)
        

    def close(self):
        #this will close the connection to database
        self.conn.close();

    def getGame(self, name, p1, p2):
        #this gets gameName and players name from database
        self.cur = self.conn.cursor();
        game = self.cur.execute(f"""SELECT * 
            FROM Game
            JOIN Player
            WHERE (Game.GAMEID = Player.GAMEID)
            ORDER BY Player.PLAYERID""")
     #   print("in getgame")
     #   print(game.fetchall())
        name = game[1]
        for row in game:
            p1 = row
        #print(game[1])
        #p1 = 
        self.cur.close();
        self.conn.commit();
    
    def setGame(self, name, p1, p2):
    # this will add gameName and player names to database
    #    self.cur.execute(f"""INSERT INTO BallTable(BALLID, TABLEID) SELECT (SELECT MAX(BALLID) FROM Ball), (SELECT MAX(TABLEID) FROM TTable)  ;""")
            
        self.cur = self.conn.cursor();
        self.cur.execute(f"""INSERT INTO Game (GAMENAME)VALUES ("{name}");""")
        self.cur.execute(f""" INSERT INTO Player(PLAYERNAME, GAMEID)
                    VALUES ("{p1}", (SELECT MAX(GAMEID) FROM Game));""")
        self.cur.execute(f""" INSERT INTO Player(PLAYERNAME, GAMEID)
                    VALUES ("{p2}", (SELECT MAX(GAMEID) FROM Game));""")

        data = self.cur.execute("""SELECT * FROM Player""")
      #  print(data.fetchall())

        self.cur.close();
        self.conn.commit();


    def newShot(self, gameName, playerName, table, xvel, yvel ):
        #this will save the shot to Shot
        self.cur = self.conn.cursor();
      #  print(playerName)

        pId = self.cur.execute(f"""SELECT PLAYERID FROM Player 
           WHERE Player.PLAYERNAME = '{playerName}';""").fetchone()[0]
      #  print(pId)
     #   pId = pId.fetchone()

        gId = self.cur.execute(f"""SELECT GAMEID FROM Game 
            WHERE Game.GAMENAME = '{gameName}';""").fetchone()[0]
     #   gId = gId.fetchone()
     #   print(pId)
     #   print(gId)

        #self.cur.execute(f"""INSERT INTO BallTable(BALLID, TABLEID) SELECT (SELECT MAX(BALLID) FROM Ball), (SELECT MAX(TABLEID) FROM TTable)  ;""")
            

        self.cur.execute(f"""INSERT INTO Shot(PLAYERID, GAMEID) VALUES({pId}, {gId});""")
        
        data = self.cur.execute(f"""SELECT MAX(SHOTID) FROM Shot;""")
        data = data.fetchone()
      #  print("this is shotif ", data)
        self.cur.close();
        self.conn.commit();
        return data

    def tableGame(self, tableID):
        #this will save to TableShot
        self.cur = self.conn.cursor();
        shotID = self.cur.execute(f"""SELECT MAX(SHOTID) FROM Shot""").fetchone()[0]
     #   print("tid and shotid is ", tableID, shotID)
        self.cur.execute(f"""INSERT INTO TableShot (TABLEID, SHOTID) 
                VALUES ({tableID}, {shotID});""")

        self.cur.close();
        self.conn.commit();


        

class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
      #  print("1")
        self.db = Database()
        self.db.createDB()

        if gameID: #check which constructor
        #    print("In first cinstructor")
            if (gameName or player1Name or player2Name):
                raise TypeError("Not valid parameters")
            else:
                gameID += 1
                self.gameID = gameID
                self.gameName = gameName
                self.player1Name = player1Name
                self.player2Name = player2Name
             #   self.table = table
                game = self.db.getGame(gameName, player1Name, player2Name)
              #  for row in game:
               #     print(row)

        if not gameID:
       #    print("In second cinstructor")
            if (not gameName or not player1Name or not player2Name):
                raise TypeError("Not valid parameters")
            else:
                game = self.db.setGame(gameName, player1Name, player2Name)

    def shoot( self, gameName, playerName, table, xvel, yvel ):
       # db = Database()
       # self.db.cur = self.db.conn.cursor();
        sId = self.db.newShot(gameName, playerName, table, xvel, yvel)
        
     #   print("before cur ball")
     #   print(table)
        #find the cue ball in table
        cue_ball = table.cueBall()
     #   print("2")
      #  print(table)
        #set cue ball to rolling ball
        xpos = cue_ball.obj.still_ball.pos.x
        ypos = cue_ball.obj.still_ball.pos.y
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL

        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos
        cue_ball.obj.rolling_ball.number = 0
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel
        speed = math.sqrt((xvel * xvel) + (yvel * yvel))
        #calculate acceleration for the 11th time
        if (speed > 0.01):
            cue_ball.obj.rolling_ball.acc.x = (xvel * -1.0)/speed * 150.0
            cue_ball.obj.rolling_ball.acc.y = (yvel * -1.0)/speed * 150.0
        else:
            cue_ball.obj.rolling_ball.acc.x = 0.0
            cue_ball.obj.rolling_ball.acc.y = 0.0

        num= 0
        oldTime = table.time
        newTime = 0.0
        lTime = 0.0
      #  tId = self.db.writeTable(table) #write to database 
      #  sId = self.db.tableGame(tId+1)
        #loop until table is NULL
        svg = ""
        svg = table.svg()
        while (table != None):

            seg = table.segment()
            if (seg is None): #is table empty break from loop
                copytable = table.roll(num)
                copytable.time = table.time + num
                tId = self.db.writeTable(copytable) #write to database 
                sId = self.db.tableGame(tId+1)
                break
            newTime = seg.time #get new time
            loopTime = math.floor((newTime - oldTime) / FRAME_RATE) #find loop int
            for k in range(loopTime): #loop thorugh that
                lTime = k * FRAME_RATE #find lTime
                copytable = table.roll(lTime) #roll
                svg += copytable.svg()
                copytable.time = copytable.time + lTime
                tId = self.db.writeTable(copytable) #write to database 
                sId = self.db.tableGame(tId+1)
          #  tId = self.db.writeTable(table) #write to database 
          #  sId = self.db.tableGame(tId)
       #     table = table.segment()  #call new segment
            table = seg
            oldTime = table.time
          #  print(svg)
        return svg
        


#subprocess.run(ffmpeg_cmd)