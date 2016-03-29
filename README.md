# swish
Swing analysis

Swish is designed for detecting and classifying shots played in a game of squash based on wrist movement. 

It has some challenges beyond golf swing analysis because not only do I want to classify different types of swings based on the shot played, but be able to detect swings that are a result of playing a shot during a game, filtering out the noise of the racket moving while just moving around the court. 

I have named this project swish based on advice from my coach many years ago - "if you don't hear a 'swish' from your racket when you play a shot, you played the shot wrong". That's a bit of an exaggeration, but it suits the purpose of coaching, and I want swish to be used as a coaching tool eventually.

Using PebbleJS to send accelerometer data from my Pebble Time, from which I can determine speed, displacement etc. Unfortunately I don't have a gyroscope yet. Not necessary at this stage, but would be really helpful and possibly critical later on.

Using Python, notably Pandas, to analyse the data.

