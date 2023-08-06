# queens8 Package 0.1.2
last change 25-Apr-2022

## Introduction to the n Queens and 8 Queens problem.
In the 19th century the n Queens puzzle was formulated. The aim of the puzzle was to place
n Chess Queens on a n x n chessboard such that no Queen attacks any other Queen. That is every row, every
column and every diagonal has no more than one of the n Queens placed in that row, column or diagonal.

In 1848 Chess Master Max Bezzel proposed the problem for n=8, the Chess Board we are all familiar with.
In 1850 Franz Nauck extended the problem to other n x n Chess boards, as well as publish soloutions to the 8 x 8
variant. Many mathematicians of the time worked on this, including the esteemed Karl Friedrich Gauss.

With the advent of structured progamming Edsger Dijikstra wrote a program to solve this problem for n=8, with a method
known as depth first backtracking. The Dijikstra solution also had an elegant method of charaterizing the diagonals.

In his program the user chooses which column the Queen on the first row occupies and the program looks for the first
solution in placing the other 7 Queens.

|Column Number|Chess Notation|
|-----------------|------------------|
|1|Queens Rook 1|
|2|Queens Knight 1|
|3|Queens Bishop 1|
|4|Queen 1|
|5|King 1|
|6|Kings Bishop 1|
|7|Kings Knight 1|
|8|Kings Rook 1|

## Symmetry

When you run this the careful observer will notice the solutions 1 and 8 are really the same with 
there only being a rotation of the board between them. You might also observe 2 and 6 are the same
with a rotation between them.

![Symmetry between solution 1 and 8](ChessSym.png)

A fundamental solution is the set of a solution with all symmetric solutions to that solution. A symmetric
solution is either a rotation or a reflection. There is one solution which is exactly equal to it's reflection,
so it has no reflections.

There are three counter clockwise rotations, that of 90, 180 and 270 degrees.

A horizontal reflection is a relection around the line which
lies between the King and Queen columns. A vertical reflection is around the line between the 4th and 5th rows.
There are also reflections around the longest up diagonal and the longest down diagonal. Both of these diagonal
reflections together are a reflection about the center point of the board.

Any composition of these operations is again another symmetry.
We keep putting new ones in until there are no new symmetries.

## The Dijikstra Wirth algorithm.

The Dijikstra algorithm has a set of flags one for every row, every column, every Up Diagonal and every Down Diagonal.
This make 8 rows, 8 columns, 15 Up Diagonals and 15 Down diagonals. The Up Diagonals are characterized by K = Row + Column.
K characterizes the diagonal with K in {2 .. 16}. The DownDiagonals are characterized by K = Row - Column. K
characterizes the diagonal with K in {-7 .. 7}. The diagonal flags (as well as row and column) are lists of flags. The
diagonal are lists of length 17. The negative indexes for Down Diagonals work well with Python these being the distance from the
end of the list.

## This package has 4 different functions.

This package has 4 different functions which are sellected by menu:

1) The fundamental Dijikstra algorithm with a Graphics like board display.

2) A search for all fundamental solutions, that is pruning symmetries.

3) The Dijikstra algorithm showing the board and all symmetrical boards.

4) Showing which Dijikstra soloutiions are symmetric to each other as sets.

## The Pseudo graphical board display.

The board is shown by using tkinter. The root frame contains 8 frames, each of which is a row.
Each row is 8 characters. The Empty square is a Unicode '\u3000' because an ascii space is not
sized right. The color of the square is the background color. White Queens '\u2665' are queens
on black squares and Black Queens '\u265b' are placed on white squares for good contrasts. An example of
board for 1 and 8 are in the section labeled symmetry. The board or boards
remain until the "Enter to Proceed!" is replied to. Then the boards are destroyed.

## Installing Queens8.

The simplest method : pip install queens8

## Running Queens8.

```
#!python

from queens8 import Queens8

Queens8.Go()
```

Queens8 will then prompt:
```
A  : The orginal Dijkstra and Wirth solution to the 8 queens problem.
B  : Do all solutions with no symmetries
C  : Like Queens8 only show the symmetries too
E  : Of the 8 returned by Queens8 as equivalence sets (no graphics)
Q  : To Quit 
X  : Same as Q
select:q

```
A Q or an X followed by enter will exit queens8.

An A or a will prompt for a column on row 1 to place the first queen. All the steps in
the depth first backtracking search will be displayed. The final board will be displayed also.

```
On which row do you want the first Queen?
valid entries an in range 1..8
enter any other integer to halt.
?:5
  1: Place Queen 1 on Row 5
  2: Place Queen 2 on Row 1
  3: Place Queen 3 on Row 4
  4: Place Queen 4 on Row 6
  5: Place Queen 5 on Row 3
  5: Take Queen 5 from row 3
  7: Place Queen 5 on Row 8
  8: Place Queen 6 on Row 2
  9: Place Queen 7 on Row 7
 10: Place Queen 8 on Row 3
2 6 8 3 1 4 7 5 
Enter to Proceed
On which row do you want the first Queen?
valid entries an in range 1..8
enter any other integer to halt.
?:0
```
The B entry shows all 12 fundamental solutions. Each board representing all
symmetries. This prompts for the choice to see the 12 boards or for a text line
showing each column for each row for each solution.
```
select:b
Display Queens Y or N?y
Number of Distinct Solutions = 12 Total Solutions = 92
Enter to Proceed!
```
The C entry is like the A entry, except that the board and all symmetric boards
are displayed!
```
select:c
On which row do you want the first Queen?
valid entries an in range 1..8
enter any other integer to halt.
?:5
Enter to Continue
On which row do you want the first Queen?
valid entries an in range 1..8
enter any other integer to halt.
?:0
```
The D entry shows for for the Dijkstra solutions, which ones are really the same
fundamental solutions.
```
select:e
{1, 8}
{2, 6}
{3}
{4}
{5}
{7}

```
For each of the 8 solutions a set of all symmetric solutions is made. The program
looks for which one are disjoint, O(n^2^) process.

## Look For:

This subject is also discussed in a book I have written. I will update this 'README.md'
when the book is published.