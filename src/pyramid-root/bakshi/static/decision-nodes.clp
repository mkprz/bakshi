;;;======================================================
;;;   Expert-System Router Configuration (ERC)
;;;     or Bakshi Router Configuration Wizard
;;;
;;;     This expert system prescibes a uci configuration script
;;;     for a small-office/home-office router
;;;     http://wiki.openwrt.org/doc/uci
;;;
;;;     For use with http://github.com/mkprz/bakshi
;;;
;;;     mike perez: meekprize@gmail.com; kf5qvo@outlook.com
;;;     Feb - Oct, 2013; Nov - Feb 2014/15
;;;======================================================

; decision-tree-nodes strategy based on design patterns from
; http://www.csie.ntu.edu.tw/~sylee/courses/clips/design.htm
; with some influence from the Automotive pyclips example

; external python function: usrprompt -- prompt user with decision node question and possible answers
; external python function: addnetcfg    -- amend uci script with one or more commands

;;;****************
;;;* STARTUP RULE *
;;;****************


;;;***************
;;;* QUERY RULES *
;;;***************

(defrule initialize ""
  (not (node (name root)))
=>
  (assert (current-node root))
)

(defrule eval-decision-node "amend uci config script and prompt user based on current-node"
  (current-node ?name)
  (not (user-response ?name ?x))
  (node (name ?name)
    (type decision)
    (prompt ?prompt)
    (valid-choices $?choices)
    (netcfg ?cmd $?args)
  )
=>
  (bind ?addnetcfg-result (python-call addnetcfg ?id ?name ?cmd $?args))
  (assert (user-response ?name (python-call usrprompt ?id ?name ?prompt $?choices)))
)

;;; trap errors from python-call
;;;
;(defrule trap-python-error "trap errors from python-call"
;  ?curnode <- (current-node ?name)
;  ?usrrsp <- (user-response ?name ERROR)
;  (node (name ?name)
;    (type decision)
;    (valid-choices $?choices)
;    (branch-nodes $?branches)
;  )
;=>
;  (retract ?curnode) ; retract current-node
;  (assert (error-state TRUE)) ; assert error-state
;)

(defrule traverse-decision-tree "trigger new current node based on user response"
  ?curnode <- (current-node ?name)
  ?usrrsp <- (user-response ?name ?selected-choice)
  (node (name ?name)
    (type decision)
    (valid-choices $?choices)
    (branch-nodes $?branches)
  )
=>
  (retract ?curnode) ; retract current-node
  (bind ?n (member$ ?selected-choice $?choices)) ; find index of selected choice
  (bind ?next (nth$ ?n $?branches)) ; find node based on index of selected choice
  (assert (current-node ?next)) ; assert new current-node
)


;;; ***************************
;;; * DEFTEMPLATES & DEFFACTS *
;;; ***************************

; use this fact template to develop your own decision-tree-nodes
; for example:
; (node
;   (name nodeX)
;   (prompt "Do you need help?"
;   (valid-choices yes no)
;   (branch-nodes nodeY nodeZ)
; )
; 1) While traversing the decision-tree, when the current node is nodeX,
; the user will be prompted with "Do you need help? (yes no)"
; If user responds with no then current node becomes nodeZ (via rules defined below)
; because the multislot order of "no" corresponds to "nodeZ"
;
; 2) Multislot uci contains name of a python function and function arguments
; that will amend the prescribed uci configuration script
;
; 3) Slot type should be one of root, decision, or leaf to indicate where in the tree the node exists
(deftemplate node
  (slot name)
  (slot type (default decision))
  (slot prompt (type STRING))
  (slot selected-choice (default none))
  (multislot valid-choices (default no yes))
  (multislot branch-nodes (default node-catch-all node-catch-all))
  (multislot netcfg)
)


     root
  0        1
00 01   10  11
# use Shannon's Entropy measure to determine the question that gives the most information

; initial fact list / decision tree
; add your decision nodes here
(deffacts decision-tree
  (node
    (type root)
    (name root)
    (prompt "Start the UCI Wizard?")
    (branch-nodes node-cancel node-start)
  )
  (node (name node-start)
    (question "Is this a private residence?")
    (branch-nodes node-0 node-1)
  )
  (node "1: yes private residence"
    (name node-1)
    (prompt "How many people connect to the internet via this router?")
    (valid-choices just-me the-whole-family me-and-my-partner me-and-my-roommates other)
    (branch-nodes node-single-residen)
  )
  (node
    (name node-is-cord-cutter)
    (prompt "Canceled cable subscription?")
    (branch-nodes yes-cord-cutter is-shared-printer)
  )
  (node
    (name end-thank-you)
    (type leaf)
  )
)
