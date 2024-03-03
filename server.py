import sys;
import cgi;
import os;
import math;
import Physics;
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;

class Myserver (BaseHTTPRequestHandler):
    def do_GET(self):
        parsed  = urlparse( self.path );
        path = parsed.path

        # check if the web-pages matches the list
        if path in [ '/shoot.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();
            

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );

            fp.close();

        elif path.startswith('/table-') and path.endswith('.svg'):
            tableNum = path.split('-')[1].split('.')[0]
            filePath = f'./table-{tableNum}.svg'
            if os.path.isfile(filePath):
                #file exists
                 # get the form data and turn it into a dictionary
                form_data = dict( parse_qsl( parsed.query ) );
            # retreive the HTML file & insert form data into the HTML file
                fp = open( '.'+path );
                content = fp.read() % form_data;
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.send_header( "Content-length", len( content ) );
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
                fp.fclose()

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

    def do_POST(self):
        # handle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        # get data send
        if parsed.path in [ '/display.html' ]:
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               }
                                   );
            # delete all svg files
            files = os.listdir()
            for fileName in files:
                if fileName.endswith(".svg"):
                    os.remove(fileName)

            rb_dx = float(form["rb_dx"].value)
            rb_dy = float(form["rb_dy"].value)
            speed = math.sqrt((rb_dx * rb_dx) + (rb_dy * rb_dy))
            if(speed > 0.01):
                rb_accx = (rb_dx * -1.0) / speed * 150.0
                rb_accy = (rb_dy * -1.0) / speed * 150.0
            
            else:
                rb_accx = 0.0
                rb_accy = 0.0
            # make a table given values inputted
            table = Physics.Table()
            x = float(form["sb_x"].value)
            y = float(form["sb_y"].value)
            pos = Physics.Coordinate(x, y)
    
            sb_number = int(form["sb_number"].value)
            sb = Physics.StillBall(sb_number, pos)

            pos2 = Physics.Coordinate(float(form["rb_x"].value), float(form["rb_y"].value))
            vel = Physics.Coordinate(rb_dx, rb_dy)
            acc = Physics.Coordinate(rb_accx, rb_accy)
            rb = Physics.RollingBall(0, pos2, vel, acc)
            table += sb
            table += rb
            n=0
            # html string describing  the original ball
            html_content = f"""<html><body><h1> <a href = "/shoot.html">Back</a></h1>
            <p>Original ball starts at posX: {float(form["rb_x"].value)}, posY: {float(form["rb_y"].value)}</p>
            <p>Velocity X: {rb_dx}, velocity Y: {rb_dy}</p>
            <p>Still ball at posX: {x}, posY: {y}</p><br><br>"""

            # html get all svgs produced
            while (table != None):
                filename = "table-%s.svg" %n
                file_open = open(filename, "w")
                file_open.write(table.svg())
             #   print("in whikeloop")
                table = table.segment()
                html_content +=  f"""<img src="table-{n}.svg"></img><br><br>"""
                file_open.close()
                n+=1
            html_content += """</p></body></html>"""
            
        #    print("naur ",html_content)
        # generate the headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header( "Content-length", len( html_content ) );
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))
            


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), Myserver );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();

        