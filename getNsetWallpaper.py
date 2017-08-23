import re
import urllib.request
import contextlib
import os
import getpass



def getURL():
	xml_data=""
	url = "http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=en-US"
	bing_url="http://www.bing.com/"
	img_url=""
	with contextlib.closing(urllib.request.urlopen(url)) as fp:
		while(True):
			block=fp.read(1024*8)
			if not block:
				break
			xml_data+=(str(block))

	img_location=re.findall("<url>*.*</url>",xml_data)
	img=img_location[0]
	img_url=str(img.replace("<url>",''))
	img_url=str(img_url.replace("</url>",''))
	img_url=str(bing_url+img_url)
	#print(img_url)
	return img_url



def getImage(image_url):

	url_parse=img_url.split('/')
	image_file_name=url_parse[len(url_parse)-1]
	#print(image_file_name)
	system_user=getpass.getuser()
	file_location="/home/"+str(system_user)+"/Pictures/BingDaily/"
	image_file_name=file_location+image_file_name
	file=open(image_file_name,'wb')
	with contextlib.closing(urllib.request.urlopen(image_url)) as rfp:
		while(True):
			block=rfp.read(1024*8)
			if not block:
				break
			file.write(block)
		file.close()
	return image_file_name



def setWallapper(file_name):
	command= "gsettings set org.cinnamon.desktop.background picture-uri "
	file_name=file_name
	final_command=command+file_name
	print(final_command)
	os.system(final_command)
	return None


if __name__=="__main__":
	img_url=getURL()
	image_file_name=getImage(img_url)
	setWallapper(image_file_name)