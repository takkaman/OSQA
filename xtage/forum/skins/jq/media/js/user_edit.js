// this is the js file for edit.html in users/ folder

        function previewImage(file)
        {
          var MAXWIDTH  = 128;
          var MAXHEIGHT = 128;
          var div = document.getElementById('preview');
          var submitbtn = document.getElementById("submit_img");
          if (file.files && file.files[0])
          {
              // check the img file with suffix of jpeg, jpg, png, gif
              var temp = file.value.split(".");
              var suffix = temp[temp.length-1];
              suffix = suffix.toUpperCase();
              if (suffix != 'JPEG' && suffix != 'JPG' && suffix != 'GIF' && suffix != 'PNG')
              {
                  alert('please select an image file with suffix JPEG/JPG/GIF/PNG');
                  return;
              }   
              // file size check, should not > 2m
              var filelimit = 2*1024*1024;
              var filesize = file.files[0].size;
              if (filelimit < filesize){
                  alert('image file too large (> 2M) ');
                  // submitbtn.style.display = 'none';
                  return;
              }
              div.innerHTML ='<img id=imghead>';
              var img = document.getElementById('imghead');
              img.onload = function(){
                var rect = calcImgZoomParam(MAXWIDTH, MAXHEIGHT, img.offsetWidth, img.offsetHeight);
                img.width  =  rect.width;
                img.height =  rect.height;
                img.width  = MAXWIDTH;
                img.height  = MAXHEIGHT;
		// img.style.marginLeft = rect.left+'px';
                img.style.marginTop = rect.top+'px';
                img.style.marginTop = 0 + 'px';
                img.style.float = 'left';
              }
              var reader = new FileReader();
              reader.onload = function(evt){img.src = evt.target.result;}
              reader.readAsDataURL(file.files[0]);
          }
          else //for IE
          {
            var sFilter='filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale,src="';
            file.select();
            var src = document.selection.createRange().text;
            div.innerHTML = '<img id=imghead>';
            var img = document.getElementById('imghead');
            img.width = MAXWIDTH;
            img.height = MAXHEIGHT; 
            img.filters.item('DXImageTransform.Microsoft.AlphaImageLoader').src = src;
            var rect = calcImgZoomParam(MAXWIDTH, MAXHEIGHT, img.offsetWidth, img.offsetHeight);
            // console.log("IE: img.width= ", rect.width, " img.height= ", rect.height );
            status =('rect:'+rect.top+','+rect.left+','+rect.width+','+rect.height);
            div.innerHTML = "<div id=divhead style='width:"+rect.width+"px;height:"+rect.height+"px;margin-top:"+rect.top+"px;"+sFilter+src+"\"'></div>";
            div.innerHTML = "<div id='divhead' style='width:"+MAXWIDTH+"px;height:"+MAXHEIGHT+"px;margin-top:0px;"+sFilter+src+"\"'></div>";
          }
          div.style.display = "";
          submitbtn.style.display = '';
        }

        function calcImgZoomParam( maxWidth, maxHeight, width, height ){
            console.log("enter calcImgZoomparam");
            var param = {top:0, left:0, width:width, height:height};
            if( width>maxWidth || height>maxHeight )
            {
                rateWidth = width / maxWidth;
                rateHeight = height / maxHeight;
                 
                if( rateWidth > rateHeight )
                {
                    param.width =  maxWidth;
                    param.height = Math.round(height / rateWidth);
                }else
                {
                    param.width = Math.round(width / rateHeight);
                    param.height = maxHeight;
                }
            }
             
            param.left = Math.round((maxWidth - param.width) / 2);
            param.top = Math.round((maxHeight - param.height) / 2);
            return param;
        }
