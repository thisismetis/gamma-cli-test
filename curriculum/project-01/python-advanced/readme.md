---
date: w01d03
duration: 50
maintainer: larakattan
order: 4
title: Optional Python Advanced
---

# Sample Lesson Plan

- (20 m) [Advanced Python Datatypes](advanced_python_datatypes.ipynb)
- (15 m) [Deep and Shallow Copy](deep_and_shallow_copy.ipynb)
- (15 m) [Pickle](pickle_saving_objects_for_later.ipynb)

# Learning Objectives

### Advanced Python Data Types
The students will be:

* Familiar with DefaultDict
* Familiar with NamedTuples
* Familiar with Deques
* Understand the difference between a list and a generator
* Be familiar with `yield` vs `return` and the purpose of generators

### Deep Copy

The students will:

* Understand how the memory is assigned (roughly)
* Understand why deep copy is necessary
* Know how to deep copy and when it is necessary.

### Pickle: Saving Objects for Later

The students will:

* Know what pickling is
* Understand how to dump/load an object
* Be familiar with how pickle can fit into their workflow

# Depends On

[Python Review](https://github.com/thisismetis/dscurriculum_gamma/tree/master/curriculum/project-01/python-review)

[Intro to Pandas](https://github.com/thisismetis/dscurriculum_gamma/tree/master/curriculum/project-01/pandas-intro)

# Instructor Notes

### Advanced Python Data Types

This notebook walks through some of the more niche data types available in the
collections module. It also introduces the idea of generators and demonstrates
the idea of a cursor. This notebook is heavily annotated and should act as
a reference for students later.

### Deep Copy

This notebook introduces the concept of deep copying and shallow copying.  Cartoons are included to illustrate where variables point in memory.

### Pickle: Saving Objects for Later

This notebook introduces the idea of pickling data. In particular, it
focuses on the technique of dumping and loading from file in a byte format.
There is also some discussion of how pickle can be added to a workflow to
help control for data loss and to stop repeat procedures like needing to
clean data every time a notebook starts. It also discusses breaking work
into multiple notebooks that each do one job well (the first discussion of
workflow).


# Additional Resources