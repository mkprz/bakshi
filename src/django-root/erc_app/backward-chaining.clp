(deftemplate domain-rule "capture link between goal and conditions"
	(multislot if (default none))
	(multislot then (default none))
)

(deftemplate userprompt "structure of a user prompt"
	(slot prompt-id (type SYMBOL))
	(slot prereqs-satified (type SYMBOL) (default yes))
	(slot query-str (type STRING))
	(multislot answer_options (default none))
)

(deftemplate response "structure of a user response"
	(slot prompt-id (type SYMBOL))
	(slot answer (type STRING))
)

(defrule do-user-query "...when prompt has prereqs satisfied and no response exists"
	?r <- (userprompt
		(prereqs-satisfied yes)
		(prompt-id ?pid)
		(query-str ?query)
		(answer_options $?choices)
	(not (response (prompt-id ?pid))
=>
	(python-call setprompt ?pid ?query $?choices)
)
