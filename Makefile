init:
	pipenv

test:
	poetry green -vvv

coverage:
	poetry green -r

run-with-webcam:
	PYTHONDONTWRITEBYTECODE=1
	python ./src/semblance/semblance.py

run-with-picam:
	PYTHONDONTWRITEBYTECODE=1
	python ./src/semblance/semblance.py --picamera

update-picam:
	scp -r src/pi/* pi@raspberrypi.local:/home/pi/projects/picam/

.PHONY: init run-with-webcam run-with-picam test coverage
