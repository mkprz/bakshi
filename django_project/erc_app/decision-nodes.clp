; based on design patterns from 
; http://www.csie.ntu.edu.tw/~sylee/courses/clips/design.htm

; node struct
(deftemplate node
	(slot name)
	(slot type)
	(slot question)
	(slot selected-answer)
	(multislot possible-answers (type String) (default "yes" "no" "skip"))
	(multislot branch-nodes (default none))
)

;init
(defrule initialize
	(not (node (name root)))
=>
	(assert (current-node root))
)

;ask away
(deffunction setprompt (?question)
	(while (and (neq ?answer yes) (neq ?answer no))
		(printout t ?question crlf ?choices) 
		(bind ?answer (read))
	(return ?answer)

(defrule ask-decision-node-question
	?node <- (current-node ?name)
	(node (name ?name)
		(type decision)
		(question ?question)
		(possible-answers ?choices)
	)
	(not (answer ?))
=>
	(assert (answer (setprompt ?name ?question ?choices)))
)

;response
(defrule proceed-to-branch-node
	?node <- (current-node ?name)
	(node (name ?name)
		(type decision)
		(possible-answers ?choices)
		(branch-nodes ?branches)
	)
	?answer <- (answer ?)
	?n <- (member$ ?answer ?choices)
	?branch <- (nth$ ?n ?branches)
=>
	(retract ?node ?answer)
	(assert (current-node ?branch))
)


