init:
	pipenv

test:
	green -vvv

coverage:
	green -r

run:
	PYTHONDONTWRITEBYTECODE=1
	python ./src/semblance/semblance.py

update-picam:
	scp -r src/camera_client.py pi@raspberrypi.local:/home/pi/projects/picam/client.py

proxy-picam:
	python ./src/semblance/camera_proxy.py

.PHONY: init run test coverage
