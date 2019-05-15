<head>
    <h2>Football Players Performance Analysis</h2>
</head>
<body>
<main>
  
<h3>Tracks football players and computes their absolute coordinates on football field.</h3>
</main>
 
<h4>How to setup & run: </h4>
<br/>
<ul>
    <li>$ pip install -r requirements.txt</li>
    <li>Download weights and config files from https://pjreddie.com/darknet/yolo/:<br/>
tiny version gave less accurate detection results, bigger one is preferred.</li>
<li>Download class txt file from 
<a href="https://drive.google.com/file/d/1ZtWlNf5VYXsjs3bgHoRm8lkV_W54c9Md/view?usp=sharing">
link</a></li>
<li>Download veo video from <a href="https://app.veo.co/matches/">link</a> and make two videos, simply divide it by the field part it films.<br/></li>
 <li>Alternative: download one of ours videos we used for testing:<br/>
  <a href="https://drive.google.com/file/d/1M0B9JzqQzEgAnRL74ujEWlXaz_utkgnb/view?usp=sharing">
  link</a> to video filming left part of football field<br/>
  <a href="https://drive.google.com/file/d/1I4FCz0L-KEtz-Ma7EIcEWfmFwLNtEkY3/view?usp=sharing">link</a> to video filming right part of football field</li>
<li>Write paths to weights, class txt, config and videos files in config.py</li>
<li>$ python3 main.py</li>
</ul>
<br/>
<h5>Created by Uhera Andrii, Maistruk Andri 2019.</h5> 
</body>