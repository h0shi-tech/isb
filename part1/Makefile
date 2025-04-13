CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra

all: cpp java

cpp: random_generator.cpp
	$(CXX) $(CXXFLAGS) -o random_generator random_generator.cpp

java: RandomGenerator.java
	javac RandomGenerator.java

run_cpp: cpp
	./random_generator

run_java: java
	java RandomGenerator

clean:
	rm -f random_generator RandomGenerator.class random_sequence.txt random_sequence_java.txt

.PHONY: all cpp java run_cpp run_java clean 