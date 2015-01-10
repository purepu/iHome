<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Home Music</title>
  <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0" /> 
  <link rel="stylesheet" media="all" href="style.css" type="text/css">
  <script src="js/jquery.min.js"></script>
  <script src="http://cdn.jquerytools.org/1.2.7/full/jquery.tools.min.js"></script>
</head>

<body>
  <div class="wrap">
    <header>
      <div class="logo"><a href="/"><img src="images/logo.png" alt="Home Music"/></a></div>
      <div class="options">
      	<ul>
      		<li>Search</li>
      		<li>Menu</li>
      	</ul>
      </div>
      <div class="clear"></div>
	    <div class="search-box">
	    	<form action="#">
	    		<input type="text" name="q" placeholder="Search gallery" />
	    		<input type="submit" value="Go" />
	    	</form>
	    	<div class="clear"></div>
	    </div>
	    <nav class="vertical menu">
	    	<ul>
	            <li><a href="#" onclick="$.get('/pause', null);">Pause/Resume</a></li>
	            <li><a href="#" onclick="$.get('/volup', null);">Volume Up</a></li>
	            <li><a href="#" onclick="$.get('/voldown', null);">Volume Down</a></li>
        	</ul>
	    </nav>
    </header>
    
        
    <div class="content">
    	<article class="underline" onclick="$.get('/play/douban.fm', null);">
		<div class="post-preview">
			<img src="http://img3.douban.com/lpic/o415236.jpg" alt="title of the image"/>
		</div>
		<div class="post-content">
			<h2>douban.fm</h2>
		</div>
		<div class="clear"></div>
		</article>
%for s in songs:
    	<article class="underline" onclick="$.get('/play/{{s}}', null);">
		<div class="post-preview">
			<img src="/cover/{{s}}" alt="title of the image"/>
		</div>
		<div class="post-content">
			<h2>{{s.split('.')[0]}}</h2>
		</div>
		<div class="clear"></div>
		</article>
%end
    </div>
  </div>
 
  <script type="text/javascript">
     window.addEventListener("load",function() {
  	  // Set a timeout...
  	  setTimeout(function(){
  	    // Hide the address bar!
  	    window.scrollTo(0, 1);
  	  }, 0);
  	});
     $('.search-box,.menu' ).hide();   
     $('.options li:first-child').click(function(){	
     		$(this).toggleClass('active'); 	
     		$('.search-box').toggle();        			
     		$('.menu').hide();  		
     		$('.options li:last-child').removeClass('active'); 
     });
     $('.options li:last-child').click(function(){
   		$(this).toggleClass('active');      			
   		$('.menu').toggle();  		
   		$('.search-box').hide(); 
   		$('.options li:first-child').removeClass('active'); 		
  	   //$(this).toggleClass('active');
  	   //$.get('/pause', null);
     });
     $('.content').click(function(){
     		$('.search-box,.menu' ).hide();   
     		$('.options li:last-child, .options li:first-child').removeClass('active');
     });
  </script>
</body>
</html>
