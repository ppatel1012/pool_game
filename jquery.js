
document.addEventListener('DOMContentLoaded', function(){
    const svg = document.getElementById('poolTable');
    let currenttime = 0.0;
        
      //  const canvas = document.getElementById('poolTable');
    const cueBall = document.getElementById('cue');
    const cueLine = document.getElementById('cueLine');
     //  const ctx = canvas.getContext('2d');
    const velocityDisplay = document.getElementById('velocity');
    let isDragging = false;
    svg.addEventListener('mousedown', startDragging);
    svg.addEventListener('mousemove', dragCue);
    svg.addEventListener('mouseup', endDragging);

    function getSVGsFromServer() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var svgData = xhr.responseText;
                displaySVGs(svgData);
            }
        };
     //   xhr.open('GET', '/api/get_svgs', true);
     //   xhr.open('POST', '/api/get_svgs', true);

     //   xhr.send();
    }
    
    // Function to split SVG data and display one SVG at a time
    function displaySVGs(svgData) {
        const svgContainer = document.getElementById("svgContainer");
        var i = 0;
        var svgs = svgData.split('</svg>'); // Split SVG data into an array of SVG strings
        console.log("in the one i added now to see");
    // Loop through the SVG strings
        var element = document.getElementById("poolTable");
        svgs.forEach(function(svgString) {
                i = i+1;
                var html_string = `<svg>${svgString}</svg>`;
                html_string += `
                 <line id="cueLine" stroke="black" stroke-width="10" x1="0" y1="0" x2="0" y2="0"></line>
                 </svg>
                 <div id="svgContainer"></div><p>"Player 1 turn"</p>
                 <script
                        src="jquery.js" />
                 </script></div><br>`;//</body></html>`;
            // Append the SVG string to the container
                console.log("jjhkehy7rytegwjeusiy ", i);
                if (i==2){
                    console.log(html_string)
                }

             //   setTimeout(function() {
             //       svgContainer.innerHTML = html_string;
             //   }, 10);
               // svgContainer.innerHTML = html_string
               // setTimeout
                document.body.innerHTML += html_string
               // element.innerHTML = html_string;
        });
        
    }
    function startDragging(e) {
        cueLine.style.visibility = "visible";
      //  const rect = cueBall.getBoundingClientRect();
           // parseFloat(cueBall.getAttribute('cx'));
           // const cueBallY = parseFloat(cueBall.getAttribute('cy'));
      //  const mouseX = e.pageX;
      //  console.log("Mouse is %d ", e.pageY);
      //  console.log("ball at %d   ", rect.top);
      //  console.log("ball at %d   ", rect.bottom);
      //  const mouseY = e.pageY;
        isDragging = true;
    }

    function dragCue(e) {
        if (isDragging) {
            const cueBallX = parseFloat(cueBall.getAttribute('cx'));
            const cueBallY = parseFloat(cueBall.getAttribute('cy'));
            const rect = cueBall.getBoundingClientRect();
            const centerX = (rect.left + rect.width / 2);
            const centerY = rect.top + rect.height / 2;
            const deltaX = centerX - e.clientX;
            const deltaY = centerY - e.clientY;
            const radius = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            const angle = Math.atan2(deltaY, deltaX);
            const scale = 4; // Adjust this scale factor as needed
            const mouseX = cueBallX + scale * radius * Math.cos(angle);
            const mouseY = cueBallY + scale * radius * Math.sin(angle);
            updateCueLine(mouseX, mouseY);
            console.log("mouseX is what %d mouseY %d  ", mouseX, mouseY);
             //   updateVelocityDisplay(centerX, centerY, mouseX, mouseY);
        }
    }

    function endDragging(e) {
        isDragging = false;
        cueLine.style.visibility = "hidden";
        const cueBallX = parseFloat(cueBall.getAttribute('cx'));
        const cueBallY = parseFloat(cueBall.getAttribute('cy'));
       // const cueLine = parseFloat()
        const rect = cueBall.getBoundingClientRect();
        const centerX = (rect.left + rect.width / 2);
        const centerY = rect.top + rect.height / 2;
        const deltaX = centerX - cueLine.getAttribute("x2");
        const deltaY = centerY - cueLine.getAttribute("y2");
     //   const deltaX = centerX - e.clientX;
     //   const deltaY = centerY - e.clientY;
        const radius = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        const angle = Math.atan2(deltaY, deltaX);
        const scale = 2; // Adjust this scale factor as needed
        const mouseX = cueBallX + scale * radius * Math.cos(angle);
        const mouseY = cueBallY + scale * radius * Math.sin(angle);     
           //     updateCueLine(0, 0);
        console.log("mouseX is what %d mouseY %d  ", mouseX, mouseY);
             //   updateVelocityDisplay(center

            // Calculate the length of the line using the Pythagorean theorem
        //    console.log("mouse x and y is %d   %d  ", mouseX, mouseY);
        //    console.log("cueall is %d  %d  ", cueBallX, cueBallY);
        console.log("length is %d %d  ", ((mouseX)-(cueBallX)), (mouseY-cueBallY));
        const length = Math.sqrt((mouseX - cueBallX) ** 2 + (mouseY - cueBallY) ** 2);
            // Display the length of the line
        //console.log("Length of the line: ", length);
        velocityDisplay.textContent = length;
        
        sendDataToServer(mouseX-cueBallX, mouseY-cueBallY, length);
           // velocityDisplay = 
    }

    function updateCueLine(mouseX, mouseY) {
        const cueBallX = parseFloat(cueBall.getAttribute('cx'));
        const cueBallY = parseFloat(cueBall.getAttribute('cy'));
            // Update the line's endpoints
        cueLine.setAttribute('x1', cueBallX);
        cueLine.setAttribute('y1', cueBallY);
        cueLine.setAttribute('x2', mouseX);
        cueLine.setAttribute('y2', mouseY);
        updateVelocityDisplay(cueBallX, cueBallY, mouseX, mouseY);
    }

    function updateVelocityDisplay(mouseX, mouseY) {
        const cueBallX = parseFloat(cueBall.getAttribute('cx'));
        const cueBallY = parseFloat(cueBall.getAttribute('cy'));
        const velocityX = mouseX - cueBallX;
        const velocityY = mouseY - cueBallY;
      //  $('#valvelocity').remove();
        velocityDisplay.textContent = `Velocity X: ${velocityX.toFixed(2)}, Velocity Y: ${velocityY.toFixed(2)}`;
        console.log("cuebllx is %d and mouse  is %d ", cueBallY, mouseY);
        const valuex = Math.sqrt(velocityX*velocityX + velocityY*velocityY);
        console.log("Velocity i s %d  ", valuex);
       // getSVGsFromServer();
    }

    function getAnimate(svgData){
        console.log("jjhkehy7rytegwjeusiy");
        console.log(svgData);
        var dataToSend = {svgData: svgData};
        $.ajax({
            type: "POST", url: "animate.html", data: dataToSend, 
            success: function(response){
                console.log("data html sent successfully ");
                console.log("whatdthis");
                displaySVGs(response);
            }, 
            error: function(xhr, status, error){
                console.error("Errorsending data: ", error);
            }
        })
    }

    function sendDataToServer(mouseX, mouseY, length){
        var dataToSend = {
            mouseX: mouseX,
            mouseY: mouseY,
            length: length
        };

        $.ajax({
            type: "POST", url: "gamepoolvel.html", data: dataToSend, 
            success: function(response){
                console.log("data sent successfully ");
                console.log("what is this");
                displaySVGs(response);
            }, 
            error: function(xhr, status, error){
                console.error("Error sending data: ", error);
            }
        })
    }
    });
