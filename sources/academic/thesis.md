title: Active Learning of Automata with Resources

My PhD thesis is entitled Active Learning of Automata with Resources.
It was conducted under the joint supervision of
[Véronique Bruyère](https://web.umons.ac.be/fs-informatique/equipes/veronique-bruyere/)
(University of Mons) and
[Guillermo A. Pérez](https://gaperez64.github.io/) (University of Antwerp).
It was funded by the F.R.S.-FNRS Research Fellow project ARTWORK.
The jury was composed of Dana Fisman, Daniel Neider, Ocan Sankur, Frits W. Vaandrager,
and Jef Wijsen, as well as my supervisors Véronique Bruyère and Mickael Randou.

  * The private defense happened on June 19, 2024 at the University of Antwerp
  in the sole presence of the jury \[[slides](talks/2024/private.pdf)\].
  * The public defense (intended to be a less technical and more accessible presentation) will take place at the University of Mons on Septembre 11, 2024.
  <!-- * The public defense (intended to be a less technical and more accessible presentation) happened at the University of Mons on Septembre 11, 2024 [LINK TO SLIDES HERE]. -->
  <!-- * The manuscript is accessible [LINK]. -->

## Abstract

Computer systems are ubiquitous nowadays and it goes without saying that their
correctness is of capital importance in a lot of cases.
However, identifying bugs and faults in computer systems is a hard and
complex task.
On top of well-known methods such as unit testing, integration testing, and so
on, one can apply *model checking* techniques, which
formally verify that a *model* (an abstract representation of the system)
behaves correctly with regards to a set of constraints.
Constructing a model from a system is itself complex and may introduce errors
that do not occur in the actual system.
Fortunately, if the system can be modeled by an *automaton* (a state machine
describing which execution is valid or invalid), one can apply
*active automata learning* algorithms to automatically construct
automata by interacting with the computer system in a black-box manner, i.e., by
only observing runs of the system without having access to its internal details.
While the original algorithm introduced in 1987 by Dana Angluin focused on
simple automata than can only use their
states to determine whether a word is valid or not, many efforts were made in
recent years to learn more complex (and, thus, more expressive) families of
automata that can use *resources*, such as a stack, registers, \etc
In this thesis, we present two learning algorithms for two distinct extensions
of automata (with different available resources), as well as a model checking
approach for JSON documents, relying on automata learning.
We divide our contributions into three axes.

Firstly, we provide a learning algorithm for a family of automata extended with a
natural counter, which can be incremented or decremented along the transitions.
Furthermore, it can be tested against zero, allowing different behaviors based
on the current counter value.
Since the counter does not have an upper bound in general, the number
of pairs of a state and a counter value is potentially infinite, meaning that
learning the behavior of a system requires special care.
We provide a finite characterization of this behavior that can be learned by
querying the system, and from which a one-counter automata can be extracted.
We show that the algorithm builds a polynomial number of hypotheses in the size
of this characterization but requires exponentially many interactions to do so.

Secondly, we focus on JSON documents, which can be used to store and transfer
information in a way that is easily readable by a human and by a computer.
More precisely, we assume that we are in a streaming context, \ie, the document
is received piece by piece (which happens when a document is sent via a network,
for instance), and that we want to verify whether the document is valid with
regards to a set of constraints, given as a JSON schema.
The classical algorithm exploring the constraints and the document in parallel
requires to keep the full document in memory in the worst case and, thus,
is not always appropriate in a streaming scenario.
Our new approach first learns an automaton augmented with a stack that is then
abstracted and used to efficiently decide whether a document is valid, without
needing to store the whole document.
That is, our validation algorithm has a lower overall memory requirement, at the
cost of needing more time to validate a document, as observed on experimental
results.

Finally, we study automata whose resources are timers that can be used to encode
timing constraints.
A timer is started at some value and decreases over time.
Then, when it reaches zero, a special event occurs that must be handled,
similarly to interruptions in a processor.
It may happen that multiple timers reach zero at the same time, or that the
user provides an input exactly at the same time a timer times out.
In these cases, the model has a non-deterministic behavior as the automaton
may decide to process these events in any order.
We study the timed behavior of such an automaton and provide conditions
ensuring that any untimed behavior can be observed without this non-determinism.
Finally, we give an active learning algorithm, requiring a factorial number
of interactions in the number of timers, and polynomial in the number of states.
As, in practice, the number of timers remains relatively small, we claim that
our algorithm can be used for real-world applications.