%%% -*- Mode: Prolog; -*-

:- use_module('../distributionalclause.pl').
:- use_module('../random/sampling.pl').
:- use_module(library(lists)).

:- set_options(default),set_inference(backward(lw)), set_query_propagation(true). % enable query propagation







mode ~ finite([0.3:mode1,0.7:mode2]).

pfaulty ~ val(_).
faulty ~ finite([PF:true,NPF:false]):= pfaulty~=PF, NPF is 1-PF.


temperature ~ gaussian(0.5,1.0) := faulty=false, mode~=mode1.
temperature ~ gaussian(2.0,2.0) := faulty~=false, mode~=mode2.
temperature ~ val(2.0) := faulty~=true.



	
fco(N,PF) :-
	init,
	eval_query([temperature~=2.0,pfaulty~=PF],[],faulty~=true,N,P,A,B), 
	write('probability faulty~=true: '),writeln(P).


all_experiments :-
	init,
	findall(
		(N,PF), 
		(
			member(N,[10,100,1000,10000,100000]),
			member(PF,[0.1,0.01,0.001,0.0001,0.00001])
		),
		List
		),
	experiment(100,List),
	true.


experiment(_,[]):- true.

experiment(Runs, [(N,PF) | Tail]) :-
	File='faulty.txt',
	Q=[faulty~=true],
	E=[temperature~=2.0,pfaulty~=PF],
	experiment_lw(File,Q,E,N,Runs,PF),
	experiment(Runs, Tail),
	writeln(N),
	writeln(PF),
	true.


experiment_lw(File,Q,E,N,Repeat,PF) :-
	I is cputime,
	findall(
		P,
		(
			between(
				1,
				Repeat,
				_
			),
			distributionalclause:eval_query_backward_lw(
				E,[],Q,1,N,P1,_,SSum
			),
			(
				SSum>0 -> P=P1;P is random
			)
		),
		List
	),
	T is (cputime-I)/Repeat,
	(
		ground(AVG)->
			variance(List,AVG,V);
			avgvar(List,AVG,V)
	),
	
	
	open(File,'append',F),
 	write(F,N), write(F,','),
 	write(F,PF), write(F,','),
	write(F,AVG), write(F,','),
	write(F,T),nl(F),
	close(F).
