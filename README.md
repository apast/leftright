# leftright
Diff binary files over HTTP

[![Build Status](https://travis-ci.org/apast/leftright.svg?branch=master)](https://travis-ci.org/apast/leftright)
[![Code Climate](https://codeclimate.com/github/apast/leftright/badges/gpa.svg)](https://codeclimate.com/github/apast/leftright)


leftright REST API is the new web platform to compare two strings.

It runs using Tornado Web, one of the main python asynchronous networking library. It uses non-blocking network I/O and can scale for thousand of requests under right server conditions.

Hope you enjoy!

## Preparing your environment

### The bash way
```
git clone https://github.com/apast/leftright.git leftright
cd leftright
run the following script:
bash leftright.sh
```

### The pythonic way
If you prefer to run by your own, you can run the following commands:

```virtualenv venv
. venv/bin/activate
pip install -r requirements.pip
cd src
python -m leftright
```

### Some more details about command line interface
For some help, you can run:

```
python -m leftright -h
```

## Continuous Integration
Our Travis-CI dashboard is available and there you can following the most updated info about build status, branch evolution and tests & code coverage statuses:

[![Build Status](https://travis-ci.org/apast/leftright.svg?branch=master)](https://travis-ci.org/apast/leftright)

Hope to achieve 100% including patch tornadoweb.ioloop.IOLoop ASAP! We are almost there!

## Code Quality

[![Code Climate](https://codeclimate.com/github/apast/leftright/badges/gpa.svg)](https://codeclimate.com/github/apast/leftright)

Our dashboard for code quality is running over Code Climate platform and can be accessed [here](https://codeclimate.com/github/apast/leftright/).

## Stay in Touch

If you want to contact me, you can find me out at:
+ [LinkedIn](https://linkedin.com/in/andrepastore)
+ [Twitter](https://twitter.com/apast)


## Acknowledges

Thanks for your time and consideration to read my how to and analyse my project!

For any issues, questions or ideas for improvement, it will be a pleasure to listen and share more with you!
