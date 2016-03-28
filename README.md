# autotest

## Before test

#### Make sure robotframework and robotframework-selenium2library have been installed, if no, follow steps below:

	#install robotframework
	$easy_install robotframework
	
	#Check if robotframework is installed:
	$pybot --help
	
	#install robotframework-selenium2library
	$easy_install robotframework-selenium2library

#### Run test
Take login test for example: 

	$pybot login
	$pybot login/valid_login.txt
	$pybot login/invalid_login.txt
