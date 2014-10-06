; Expert-System Router Configuration (ERC) or Bakshi Router Configuration Wizard
; mike perez: meekprize@gmail.com; kf5qvo@outlook.com
; Feb - Oct, 2013

; decision-tree-nodes strategy based on design patterns from
; http://www.csie.ntu.edu.tw/~sylee/courses/clips/design.htm

; external python function: usrprompt -- prompt user with decision node question and possible answers
; external python function: netcfg_*   -- one or more functions to configure network

; fact template: node
; use this data structure to develop your own decision-tree-nodes
; multislot branch-nodes corresponds to multislot possible-answers
; multislot netcfg contains name of a python function and function arguments
(deftemplate node
  (slot name)
  (slot type (default decision))
  (slot question (type STRING))
  (slot selected-choice (default none))
  (multislot valid-choices (default yes no))
  (multislot branch-nodes (default none))
  (multislot netcfg)
)

; rule: moveto-next-node
; the user response triggers a new current-node in the decision-tree
(defrule moveto-next-node
  ?curnode <- (current-node ?name)
  ?usrrsp <- (user-response ?name ?selected-choice)
  (node (name ?name)
    (type decision)
    (valid-choices $?choices)
    (branch-nodes $?branches)
  )
=>
  (retract ?usrrsp) ; retract answer
  (retract ?curnode) ; retract current-node
  (bind ?n (member$ ?selected-choice $?choices)) ; find index of selected choice
  (bind ?next (nth$ ?n $?branches)) ; find node for index
  (assert (current-node ?next)) ; assert new current-node
)

; rule: eval-decision-node
; using the current-node in the decision tree, trigger a user prompt
(defrule eval-decision-node
  (current-node ?name)
  (interview-id ?id)
  (not (user-response ?name ?x))
  (node (name ?name)
    (type decision)
    (question ?question)
    (valid-choices $?choices)
    (netcfg ?func-name $?func-args)
  )
=>
  (bind ?rslt (python-call netcfg ?id ?func-name ?name $?func-args))
  (printout t $rslt crlf)
  (assert (user-response ?name (python-call setdecisionnode ?id ?name ?question $?choices)))
)


;init
(defrule initialize
  (not (node (name root)))
=>
  (assert
    (node (name root)
      (question "Is this a household?")
      (branch-nodes node-parental-controls node-is-shared-printer)
    )
  )
  (assert (current-node root))
  (assert (interview-id (python-call startinterview)))
)

; initial fact list
; add your decision nodes here
(deffacts decision-tree
  (node (name node-parental-controls)
    (question "Would you like parental controls?")
    (branch-nodes need-parental-controls is-cord-cutter)
  )
  (node (name node-is-shared-printer)
    (question "Share your printer over the network?")
    (branch-nodes yes-printer-share end-thank-you)
  )
  (node (name node-is-cord-cutter)
    (question "Canceled cable subscription?")
    (branch-nodes yes-cord-cutter is-shared-printer)
  )
  (node (name end-thank-you)
    (type leaf)
  )
)
