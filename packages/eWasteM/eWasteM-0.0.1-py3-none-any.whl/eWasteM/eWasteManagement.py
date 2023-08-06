def emailCheck(email):
	if "@" in email:
		return ("is_email")
	else:
		return ("not_a_email")

def checkImage(image):
	a=[".jpg",".png",".jpeg"]
	if image[-4:]==".png":
		return True
	elif image[-5:]==".jpeg":
		return True
	elif image[-4:]==".png":
		return True
	else:
		return False

