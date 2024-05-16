import sys
import cgi
import os
import math
import Physics
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl, parse_qs

class Myserver(BaseHTTPRequestHandler):


    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path in ['/poolgame.html']:
            fp = open('.' + self.path)
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
            fp.close()

        elif path in ['/gamepool.html']:
            print("*********went in here")

        elif path == '/jquery.js':
            filePath = './jquery.js'
            if os.path.isfile(filePath):
                fp = open(filePath, 'r')
                content = fp.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/javascript')
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
                fp.close()

        elif path in ['/original.svg']:
            filePath = './original.svg'
            if os.path.isfile(filePath):
                fp = open(filePath, 'r')
                content = fp.read()
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
                fp.close()
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

    def do_POST(self):
        global player1, player2, name, velocity, mouseX, mouseY, table
        parsed = urlparse(self.path)
        if parsed.path in ['/gamepool.html']:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE':
                         self.headers['Content-Type']})
            player1 = form["p1Name"].value
            player2 = form["p2Name"].value
            name = form["gameName"].value
            print("*******ghghhgg********")
            print(player1, player2, name)
            table = Physics.Table()
            table = table.initialBoard()
          #  db = Physics.Database()
          #  game = Physics.Game(gameName=name, player1Name=player1, player2Name=player2)
          #  print("stughhghghghghghghgff");
          #  game.shoot(name, player1, table, 400, 500)
            playerTurn = Physics.Table()
            playerTurn = playerTurn.getPlayerTurn()
            if (playerTurn == 1):
                playerTurn = player1
            else:
                playerTurn = player2

            html_content = f"""<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">    
<meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body><h1> <a href="http://localhost:55060/poolgame.html">Back</a></h1>
            <p>Take a Shot Player {playerTurn} </p><br><br><div style="text-align: center;"><!--?xml version="1.0" encoding="UTF-8" standalone="no"?-->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
<svg width="280" height="550" viewBox="-25 -25 1400 2750" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<rect id="poolTable" width="1350" height="2700" x="0" y="0" fill="#C0D0C0"></rect> <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen"></rect>
 <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen"></rect>
 <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen"></rect>
 <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen"></rect>
 <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen"></rect>
 <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen"></rect>
 <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen"></rect>
 <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen"></rect>
 <circle cx="0.0" cy="0.0" r="114.0" fill="black"></circle>
 <circle cx="0.0" cy="1350.0" r="114.0" fill="black"></circle>
 <circle cx="0.0" cy="2700.0" r="114.0" fill="black"></circle>
 <circle cx="1350.0" cy="0.0" r="114.0" fill="black"></circle>
 <circle cx="1350.0" cy="1350.0" r="114.0" fill="black"></circle>
 <circle cx="1350.0" cy="2700.0" r="114.0" fill="black"></circle>
 <circle cx="675.0" cy="675.0" r="28.5" fill="YELLOW"></circle>
 <circle cx="644.0913812015212" cy="621.1849639481128" r="28.5" fill="BLUE"></circle>
 <circle cx="706.5472335871077" cy="621.1616446578503" r="28.5" fill="RED"></circle>
 <circle cx="613" cy="567" r="28.5" fill = "PURPLE"></circle>
 <circle cx="675" cy="567" r="28.5" fill = "BLACK"></circle>
 <circle cx="737" cy="567" r="28.5" fill = "ORANGE"></circle>
 <circle cx="582" cy="513" r="28.5" fill = "GREEN"></circle>
 <circle cx="644" cy="513" r="28.5" fill = "BROWN"></circle>
 <circle cx="706" cy="513" r="28.5" fill = "LIGHTYELLOW"></circle>
 <circle cx="768" cy="513" r="28.5" fill = "LIGHTBLUE"></circle>
 <circle cx="551" cy="459" r="28.5" fill = "MEDIUMPURPLE"></circle>
 <circle cx="613" cy="459" r="28.5" fill = "LIGHTSALMON"></circle>
 <circle cx="675" cy="459" r="28.5" fill = "LIGHTGREEN"></circle>
 <circle cx="737" cy="459" r="28.5" fill = "SANDYBROWN"></circle>
 <circle cx="799" cy="459" r="28.5" fill = "PINK"></circle>
 <circle id="cue" cx="672.2496051731046" cy="2025.0" r="28.5" fill="WHITE"></circle>
 <line id="cueLine" stroke="black" stroke-width="10" x1="0" y1="0" x2="0" y2="0"></line>
 </svg><div id="velocity">Velocity X: -352.30, Velocity Y: -1614.06</div>
 <div id="svgContainer"></div>
 <script
        src="jquery.js" />
 </script></div><br></body></html>"""

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header("Content-length", len(html_content))
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))
        # if parsed.path in ['/gamepool.html']:
        elif parsed.path in ['/gamepoolvel.html']:
         #   form = cgi.FieldStorage( fp=self.rfile, headers=self.headers,
         #       environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': 
         #           self.headers['Content-Type'], });
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            mouseX = float(form_data['mouseX'][0])
            mouseY = float(form_data['mouseY'][0])
            velocity = float(form_data['length'][0])
            game = Physics.Game(gameName=name, player1Name=player1, player2Name=player2)
         #   print("stughhghghghghghghgff");
            svg_data = game.shoot(name, player1, table, mouseX, mouseY)
            
            
            print("Received data:", velocity)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header("Content-length", len(svg_data))
            self.end_headers()
            self.wfile.write(bytes(svg_data, "utf-8"))

        elif parsed.path in ['/animate.html']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
          #  print("rj ejrhkj er ", form_data)
            svg_data = form_data['svgData'][0]
          #  print(svg_data)
          #  svg_data = (form_data['mouseX'][0])
            print("777777777777777")
            print(svg_data)
            print("111111111111")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(svg_data))
            self.end_headers()
            self.wfile.write(bytes(svg_data, "utf-8"))

        elif parsed.path in ['/api/get_svgs']:  # Handle POST request for SVGs
            print("went in here so liek now whatatatta")
            svg_data = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";  # Initialize an empty string to store SVG data
            table = Physics.Table()
            table = table.initialBoard()
            db = Physics.Database()
            print(name, player1, player2)
            game = Physics.Game(gameName=name, player1Name=player1, player2Name=player2)
            print("stughhghghghghghghgff");
            svg_data = game.shoot(name, player1, table, mouseX, mouseY)
            print(svg_data)
          #  for i in range(3):  # Generate 10 SVGs
          #      table = db.readTable(i);
                # Replace this with logic to get SVG data from your database or elsewhere
          #      svg_data += table.svg()
          #      svg_data += """\n"""
          #  svg_data += """</svg><br><br>"""
        #  html_content += f"""<script src="jquery.js" /></script>"""
        #  html_content += """</svg></body></html>"""
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(svg_data))
            self.end_headers()
            self.wfile.write(bytes(svg_data, "utf-8"))

    def extract_velocity_from_html(self, html_content):
        start_index = html_content.find('<div id="velocity">')
        end_index = html_content.find('</div>', start_index)
        if start_index != -1 and end_index != -1:
            div_content = html_content[start_index:end_index]
            start_velocity_index = div_content.find('Velocity X: ') + len('Velocity X: ')
            end_velocity_index = div_content.find(',', start_velocity_index)
            velocity = div_content[start_velocity_index:end_velocity_index]
            return velocity.strip()
        else:
            return None

if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), Myserver );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
