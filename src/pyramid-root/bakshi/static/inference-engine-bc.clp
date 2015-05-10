;;; http://www.csie.ntu.edu.tw/~sylee/courses/clips/design.htm
;;;

;;; Module BC for backward-Chaining engine
(defmodule BC
  (export ?ALL))


;;; A template for backward chaining rules:
(deftemplate BC::rule
  (multislot if)
  (multislot then))

;;; Each if, <condition>, is either
;;;
;;;    <attribute> is <value>
;;;
;;; or
;;;
;;;    <attribute> is <value> and <condition>
;;;
(deftemplate BC::attribute
  (slot name)
  (slot value))

(deftemplate BC::goal
  (slot attribute))

;;; Backward Chaining Inference Engine
;;; modules should be a sub-goal like vpn-config or QoS-config
;;; Solving all module-level sub-goals results in a presribed UCI config script
;;; Solving all consequents (then-statements) in modules results in solving the module-level sub-goal
;;; Solving an antecedent (if-statement) results in satisfying a consequent
;;;


;;; if sub-goal g-name is a consequent of unresolved rule with antecedent a-name,
;;; then add a-name to sub-goals
;;;
(defrule BC::attempt-rule "build-up sub-goals as needed"
   (goal (attribute ?g-name))
   (rule (if ?a-name $?)
         (then ?g-name $?))
   (not (attribute (name ?a-name)))
   (not (goal (attribute ?a-name)))
   =>
   (assert (goal (attribute ?a-name))))

;;; unresolved sub-goal g-name has no known if so we must ask user for this information (part 1)
(defrule BC::ask-attribute-value "ask for un-inferable value"
   ?goal <- (goal (attribute ?g-name))
   (not (attribute (name ?g-name)))
   (not (rule (then ?g-name $?)))
   (not (ui-state ok))
   =>
   (python-call setprompt ?g-name "yes" "no" "idk")
   (assert (ui-state ok))
   (halt)
)

;;; unresolved sub-goal g-name has no known if so we must ask user for this information (part 2)
(defrule BC::get-attribute-value "ask for un-inferable value"
   ?ui-state <- (ui-state ok)
   ?goal <- (goal (attribute ?g-name))
   (not (attribute (name ?g-name)))
   (not (rule (then ?g-name $?)))
   =>
   (retract ?ui-state)
   (retract ?goal)
   (bind ?answer (python-call getprompt ?g-name))
   (assert (attribute (name ?g-name)
                      (value ?answer)))
)

;;; retract goals as they are satisfied w/o user interaction
(defrule BC::goal-satisfied "retract satisfied sub-goal"
   (declare (salience 100))
   ?goal <- (goal (attribute ?g-name))
   (attribute (name ?g-name))
   =>
   (retract ?goal))

;;; infer sub-goals from resolved ifs
(defrule BC::rule-satisfied "infer sub-goals from resolved ifs"
   (declare (salience 100))
   (goal (attribute ?g-name))
   (attribute (name ?a-name)
              (value ?a-value))
   ?rule <- (rule (if ?a-name is ?a-value)
                  (then ?g-name is ?g-value))
   =>
   (retract ?rule)
   (assert (attribute (name ?g-name)
                      (value ?g-value))))

;;; retract if-then statements that cannot resolve sub-goal
(defrule BC::remove-rule-no-match
   (declare (salience 100))
   (goal (attribute ?g-name))
   (attribute (name ?a-name) (value ?a-value))
   ?rule <- (rule (if ?a-name is ~?a-value)
                  (then ?g-name is ?g-value))
   =>
   (retract ?rule))

;;; by piecemeal, resolve ifs with multiple attributes (e.g., if x is 1 and y is 7)
(defrule BC::modify-rule-match "resolve each attribute in if one by one"
   (declare (salience 100))
   (goal (attribute ?g-name))
   (attribute (name ?a-name) (value ?a-value))
   ?rule <- (rule (if ?a-name is ?a-value and
                      $?rest)
                  (then ?g-name is ?g-value))
   =>
   (retract ?rule)
   (modify ?rule (if $?rest)))


;;; focus on modules as ordered in deffact module-seq
;;; change module-seq so that currently focused module is removed
;;;
(defrule BC::focus-next-module
  ?list  <- (module-seq ?next-module $?other-modules)
  (not (module-state ?next-module))
  =>
  (retract ?list)
  (assert (module-seq $?other-modules))
  (assert (module-state ?next-module)))
(deffacts BC::module-order
  (module-seq QOS GUESTWIFI))


(defrule BC::QOS-questions
  ?state <- (module-state QOS)
  =>
  (retract ?state)
  (assert (goal (attribute qos-desireable)))
  (assert (rule (if laggy-browsing is yes and multiple-devices-on-network is yes)
    (then multiple-devices-using-heavy-bandwidth is yes)))
  (assert (rule (if multiple-devices-using-heavy-bandwidth is yes)
    (then qos-desireable is yes)))
)
(defrule BC::QOS-configs
  (attribute (name qos-desireable) (value yes))
  =>
  (python-call addnetcfg qos allthingsequal))

(defrule BC::GUESTWIFI-questions
  ?state <- (module-state GUESTWIFI)
  =>
  (retract ?state)
  (assert (goal (attribute guestwifi-desireable)))
  (assert (rule (if guests-come-over is yes and guests-are-questionable is yes and guests-use-wifi is yes)
    (then guestwifi-desireable is yes)))
)
(defrule BC::GUESTWIFI-configs
  (attribute (name guestwifi-desireable) (value yes))
  =>
  (python-call addnetcfg guestwifi separate_network))
