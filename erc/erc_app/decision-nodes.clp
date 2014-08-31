; Expert-System Router Configuration (ERC) or Bakshi Router Configuration Wizard
; mike perez: meekprize@gmail.com; kf5qvo@outlook.com
; Feb - Oct, 2013

; decision-tree-nodes strategy based on design patterns from 
; http://www.csie.ntu.edu.tw/~sylee/courses/clips/design.htm

; function: setprompt
; based on current-node, present user with a prompt
; -- use within the CLIPS interactive shell
; -- if using the web interface, use the same-named external python/django function
(deffunction setprompt (?name ?question $?choices)
	(assert (invalid-response))
	(bind ?answer false)
	(while invalid-response
		(printout t ?name crlf ?question crlf $?choices)
		(bind ?answer (read))
		(assert (check-response ?choices ?answer)))
	(return ?answer)
)

; rule: valid-response
; check if user response is valid
(defrule valid-response
	(check-response ($? ?answer $?) ?answer)
=>
	(retract (invalid-response))
)


; fact template: node
; use this data structure to develop your own decision-tree-nodes
; multislots branch-nodes and script-cmds correspond to multislot possible-answers
(deftemplate node
	(slot name)
	(slot type (default decision))
	(slot question (type STRING))
	(multislot possible-answers (default yes no))
	(multislot script-cmds (default none))
	(multislot branch-nodes (default none))
)

; rule: ask-decision-node-question
; using the current-node in the decision tree, trigger a user prompt
(defrule ask-decision-node-question
	(not (answer ?))
	?node <- (current-node ?name)
	(node (name ?name)
		(type decision)
		(question ?question)
		(possible-answers $?choices))
=>
	(assert (answer (setprompt ?name ?question $?choices)))
)

; rule: proceed-to-branch-node
; the user response triggers a new current-node in the decision-tree
(defrule proceed-to-branch-node
	(answer ?choice)
	(current-node ?name)
	(node (name ?name)
		(type decision)
		(possible-answers $?choices)
		(script-cmds $?cmds)
		(branch-nodes $?branches)
	)
=>
	(retract (answer ?choice))		; retract answer
	(retract (current_node ?name)		; retract current-node
	(bind ?n (member$ ?choice $?choices))	; find index of selected choice
	(bind ?cmd (nth$ ?n $?cmds))		; find cmd for index
	(bind ?next (nth$ ?n $?branches))	; find node for index
	(assert (current-node ?next))		; assert new current-node
)

; initial fact list
; add your decision nodes here
(deffacts decision-tree
	(current-node root)
	(node (name root)
		(question "Is this a household?")
		(branch-nodes ask-parental-controls ask-shared-printer)
	)
	(node (name ask-parental-controls)
		(question "Would you like parental controls?")
		(branch-nodes need-parental-controls is-cord-cutter)
	)
	(node (name shared-printer)
		(question "Share your printer over the network?")
		(branch-nodes yes-printer-share end-thank-you)
	)
	(node (name is-cord-cutter)
		(question "Canceled cable subscription?")
		(branch-nodes yes-cord-cutter is-shared-printer)
	)
	(node (name yes-cord-cutter)
		(selected-answer yes)
		(branch-nodes end-thank-you)
	)
	(node (name end-thank-you)
		(type leaf)
	)	
)

