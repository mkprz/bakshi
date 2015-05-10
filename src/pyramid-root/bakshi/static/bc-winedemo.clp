;;; To select the best color of wine to serve with a meal.

;;; for use with backward-chaining inference engine defined in inference-engine-bc.clp
;;;

(defmodule ERC (import BC ?ALL))

(deffacts ERC::wine-rules
	(rule (antecedent main-course is red-meat)
		(consequent best-color is red))

	(rule (antecedent main-course is fish)
		(consequent best-color is white))

	(rule (antecedent main-course is poultry and meal-is-turkey is yes)
		(consequent best-color is red))

	(rule (antecedent main-course is poultry and meal-is-turkey is no)
		(consequent best-color is white)))

(deffacts ERC::initial-goal
	(goal (attribute best-color)))
