#!/bin/bash

counter=1
while [ $counter -le 100 ]
do
	curl -X POST -d "email=joonsang@naver.com&password=wnstkd003!" ec2-52-78-168-195.ap-northeast-2.compute.amazonaws.com:8000/accounts/obtain_token/
	((counter++))
done
echo All done
