; based on design patterns from 
; http://www.csie.ntu.edu.tw/~sylee/courses/clips/design.htm

; node struct
(deftemplate node
	(slot name)
	(slot type (default decision))
	(slot question (type STRING))
	(slot script-cmd (type STRING))
	(slot selected-answer (default none))
	(multislot possible-answers (default yes no))
	(multislot branch-nodes))

;init
(defrule initialize
	(not (node (name root)))
=>
	(assert (node (name root)
			(question "Is this a household?")
			(branch-nodes yes-household is-shared-printer)
		)
	)
	(assert (current-node root))
)

(defrule root-response
	(current-node root)
	?node <- (node (name root)
			(branch-nodes ?yes-branch ?no-branch))
	(not (node (name ?yes-branch)))
	(not (node (name ?no-branch)))
=>
	(assert (node (name ?yes-branch)
			(question "kids?")
			(branch-nodes yes-kids is-cord-cutter)
		)
	)
	(assert (node (name ?no-branch)
			(question "Do you wish to share your printer over the network?")
			(branch-nodes yes-printer-share end-thank-you)
		)
	)
)

(defrule yes-household-response
	(current-node yes-household)
	(not (node (name yes-kids)))
	(not (node (name is-cord-cutter)))
=>
	(assert (node (name yes-kids)
			(question "Do you want parental controls?")
			(branch-nodes yes-parental-controls is-cord-cutter)
		)
	)
	(assert (node (name is-cord-cutter)
			(question "Have you canceled your cable provider in favor of a pure internet experience? Are you a cord-cutter?")
			(branch-nodes yes-cord-cutter is-shared-printer)
		)
	)
)

(defrule is-cord-cutter-response
	(current-node is-cord-cutter)
	(not (node (name yes-cord-cutter)))
	(not (node (name is-shared-printer)))
=>
	(assert (node (name yes-cord-cutter)
			(selected-answer yes)
			(branch-nodes end-thank-you)
		)
	)
	(assert (node (name end-thank-you)
			(type leaf)
		)
	)
	
)

;ask away
(deffunction setprompt (?name ?question $?choices)
	(bind ?answer false)
	(while (and (neq ?answer yes) (neq ?answer no))
		(printout t ?name crlf ?question crlf $?choices)
		(bind ?answer (read)))
	(return ?answer)
)

(defrule ask-decision-node-question
	?node <- (current-node ?name)
	(node (name ?name)
		(type decision)
		(question ?question)
		(possible-answers $?choices))
	(not (answer ?))
=>
	(assert (answer (setprompt ?name ?question $?choices)))
)

;response
(defrule proceed-to-branch-node
	?answer_fact <- (answer ?choice)
	?node_fact <- (current-node ?name)
	(node (name ?name)
		(type decision)
		(possible-answers $?choices)
		(branch-nodes $?branches))
=>
	(retract ?node_fact ?answer_fact)
	(bind ?n (member$ ?choice $?choices))
	(bind ?next (nth$ ?n $?branches))
	(assert (current-node ?next))
)